import random
from concurrent.futures import ThreadPoolExecutor

import pytest

from algo_discovery.swarm.ledger import BudgetExhausted, LeaseLost, Ledger
from algo_discovery.swarm.models import initial_genotypes
from algo_discovery.swarm.supervisor import mutate, replacement


@pytest.fixture
def market(tmp_path):
    clock = [100.0]
    ledger = Ledger(tmp_path / "ledger.sqlite3", clock=lambda: clock[0])
    ledger.initialize()
    root = ledger.submit({"abstract": "A sufficiently long abstract for a local ledger test."})
    agents = [ledger.create_agent(g.model_dump()) for g in initial_genotypes()]
    return ledger, root, agents, clock


def win(ledger, task, agent, amount=2000):
    assert ledger.bid(task, agent, amount, 1, auction_seconds=0)
    ledger.award_due()
    return ledger.assignment(agent)


def outcome(solved, remaining):
    return {
        "completed_requirements": solved,
        "child_groups": [remaining] if remaining else [],
        "specification": {},
        "summary": "test",
        "changes": [],
    }


def test_auction_reserves_funds_then_charges_only_winner(market):
    ledger, root, agents, clock = market
    for agent, amount in zip(agents, [2000, 1000, 500], strict=True):
        assert ledger.bid(root, agent, amount, 0.8, auction_seconds=1)
    assert [a["balance"] for a in ledger.agents()] == [10000] * 3
    assert not ledger.bid(root, agents[0], 2000, 0.9)
    clock[0] += 2
    ledger.award_due()
    assert [a["balance"] for a in ledger.agents()] == [8000, 10000, 10000]
    assert all(a["reserved"] == 0 for a in ledger.agents())
    assert ledger.assignment(agents[0])["status"] == "Assigned"


def test_partial_reward_child_escrow_and_failure_burn(market):
    ledger, root, agents, _ = market
    task = win(ledger, root, agents[0])
    result = outcome(["problem", "equations"], ["circuit_plan", "measurement", "audit"])
    ledger.complete(root, agents[0], task["token"], result)
    assert ledger.agents()[0]["balance"] == 28000
    assert ledger.root(root)["status"] == "open"  # Own portion done, whole tree pending.
    child = next(t for t in ledger.tasks(root) if t["parent_id"] == root)
    assert child["reward"] == 30000
    assigned = win(ledger, child["id"], agents[1], 5000)
    ledger.fail(child["id"], agents[1], assigned["token"], "simulated OOM")
    assert ledger.agents()[1]["balance"] == 0
    assert ledger.agents()[1]["status"] == "dead"
    assert ledger.summary(root)["escrow_remaining_cents"] == 30000
    new = replacement(ledger, random.Random(42))
    born = next(a for a in ledger.agents() if a["id"] == new)
    assert born["balance"] == 10000
    assert born["parent_id"] == agents[0]
    assert ledger.verify_history()


def test_expired_lease_reopens_task_and_fences_stale_completion(market):
    ledger, root, agents, clock = market
    old = win(ledger, root, agents[0])
    clock[0] += 20
    ledger.heartbeat(agents[0])
    clock[0] += 31
    ledger.reap()
    assert ledger.tasks(root)[0]["status"] == "Open"
    assert ledger.agents()[0]["balance"] == 0
    with pytest.raises(LeaseLost):
        ledger.complete(
            root,
            agents[0],
            old["token"],
            outcome(["problem"], ["equations", "circuit_plan", "measurement", "audit"]),
        )
    # A late heartbeat does not revive the dead worker or its expired token.
    ledger.heartbeat(agents[0])
    assert ledger.agents()[0]["status"] == "dead"


def test_double_completion_is_paid_exactly_once(market):
    ledger, root, agents, _ = market
    task = win(ledger, root, agents[0])
    result = outcome(["problem", "equations"], ["circuit_plan", "measurement", "audit"])

    def settle(_):
        try:
            ledger.complete(root, agents[0], task["token"], result)
            return True
        except LeaseLost:
            return False

    with ThreadPoolExecutor(max_workers=2) as pool:
        assert sum(pool.map(settle, range(2))) == 1
    assert ledger.summary(root)["paid_cents"] == 20000
    assert len(ledger.tasks(root)) == 2


def test_remaining_work_cannot_be_dropped_duplicated_or_minted(market):
    ledger, root, agents, _ = market
    task = win(ledger, root, agents[0])
    for bad in [
        outcome([], []),
        outcome(["problem"], []),
        outcome(["problem"], ["equations", "equations", "circuit_plan", "measurement", "audit"]),
    ]:
        with pytest.raises(ValueError):
            ledger.complete(root, agents[0], task["token"], bad)
    assert ledger.summary(root)["paid_cents"] == 0
    assert len(ledger.tasks(root)) == 1


def test_call_budget_is_atomic_and_usage_is_distinct_from_virtual_money(market):
    ledger, _, agents, _ = market
    root = ledger.submit({"abstract": "Another bounded local ledger task."}, max_calls=1)
    task = win(ledger, root, agents[0])
    call = ledger.reserve_call(root, agents[0], task["token"], "claude-haiku-5-5")
    with pytest.raises(BudgetExhausted):
        ledger.reserve_call(root, agents[0], task["token"], "claude-haiku-5-5")
    ledger.finish_call(call, status="returned", input_tokens=150, output_tokens=100, elapsed=0.2)
    ledger.finish_call(call, status="succeeded")
    report = ledger.summary(root)
    assert (report["input_tokens"], report["output_tokens"]) == (150, 100)
    assert report["calls_without_usage"] == 0
    assert next(a for a in ledger.agents() if a["id"] == agents[0])["balance"] == 8000


def test_failed_root_rejects_late_settlement(market):
    ledger, root, agents, _ = market
    task = win(ledger, root, agents[0])
    ledger.fail_root(root, "provider blocked")
    with pytest.raises(LeaseLost):
        ledger.complete(
            root,
            agents[0],
            task["token"],
            outcome(["problem"], ["equations", "circuit_plan", "measurement", "audit"]),
        )
    assert all(task["status"] == "Failed" for task in ledger.tasks(root))


def test_failed_root_releases_pending_bid_reservations(market):
    ledger, root, agents, _ = market
    assert ledger.bid(root, agents[0], 2000, 1)
    ledger.fail_root(root, "provider blocked")
    assert all(agent["reserved"] == 0 for agent in ledger.agents())
    assert ledger.summary(root)["paid_cents"] == 0


def test_history_tamper_is_detected_and_supervisor_is_exclusive(market):
    ledger, _, _, clock = market
    assert ledger.supervisor_lease("first")
    assert not ledger.supervisor_lease("second")
    clock[0] += 31
    assert ledger.supervisor_lease("second")
    assert ledger.verify_history()
    with ledger.transaction() as db:
        db.execute("UPDATE events SET data='{}' WHERE seq=1")
    assert not ledger.verify_history()


def test_mutation_changes_exactly_one_gene():
    genotype = initial_genotypes()[0]
    for seed in range(30):
        child, gene = mutate(genotype, random.Random(seed))
        before, after = genotype.model_dump(), child.model_dump()
        assert [key for key in before if before[key] != after[key]] == [gene]
        if gene == "preferences":
            assert sum(before[gene][key] != after[gene][key] for key in before[gene]) == 1


def test_attempt_limit_terminates_instead_of_requeueing_forever(market):
    ledger, _, agents, _ = market
    root = ledger.submit({"abstract": "Another bounded local ledger task."}, max_attempts=1)
    task = win(ledger, root, agents[0])
    ledger.fail(root, agents[0], task["token"], "invalid output")
    assert ledger.root(root)["status"] == "failed"
    assert ledger.tasks(root)[0]["status"] == "Failed"
