# Intelligent-contract submission

## Title

FlowDispatch — Consensus Compatibility Max-Flow

## Description

FlowDispatch is a reusable GenLayer intelligent contract for allocating
multi-unit capacity to demand when compatibility depends on natural-language
profiles. GenLayer validators independently derive a closed bipartite graph of
compatible source and sink indices under the caller's policy. Deterministic
contract code then runs a bounded augmenting-path max-flow algorithm, records
the final allocations and total flow, and exposes unmet demand before the owner
seals the result. One deployment supports many owner-keyed dispatches. The
reviewed version fully normalizes leader output before exact validator
comparison, rejects zero or ambiguous role identities, and makes missing reads
fail closed. GenVM lint and strict type checking pass, all 8 direct tests pass,
the five-validator GLSim flow passes, and the exact source was redeployed and
exercised successfully on StudioNet on 2026-09-20.

## Evidence

- Contract: https://explorer-studio.genlayer.com/address/0x96AdEf6EE9cC767112401eD91aae69400698C375
- Deployment: https://explorer-studio.genlayer.com/tx/0x77b43764f7dff8e9c850b03c5c6fa19141b96cdc233b3647a4f9523c13f58477
- Intelligent write: https://explorer-studio.genlayer.com/tx/0xaf455a3b1ce5a4cb39d2c76f1dbc68fdcc55890ea4646d00f325dff352fa721a
- Exact-source proof: https://github.com/Leokings/flowdispatch/blob/main/deployments/studionet.json

## GitHub repository

https://github.com/Leokings/flowdispatch
