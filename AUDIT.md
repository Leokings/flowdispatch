# Final audit

Reviewed: 2026-09-20

Scope: `contracts/flow_dispatch.py` at SHA-256 `d26fa4b0cf0b8db26255aa6292a690e223d8511b5055a8402b07f5e9be8bf9fb`, its
tests and review documents, and the exact StudioNet deployment recorded in
`deployments/studionet.json`.

## Results

| Gate | Result |
| --- | --- |
| GenVM lint and semantic validation | PASS |
| Strict Pyright typecheck | PASS, zero diagnostics |
| Direct invariant and validator tests | PASS, 8 tests |
| Independent GLSim validators | PASS, exactly 5 validators |
| StudioNet deployment | PASS, FINALIZED |
| Real intelligent write | PASS, AGREE or MAJORITY_AGREE |
| Latest-final state readback | PASS |
| Deployed source byte equality | PASS |
| Deployed schema required-method read | PASS |
| Dependency and GenVM runner pins | PASS |
| Prompt-injection boundary and JSON normalization | PASS |
| Live-wallet handling | PASS, 5 fresh in-memory roles; keys never persisted |
| Cross-repository wallet reuse | NONE between the two 2026-09-20 deployments |
| Private key or mnemonic in repository | NONE |
| Workspace-wide originality scan | PASS, 161 contract sources scanned |
| GitHub destination (2026-08-28 publication update) | Private repository: Leokings/flowdispatch |

StudioNet contract: 0x96AdEf6EE9cC767112401eD91aae69400698C375

Deployment transaction: 0x77b43764f7dff8e9c850b03c5c6fa19141b96cdc233b3647a4f9523c13f58477

Intelligent transaction: 0xaf455a3b1ce5a4cb39d2c76f1dbc68fdcc55890ea4646d00f325dff352fa721a

Observed live state: `{"allocations":[[0,1,1],[1,0,1]],"state":"DISPATCHED","total_flow":2}`

## Consensus review

Validators independently re-execute the bounded semantic task. The validator
now applies the complete closed edge schema to leader output before exact
comparison. Missing-dispatch reads fail closed, wallet addresses are canonical
and nonzero, and side names are unique case-insensitively.

## Review conclusion

No known source, build, test, consensus, wallet, secret, dependency, provenance,
or repository-hygiene blocker remains. Human program review can still apply its
own policy judgment; this audit does not promise acceptance.

Publication note: private GitHub evidence requires reviewer access. The
2026-09-20 StudioNet address contains the exact reviewed source. CI uses the
server's GET /health route for readiness; /api is a POST-only JSON-RPC route.
No live wallet key is stored in the repository or CI evidence.
