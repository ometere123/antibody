# Antibody deployment evidence

No canonical deployment is recorded yet.

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
