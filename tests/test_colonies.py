"""Collective survival: treasury routing, colony death and replacement, funded respawns, and
the no-selection control."""

import json
import random

import pytest

from a2m.llm.client import LLM, Budget
from a2m.run import run
from a2m.sandbox import Sandbox
from a2m.swarm.agent import Agent
from a2m.swarm.colonies import Colonies, ColoniesConfig, ColonyConfig, Genome
from a2m.swarm.economy import Economy, EconomyConfig
from a2m.swarm.runtime import Swarm, SwarmConfig
from a2m.tasks import load_card
from a2m.workspace import Workspace


def _agent(e=5.0):
    return Agent(id="a", model="m", energy=e, affinities={})


def test_collective_routes_everything_through_treasury():
    eco = Economy(EconomyConfig(), "collective", treasury=10.0)
    a = _agent()
    eco.charge(a, "implement", 0)
    eco.distribute([("a", "implement")], 4.0, {"a": a}, 0, "x")
    assert a.energy == 5.0 and eco.treasury == pytest.approx(10 - 2 + 4 * 0.45)
    a.energy = -1
    assert not eco.is_dead(a) and not eco.can_spawn(a) and eco.colony_mortal


def test_both_taxes_earnings_and_agents_pay_costs():
    eco = Economy(EconomyConfig(), "both", treasury=0.0, tax=0.25)
    a = _agent()
    eco.charge(a, "implement", 0)
    assert a.energy == 3.0 and eco.treasury == 0.0
    eco.distribute([("a", "implement")], 4.0, {"a": a}, 0, "x")
    assert a.energy == pytest.approx(3 + 1.8 * 0.75) and eco.treasury == pytest.approx(1.8 * 0.25)
    a.energy = 0
    assert eco.is_dead(a)


def test_individual_mode_is_unchanged():
    eco = Economy(EconomyConfig())
    assert eco.treasury is None and not eco.colony_mortal and eco.agents_mortal


def test_colony_charge_refuses_when_broke():
    eco = Economy(EconomyConfig(), "both", treasury=2.0)
    assert not eco.colony_charge(3.0, "respawn", 0) and eco.treasury == 2.0
    assert eco.colony_charge(2.0, "respawn", 0) and eco.treasury == 0.0


def test_genome_mutation_stays_in_bounds():
    rng = random.Random(0)
    g = Genome.default(SwarmConfig())
    for _ in range(200):
        g = g.mutate(rng, 0.5)
        assert 1 <= g.min_families <= 5 and 1 <= g.max_attempts <= 5
        assert 0 <= g.critiques_required <= 2
        assert all(0.25 <= v <= 4.0 for v in g.role_bias.values())
    cfg = Genome(g.role_bias, 2, 4, 0).apply(SwarmConfig())
    assert cfg.min_families == 2 and cfg.max_attempts == 4 and not cfg.critics_enabled


def _ws(tmp_path, budget):
    return Workspace(load_card("arxiv-1407.6402"), Sandbox(), budget, tmp_path / "r",
                     verbose=False)


def test_both_mode_respawns_are_paid_by_the_colony(tmp_path):
    budget = Budget(1.0)
    swarm = Swarm(_ws(tmp_path, budget), {}, SwarmConfig(n_agents=3), 0, survival="both",
                  treasury=5.0, respawn_cost=3.0)
    for _ in range(3):
        swarm._new_agent()
    for a in swarm.agents.values():
        a.energy = 0.0
    swarm._lifecycle()
    assert len(swarm.lineage.deaths) == 3
    assert swarm.respawns == 1 and swarm.economy.treasury == pytest.approx(2.0)
    assert len(swarm.alive()) == 1


def test_broke_colonies_die_and_are_refounded_with_history(tmp_path):
    budget = Budget(1.0)
    ws = _ws(tmp_path, budget)
    cfg = ColoniesConfig(
        SwarmConfig(n_agents=3, max_agents=3, models=["claude-haiku-5-5"]),
        ColonyConfig(survival="collective", n_colonies=2, initial_treasury=2.0, max_rounds=6,
                     max_foundings=3, parallel_colonies=False))
    llm = LLM("claude-haiku-5-5", budget, "mock", mock_seed=0)
    col = Colonies(ws, {"claude-haiku-5-5": llm}, cfg, seed=0)
    col.run()
    st = col.stats()
    assert st["colony_deaths"] >= 1 and st["foundings"] >= 1
    assert all(d["cause"] for d in st["colony_lineage"])
    founded = col.colonies[2:]
    assert founded
    notes = [a.notes for c in founded for a in c.swarm.agents.values()]
    assert any("Colony k" in n and "died" in n for n in notes)
    # every colony's candidates are merged for submission with unique ids
    assert all(cid.startswith("k") for cid in ws.candidates)


@pytest.fixture
def _runs(tmp_path, monkeypatch):
    monkeypatch.setenv("A2M_RUNS_DIR", str(tmp_path / "runs"))


@pytest.mark.parametrize("variant", ["swarm_collective", "swarm_both"])
def test_colony_variants_run_end_to_end(_runs, variant):
    d = run(variant, "arxiv-1411.5949", seed=0, llm_mode="mock", verbose=False)
    sub = json.loads((d / "submission.json").read_text())
    assert sub["candidates"] and sub["stats"]["survival"] in ("collective", "both")
    assert (d / "colonies" / "k1" / "events.jsonl").exists()
    assert (d / "colonies" / "k1" / "stats.json").exists()


def test_independent_control_has_no_colony_selection(_runs):
    d = run("swarm_colonies_independent", "arxiv-1407.6402", seed=0, llm_mode="mock",
            verbose=False)
    st = json.loads((d / "submission.json").read_text())["stats"]
    assert st["selection"] is False and st["colony_deaths"] == 0 and st["foundings"] == 0
    assert all(c["treasury"] is None for c in st["colonies"])
