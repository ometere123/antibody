#!/usr/bin/env python3
"""Deploy Antibody only to stable GenLayer Studionet (chain 61999).

The script never reads a private key. It uses the account already configured in
the official GenLayer CLI and aborts before signing if the explicit RPC does not
report the expected chain ID.
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "contracts" / "antibody.py"
PREFLIGHT = ROOT / "scripts" / "preflight.py"
STUDIONET_RPC = "https://studio.genlayer.com/api"
EXPECTED_CHAIN_ID = 61999


def run(command: list[str]) -> None:
    print("+", " ".join(command), flush=True)
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode != 0:
        raise SystemExit(completed.returncode)


def rpc_chain_id() -> int:
    payload = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_chainId",
        "params": [],
    }).encode("utf-8")
    request = urllib.request.Request(
        STUDIONET_RPC,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "antibody-studionet-deployer/1.0",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = json.loads(response.read().decode("utf-8"))
    value = body.get("result")
    if not isinstance(value, str):
        raise RuntimeError(f"eth_chainId returned no hex result: {body!r}")
    return int(value, 16)


def main() -> int:
    run([sys.executable, str(PREFLIGHT)])

    try:
        actual = rpc_chain_id()
    except Exception as exc:
        print(f"ERROR: unable to verify Studionet chain identity: {exc}", file=sys.stderr)
        return 2
    if actual != EXPECTED_CHAIN_ID:
        print(
            f"ERROR: refusing deployment: expected chain {EXPECTED_CHAIN_ID}, RPC returned {actual}",
            file=sys.stderr,
        )
        return 2
    print(f"CHAIN LOCK OK: {STUDIONET_RPC} -> {actual}")

    cli = shutil.which("genlayer")
    if cli is None:
        print("ERROR: official genlayer CLI is not installed/on PATH", file=sys.stderr)
        return 2
    if not CONTRACT.is_file():
        print(f"ERROR: contract not found: {CONTRACT}", file=sys.stderr)
        return 2

    # Show the already-configured signer before any deployment transaction.
    run([cli, "account", "show"])
    # Explicit RPC avoids relying on, or mutating, any saved default network.
    run([cli, "deploy", "--contract", str(CONTRACT), "--rpc", STUDIONET_RPC])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
