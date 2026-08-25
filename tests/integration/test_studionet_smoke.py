import json
import os
from pathlib import Path

import pytest
from gltest import get_contract_factory
from gltest.types import TransactionHashVariant, TransactionStatus
from gltest.utils import extract_contract_address

from tests.studionet_support import emit_record, ok, source_schema_proof, wallet_accounts


pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(os.environ.get("RUN_STUDIONET") != "1", reason="opt-in live StudioNet test"),
]


def test_studionet_semantic_max_flow_dispatch():
    accounts = wallet_accounts("flowdispatch", 5)
    owner, source_a, source_b, sink_a, sink_b = accounts[:5]
    source = Path(__file__).resolve().parents[2] / "contracts" / "flow_dispatch.py"
    factory = get_contract_factory(contract_file_path=source)
    deployed = ok(factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED))
    address = extract_contract_address(deployed)
    contract = factory.build_contract(address, account=owner)
    dispatch_id = f"{str(owner.address).lower()}:DESK-SHIFT"
    sources = json.dumps([{"name": "Mobile unit", "capacity": 1, "offer": "Provides intake or records support.", "wallet": str(source_a.address)}, {"name": "Intake specialist", "capacity": 1, "offer": "Provides intake support only.", "wallet": str(source_b.address)}])
    sinks = json.dumps([{"name": "Intake desk", "demand": 1, "need": "Needs one unit of intake support.", "wallet": str(sink_a.address)}, {"name": "Records desk", "demand": 1, "need": "Needs one unit of records support.", "wallet": str(sink_b.address)}])
    setup = ok(contract.open_dispatch(args=["desk-shift", sources, sinks, "Connect only offers that directly satisfy the stated need." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    intelligent = ok(contract.compute_flow(args=[dispatch_id]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    state = contract.get_dispatch(args=[dispatch_id]).call(transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    assert state["schema"] == "flowdispatch/dispatch/v1" and state["state"] == "DISPATCHED" and 0 <= state["total_flow"] <= 2
    proof = source_schema_proof(address, source, {"compute_flow", "allocations", "unmet_units"})
    emit_record("flowdispatch", "B", address, deployed, [setup], intelligent, accounts, proof, {"state": state["state"], "total_flow": state["total_flow"], "allocations": state["allocations"]})
