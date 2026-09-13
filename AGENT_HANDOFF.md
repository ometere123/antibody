# Antibody final-runtime handoff

The repository implementation is complete enough for local/source review. The remaining work requires an environment that has the official GenLayer tooling, a funded signer and network access. Do not change the target network.

## Immutable target

- network: **Studionet**
- chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- explorer: `https://explorer-studio.genlayer.com`

The committed deployment script verifies the RPC chain ID before it asks the CLI to deploy.

## Do not add a frontend

Antibody is a standalone Intelligent Contract submission. The public fixture endpoint is test evidence only, not a product frontend.

## Finish in this order

1. Work from the repository root and preserve the contract architecture. Do not swap network configuration or dependencies without a demonstrated compatibility reason.
2. Run `python scripts/preflight.py` and `pytest tests/source -q`.
3. Install `requirements-test.txt`; run `pytest tests/direct -v -s`. Fix any actual runtime incompatibility without weakening these invariants: independent validator replay, grounded `VIOLATION` evidence, reserved bounty solvency, permanent counterexample inheritance, stale-clear invalidation and deterministic full-corpus certification.
4. If available, run the published GenVM linter against `contracts/antibody.py`. Record the exact version and result rather than claiming a pass without evidence.
5. Deploy the synthetic fixture logic in `fixtures/test_agent.py` to a public HTTPS, non-production endpoint. Preserve the `POST {"input": "..."}` protocol. Use no real secrets, accounts, funds or side effects.
6. Confirm the funded CLI signer with `genlayer account show`.
7. Run `python scripts/deploy_studionet.py`. Do not bypass its chain-identity check.
8. Wait for a finalized successful deployment, capture contract address, deployment transaction, source hash and CLI version.
9. Execute a full live lifecycle:
   - register a program with a synthetic cross-user-data invariant and funded bounty;
   - register vulnerable v1;
   - open a bonded challenge using the administrator-impersonation probe;
   - resolve it and prove challenger payout + permanent counterexample + v1 `BREACHED`;
   - register fixed v2;
   - replay CE-1 on v2 and finalize v2 to `REGRESSION_CLEAR`;
   - verify `is_regression_clear(v2, program_hash) == true`;
   - confirm a second independent failure against the active version and prove the previous clear state is invalidated until the expanded corpus is replayed.
10. Fill `docs/DEPLOYMENT.md` only with observed transaction hashes/readbacks. Never invent evidence.
11. Re-run preflight and tests, commit the evidence update, and push.

## Reviewer-facing invariant

The submission should be explainable in one sentence:

> a permissionless adversarial failure can earn a bounty only after independent GenLayer replay, then becomes permanent regression memory that every future version must pass before the protocol will call it regression-clear.

Do not broaden the claim to “the agent is safe”.
