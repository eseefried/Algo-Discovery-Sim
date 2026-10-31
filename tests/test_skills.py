"""The skill tree: `skills/<domain>/`.

These tests pin the properties the benchmark's validity rests on - that a profile never hands
agents the method they are asked to rebuild, that a hidden oracle cannot be shipped into the
sandbox, and that evaluator-side learnings never reach a prompt.
"""

import pytest

from a2m import domains, skills
from a2m.evaluators import REGISTRY as EVALUATORS
from a2m.swarm.agent import ROLES

# Words that would give away the method a task in that field asks the swarm to rebuild.
# A profile may describe the field; it may not describe the answer.
BANNED = {
    "quantum": ["bernstein", "vazirani", "chebyshev", "fixed-point", "fixed point", "grover",
                "phase kickback", "draper", "amplitude amplification"],
    "materials": ["basin", "hopping", "metropolis", "simulated annealing", "genetic",
                  "monte carlo"],
    "chemistry": ["selfies", "genetic algorithm", "discriminator", "crossover", "mutation"],
    "biology": ["adalead", "rollout", "greedy", "surrogate", "threshold", "evolutionary"],
    "dynamics": ["string method", "nudged", "elastic band", "reparametr", "arc length",
                 "normal component", "tangent"],
}


@pytest.mark.parametrize("domain", sorted(skills.available()))
def test_profile_loads_and_is_complete(domain):
    profile = domains.get(domain)
    assert profile.domain == domain
    assert profile.summary and profile.conventions
    assert set(profile.roles) >= set(ROLES)
    assert set(profile.role_bias) == set(ROLES)
    assert all(v > 0 for v in profile.role_bias.values())
    assert set(profile.colony_genome) == {"min_families", "max_attempts", "critiques_required"}
    assert profile.eval_timeout_s > 0
    assert "numpy" in profile.libraries


@pytest.mark.parametrize("domain", sorted(skills.available()))
def test_profile_never_names_the_method(domain):
    """The prompt block describes the field, never the algorithm under reconstruction."""
    text = domains.get(domain).prompt_block().lower()
    leaked = [w for w in BANNED[domain] if w in text]
    assert not leaked, f"{domain}/SKILL.md leaks method hints: {leaked}"


@pytest.mark.parametrize("domain", sorted(skills.available()))
def test_declared_tools_exist_and_import(domain):
    profile = domains.get(domain)
    for tool in profile.tools:
        module = skills.tool_module(domain, tool["module"])
        assert module is not None
        assert skills.tool_path(domain, tool["module"]).is_file()


def test_sandbox_tools_can_be_shipped_and_hidden_ones_cannot():
    assert skills.tool_source("chemistry", "chem").startswith('"""')
    assert skills.tool_source("materials", "lj")
    assert skills.tool_source("dynamics", "potential2d")
    # the RNA oracle measures against a hidden target and must stay in the runner
    with pytest.raises(skills.SkillError, match="sandbox: false"):
        skills.tool_source("biology", "rna")


def test_evaluators_only_ship_tools_their_domain_declares():
    for evaluator in EVALUATORS.values():
        tool = getattr(evaluator, "tool", None)
        if tool is None:
            continue
        domain, module = tool
        assert domain == evaluator.domain
        assert module in domains.get(domain).sandbox_tools()
        assert evaluator.taskmod_src()


def test_every_domain_has_an_evaluator_and_a_learnings_dir():
    covered = {e.domain for e in EVALUATORS.values()}
    assert covered == set(skills.available())
    for domain in skills.available():
        assert skills.learnings_dir(domain).is_dir()


def test_learnings_never_enter_a_prompt():
    """Artifacts quote the sealed rubric, so they must not be reachable from a profile."""
    marker = "SENTINEL-LEARNING-CONTENT"
    path = skills.learnings_dir("quantum") / "zz-prompt-leak-probe.md"
    path.write_text(f"# {marker}\n")
    try:
        domains.load.cache_clear() if hasattr(domains.load, "cache_clear") else None
        assert marker not in domains.load("quantum").prompt_block()
    finally:
        path.unlink()


def test_quantum_profile_documents_the_oracle_contract():
    """Quantum is the primary domain; its black-box contract must be stated up front."""
    profile = domains.get("quantum")
    block = profile.prompt_block().lower()
    assert "a2m_task" in block and "oracle" in block
    assert any("phase" in s.signature or "phase" in s.description for s in profile.skills)
    for expected in ("little-endian", "ancilla", "one query", "cap"):
        assert expected in block, expected
