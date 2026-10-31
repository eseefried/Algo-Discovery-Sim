"""Domain profiles, loaded from the on-disk skill tree (`skills/<domain>/SKILL.md`).

A profile is the three things the swarm reads about a field:

* **agent profile** - what each role means here, and the starting role affinities newly born
  agents inherit. A field where implementations are fiddly starts with more implementers; one
  where a wrong answer is expensive starts with more critics.
* **colony profile** - the starting genome for colonies in this field (how many method
  families to carry, how many repair attempts a lineage gets, how many critiques a candidate
  must survive), plus the sandbox time one evaluation is allowed.
* **skill profile** - the helpers the runner injects into the sandbox as `a2m_task`, and the
  libraries candidate code may import.

Profiles carry **no method hints**. They describe the field's conventions, units and pitfalls,
the things any practitioner knows before reading a paper, and never the algorithm a task asks
the swarm to rebuild. `tests/test_domains.py` enforces that against a per-domain list of
banned method words - without it, a cross-domain score would not be comparable with the
quantum one.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from a2m import skills
from a2m.swarm.agent import ROLES


@dataclass(frozen=True)
class Skill:
    """One helper the runner injects into the sandbox, as described to agents."""

    signature: str
    description: str


@dataclass(frozen=True)
class DomainProfile:
    domain: str
    summary: str                       # what reconstruction work looks like here
    conventions: str                   # units, idioms, pitfalls; never a method
    roles: dict[str, str]              # role -> what it means in this field
    role_bias: dict[str, float]        # starting affinities for newly born agents
    colony_genome: dict[str, int]      # min_families, max_attempts, critiques_required
    libraries: tuple[str, ...]         # top-level imports candidate code may use
    skills: tuple[Skill, ...] = ()     # a2m_task helpers, if the field injects any
    tools: tuple[dict, ...] = field(default_factory=tuple)   # declared tool modules
    eval_timeout_s: int = 90           # sandbox wall-clock for one evaluation
    backends: tuple[str, ...] = ()     # optional accelerated backends, when installed

    def __post_init__(self):
        missing = set(ROLES) - set(self.roles)
        if missing:
            raise ValueError(f"{self.domain}: SKILL.md roles missing {sorted(missing)}")
        if set(self.role_bias) != set(ROLES):
            raise ValueError(f"{self.domain}: role_bias must cover exactly {sorted(ROLES)}")

    def role_text(self, role: str) -> str:
        return self.roles.get(role, "")

    def sandbox_tools(self) -> list[str]:
        return [t["module"] for t in self.tools if t.get("sandbox")]

    def skills_text(self) -> str:
        if not self.skills:
            return ""
        lines = [f"  {s.signature}\n      {s.description}" for s in self.skills]
        return ("The trusted runner provides these helpers inside the sandbox as `a2m_task`:\n"
                + "\n".join(lines))

    def prompt_block(self) -> str:
        parts = [f"Field: {self.domain}. {self.summary}",
                 f"Conventions in this field:\n{self.conventions}"]
        skills_text = self.skills_text()
        if skills_text:
            parts.append(skills_text)
        if self.backends:
            parts.append("Accelerated backends available when installed: "
                         + "; ".join(self.backends))
        return "\n\n".join(parts)


def _one_line(text: str) -> str:
    return " ".join(str(text).split())


def load(domain: str) -> DomainProfile:
    meta, sections = skills.read_skill(domain)
    tools = tuple(meta.get("tools") or ())
    # Skills come from the tool modules a domain ships, plus any the runner provides without
    # a module behind them (the quantum oracle placeholder is built by the harness itself).
    entries = list(meta.get("skills") or []) + [s for t in tools for s in (t.get("skills") or [])]
    declared = tuple(Skill(signature=s["signature"], description=_one_line(s["description"]))
                     for s in entries)
    return DomainProfile(
        domain=meta.get("domain", domain),
        summary=_one_line(sections.get("summary", "")),
        conventions=sections.get("conventions", ""),
        roles={k: _one_line(v) for k, v in (meta.get("roles") or {}).items()},
        role_bias={k: float(v) for k, v in (meta.get("role_bias") or {}).items()},
        colony_genome={k: int(v) for k, v in (meta.get("colony_genome") or {}).items()},
        libraries=tuple(meta.get("libraries") or ()),
        skills=declared,
        tools=tools,
        eval_timeout_s=int(meta.get("eval_timeout_s", 90)),
        backends=tuple(_one_line(b) for b in (meta.get("backends") or ())),
    )


REGISTRY: dict[str, DomainProfile] = {d: load(d) for d in skills.available()}


def get(domain: str) -> DomainProfile:
    try:
        return REGISTRY[domain]
    except KeyError:
        raise KeyError(f"no skill profile for domain {domain!r}; "
                       f"known: {sorted(REGISTRY)}") from None


def names() -> list[str]:
    return sorted(REGISTRY)


def default_libraries(domain: str) -> list[str]:
    return list(get(domain).libraries)
