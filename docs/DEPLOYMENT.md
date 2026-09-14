# Antibody deployment evidence

## Verified Studionet deployment

The following deployment was finalized on the locked target network. The
receipt reported majority agreement and successful leader/validator contract
execution.

- Network: Studionet
- Chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- Explorer: `https://explorer-studio.genlayer.com`
- Source commit: `379fb69f394370de05d8e18385b10160edf0c073`
- Contract source SHA-256: `19df96c5964f2da5a12765188cad10b102994c6ce1d0b9ba2194e113891a70e0`
- Contract source bytes: `56100`
- Deployer: `0x24fAe7cD031Ed702Be63BDeA8912141805B996bd`
- Contract address: `0x81B956AE9Ae7825CE4d2dE2FA2b9a8E31Aec42fb`
- Deployment transaction: `0x8d20d16b94361c6e104dd3c3c7741f2605a5190f5e4a23b56ace2a0545765d7e`
- Finalized state: `FINALIZED`
- Consensus result: `MAJORITY_AGREE`
- Execution result: `SUCCESS` (`FINISHED_WITH_RETURN`)
- Explorer contract: [Antibody on Studionet](https://explorer-studio.genlayer.com/address/0x81B956AE9Ae7825CE4d2dE2FA2b9a8E31Aec42fb)

## Live lifecycle status

The deployed contract is ready for lifecycle evidence, but no lifecycle
transactions are recorded here yet. The repository fixture is localhost-only
and the contract intentionally rejects localhost/private endpoints. A public
HTTPS deployment of the existing synthetic fixture is therefore required
before recording program, challenge, consensus, counterexample, payout and
regression-certification evidence. No hashes or state claims below are
invented.

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

## Lifecycle evidence (pending public fixture)

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
