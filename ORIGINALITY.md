# Originality audit

The original mechanism source was compared against 161 GenLayer contract
sources in the workspace. All twenty new target contracts were excluded from
the pre-existing comparison pool. The 2026-09-20 hardening changed only the
consensus boundary, role validation, and a missing-record view; it did not
introduce a new mechanism or copy another implementation.

Nearest pre-existing source: `promocart\contracts\promotion_rule_engine.py`

Combined structural score: `0.162197`

Token score: `0.267577`

AST score: `0.081167`

Nearest contract in this new set: `portfolioknapsack\contracts\portfolio_knapsack.py` with combined
score `0.468863`. That score reflects shared safe GenLayer
boilerplate. The mechanisms differ materially:

- This repository: Consensus builds a source-to-sink compatibility graph; deterministic augmenting paths calculate a multi-unit feasible flow rather than one-to-one matching.
- Other repository: Consensus rates bounded proposals; deterministic zero-one knapsack maximizes total benefit under a declared capacity with explicit tie-breaking.

The two do not share the same semantic input, deterministic algorithm, storage
record, state lifecycle, or decision views. Exact source SHA-256 values are also
unique across all twenty repositories. The complete machine-readable reports are
`review-tools/twenty-originality-audit.json` and
`review-tools/twenty-pairwise-audit.json` at the workspace level.

Similarity scoring is a review aid, not a guarantee of a human review outcome.

## Accepted/pending Portal comparison — 2026-09-20

The title and mechanism were checked against the 26 accepted and two pending
Portal submissions. No submission combines consensus-derived bipartite
compatibility edges with deterministic multi-unit max-flow allocation. The
closest concepts remain materially distinct:

- `Semantic Resource Mutex` resolves exclusive resource conflicts; it does not
  allocate capacities and demands over a compatibility graph.
- `Consensus Asset Admission & Trait Mapper` classifies assets and traits; it
  does not solve a flow network or expose unmet demand.
- `Bounded Saga Recovery Governor` chooses a recovery plan; it does not compute
  source-to-sink allocations.

A workspace search outside this repository found no other Python contract using
`compatible_edges`, `_max_flow`, `max flow`, or `unmet_units`.
