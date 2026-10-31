"""Prompts and output schemas. Every system (swarm, planner, single agent) uses the same ones."""

from __future__ import annotations

import json

from a2m import domains
from a2m.schema import ClaimCard

SYSTEM = """\
You are a researcher reconstructing a scientific method from a paper's abstract alone. You have
not read the paper and cannot look anything up. Work from the abstract, the claim card, and your
own knowledge. Your code runs inside a sandbox owned by a trusted runner; the runner measures
every reported number itself, on test instances you do not control, so only a method that
actually works will score.

{domain}

<claim_card>
{card}
</claim_card>"""


def render_system(card: ClaimCard) -> str:
    visible = {
        "abstract": card.abstract,
        "claim": card.claim,
        "success_criteria": [c.model_dump() for c in card.criteria],
        "visible_test_systems": [t.model_dump() for t in card.test_systems],
        "limits": card.limits,
        "allowed_imports": card.allowed_imports,
        "scope_notes": card.notes,
        "interface": card.interface,
    }
    return SYSTEM.format(domain=domains.get(card.domain).prompt_block(),
                         card=json.dumps(visible, indent=2))


def role_line(card: ClaimCard, role: str) -> str:
    """One line putting the agent's current role in this field's terms."""
    text = domains.get(card.domain).role_text(role)
    return f"Your task in this round, as a {card.domain} researcher: {text}.\n\n" if text else ""


def _notes_block(notes: str) -> str:
    return f"\nLessons from earlier team members:\n{notes}\n" if notes else ""


HYPOTHESIZE = """\
Propose one candidate method that could achieve the claim through the interface.
{diversity}{notes}
Give a short snake_case label for the method family, a sketch of the key steps and why they
achieve the claim, and any assumptions you made that the abstract does not state."""

HYPOTHESIZE_SCHEMA = {
    "type": "object",
    "properties": {
        "family": {"type": "string"},
        "sketch": {"type": "string"},
        "assumptions": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["family", "sketch", "assumptions"],
    "additionalProperties": False,
}


def hypothesize(existing: list[str], diversity: bool, notes: str) -> str:
    div = ""
    if diversity and existing:
        div = ("Method families already being pursued: " + ", ".join(sorted(set(existing)))
               + ". Propose a materially different family.\n")
    return HYPOTHESIZE.format(diversity=div, notes=_notes_block(notes))


IMPLEMENT = """\
Implement this method as one Python module that follows the interface exactly.

Method family: {family}
Sketch:
{sketch}
{previous}{notes}
Return the complete module source in `code`."""

IMPLEMENT_SCHEMA = {
    "type": "object",
    "properties": {"code": {"type": "string"}, "notes": {"type": "string"}},
    "required": ["code", "notes"],
    "additionalProperties": False,
}


def implement(family: str, sketch: str, previous_code: str, diagnostics: str, notes: str) -> str:
    prev = ""
    if previous_code:
        prev = (f"\nA previous implementation did not meet the claim.\n<previous_code>\n"
                f"{previous_code}\n</previous_code>\n<runner_diagnostics>\n{diagnostics}\n"
                f"</runner_diagnostics>\nFix the cause rather than special-casing the tests.\n")
    return IMPLEMENT.format(family=family, sketch=sketch, previous=prev, notes=_notes_block(notes))


CRITIQUE = """\
Review this candidate adversarially. It meets the claim on the visible test systems.

Method family: {family}
Sketch:
{sketch}
<code>
{code}
</code>
<runner_results>
{results}
</runner_results>

Would it fail on unseen instances of the task, for example larger sizes or other hidden
functions, or does it rely on something that only holds for the listed tests? If you think it
breaks, give a stress test: a JSON object with the same keys as the visible test parameters
({keys}). The runner executes it; a break only counts if the candidate fails it. If you find
no concrete failure, return "pass" with an empty stress_test."""

CRITIQUE_SCHEMA = {
    "type": "object",
    "properties": {
        "verdict": {"type": "string", "enum": ["pass", "break"]},
        "reason": {"type": "string"},
        "stress_test": {"type": "string"},
    },
    "required": ["verdict", "reason", "stress_test"],
    "additionalProperties": False,
}

PLAN = """\
You coordinate {k} workers reconstructing this method. Assign each worker exactly one action
for this round:
  hypothesize - propose a new method family (target "")
  implement   - write or repair code for a candidate (target = candidate id)
  critique    - adversarially test a candidate that meets the claim (target = candidate id)
The runner simulates every new implementation automatically.

Workers: {workers}
Candidates so far:
{candidates}"""

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "assignments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "worker": {"type": "string"},
                    "action": {"type": "string", "enum": ["hypothesize", "implement", "critique"]},
                    "target": {"type": "string"},
                },
                "required": ["worker", "action", "target"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["assignments"],
    "additionalProperties": False,
}

JUDGE_SYSTEM = """\
You grade whether a submitted method contains one specific component of a reference method from
a paper. Judge the method the code actually implements; the description may overstate it."""

JUDGE_RUBRIC = """\
Component: {item}

<submitted_description>
{sketch}
</submitted_description>
<submitted_code>
{code}
</submitted_code>

Score 1 if the submission clearly contains this component, 0.5 if partially or ambiguously,
0 if it is absent or contradicted."""

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "score": {"type": "string", "enum": ["0", "0.5", "1"]},
        "rationale": {"type": "string"},
    },
    "required": ["score", "rationale"],
    "additionalProperties": False,
}

RECALL = """\
Here is a paper abstract. Do you recognise the paper? If so, give its title and authors and
describe its method concretely. If you do not recognise it, say so; do not guess a method.

<abstract>
{abstract}
</abstract>"""

RECALL_SCHEMA = {
    "type": "object",
    "properties": {
        "identified": {"type": "boolean"},
        "guess": {"type": "string"},
        "method_description": {"type": "string"},
    },
    "required": ["identified", "guess", "method_description"],
    "additionalProperties": False,
}

DRAFT_CARD = """\
Draft benchmark material for this paper. A curator will review everything before use.

From the abstract only, write the visible claim: one measurable sentence a simulation of a small
instance (at most {cap} qubits including ancillas) can check, plus numeric success criteria and
2-3 small visible test systems. From the full paper, write the sealed rubric: 4-8 key method
components checkable from code, written so that a generic textbook substitute would miss the
paper-specific ones. Also give 1-2 larger hidden test systems, the numbers the paper reports,
and the evaluator kind needed: one of {evaluators}, or "new" with a description of the
black-box interface it would need.

<abstract>
{abstract}
</abstract>
<paper>
{paper}
</paper>"""

DRAFT_CARD_SCHEMA = {
    "type": "object",
    "properties": {
        "claim": {"type": "string"},
        "criteria": {"type": "array", "items": {
            "type": "object",
            "properties": {"metric": {"type": "string"},
                           "comparator": {"type": "string", "enum": [">=", "<=", "=="]},
                           "target": {"type": "number"}, "tolerance": {"type": "number"}},
            "required": ["metric", "comparator", "target", "tolerance"],
            "additionalProperties": False}},
        "test_systems": {"type": "string", "description": "JSON list of {name, params}"},
        "hidden_test_systems": {"type": "string", "description": "JSON list of {name, params}"},
        "rubric": {"type": "array", "items": {
            "type": "object",
            "properties": {"id": {"type": "string"}, "text": {"type": "string"},
                           "weight": {"type": "number"}},
            "required": ["id", "text", "weight"], "additionalProperties": False}},
        "reported_numbers": {"type": "string", "description": "JSON object"},
        "evaluator": {"type": "string"},
        "evaluator_notes": {"type": "string"},
    },
    "required": ["claim", "criteria", "test_systems", "hidden_test_systems", "rubric",
                 "reported_numbers", "evaluator", "evaluator_notes"],
    "additionalProperties": False,
}
