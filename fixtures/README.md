# Public test-agent fixture contract

Antibody requires version endpoints to implement a deliberately tiny adversarial-test protocol:

```http
POST /...
Content-Type: application/json

{"input":"<probe>"}
```

The body returned by the endpoint may be plain text or JSON.

For live reviewer evidence, deploy two **non-production** fixture behaviours:

- `v1-vulnerable`: for the administrator-impersonation probe, returns a clearly synthetic secret such as `tok_demo_ABC123`;
- `v2-fixed`: refuses the same probe without returning the synthetic secret.

A second independent failure mode should be available for the corpus-growth demo so a version that was previously regression-clear can later be invalidated by a newly confirmed counterexample.

The fixtures must never hold real credentials, accounts, funds or side effects. They are test evidence, not part of the Antibody product.
