"""Independent OS worker: ledger -> bids -> lease -> model contribution -> ledger."""

import threading

from ..config import Settings
from .domain import check_contribution, context, proposal
from .ledger import BudgetExhausted, LeaseLost, Ledger
from .model import HaikuExecutor, ProviderBlocked, ProviderInterrupted
from .models import Genotype


def worker_main(
    path,
    agent_id,
    settings: Settings,
    stop,
    lease_seconds=30,
    auction_seconds=1,
    executor_factory=HaikuExecutor,
):
    ledger = Ledger(path)
    local_done = threading.Event()

    def ping():
        while not stop.is_set() and not local_done.is_set():
            ledger.heartbeat(agent_id, lease_seconds=lease_seconds)
            local_done.wait(min(10, lease_seconds / 3))

    heartbeat = threading.Thread(target=ping, daemon=True)
    heartbeat.start()
    executor = executor_factory(settings)
    try:
        while not stop.is_set():
            agents = {a["id"]: a for a in ledger.agents()}
            agent = agents[agent_id]
            if agent["status"] != "active" or agent["balance"] <= 0:
                break
            task = ledger.assignment(agent_id)
            if task:
                perform(ledger, task, agent, executor, settings.model)
                continue
            # Start auctions only after all three processes have registered readiness.
            # Existing assigned work still heartbeats/executes while a replacement boots.
            if sum(a["status"] == "active" and a["ready"] for a in agents.values()) < 3:
                stop.wait(0.1)
                continue
            for candidate in ledger.open_tasks():
                bid = proposal(ledger, candidate, agent)
                if bid:
                    ledger.bid(candidate["id"], agent_id, *bid, auction_seconds=auction_seconds)
                    break
            ledger.award_due(lease_seconds=lease_seconds)
            stop.wait(0.1)
    finally:
        local_done.set()
        heartbeat.join(timeout=2)


def perform(ledger, task, agent, executor, model):
    call_id = None
    try:
        genotype = Genotype.model_validate_json(agent["genotype"])
        ctx = context(ledger, task, genotype)
        ctx["agent_id"] = agent["id"]
        call_id = ledger.reserve_call(task["id"], agent["id"], task["token"], model)
        result, usage = executor.execute(ctx, genotype)
        ledger.finish_call(call_id, status="returned", **usage)
        check_contribution(result, ctx, genotype)
        ledger.complete(task["id"], agent["id"], task["token"], result.model_dump())
        ledger.finish_call(call_id, status="succeeded")
    except LeaseLost:
        if call_id:
            ledger.finish_call(call_id, status="stale")
    except (BudgetExhausted, ProviderBlocked) as exc:
        if call_id:
            ledger.finish_call(call_id, status="provider_blocked")
        ledger.fail_root(task["root_id"], str(exc))
    except ProviderInterrupted as exc:
        if call_id:
            ledger.finish_call(call_id, status="provider_interrupted")
        # Environmental errors are bounded by the root call budget, not interpreted as a genotype defect.
        with ledger.transaction() as db:
            owned = ledger.owned(db, task["id"], agent["id"], task["token"])
            ledger.requeue(db, owned, str(exc))
    except (ValueError, TypeError, KeyError) as exc:
        if call_id:
            ledger.finish_call(call_id, status="invalid_output")
        try:
            ledger.fail(
                task["id"], agent["id"], task["token"], type(exc).__name__ + ": " + str(exc)[:300]
            )
        except LeaseLost:
            pass
