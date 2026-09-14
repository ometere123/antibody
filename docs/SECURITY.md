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

### State before payout

For confirmed challenges and withdrawals, storage accounting is updated before the outgoing transfer message is emitted.

## Endpoint admission

Registered endpoints must be canonical public HTTPS DNS URLs. The contract rejects obvious local/private/ambiguous targets, explicit ports, userinfo, query strings, fragments and percent-encoded ambiguity. Runtime egress protections remain an additional boundary.
