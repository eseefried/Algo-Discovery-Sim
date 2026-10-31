"""Identify f(x) = a.x XOR b from a black-box oracle U_f|x>|y> = |x>|y XOR f(x)>."""

from __future__ import annotations

import itertools
import random
from typing import Any

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from a2m.evaluators.base import CircuitEvaluator
from a2m.sandbox import circuits as circ

INTERFACE = """\
Write one Python module that defines:

  build_circuits(spec: dict) -> list[QuantumCircuit]
  postprocess(counts_list: list[dict[str, int]], spec: dict) -> {"a": list[int], "b": int}

spec = {"n": <number of input bits>, "shots": <shots per circuit>}.

The black box is available ONLY as an opaque gate: `from a2m_task import oracle`, then
`qc.append(oracle(n + 1), [0, 1, ..., n - 1, t])`. It acts as U_f|x>|y> = |x>|y XOR f(x)>,
x on the n listed input qubits (qubit i carries x_i), y on the last listed qubit, where
f(x) = a_0 x_0 XOR ... XOR a_{n-1} x_{n-1} XOR b. You cannot inspect a or b. Every appended
oracle gate counts as one query. Circuits must end in measurements of the bits you need.

The runner simulates each returned circuit `spec["shots"]` times against a hidden (a, b) and
passes their Qiskit counts dicts, in the same order, to postprocess. Qiskit bitstrings are
little-endian: the last character is classical bit 0. Return a[i] for input bit i and the
offset b. Gates must come from Qiskit's standard library (or circuits built from them).
"""


def oracle_circuit(n: int, a: tuple[int, ...], b: int) -> QuantumCircuit:
    qc = QuantumCircuit(n + 1, name="U_f")
    for i, ai in enumerate(a):
        if ai:
            qc.cx(i, n)
    if b:
        qc.x(n)
    return qc


def instances(params: dict[str, Any]) -> list[tuple[tuple[int, ...], int]]:
    n = int(params["n"])
    every = [(a, b) for a in itertools.product((0, 1), repeat=n) for b in (0, 1)]
    k = params.get("instances", "all")
    if k == "all" or int(k) >= len(every):
        return every
    return random.Random(int(params.get("seed", 0))).sample(every, int(k))


def _parse(answer: Any, n: int) -> tuple[tuple[int, ...], int] | None:
    try:
        a = tuple(int(v) for v in answer["a"])
        b = int(answer["b"])
    except (KeyError, TypeError, ValueError):
        return None
    return (a, b) if len(a) == n else None


class AffineBooleanId(CircuitEvaluator):
    name = "affine_boolean_id"
    interface = INTERFACE

    def public_spec(self, params):
        return {"n": int(params["n"]), "shots": int(params.get("shots", 32))}

    def score(self, code, params, circuits, stats, sandbox):
        n, shots = int(params["n"]), int(params.get("shots", 32))
        if not any(op["name"] == "measure" for d in circuits for op in d["ops"]):
            return {"ok": False, "error": "no circuit measures anything"}
        sim = AerSimulator(seed_simulator=int(params.get("seed", 0)))
        cases = instances(params)
        batch = []
        for a, b in cases:
            qcs = transpile([circ.load(d, oracle_circuit(n, a, b)) for d in circuits], sim,
                            optimization_level=0)
            res = sim.run(qcs, shots=shots).result()
            batch.append([dict(res.get_counts(i)) for i in range(len(qcs))])
        post = sandbox.run("post", code, {"spec": self.public_spec(params), "batch": batch})
        if not post["ok"]:
            return {"ok": False, "error": "postprocess failed:\n" + post["error"]}
        answers = post["result"]
        hits = sum(_parse(ans, n) == truth for ans, truth in zip(answers, cases))
        return {"ok": True, "metrics": {
            "success_rate": hits / len(cases),
            "oracle_queries": stats["oracle_queries"],
            "num_qubits": stats["num_qubits"],
            "two_qubit_gates": stats["two_qubit_gates"],
            "depth": stats["depth"],
            "instances": len(cases),
        }}
