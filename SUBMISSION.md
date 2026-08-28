Project name: FlowDispatch

Category: Intelligent Contracts

Batch: B

One-line description: Semantic compatibility max-flow dispatch.

What it does: Consensus builds a source-to-sink compatibility graph; deterministic augmenting paths calculate a multi-unit feasible flow rather than one-to-one matching.

Why GenLayer: GenLayer consensus performs the bounded semantic step, then deterministic contract code executes and stores the mechanism-specific result.

Reusable: Yes. One deployment supports many independently keyed records and callers; the live fixture is only an example.

Repository: https://github.com/Leokings/flowdispatch (private; reviewers require read access).

Contract source: contracts/flow_dispatch.py

Source SHA-256: 01de57c491fd6179892745e9637b490b26bbe452ebfd542bcb1d6d31d3702add

StudioNet contract: https://explorer-studio.genlayer.com/address/0xcfd1Eea2067e582482aa509104960566E033d610

Deployment transaction: https://explorer-studio.genlayer.com/tx/0x6c16b553f70bdf1b830b4ca19e83d0f31d4c8ac31a7212a8fdb0d3b1d2ae80dd

Intelligent transaction: https://explorer-studio.genlayer.com/tx/0x8e75d66ddc8570adec8f272666aaadba15e6f12c4cc7aae892305463c2a012e4

Verification: GenVM lint PASS; strict typecheck PASS; 4 direct tests PASS; five-validator GLSim PASS; finalized StudioNet intelligent write and latest-final readback PASS; exact deployed-source and schema verification PASS.

Originality: Compared with 161 workspace contract sources. Nearest pre-existing structural score is 0.162197; mechanism and source hash are distinct.

Data boundary: Caller-supplied public data only. No external source fetching, funds, identity attestation, legal effect, or private-data guarantee.

Plain-text portal fields: SUBMISSION.txt. Notes / Description is within the 1,000-character form limit.
