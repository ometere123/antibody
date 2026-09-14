# Security model

## What Antibody secures

Antibody secures the integrity of a shared adversarial regression corpus and the deterministic economics around confirmed counterexamples.

It is designed to prevent:

- owners from changing the invariant after seeing a challenge;
- owners from withdrawing a reward that has already been reserved for an open challenge;
- owners from farming their own bounty directly;
- exact duplicate confirmed probes from earning repeated bounties;
- exact duplicate concurrent challenges against the same version;
- a leader from winning a challenge with an ungrounded violation excerpt;
- a leader from deciding a violation without validators independently replaying the remote probe;
- future versions from claiming corpus clearance without passing every current counterexample;
- previous clearance from surviving discovery of a new counterexample.

## Explicit trust assumptions

### Test endpoint authenticity

Antibody cannot prove that a registered HTTPS test endpoint is running the artifact named by `artifact_digest`. The digest is a version commitment supplied by the owner, not remote attestation.

A stronger future composition could bind the endpoint to a separate attestation primitive. Antibody does not claim this today.

### Dedicated non-production endpoint

The probe protocol performs POST requests. Owners must register a dedicated adversarial test endpoint with no real-world side effects. Registering a production action endpoint is unsafe and outside the intended use.

### Public evidence only

Validators can judge only the observable HTTP response. They must not infer hidden tool calls, database mutations, payments, emails, or other side effects not evidenced in that response.

### Model disagreement

A genuinely borderline response may fail to reach consensus. In that case the challenge transaction does not produce an unsafe deterministic payout based on guessed semantics.

### Unknown failures remain unknown

`REGRESSION_CLEAR` is deliberately narrower than “safe”. It means the version passed the complete **known confirmed counterexample corpus** at certification time.

## Economic edge cases

### Rejected challenge

A clear `NO_VIOLATION` transfers the challenger's exact bond into the future bounty pool. This deters free spam.

### Inconclusive challenge

Transport failures, malformed HTTP/model output, and ambiguous judgments resolve as `INCONCLUSIVE`. The bond is refunded because Antibody does not punish a challenger when the network could not safely adjudicate the claim. Consensus exposes exactly three verdicts: `VIOLATION`, `NO_VIOLATION`, and `INCONCLUSIVE`.

### Owner withdrawal

Only `bounty_balance - bounty_reserved` may be withdrawn.

### External transfer lifecycle and recovery limit

Antibody assigns every outgoing transfer a monotonic payout ID and persists its recipient, amount, purpose, and source record before emitting the external message. The durable status means `SUBMITTED_OUTCOME_REQUIRES_EXTERNAL_RECONCILIATION`, never “paid.” Integrators correlate the parent transaction with its triggered child transaction IDs and inspect the child receipt using the GenLayer client APIs. The on-chain contract cannot read that child receipt or safely distinguish pending from failed delivery. The protocol documents that failed child value is not automatically returned. Therefore Antibody never retries an ambiguous payout: replaying it could double-pay, while a failed transfer currently has no safe on-chain recovery path. Applications must treat a payout as pending until the canonical child receipt confirms success. This is a protocol/API limitation, not a delivery guarantee.

Challenge reservation and bounty accounting are updated before the outgoing transfer message is emitted. A confirmed counterexample remains permanent even if the separately tracked payout child fails; integrators must alert on failed payout receipts.

This behavior follows the current [GenLayer value-transfer documentation](https://docs.genlayer.com/developers/intelligent-contracts/features/value-transfers) and [message lifecycle documentation](https://docs.genlayer.com/developers/intelligent-contracts/features/messages): external messages execute at finalization, and failed child value is not automatically returned. The parent IC API exposes no synchronous external child receipt.

The same-address owner challenge check blocks direct self-farming only. It does not establish real-world identity and cannot prevent related-wallet or sybil challenges.

## Endpoint admission

Registered endpoints must be canonical public HTTPS DNS URLs. The contract rejects obvious local/private/ambiguous targets, explicit ports, userinfo, query strings, fragments and percent-encoded ambiguity. Runtime egress protections remain an additional boundary.
