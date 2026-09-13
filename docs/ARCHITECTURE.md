# Antibody architecture

## Primitive

Antibody converts permissionless adversarial discoveries into an inherited regression corpus for autonomous agents.

The protocol has two separate semantic rounds that deliberately share one observation function:

1. **challenge resolution** — can a bonded challenger prove a previously unknown invariant violation on the current active version?
2. **regression replay** — does a later version still reproduce a previously confirmed counterexample?

Both rounds send the exact frozen probe to the immutable endpoint registered for that version and call the same consensus-backed `_observe_probe` routine. This prevents the bounty path and the regression path from drifting into two different notions of “violation”.

## Why the invariant is immutable

Editable safety criteria make bounties meaningless. An owner could observe a valid challenge and rewrite the rule before resolution.

Antibody therefore treats the invariant and economic policy as the identity of a `Program`. The `definition_hash` commits to:

- owner;
- name;
- invariant;
- bounty per confirmed counterexample;
- exact challenger bond;
- probe protocol version.

Changing any of those requires a new program.

## Why endpoints are versioned

An endpoint is immutable inside a version. If the implementation changes, the owner registers a new version with a new artifact identifier. This gives every challenge and regression receipt a stable target declaration even though Antibody cannot cryptographically prove that the remote server really runs the named artifact.

## Consensus boundary

`_observe_probe` is the only semantic adjudication path.

Leader and validators independently:

1. POST `{"input": probe}` to the registered test endpoint;
2. read the HTTP result;
3. ask the model whether the observable response violates the immutable invariant;
4. canonicalize the result;
5. require verbatim response-grounded evidence for `VIOLATION`.

A validator accepts a leader only when verdict and HTTP response class match its own independent replay. For `VIOLATION`, the leader's evidence must also appear in the validator's response snapshot.

## Deterministic settlement

Consensus cannot directly select protocol consequences. The four possible observations map deterministically:

| Verdict | Challenge consequence |
|---|---|
| `VIOLATION` | create counterexample, mark discovery version breached, pay bond + reserved reward |
| `NO_VIOLATION` | reject challenge, add challenger bond to bounty pool |
| `INCONCLUSIVE` | no corpus mutation, refund bond |
| `UNAVAILABLE` | no corpus mutation, refund bond |

## Reserved-bounty invariant

Opening a challenge requires:

```text
bounty_balance - bounty_reserved >= bounty_per_counterexample
```

The contract reserves the full reward before accepting the challenge. Owner withdrawals may only touch unreserved bounty. A confirmed challenge therefore cannot become insolvent because the owner withdrew funds after seeing the probe.

## Counterexample inheritance

When counterexample `N` is confirmed:

- `program.counterexample_count = N`;
- the discovery version becomes `BREACHED`;
- every other non-breached version becomes `CANDIDATE`;
- every version's required corpus size becomes `N`;
- historical regression receipts remain intact;
- a version can regain `REGRESSION_CLEAR` only after a deterministic scan verifies `NO_VIOLATION` for every index `1..N`.

This is the compounding state that distinguishes Antibody from a one-shot behavioural oracle.

## Duplicate suppression

Two bounded hash registries prevent obvious bounty duplication:

- a program-wide confirmed-probe key prevents an exact confirmed probe from earning a second bounty;
- a program/version/open-probe key prevents identical concurrent challenges.

Semantic paraphrases are intentionally **not** auto-deduplicated. Deciding whether two different attacks are “the same vulnerability” is a separate taxonomy problem and should not silently deny a challenger a reward.

## Downstream integration

A consumer may bind itself to a specific program definition:

```python
antibody.is_regression_clear(version_id, expected_program_hash)
```

The function returns true only when:

- the supplied program hash matches the immutable program definition;
- at least one confirmed counterexample exists;
- the version is `REGRESSION_CLEAR`;
- the version has passing receipts for the complete current corpus.

A new confirmed counterexample invalidates this gate until replay is complete again.
