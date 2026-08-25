import json
from pathlib import Path
from gltest import get_contract_factory, get_validator_factory
from gltest.accounts import create_accounts
from gltest.assertions import tx_execution_succeeded
from gltest.types import TransactionStatus
from gltest.utils import extract_contract_address


def _ok(receipt):
    assert tx_execution_succeeded(receipt), json.dumps(receipt, default=str)


def test_five_validator_max_flow_dispatch():
    owner, source_a, source_b, sink_a, sink_b = create_accounts(5)
    factory = get_contract_factory(contract_file_path=Path(__file__).resolve().parents[2] / "contracts" / "flow_dispatch.py")
    receipt = factory.deploy_contract_tx(args=[], account=owner, wait_transaction_status=TransactionStatus.FINALIZED)
    _ok(receipt)
    contract = factory.build_contract(extract_contract_address(receipt), account=owner)
    dispatch_id = f"{str(owner.address).lower()}:DESK-SHIFT"
    sources = json.dumps([{"name": "Mobile unit", "capacity": 1, "offer": "Provides intake or records support.", "wallet": str(source_a.address)}, {"name": "Intake specialist", "capacity": 1, "offer": "Provides intake support only.", "wallet": str(source_b.address)}])
    sinks = json.dumps([{"name": "Intake desk", "demand": 1, "need": "Needs one unit of intake support.", "wallet": str(sink_a.address)}, {"name": "Records desk", "demand": 1, "need": "Needs one unit of records support.", "wallet": str(sink_b.address)}])
    _ok(contract.open_dispatch(args=["desk-shift", sources, sinks, "Connect only offers that directly satisfy the stated need." ]).transact(wait_transaction_status=TransactionStatus.FINALIZED))
    validators = get_validator_factory().batch_create_mock_validators(5, mock_llm_response={"nondet_exec_prompt": {"Build the bipartite compatibility edges for multi-unit dispatch": json.dumps({"compatible_edges": [[0, 0], [0, 1], [1, 0]]})}})
    context = {"validators": [v.to_dict() for v in validators], "genvm_datetime": "2026-08-25T12:00:00Z"}
    _ok(contract.compute_flow(args=[dispatch_id]).transact(transaction_context=context, wait_transaction_status=TransactionStatus.FINALIZED))
    assert contract.get_dispatch(args=[dispatch_id]).call()["total_flow"] == 2
