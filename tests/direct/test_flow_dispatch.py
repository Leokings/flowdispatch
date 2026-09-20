import json


POLICY = "Connect a source and sink only when the offered capability directly satisfies the stated need."


def _sides(wallets):
    sources = json.dumps([
        {"name": "Mobile unit", "capacity": 1, "offer": "Provides either intake support or records support.", "wallet": str(wallets[0])},
        {"name": "Intake specialist", "capacity": 1, "offer": "Provides intake support only.", "wallet": str(wallets[1])},
    ])
    sinks = json.dumps([
        {"name": "Intake desk", "demand": 1, "need": "Needs one unit of intake support.", "wallet": str(wallets[2])},
        {"name": "Records desk", "demand": 1, "need": "Needs one unit of records support.", "wallet": str(wallets[3])},
    ])
    return sources, sinks


def _open(contract, vm, owner, wallets):
    sources, sinks = _sides(wallets)
    vm.sender = owner
    return contract.open_dispatch("desk-shift", sources, sinks, POLICY)


def test_residual_rerouting_reaches_true_max_flow(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    wallets = [direct_bob, direct_charlie, direct_accounts[3], direct_accounts[4]]
    dispatch_id = _open(contract, direct_vm, direct_alice, wallets)
    direct_vm.mock_llm(r".*Build the bipartite compatibility edges for multi-unit dispatch.*", json.dumps({"compatible_edges": [[0, 0], [0, 1], [1, 0]]}))
    contract.compute_flow(dispatch_id)
    assert contract.get_dispatch(dispatch_id)["total_flow"] == 2
    assert contract.allocations(dispatch_id) == [[0, 1, 1], [1, 0, 1]]


def test_unmet_units_are_explicit(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    wallets = [direct_bob, direct_charlie, direct_accounts[3], direct_accounts[4]]
    dispatch_id = _open(contract, direct_vm, direct_alice, wallets)
    direct_vm.mock_llm(r".*Build the bipartite compatibility edges.*", json.dumps({"compatible_edges": [[1, 0]]}))
    contract.compute_flow(dispatch_id)
    assert contract.unmet_units(dispatch_id) == 1


def test_wallet_roles_cannot_overlap(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    sources, sinks = _sides([direct_bob, direct_charlie, direct_bob, direct_accounts[3]])
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("wallet_roles_overlap"):
        contract.open_dispatch("bad-shift", sources, sinks, POLICY)


def test_edge_endpoint_is_bounded(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    wallets = [direct_bob, direct_charlie, direct_accounts[3], direct_accounts[4]]
    dispatch_id = _open(contract, direct_vm, direct_alice, wallets)
    direct_vm.mock_llm(r".*Build the bipartite compatibility edges.*", json.dumps({"compatible_edges": [[0, 9]]}))
    with direct_vm.expect_revert("[LLM_ERROR] edge_out_of_bounds"):
        contract.compute_flow(dispatch_id)


def test_validator_rejects_extra_leader_fields(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    wallets = [direct_bob, direct_charlie, direct_accounts[3], direct_accounts[4]]
    dispatch_id = _open(contract, direct_vm, direct_alice, wallets)
    edges = [[0, 0], [0, 1], [1, 0]]
    direct_vm.mock_llm(
        r".*Build the bipartite compatibility edges for multi-unit dispatch.*",
        json.dumps({"compatible_edges": edges}),
    )
    contract.compute_flow(dispatch_id)
    assert direct_vm.run_validator() is True
    assert direct_vm.run_validator(
        leader_result={"compatible_edges": edges, "extra": True}
    ) is False


def test_missing_unmet_units_view_fails_closed(contract, direct_vm):
    with direct_vm.expect_revert("dispatch_missing"):
        contract.unmet_units("missing-dispatch")


def test_zero_wallet_is_rejected(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    sources, sinks = _sides([
        "0x" + "0" * 40,
        direct_charlie,
        direct_accounts[3],
        direct_accounts[4],
    ])
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("invalid_wallet"):
        contract.open_dispatch("zero-wallet", sources, sinks, POLICY)


def test_side_names_must_be_unique_case_insensitively(contract, direct_vm, direct_alice, direct_bob, direct_charlie, direct_accounts):
    sources = json.dumps([
        {"name": "Mobile Unit", "capacity": 1, "offer": "Provides general intake support.", "wallet": str(direct_bob)},
        {"name": "mobile unit", "capacity": 1, "offer": "Provides specialist intake support.", "wallet": str(direct_charlie)},
    ])
    _, sinks = _sides([direct_bob, direct_charlie, direct_accounts[3], direct_accounts[4]])
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("invalid_or_duplicate_sources_entry"):
        contract.open_dispatch("duplicate-name", sources, sinks, POLICY)
