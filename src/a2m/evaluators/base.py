"""Trusted evaluators.

An evaluator owns everything a candidate must not control: which instances are tested, what
the black box is, how the simulation runs, and how the answer is scored. Candidate code only
proposes - circuits, coordinates, molecules, sequences, paths - and the runner measures.
Numbers a candidate prints or returns as a "score" are never used.

Two flows:

* :class:`CircuitEvaluator` - quantum. The candidate builds circuits containing an opaque
  oracle placeholder; the runner substitutes the real oracle and simulates.
* :class:`CallEvaluator` - everything else. The runner ships a task module into the sandbox
  as ``a2m_task`` and calls one entry function, then scores the returned answer with the same
  task module in the parent, so the objective cannot drift between the two sides.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from a2m.domains import get as get_domain
from a2m.sandbox import Sandbox
from a2m.sandbox import circuits as circ
from a2m.sandbox.static import scan
from a2m.schema import ClaimCard
from a2m.skills import tool_source


class Evaluator(ABC):
    name: str
    domain: str
    interface: str

    def timeout_for(self, card: ClaimCard) -> int:
        return int(card.limits.get("eval_timeout_s") or get_domain(self.domain).eval_timeout_s)

    def guard(self, code: str, card: ClaimCard) -> dict | None:
        """Cheap static rejection before any candidate code runs."""
        problems = scan(code, card.allowed_imports)
        if problems:
            return {"ok": False, "error": "static check failed: " + "; ".join(problems)}
        return None

    @abstractmethod
    def evaluate(self, code: str, params: dict[str, Any], sandbox: Sandbox,
                 card: ClaimCard) -> dict[str, Any]:
        """Run one test system and return {"ok", "metrics"|"error", ...}."""


# --------------------------------------------------------------------------- quantum


class CircuitEvaluator(Evaluator):
    domain = "quantum"

    def evaluate(self, code, params, sandbox, card):
        bad = self.guard(code, card)
        if bad:
            return bad
        qubit_cap = int(card.limits.get("qubit_cap", 0)) or 10**6
        built = sandbox.run("build", code, {"spec": self.public_spec(params)},
                            timeout_s=self.timeout_for(card))
        if not built["ok"]:
            return {"ok": False, "error": "build failed:\n" + built["error"]}
        try:
            st = circ.stats(built["result"])
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "error": f"circuit could not be reconstructed: {e}"}
        if st["num_qubits"] > qubit_cap:
            return {"ok": False, "error": f"uses {st['num_qubits']} qubits; cap is {qubit_cap}",
                    "stats": st}
        try:
            out = self.score(code, params, built["result"], st, sandbox)
        except Exception as e:  # noqa: BLE001
            return {"ok": False, "error": f"evaluation failed: {type(e).__name__}: {e}", "stats": st}
        out.setdefault("stats", st)
        return out

    @abstractmethod
    def public_spec(self, params: dict[str, Any]) -> dict[str, Any]:
        """The part of a test system the candidate may see (no hidden instance data)."""

    @abstractmethod
    def score(self, code: str, params: dict[str, Any], circuits: list[dict], stats: dict,
              sandbox: Sandbox) -> dict[str, Any]:
        ...


# ------------------------------------------------------------------------- everything else


class CallEvaluator(Evaluator):
    """Calls one entry function in the sandbox and scores what it returns."""

    entry: str
    # (domain, module) of the skill tool shipped into the sandbox as `a2m_task`. None means
    # nothing is shipped, which is how a hidden oracle stays in the runner.
    tool: tuple[str, str] | None = None

    def taskmod_src(self) -> str | None:
        return tool_source(*self.tool) if self.tool else None

    def call(self, sandbox: Sandbox, code: str, args: list[Any], card: ClaimCard,
             timeout_s: int | None = None) -> dict[str, Any]:
        return sandbox.run("call", code, {"entry": self.entry, "args": args,
                                          "taskmod_src": self.taskmod_src()},
                           timeout_s=timeout_s or self.timeout_for(card))

    def evaluate(self, code, params, sandbox, card):
        bad = self.guard(code, card)
        if bad:
            return bad
        try:
            return self.run_and_score(code, params, sandbox, card)
        except Exception as e:  # noqa: BLE001 - a broken candidate must not stop the run
            return {"ok": False, "error": f"evaluation failed: {type(e).__name__}: {e}"}

    @abstractmethod
    def run_and_score(self, code: str, params: dict[str, Any], sandbox: Sandbox,
                      card: ClaimCard) -> dict[str, Any]:
        ...


def failed(result: dict, what: str) -> dict:
    """Turn a sandbox failure into an evaluator error result."""
    return {"ok": False, "error": f"{what} failed:\n{result.get('error', '')}"}
