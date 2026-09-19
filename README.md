# Antibody

**Permissionless adversarial regression memory for autonomous agents on GenLayer.**

Antibody is a standalone reusable Intelligent Contract primitive. It lets an agent owner freeze a behavioural invariant and post a native-GEN counterexample bounty. Anyone can bond an adversarial probe against the current agent version. GenLayer validators independently replay the probe against the version's dedicated public test endpoint and judge whether the observable response violates the frozen invariant.

A confirmed failure does not disappear after the bounty is paid. It becomes a permanent counterexample in the program's regression corpus. Every existing and future version inherits that corpus. A version can become `REGRESSION_CLEAR` only after every confirmed counterexample has been replayed without reproducing the violation.

There is **no frontend**. Antibody is intentionally a contract primitive, not a Project submission.

Program invariants, endpoint URLs, and artifact identifiers are owner-supplied. Definition hashes freeze exactly those submitted values; they do not prove that an endpoint runs the claimed artifact, that its behavior is complete, or that metadata is truthful. The same-address owner check blocks direct self-challenges only; it does not prevent related-wallet or sybil behavior.

## Network lock

This repository targets the stable hosted **Studionet** only:

- chain ID: `61999`
- RPC: `https://studio.genlayer.com/api`
- network alias: `studionet`
- explorer: `https://explorer-studio.genlayer.com`

Deployment tooling verifies the chain ID before submitting a deployment.

## Why Antibody is different

A normal behavioural audit asks whether a known test passes now. Antibody turns *newly discovered failures* into shared protocol memory:

```text
owner freezes invariant + funds bounty
              |
              v
        active version
              |
      adversarial probe
              |
              v
   independent GenLayer replay
        /             \
VIOLATION          NO_VIOLATION
   |                    |
   v                    v
bounty paid         bond joins pool
   |
   v
permanent counterexample
   |
   +-----------------------------+
   |                             |
old versions invalidated   future versions inherit
                                 |
                           replay full corpus
                                 |
                           REGRESSION_CLEAR
```

The important object is not a one-off verdict. It is the **counterexample corpus** that compounds with use.

## Trust boundary

Antibody verifies a very precise claim:

> When validators independently submitted this frozen probe to this registered test endpoint, the observable response did or did not reproduce behaviour forbidden by the frozen invariant.

It does **not** prove:

- that the test endpoint is the production deployment;
- that the owner registered every relevant invariant;
- that an agent is universally safe;
- that a `REGRESSION_CLEAR` version has no unknown failures;
- that hidden side effects occurred when they are not observable in the response.

`REGRESSION_CLEAR` means only: **this version passed every confirmed counterexample currently in this program's corpus.**

## Probe protocol

Each version registers an immutable dedicated HTTPS test endpoint. Antibody sends:

```json
{"input": "<frozen adversarial probe>"}
```

The endpoint may return text or JSON. Validators treat the response as hostile data and reason only about whether the observable response violates the frozen invariant.

A registered endpoint should be a dedicated, non-production adversarial test surface with no real-world side effects. The endpoint is immutable for that version; changing the implementation requires registering a new version.

## Core state

### Program

A program freezes:

- owner;
- name;
- behavioural invariant;
- bounty per confirmed counterexample;
- exact challenge bond;
- native-GEN bounty balance;
- active version;
- permanent counterexample count;
- immutable definition hash.

The invariant and economic terms cannot be edited after registration. A new policy should be a new program. That prevents moving the goalposts after a challenge is opened.

### Version

A version freezes:

- program;
- label;
- dedicated test endpoint;
- owner-supplied artifact digest/identifier;
- definition hash.

Its regression state is one of:

- `CANDIDATE`
- `REGRESSION_CLEAR`
- `BREACHED`

### Challenge

A challenge freezes:

- program and version;
- challenger;
- adversarial probe;
- exact challenge bond;
- reserved bounty reward;
- probe digest.

Only the current active version may be challenged for a bounty. This prevents draining the pool by rediscovering failures in intentionally retired versions.

### Counterexample

A confirmed violation creates a permanent counterexample containing the exact probe and its discovery lineage. Exact confirmed probes cannot be submitted as new bounty challenges again; future versions must replay them through `run_regression` instead.

## Consensus is load-bearing

The leader:

1. sends the frozen probe to the version's registered endpoint;
2. observes the HTTP response;
3. asks the model for `VIOLATION`, `NO_VIOLATION`, or `INCONCLUSIVE`;
4. for `VIOLATION`, supplies a short verbatim response excerpt.

Validators independently repeat the HTTP request and the semantic judgement. They reject the leader unless they independently agree on:

- verdict category;
- HTTP response class;
- and, for a violation, that the leader's evidence excerpt is present in the validator's own response snapshot.

The consensus result is deliberately bounded. The model does not choose money, status, inheritance, or certification.

## Deterministic protocol mechanics

After consensus, ordinary contract logic handles:

- exact challenge-bond admission;
- bounty reservation before a challenge can open;
- owner self-challenge rejection;
- exact duplicate suppression;
- bounty payout;
- rejected-challenge bond capture;
- refund on inconclusive rounds, including unavailable endpoints;
- permanent counterexample indexing;
- invalidation of prior `REGRESSION_CLEAR` states when a new counterexample appears;
- version breach state;
- full-corpus certification;
- replay-safe state transitions;
- withdrawal only from unreserved bounty.

## Economics

Suppose:

```text
bounty_per_counterexample = 2 GEN
challenge_bond            = 0.1 GEN
```

Opening a challenge reserves 2 GEN from the bounty pool.

- `VIOLATION`: challenger receives bond + 2 GEN; failure enters permanent corpus.
- `NO_VIOLATION`: challenger's 0.1 GEN bond is added to the bounty pool.
- `INCONCLUSIVE`: bond is returned; corpus is unchanged.
- transport failures and malformed observations are `INCONCLUSIVE`: bond is returned; corpus is unchanged.

The reserved reward cannot be withdrawn while a challenge is pending.

Outgoing GEN transfers are recorded by `PayoutSubmitted` with a monotonic payout ID, recipient, amount, and source reference. `get_payout(id)` reports `SUBMITTED_OUTCOME_REQUIRES_EXTERNAL_RECONCILIATION`; it does not claim that the child transfer was delivered. The parent Intelligent Contract has no synchronous child-receipt API. Clients must correlate the parent transaction's triggered child transaction IDs using the GenLayer client and inspect the child receipt. Failed child value is not automatically returned by the protocol. Antibody does not retry ambiguous payouts, because a retry could pay twice; a failed external payout currently has no safe on-chain recovery path.

## Version inheritance

The strongest state transition is counterexample inheritance.

Assume `v1` has one confirmed failure:

```text
CE-1: administrator impersonation leaks a token
```

Registering `v2` gives it:

```text
required_counterexamples = 1
status = CANDIDATE
```

After `v2` passes CE-1, it can become `REGRESSION_CLEAR`.

If a new CE-2 is later confirmed against the active version, the program corpus becomes two counterexamples. All non-breached versions lose any previous clear certification until they have a passing receipt for CE-2 as well. The version on which CE-2 was discovered becomes `BREACHED` immediately.

## Public interface

### Writes

```text
register_program(name, invariant, bounty_per_counterexample, min_challenge_bond) payable
fund_bounty(program_id) payable
withdraw_bounty(program_id, amount)
set_paused(program_id, paused)
register_version(program_id, label, endpoint, artifact_digest)
open_challenge(program_id, version_id, probe) payable
cancel_challenge(challenge_id)
resolve_challenge(challenge_id)
run_regression(version_id, counterexample_index)
finalize_version(version_id)
```

### Views

```text
get_program(program_id)
get_version(version_id)
get_challenge(challenge_id)
get_payout(payout_id)
get_counterexample(counterexample_id)
get_counterexample_by_index(program_id, local_index)
get_regression(version_id, counterexample_index)
is_regression_clear(version_id, expected_program_hash)
```

`is_regression_clear` is the stable downstream integration gate. It is definition-hash bound so a consumer does not silently accept a different invariant/economic program under the same numeric ID.

## Repository

```text
contracts/antibody.py           core Intelligent Contract
scripts/preflight.py            SDK-free source/network/security checks
scripts/deploy_studionet.py     chain-locked deployment helper
fixtures/                       test-agent fixture specification
scripts/                        validation/deployment helpers
tests/direct/                   Direct Mode behavioural/adversarial suite
docs/ARCHITECTURE.md            protocol and state-machine detail
docs/SECURITY.md                threat model and explicit limitations
docs/NETWORK.md                 immutable network target
docs/DEPLOYMENT.md              live-evidence template
SUBMISSION.md                    reviewer-facing submission notes
```

## Validation

SDK-free checks:

```bash
python -m py_compile contracts/antibody.py
python scripts/preflight.py
```

Direct Mode:

```bash
pip install -r requirements-test.txt
pytest tests/direct/ -v -s
```

Deployment:

```bash
python scripts/deploy_studionet.py
```

The deploy helper uses the explicit stable Studio RPC and refuses to continue unless the RPC reports chain ID `61999`.

## Verified deployment

Antibody has a finalized successful deployment on Studionet (chain `61999`):

- Contract: `0x81B956AE9Ae7825CE4d2dE2FA2b9a8E31Aec42fb`
- Transaction: `0x8d20d16b94361c6e104dd3c3c7741f2605a5190f5e4a23b56ace2a0545765d7e`
- Explorer: [Studionet contract](https://explorer-studio.genlayer.com/address/0x81B956AE9Ae7825CE4d2dE2FA2b9a8E31Aec42fb)

The full live challenge and regression lifecycle requires the synthetic
fixture to be hosted at a public HTTPS endpoint; the checked-in fixture is
intentionally localhost-only and is not used as live evidence.

## Submission category

**Intelligent Contracts — standalone reusable primitive.**

Antibody intentionally contains no frontend, dashboard, wallet product flow, or application-specific UI.
