"""Supervise processes and mutate successful genotypes; task planning stays with workers."""

import multiprocessing
import random
import time
from uuid import uuid4

from ..config import Settings
from .ledger import Ledger
from .model import HaikuExecutor
from .models import Genotype, initial_genotypes
from .worker import worker_main


def mutate(genotype: Genotype, rng: random.Random) -> tuple[Genotype, str]:
    data = genotype.model_dump()
    gene = rng.choice(["effort", "bid_fraction", "max_parts", "max_tokens", "preferences"])
    if gene == "effort":
        data[gene] = rng.choice([x for x in ["low", "medium", "high"] if x != data[gene]])
    elif gene == "bid_fraction":
        data[gene] = data[gene] - 0.02 if data[gene] >= 0.28 else data[gene] + 0.02
    elif gene == "max_parts":
        data[gene] = 3 - data[gene]
    elif gene == "max_tokens":
        data[gene] = data[gene] - 256 if data[gene] >= 7936 else data[gene] + 256
    else:
        key = rng.choice(list(data[gene]))
        data[gene][key] = (
            data[gene][key] - 0.05 if data[gene][key] >= 0.95 else data[gene][key] + 0.05
        )
    return Genotype.model_validate(data), gene


def successful_parent(ledger: Ledger):
    agents = ledger.agents()
    with ledger.connection() as db:
        scored = []
        for agent in agents:
            count = db.execute(
                "SELECT COUNT(*) FROM tasks WHERE agent_id=? AND status='Completed'", (agent["id"],)
            ).fetchone()[0]
            elapsed = db.execute(
                "SELECT COALESCE(SUM(elapsed),0) FROM calls WHERE agent_id=?", (agent["id"],)
            ).fetchone()[0]
            if count:
                scored.append((count / max(elapsed, 0.001), count, agent["id"], agent))
        return max(scored, key=lambda item: item[:3])[-1] if scored else None


def replacement(ledger: Ledger, rng: random.Random):
    parent = successful_parent(ledger)
    base = Genotype.model_validate_json(parent["genotype"]) if parent else initial_genotypes()[0]
    child, gene = mutate(base, rng)
    agent_id = ledger.create_agent(child.model_dump(), parent_id=parent["id"] if parent else None)
    with ledger.transaction() as db:
        ledger.event(
            db,
            "genotype_mutated",
            "spawner",
            agent_id=agent_id,
            parent_id=parent["id"] if parent else None,
            gene=gene,
        )
    return agent_id


def run_ecosystem(
    ledger: Ledger,
    settings: Settings,
    *,
    root_id=None,
    max_seconds=600,
    seed=42,
    lease_seconds=30,
    auction_seconds=1,
    max_replacements=12,
    executor_factory=HaikuExecutor,
):
    owner = str(uuid4())
    if not ledger.supervisor_lease(owner):
        raise ValueError("Another supervisor owns this ledger.")
    ctx = multiprocessing.get_context("spawn")
    stop = ctx.Event()
    processes = {}
    rng = random.Random(seed)
    started, replacements = time.monotonic(), 0

    def launch(agent_id):
        process = ctx.Process(
            target=worker_main,
            args=(
                str(ledger.path),
                agent_id,
                settings,
                stop,
                lease_seconds,
                auction_seconds,
                executor_factory,
            ),
            name=agent_id,
        )
        process.start()
        processes[agent_id] = process

    try:
        # Previous processes cannot be resumed with their old lease tokens.
        for agent in ledger.agents("active"):
            ledger.mark_crashed(agent["id"])
        for genotype in initial_genotypes():
            launch(ledger.create_agent(genotype.model_dump()))
        while time.monotonic() - started < max_seconds:
            if not ledger.supervisor_lease(owner):
                raise ValueError("Supervisor lease was lost.")
            ledger.reap(lease_seconds=lease_seconds)
            if root_id and ledger.root(root_id)["status"] != "open":
                break
            for agent_id, process in list(processes.items()):
                agent = next(a for a in ledger.agents() if a["id"] == agent_id)
                if not process.is_alive() or agent["status"] != "active":
                    if agent["status"] == "active":
                        ledger.mark_crashed(agent_id)
                    if process.is_alive():
                        process.terminate()
                    process.join(timeout=3)
                    del processes[agent_id]
            while len(processes) < 3:
                if replacements >= max_replacements:
                    if root_id:
                        ledger.fail_root(root_id, "Replacement budget exhausted.")
                    return
                launch(replacement(ledger, rng))
                replacements += 1
            time.sleep(0.1)
    finally:
        stop.set()
        for process in processes.values():
            process.join(timeout=1)
            if process.is_alive():
                process.terminate()
                process.join(timeout=3)
        for agent_id in processes:
            ledger.stop_agent(agent_id)
        ledger.release_supervisor(owner)
