import random

from a2m.swarm.agent import Agent
from a2m.swarm.economy import Economy, EconomyConfig
from a2m.swarm.index import SharedIndex
from a2m.swarm.lineage import Lineage
from a2m.swarm.matching import choose, pressure


def _agents(*ids):
    return {i: Agent(id=i, model="m", energy=5.0, affinities={}) for i in ids}


def test_costs_and_death():
    eco = Economy(EconomyConfig(initial_energy=1.0))
    a = Agent(id="a", model="m", energy=1.0, affinities={})
    eco.charge(a, "implement", 0)
    assert a.energy == -1.0 and eco.is_dead(a)


def test_disabled_economy_moves_nothing():
    eco = Economy(EconomyConfig(enabled=False))
    a = Agent(id="a", model="m", energy=1.0, affinities={})
    eco.charge(a, "implement", 0)
    eco.distribute([("a", "implement")], 10, {"a": a}, 0, "x")
    assert a.energy == 1.0 and not eco.is_dead(a) and not eco.can_spawn(a)


def test_payout_rewards_progress_only():
    eco = Economy(EconomyConfig(payout_scale=4.0, frontier_bonus=2.0))
    assert eco.progress_payout(1.0, 1.0, 1.0) == 0
    assert eco.progress_payout(0.5, 0.6, 0.5) == 0
    assert eco.progress_payout(1.0, 0.0, 0.5) == 4.0 + 1.0


def test_credit_split_by_role_latest_implementer_gets_most():
    eco = Economy(EconomyConfig())
    ag = _agents("h", "i1", "i2", "s")
    chain = [("h", "hypothesize"), ("i1", "implement"), ("i2", "implement"), ("s", "simulate")]
    eco.distribute(chain, 10.0, ag, 0, "test")
    gains = {k: round(v.energy - 5.0, 4) for k, v in ag.items()}
    assert gains["h"] == 3.5 and gains["s"] == 2.0
    assert gains["i2"] == round(4.5 * 2 / 3, 4) and gains["i1"] == round(4.5 / 3, 4)


def test_dead_agents_get_no_credit():
    eco = Economy(EconomyConfig())
    ag = _agents("h")
    ag["h"].alive = False
    eco.distribute([("h", "hypothesize")], 10.0, ag, 0, "x")
    assert ag["h"].energy == 5.0


def test_lineage_feedback_prefers_progress_and_avoids_deaths_and_stalls():
    lin = Lineage()
    dead = Agent(id="d", model="m", energy=0, affinities={}, families_backed={"bad"},
                 last_failure="bad missed the claim")
    lin.record_death(dead, 3)
    lin.record_success("x", 4, "good", "implement", 2.0, 0.0)
    lin.record_success("y", 4, "partial", "implement", 2.0, 0.25)
    lin.record_failure("partial", "stuck at success_rate=0.5")
    prefer, avoid = lin.prefer_avoid()
    assert prefer == ["good"] and set(avoid) == {"bad", "partial"}
    text = lin.feedback()
    assert "good" in text and "d died" in text and "stuck" in text


def test_role_affinities_follow_earnings():
    lin = Lineage()
    lin.record_success("x", 1, "f", "critique", 9.0, 0.0)
    aff = lin.role_affinities()
    assert aff["critique"] == max(aff.values())


def test_pressure_grows_with_age_and_drops_with_claimants():
    idx = SharedIndex()
    n = idx.open("needs_implementation", "c1", tick=0, promise=0.5)
    assert pressure(n, 5) > pressure(n, 0)
    p0 = pressure(n, 0)
    n.claimed_by.add("a")
    assert pressure(n, 0) < p0


def test_choose_follows_affinity():
    idx = SharedIndex()
    idx.open("needs_implementation", "c1", 0)
    idx.open("needs_critique", "c2", 0)
    rng = random.Random(0)
    picks = [choose(idx.open_needs(), {"critique": 5.0, "implement": 0.1}, 0, rng).kind
             for _ in range(200)]
    assert picks.count("needs_critique") > 180


def test_excluded_agents_cannot_serve_a_need():
    idx = SharedIndex()
    idx.open("needs_critique", "c1", 0, exclude={"author"})
    assert idx.open_needs("author") == [] and len(idx.open_needs("other")) == 1
