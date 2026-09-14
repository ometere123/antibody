# Antibody submission notes

## Category

Standalone GenLayer Intelligent Contract.

Antibody deliberately has **no frontend**. It is a reusable protocol primitive, not an end-user application.

## One-sentence purpose

Antibody turns permissionless adversarial failures of autonomous agents into economically rewarded, consensus-confirmed counterexamples that every future version must inherit and replay before it can regain regression-clear status.

## Why this should not be reviewed as a generic “AI decides X” contract

The semantic judgement is only one step in a larger deterministic protocol:

1. owner freezes an invariant and deposits native GEN;
2. challenger posts an exact bond and frozen adversarial probe;
3. the full bounty is reserved before the challenge opens;
4. leader executes the remote probe;
5. validators independently execute the same remote probe;
6. a `VIOLATION` requires response-grounded evidence;
7. deterministic settlement pays/refunds/captures the bond according to the bounded verdict;
8. a confirmed failure becomes permanent regression memory;
9. every version's required corpus grows;
10. future certification is computed by deterministic full-corpus replay state.

No model decides how much money moves, whether a challenge is sufficiently bonded, which version is active, whether a reward is reserved, whether a probe is an exact duplicate, how inheritance works, or whether all current counterexamples have passing receipts.

## Load-bearing GenLayer consensus

Without GenLayer, one test server, one model API or one owner would become the arbiter of whether a newly discovered attack actually violates the frozen invariant.

Antibody instead requires validators to independently submit the same frozen probe to the same immutable version endpoint and independently judge the observable response. A leader cannot settle a violation with invented supporting evidence: its excerpt must appear in the validator's independently observed response.

## Novel state transition

The key state transition is not `challenge -> verdict`.

It is:

```text
confirmed challenge
       |
       v
permanent counterexample N
       |
       +--> discovery version BREACHED
       |
       +--> previous clear versions invalidated
       |
       +--> future versions inherit N
       |
       +--> downstream is_regression_clear gate turns false
```

The contract therefore becomes more useful as adversarial discoveries accumulate.

## Honest claim boundary

Antibody proves consensus-backed observations about a registered public test endpoint. It does not prove production deployment identity, universal agent safety, hidden execution, or absence of unknown vulnerabilities.

`REGRESSION_CLEAR` means exactly: the version has passing receipts for every confirmed counterexample currently in this program's immutable corpus.

## Target network

- Studionet
- chain ID `61999`
- RPC `https://studio.genlayer.com/api`

The deployment helper verifies chain identity before deploying.

## Reviewer demo to capture after deployment

Use two endpoint behaviours representing `v1` and `v2`.

### A. Confirm a real counterexample against v1

1. register program with an invariant forbidding cross-user secret disclosure;
2. deposit enough GEN for at least two counterexamples;
3. register v1;
4. challenger bonds an administrator-impersonation probe;
5. v1 returns a response containing a synthetic secret;
6. resolve challenge;
7. verify `CONFIRMED`, challenger reward, counterexample index `1`, v1 `BREACHED`.

### B. Prove inherited regression memory on v2

1. register fixed v2;
2. confirm `required_counterexamples == 1`;
3. replay counterexample `1`;
4. v2 safely refuses;
5. finalize v2;
6. verify `REGRESSION_CLEAR` and `is_regression_clear(...) == true`.

### C. Demonstrate corpus growth invalidates clearance

1. open a different adversarial challenge against active v2;
2. make the fixture expose a second synthetic failure;
3. confirm counterexample `2`;
4. verify corpus count becomes `2`;
5. verify v2 is `BREACHED` and the downstream clearance gate is false.

### D. Economic negative cases

Capture finalized receipts showing:

- exact duplicate pending challenge rejected;
- exact confirmed probe cannot earn a second bounty;
- owner cannot withdraw reserved bounty;
- clear `NO_VIOLATION` challenge transfers the bond into the bounty pool;
- `INCONCLUSIVE`, including transport failures, does not mutate the corpus.

## Validation status before live deployment

The repository includes:

- Python syntax compilation gate;
- SDK-free structural/security preflight;
- Direct Mode behavioural suite;
- chain-locked deployment helper;
- network config with stable Studionet only;
- security and architecture documents.

`docs/DEPLOYMENT.md` must only be updated with real transaction hashes after finalized on-chain execution. No fabricated deployment evidence belongs in this repository.
