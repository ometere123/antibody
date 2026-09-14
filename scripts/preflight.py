#!/usr/bin/env python3
"""Zero-dependency Antibody source/network/security preflight.

This deliberately does not import GenLayer. It catches repository drift before
Direct Mode or deployment: wrong network constants, accidental frontend files,
missing consensus replay, broken bounty reservation, unsafe ungrounded
VIOLATION settlement, and missing regression-corpus invalidation.
"""
from __future__ import annotations

import ast
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "antibody.py"
STABLE_RPC = "https://studio.genlayer.com/api"
STABLE_CHAIN = "61999"
# Keep forbidden environment identifiers out of repository text themselves.
FORBIDDEN_RPC_TOKEN = "studio" + "-dev"
FORBIDDEN_CHAIN_TOKEN = "619" + "97"


class Fail(RuntimeError):
    pass


def check(ok: bool, message: str) -> None:
    if not ok:
        raise Fail(message)


def dotted(node: ast.AST) -> str:
    parts: list[str] = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
        return ".".join(reversed(parts))
    return ""


def function_parents(tree: ast.AST) -> dict[int, tuple[str, ...]]:
    result: dict[int, tuple[str, ...]] = {}

    class Visitor(ast.NodeVisitor):
        stack: list[str] = []

        def generic_visit(self, node: ast.AST) -> None:
            result[id(node)] = tuple(self.stack)
            super().generic_visit(node)

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.stack.append(node.name)
            self.generic_visit(node)
            self.stack.pop()

    Visitor().visit(tree)
    return result


def text_files() -> list[pathlib.Path]:
    ignored = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", "artifacts"}
    result: list[pathlib.Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in ignored for part in path.parts):
            continue
        if path.suffix.lower() in {".py", ".md", ".yaml", ".yml", ".toml", ".txt", ".example"} or path.name in {".gitignore"}:
            result.append(path)
    return result


def main() -> int:
    checks = 0
    source = CONTRACT.read_text(encoding="utf-8")
    compile(source, str(CONTRACT), "exec")
    checks += 1
    tree = ast.parse(source)

    deployables = sorted(p.name for p in (ROOT / "contracts").glob("*.py") if p.name != "__init__.py")
    check(deployables == ["antibody.py"], f"unexpected deployables: {deployables}")
    checks += 1

    contract_classes = [
        node for node in tree.body
        if isinstance(node, ast.ClassDef)
        and any(dotted(base) == "gl.Contract" for base in node.bases)
    ]
    check(len(contract_classes) == 1 and contract_classes[0].name == "Antibody", "expected exactly one Antibody(gl.Contract)")
    checks += 1

    expected_methods = {
        "register_program", "fund_bounty", "withdraw_bounty", "set_paused",
        "register_version", "open_challenge", "cancel_challenge", "resolve_challenge",
        "run_regression", "finalize_version", "get_program", "get_version",
        "get_challenge", "get_counterexample", "get_counterexample_by_index",
        "get_regression", "is_regression_clear",
    }
    method_names = {n.name for n in contract_classes[0].body if isinstance(n, ast.FunctionDef)}
    missing = expected_methods - method_names
    check(not missing, f"missing public/core methods: {sorted(missing)}")
    checks += 1

    parents = function_parents(tree)
    nondet_calls = []
    unsafe_calls = []
    web_calls = []
    prompt_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = dotted(node.func)
            if name.startswith("gl.nondet."):
                nondet_calls.append((name, node.lineno, parents.get(id(node), ())))
            if name == "gl.vm.run_nondet_unsafe":
                unsafe_calls.append(node)
            if name == "gl.nondet.web.request":
                web_calls.append(node)
            if name == "gl.nondet.exec_prompt":
                prompt_calls.append(node)
    check(len(unsafe_calls) == 1, f"expected one custom-consensus host, got {len(unsafe_calls)}")
    check(web_calls and prompt_calls, "consensus path must independently exercise web + LLM reasoning")
    for name, line, hosts in nondet_calls:
        check("_observe_probe" in hosts, f"{name} escaped _observe_probe at line {line}")
    checks += 3

    observe = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_observe_probe")
    observe_text = ast.unparse(observe).replace('"', "'")
    for marker in (
        "gl.nondet.web.request", "method='POST'", "'input': probe",
        "gl.nondet.exec_prompt", "gl.vm.run_nondet_unsafe",
        "leader['verdict']", "follower['verdict']", "leader['http_class']",
        "evidence not in str(response_text)",
    ):
        check(marker in observe_text, f"consensus invariant missing: {marker}")
        checks += 1

    # A confirmed failure must create permanent memory and deterministic consequences.
    resolve = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "resolve_challenge")
    resolve_text = ast.unparse(resolve).replace('"', "'")
    for marker in (
        "VERDICT_VIOLATION", "counterexample_count", "confirmed_probe_keys",
        "_invalidate_for_new_counterexample", "bounty_balance", "_pay",
        "VERDICT_NO_VIOLATION", "VERDICT_INCONCLUSIVE", "CHALLENGE_INCONCLUSIVE",
    ):
        check(marker in resolve_text, f"settlement invariant missing: {marker}")
        checks += 1

    open_challenge = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "open_challenge")
    open_text = ast.unparse(open_challenge).replace('"', "'")
    for marker in (
        "bounty_reserved", "bounty_per_counterexample", "owner cannot challenge own program",
        "identical challenge already pending", "probe already exists in regression corpus",
    ):
        check(marker in open_text, f"challenge-admission invariant missing: {marker}")
        checks += 1

    finalize = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "finalize_version")
    finalize_text = ast.unparse(finalize)
    check("VERDICT_NO_VIOLATION" in finalize_text and "counterexample_count" in finalize_text, "certification is not full-corpus deterministic")
    check("no confirmed counterexamples exist yet" in finalize_text, "empty-corpus certification must be impossible")
    checks += 2

    invalidate = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_invalidate_for_new_counterexample")
    invalid_text = ast.unparse(invalidate)
    check("VERSION_CANDIDATE" in invalid_text and "VERSION_BREACHED" in invalid_text, "new counterexample does not invalidate stale clearance")
    checks += 1

    # Contract transfer path must match the stable native-GEN pattern used by existing repos.
    check("@gl.evm.contract_interface" in source and "emit_transfer(value=amount)" in source, "native GEN payout interface missing")
    check(source.count("@gl.public.write.payable") >= 3, "payable economic entry points missing")
    checks += 2

    # Network lock across all committed text/config. No preview identifiers may leak in.
    for path in text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        check(FORBIDDEN_RPC_TOKEN not in text.lower(), f"preview RPC token present in {path.relative_to(ROOT)}")
        check(FORBIDDEN_CHAIN_TOKEN not in text, f"preview chain id present in {path.relative_to(ROOT)}")
    checks += 2

    network_doc = (ROOT / "docs" / "NETWORK.md").read_text(encoding="utf-8")
    gltest = (ROOT / "gltest.config.yaml").read_text(encoding="utf-8")
    deploy_script = (ROOT / "scripts" / "deploy_studionet.py").read_text(encoding="utf-8")
    for text, label in ((network_doc, "NETWORK.md"), (gltest, "gltest.config.yaml"), (deploy_script, "deploy script")):
        check(STABLE_RPC in text, f"stable RPC absent from {label}")
    check(STABLE_CHAIN in network_doc and STABLE_CHAIN in deploy_script, "stable chain id lock absent")
    checks += 4

    # This is a standalone primitive: no product frontend should creep in.
    forbidden_frontend_paths = [
        ROOT / "frontend", ROOT / "web", ROOT / "app", ROOT / "pages", ROOT / "package.json",
    ]
    check(not any(p.exists() for p in forbidden_frontend_paths), "frontend/product surface detected")
    checks += 1

    # Secret hygiene: catch common committed key shapes. Example env may name variables but contain no secrets.
    key_pattern = re.compile(r"(?i)(private[_-]?key|mnemonic)\s*[=:]\s*['\"]?(0x[a-f0-9]{64}|[a-z]+(?:\s+[a-z]+){11,23})")
    for path in text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        check(key_pattern.search(text) is None, f"possible secret committed in {path.relative_to(ROOT)}")
    checks += 1

    # All Python committed source should at least parse in this SDK-free environment.
    for path in ROOT.rglob("*.py"):
        if "__pycache__" in path.parts:
            continue
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    checks += 1

    print(f"Antibody preflight PASS: {checks} checks")
    print(f"network: Studionet / chain {STABLE_CHAIN} / {STABLE_RPC}")
    print("frontend: absent")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Fail as exc:
        print(f"Antibody preflight FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
