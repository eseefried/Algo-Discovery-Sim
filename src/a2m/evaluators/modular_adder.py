"""In-place modular adder |a>|b> -> |a>|(a + b) mod 2^m>, checked on every basis input."""

from __future__ import annotations

from qiskit.quantum_info import Operator

from a2m.evaluators.base import Evaluator
from a2m.sandbox import circuits as circ

INTERFACE = """\
Write one Python module that defines:

  build_circuit(spec: dict) -> QuantumCircuit

spec = {"m": <bits per register>}. Qubits 0..m-1 hold a (qubit i = bit i, little-endian),
qubits m..2m-1 hold b. Any further qubits are ancillas that start in |0> and must end in |0>.
The circuit must map |a>|b> to |a>|(a + b) mod 2^m> for every basis input, with no
measurements. Gates must come from Qiskit's standard library (or circuits built from them).
The runner computes the circuit's unitary and checks all 4^m inputs.
"""


class ModularAdder(Evaluator):
    name = "modular_adder"
    interface = INTERFACE

    def public_spec(self, params):
        return {"m": int(params["m"])}

    def score(self, code, params, circuits, stats, sandbox):
        m = int(params["m"])
        if len(circuits) != 1:
            return {"ok": False, "error": "return exactly one circuit"}
        d = circuits[0]
        if any(op["name"] in ("measure", "reset", "oracle") for op in d["ops"]):
            return {"ok": False, "error": "the adder must be unitary: no measure/reset/oracle"}
        nq = int(d["num_qubits"])
        if nq < 2 * m:
            return {"ok": False, "error": f"needs at least {2 * m} qubits, got {nq}"}
        u = Operator(circ.load(d)).data  # column x = U|x>, Qiskit little-endian indexing
        mod = 2**m
        probs = []
        for a in range(mod):
            for b in range(mod):
                x = a + (b << m)
                y = a + (((a + b) % mod) << m)
                probs.append(float(abs(u[y, x]) ** 2))
        return {"ok": True, "metrics": {
            "correct_fraction": sum(p > 0.99 for p in probs) / len(probs),
            "mean_fidelity": sum(probs) / len(probs),
            "ancilla_qubits": nq - 2 * m,
            "num_qubits": nq,
            "two_qubit_gates": stats["two_qubit_gates"],
            "depth": stats["depth"],
        }}
