"""Trusted evaluators. They own instance generation, simulation, and scoring; candidate code
only builds circuits and post-processes raw counts. Reported numbers never come from candidates."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from a2m.sandbox import Sandbox
from a2m.sandbox import circuits as circ
from a2m.sandbox.static import scan


class Evaluator(ABC):
    name: str
    interface: str

    def evaluate(self, code: str, params: dict[str, Any], sandbox: Sandbox,
                 allowed_imports: list[str], qubit_cap: int) -> dict[str, Any]:
        problems = scan(code, allowed_imports)
        if problems:
            return {"ok": False, "error": "static check failed: " + "; ".join(problems)}
        built = sandbox.run("build", code, {"spec": self.public_spec(params)})
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
