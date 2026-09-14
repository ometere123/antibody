# Antibody deployment evidence

No canonical deployment is recorded yet.

## Current environment blocker

No deployment was attempted. The existing RPC check to `https://studio.genlayer.com/api` returned HTTP 403 instead of an `eth_chainId` result, so chain 61999 could not be verified. The installed GenLayer CLI's read-only `account show` reported its active account on `studio-dev` (chain ID 61997), which is not an allowed deployment context. Do not run deployment until RPC access is restored and the existing CLI reports the deployer on Studionet chain 61999. The repository's synthetic fixture is currently a localhost-only development server; no public HTTPS fixture host is configured, so live lifecycle evidence also remains unavailable.

This file is intentionally evidence-only: addresses and transaction hashes must be added only after finalized execution on the target network.

## Locked target

- Network: Studionet
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`

## Pre-deployment gates

```bash
python -m py_compile contracts/antibody.py
python scripts/preflight.py
pip install -r requirements-test.txt
pytest tests/direct/ -v -s
```

Then deploy with:

```bash
python scripts/deploy_studionet.py
```

The script validates `eth_chainId == 61999` before invoking the GenLayer CLI.

## Evidence fields to fill after finalization

- source commit:
- contract source SHA-256:
- deployer address:
- contract address:
- deployment transaction:
- finalized state:
- consensus result:
- CLI version:

## Lifecycle evidence to fill

- program registration transaction:
- program definition hash:
- v1 registration transaction:
- confirmed challenge transaction:
- confirmed counterexample ID/index:
- challenger reward evidence:
- v1 breached readback:
- v2 registration transaction:
- regression replay transaction:
- v2 finalize transaction:
- `is_regression_clear(v2, program_hash)` readback:
- second counterexample transaction:
- post-counterexample invalidation readback:
