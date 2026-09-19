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

## Live challenge lifecycle status (incomplete)

The deployed contract exists, and an initial program/version and two bonded
challenge attempts were exercised on Studionet. The fixture did not return
validator-reachable evidence: both challenges finalized as
`INCONCLUSIVE / TRANSPORT_UNAVAILABLE`. They did **not** create confirmed
violations or counterexamples.

Verified state currently available:

- Program ID: `1`
- Registered version ID: `1` (v1)
- Challenge attempts: two; both `INCONCLUSIVE / TRANSPORT_UNAVAILABLE`
- Confirmed counterexamples: none
- `REGRESSION_CLEAR` certification: none
- Fixture: Cloudflare Worker; reachable from the operator's browser/client,
  but not from GenLayer validators in these attempts
- Public fixture URL: not recorded here because validator reachability has
  not been established

The transaction hashes, challenge record IDs, receipt payloads, and finalized
bounty/bond readbacks for these attempts were not present in the repository
evidence reviewed for this update. They are intentionally not guessed or
represented as explorer-backed proof. If recovered from saved receipts, add
each exact hash and readback below and label the outcomes as inconclusive
troubleshooting evidence.

| Action | Transaction / record | Observed outcome |
|---|---|---|
| Antibody deployment | [`0x8d20…65d7e`](https://explorer-studio.genlayer.com/tx/0x8d20d16b94361c6e104dd3c3c7741f2605a5190f5e4a23b56ace2a0545765d7e) | `FINALIZED / MAJORITY_AGREE / SUCCESS` |
| Program registration | Hash not recovered; program ID `1` | Registered; full receipt/readback not attached |
| v1 registration | Hash not recovered; version ID `1` | Registered; endpoint readback not attached |
| Challenge attempt 1 | Hash/record ID not recovered | `INCONCLUSIVE / TRANSPORT_UNAVAILABLE`; no counterexample |
| Challenge attempt 2 | Hash/record ID not recovered | `INCONCLUSIVE / TRANSPORT_UNAVAILABLE`; no counterexample |

Consequently, no claim is made here about a confirmed violation, challenger
reward, v1 breach, inherited replay, regression-clear state, or corpus-growth
invalidation. The contract deployment is verified; the intended live
challenge-to-counterexample-to-regression demonstration remains incomplete.

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

## Remaining live evidence

Do not fill these with estimates or inferred IDs. Record them only after a
validator-reachable fixture produces finalized on-chain evidence:

- Program definition hash and finalized registration/funding receipts
- Exact challenge transaction hashes, record IDs, finalized outcomes, and
  bounty/bond accounting readbacks
- Confirmed counterexample ID/index and v1 breached readback
- v2 registration, inherited replay, finalization, and current
  `is_regression_clear` readback
- A second distinct confirmed counterexample, corpus expansion readback, and
  proof that v2 is no longer clear against the expanded corpus
- v3 registration, replay of the complete corpus, finalization, and current
  regression-clear readback
