# Antibody final-runtime handoff

The contract is already deployed successfully on Studionet. Do not redeploy it
for the fixture transport problem. The remaining live-evidence gap is that
GenLayer validators could not reach the synthetic Cloudflare Worker endpoint.
Two challenges finalized `INCONCLUSIVE / TRANSPORT_UNAVAILABLE`; no
counterexample or regression certification exists yet.

## Immutable target

- network: **Studionet**
- chain ID: **61999**
- RPC: `https://studio.genlayer.com/api`
- explorer: `https://explorer-studio.genlayer.com`

The committed deployment script verifies the RPC chain ID before it asks the CLI to deploy.

## Do not add a frontend

Antibody is a standalone Intelligent Contract submission. The public fixture endpoint is test evidence only, not a product frontend.

## Current verified state and remaining work

1. Preserve the existing contract and Studionet deployment. Keep all operations on the stable target network only.
2. Current on-chain identifiers reported by the operator: program `1`, version `1`. Two challenges resolved `INCONCLUSIVE / TRANSPORT_UNAVAILABLE`, with no counterexamples.
3. Establish a stable HTTPS fixture endpoint that GenLayer validators themselves can reach. Browser/client reachability alone is insufficient. Preserve the fixture's intended synthetic behavior and do not alter Antibody to work around transport.
4. Before spending another bond, POST the documented probes to every route and verify normal HTTPS responses from an independent client.
5. Check the exact RPC chain ID is 61999 before every transaction. Do not redeploy Antibody.
6. Only when validator reachability is demonstrated, resume from the existing program/version:
   - read back program 1, its invariant, bounty and active version before writing;
   - keep version 1 immutable; if its endpoint cannot be changed and is not the intended fixture, register the appropriate next version rather than mutating it;
   - open a bonded challenge using the administrator-impersonation probe;
   - resolve it and prove challenger payout + permanent counterexample + v1 `BREACHED`;
   - register fixed v2;
   - replay CE-1 on v2 and finalize v2 to `REGRESSION_CLEAR`;
   - verify `is_regression_clear(v2, program_hash) == true`;
   - confirm a second independent failure against the active version and prove the previous clear state is invalidated until the expanded corpus is replayed.
7. Recover exact hashes/readbacks for the earlier inconclusive attempts if available; document them only as troubleshooting evidence.
8. Fill `docs/DEPLOYMENT.md` only with observed transaction hashes/readbacks. Never invent evidence.
9. Re-run preflight and tests, commit the evidence update, and push.

## Reviewer-facing invariant

The submission should be explainable in one sentence:

> a permissionless adversarial failure can earn a bounty only after independent GenLayer replay, then becomes permanent regression memory that every future version must pass before the protocol will call it regression-clear.

Do not broaden the claim to “the agent is safe”.
