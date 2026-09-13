"""SDK-free invariants that can run even before GenLayer dependencies are installed."""
from pathlib import Path
import ast

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "contracts" / "antibody.py"


def test_contract_compiles_and_has_one_deployable():
    source = CONTRACT.read_text()
    compile(source, str(CONTRACT), "exec")
    files = sorted(p.name for p in (ROOT / "contracts").glob("*.py"))
    assert files == ["antibody.py"]


def test_consensus_and_corpus_mechanics_are_present():
    source = CONTRACT.read_text()
    for marker in (
        "gl.vm.run_nondet_unsafe",
        "gl.nondet.web.request",
        "gl.nondet.exec_prompt",
        "Counterexample",
        "_invalidate_for_new_counterexample",
        "is_regression_clear",
        "bounty_reserved",
    ):
        assert marker in source


def test_network_is_locked_to_stable_studionet():
    assert "61999" in (ROOT / "docs" / "NETWORK.md").read_text()
    assert "https://studio.genlayer.com/api" in (ROOT / "gltest.config.yaml").read_text()
    deploy = (ROOT / "scripts" / "deploy_studionet.py").read_text()
    assert "EXPECTED_CHAIN_ID = 61999" in deploy
    assert "https://studio.genlayer.com/api" in deploy


def test_public_methods_include_full_lifecycle():
    tree = ast.parse(CONTRACT.read_text())
    names = {node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)}
    assert {
        "register_program", "register_version", "open_challenge", "resolve_challenge",
        "run_regression", "finalize_version", "is_regression_clear",
    } <= names


def test_no_frontend_product_surface():
    for path in ("frontend", "web", "app", "pages", "package.json"):
        assert not (ROOT / path).exists()
