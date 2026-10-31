"""The on-disk skill tree: `skills/<domain>/`.

Each domain is a directory holding three things:

```
skills/<domain>/
  SKILL.md        declaration: roles, role bias, colony priors, libraries, tool list,
                  conventions. Parsed into a DomainProfile (see a2m/domains/profiles.py).
  tools/*.py      the helper modules. A tool marked `sandbox: true` is shipped into the
                  sandbox as `a2m_task` AND imported by the trusted runner for scoring, so
                  the objective a candidate queries is the code it is judged by. A tool
                  marked `sandbox: false` is runner-only - that is how a hidden oracle stays
                  hidden, and `tool_source` refuses to hand it out.
  learnings/      research artifacts distilled from judged runs (see a2m/learnings.py),
                  one Markdown file per run plus an INDEX.md. This is the shareable output.
```

Editing a SKILL.md changes how agents in that field are briefed and how their colonies start,
with no Python change, so a domain can be contributed as a directory.
"""

from __future__ import annotations

import importlib.util
import os
import re
from pathlib import Path
from types import ModuleType

import yaml

_tool_cache: dict[tuple[str, str], ModuleType] = {}


class SkillError(RuntimeError):
    pass


def root() -> Path:
    """The skill tree. Override with A2M_SKILLS_DIR; otherwise `skills/` beside the package."""
    env = os.getenv("A2M_SKILLS_DIR")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for base in (Path.cwd(), *here.parents):
        candidate = base / "skills"
        if candidate.is_dir():
            return candidate
    raise SkillError("no skills/ directory found; run from the repository root or set "
                     "A2M_SKILLS_DIR")


def domain_dir(domain: str) -> Path:
    d = root() / domain
    if not d.is_dir():
        raise SkillError(f"no skill directory for domain {domain!r} under {root()}")
    return d


def available() -> list[str]:
    return sorted(p.name for p in root().iterdir()
                  if p.is_dir() and (p / "SKILL.md").is_file())


def read_skill(domain: str) -> tuple[dict, dict[str, str]]:
    """Parse SKILL.md into (frontmatter, {heading: section text})."""
    text = (domain_dir(domain) / "SKILL.md").read_text()
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise SkillError(f"{domain}/SKILL.md must start with a YAML frontmatter block")
    meta = yaml.safe_load(match.group(1)) or {}
    sections: dict[str, str] = {}
    current = None
    for line in match.group(2).splitlines():
        heading = re.match(r"^##\s+(.*)$", line)
        if heading:
            current = heading.group(1).strip().lower()
            sections[current] = ""
        elif current:
            sections[current] += line + "\n"
    return meta, {k: v.strip() for k, v in sections.items()}


def _tool_spec(domain: str, name: str) -> dict:
    meta, _ = read_skill(domain)
    for tool in meta.get("tools", []) or []:
        if tool.get("module") == name:
            return tool
    raise SkillError(f"{domain}/SKILL.md does not declare a tool named {name!r}")


def tool_path(domain: str, name: str) -> Path:
    path = domain_dir(domain) / "tools" / f"{name}.py"
    if not path.is_file():
        raise SkillError(f"missing tool file {path}")
    return path


def tool_module(domain: str, name: str) -> ModuleType:
    """Import a tool for use in the trusted runner."""
    key = (domain, name)
    if key not in _tool_cache:
        path = tool_path(domain, name)
        spec = importlib.util.spec_from_file_location(f"a2m_skill_{domain}_{name}", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _tool_cache[key] = module
    return _tool_cache[key]


def tool_source(domain: str, name: str) -> str:
    """Source to ship into the sandbox. Refuses tools that are declared runner-only."""
    if not _tool_spec(domain, name).get("sandbox", False):
        raise SkillError(f"{domain}/{name} is declared sandbox: false and must not be shipped "
                         f"into the sandbox (it would expose a hidden oracle)")
    return tool_path(domain, name).read_text()


def learnings_dir(domain: str) -> Path:
    d = domain_dir(domain) / "learnings"
    d.mkdir(parents=True, exist_ok=True)
    return d
