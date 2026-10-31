"""Quantum: amplitude amplification that must not overshoot.

The hard part of this task is that the runner sweeps the marked fraction lambda over a whole
range and scores the *worst* case. A method tuned for one lambda - plain Grover with a fixed
iteration count - peaks there and collapses elsewhere, so it fails however many queries it is
given. Only a construction with the fixed-point property clears the bar across the range, and
only one that keeps the quadratic speedup clears it inside the query budget.

The black box is a phase oracle with an adjustable phase: the candidate places
`a2m_task.oracle(n, beta)` and the runner substitutes a diagonal that puts e^{i beta} on the
hidden marked states. The marked set is never visible, and one placement is one query.
"""

from __future__ import annotations

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library import DiagonalGate
from qiskit.quantum_info import Statevector

from a2m.evaluators.base import CircuitEvaluator
from a2m.sandbox import circuits as circ

INTERFACE = """\
Write one Python module that defines:

  build_circuits(spec: dict) -> list[QuantumCircuit]

spec = {"n": <qubits>, "L": <odd integer>, "delta": <float>, "lambda_min": <float>,
        "max_queries": <int>}.

Return exactly one circuit on `n` qubits with no measurements. It starts in |0...0>; the
runner reads the final statevector and sums the probability of the hidden marked states.

The black box is available only as an opaque gate with an adjustable phase:

    from a2m_task import oracle
    qc.append(oracle(n, beta), range(n))

It applies e^{i*beta} to every marked basis state and leaves the rest alone. You cannot
inspect which states are marked. Each appended oracle gate counts as one query, and you may
use at most `max_queries`.

An unknown fraction lambda of the basis states is marked. You are guaranteed only
lambda >= lambda_min. The runner evaluates your circuit at many values of lambda in that
range and scores the worst one, so a circuit that works at a single lambda will not pass.
Build the rest from Qiskit's standard gate library.
"""


def _marked(n: int, count: int, seed: int) -> list[int]:
    rng = np.random.default_rng(seed)
    return sorted(int(x) for x in rng.choice(2**n, size=count, replace=False))


def _phase_oracle(n: int, marked: list[int]):
    """Factory the runner hands to circuits.load: placeholder params -> real gate."""
    def build(*params) -> QuantumCircuit:
        beta = float(params[0]) if params else np.pi
        diag = np.ones(2**n, dtype=complex)
        for m in marked:
            diag[m] = np.exp(1j * beta)
        qc = QuantumCircuit(n)
        qc.append(DiagonalGate(list(diag)), range(n))
        return qc
    return build


def gamma(big_l: int, delta: float) -> float:
    """gamma with 1/gamma = T_{1/L}(1/delta); the fixed point holds for lambda >= 1 - gamma^2."""
    return 1.0 / np.cosh(np.arccosh(1.0 / delta) / big_l)


def lambda_floor(big_l: int, delta: float) -> float:
    g = gamma(big_l, delta)
    return 1.0 - g * g


class FixedPointSearch(CircuitEvaluator):
    name = "fixed_point_search"
    interface = INTERFACE

    def public_spec(self, params):
        big_l, delta = int(params["L"]), float(params["delta"])
        return {"n": int(params["n"]), "L": big_l, "delta": delta,
                "lambda_min": round(lambda_floor(big_l, delta), 6),
                "max_queries": (big_l - 1) // 2}

    def score(self, code, params, circuits, stats, sandbox):
        n, big_l, delta = int(params["n"]), int(params["L"]), float(params["delta"])
        if len(circuits) != 1:
            return {"ok": False, "error": "return exactly one circuit"}
        spec = circuits[0]
        if any(op["name"] in ("measure", "reset") for op in spec["ops"]):
            return {"ok": False, "error": "the circuit must be unitary: no measure or reset"}
        if int(spec["num_qubits"]) != n:
            return {"ok": False, "error": f"expected {n} qubits, got {spec['num_qubits']}"}

        floor = lambda_floor(big_l, delta)
        counts = [m for m in params["marked_counts"] if m / 2**n >= floor - 1e-9]
        if not counts:
            return {"ok": False, "error": "no test point is inside the guaranteed range"}

        probs = {}
        for count in counts:
            marked = _marked(n, count, int(params.get("seed", 0)) * 1000 + count)
            qc = circ.load(spec, _phase_oracle(n, marked))
            amps = Statevector(qc).data
            probs[count / 2**n] = float(sum(abs(amps[m]) ** 2 for m in marked))

        budget = (big_l - 1) // 2
        return {"ok": True, "metrics": {
            "min_success_probability": round(min(probs.values()), 6),
            "mean_success_probability": round(float(np.mean(list(probs.values()))), 6),
            # the budget scales with L, so the scored quantity is the overrun, not the count
            "queries_over_budget": stats["oracle_queries"] - budget,
            "oracle_queries": stats["oracle_queries"],
            "query_budget": budget,
            "num_qubits": stats["num_qubits"],
            "lambda_points": len(probs),
            "two_qubit_gates": stats["two_qubit_gates"],
        }, "stats": {**stats,
                     "guaranteed_floor": round(floor, 6),
                     "by_lambda": {round(k, 4): round(v, 6) for k, v in sorted(probs.items())}}}
