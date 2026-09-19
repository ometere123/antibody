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

## Verified deployment

- Contract: `0x81B956AE9Ae7825CE4d2dE2FA2b9a8E31Aec42fb`
- Deployment transaction: `0x8d20d16b94361c6e104dd3c3c7741f2605a5190f5e4a23b56ace2a0545765d7e`
- Result: `FINALIZED / MAJORITY_AGREE / SUCCESS`
- Explorer: [Antibody on Studionet](https://explorer-studio.genlayer.com/address/0x81B956AE9Ae7825CE4d2dE2FA2b9a8E31Aec42fb)

The deployment helper verifies chain identity before deploying.

## Current live lifecycle status

Program `1` and v1 (version `1`) are registered. Two challenge attempts
finalized as `INCONCLUSIVE / TRANSPORT_UNAVAILABLE` because validators could
not reach the Cloudflare Worker fixture. Neither attempt produced a confirmed
counterexample. No challenger reward, breached-version result, v2/v3 replay,
or regression-clear result is claimed. This is a fixture transport limitation,
not a successful attack demonstration. Challenge transaction hashes and
record IDs were not recovered into the repository evidence; see
[`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md).

## Intended reviewer demo (not yet demonstrated live)

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

## Implementation and tooling validation

The repository includes:

- Python syntax compilation gate;
- SDK-free structural/security preflight;
- Direct Mode behavioural suite;
- chain-locked deployment helper;
- network config with stable Studionet only;
- security and architecture documents.

`docs/DEPLOYMENT.md` records the verified contract deployment and the
incomplete live lifecycle separately. Do not present the planned demo above as
observed evidence.

## Suggested contribution-form entry

**Title:** Antibody — Consensus-Verified Adversarial Regression Memory for Intelligent Contracts

**Notes / Description:**

Antibody is a reusable GenLayer Intelligent Contract primitive that turns adversarial failures into permanent regression memory for future agent/service versions. Owners register a frozen invariant and fund a GEN bounty; challengers post bonded probes; validators independently replay public endpoint evidence and resolve VIOLATION, NO_VIOLATION, or INCONCLUSIVE. Confirmed violations are inherited by future versions, and REGRESSION_CLEAR applies only to the current known corpus—not universal safety. Deployed on Studionet (chain 61999). Two live challenge attempts finalized INCONCLUSIVE / TRANSPORT_UNAVAILABLE because validators could not reach the synthetic fixture. No counterexample or regression-clear result is claimed. Source, tests, and deployment receipt are linked below.

**Evidence URL:** [Antibody contract on Studionet Explorer](https://explorer-studio.genlayer.com/address/0x81B956AE9Ae7825CE4d2dE2FA2b9a8E31Aec42fb)

Repository: [github.com/ometere123/antibody](https://github.com/ometere123/antibody)
