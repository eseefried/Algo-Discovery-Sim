"""Scripted offline LLM. Lets the full loop (economy, deaths, respawns, judge) run without an
API key. It covers the two development tasks with correct, buggy, and alternative methods.
It is a test double, not a baseline: never report mock runs as results."""

from __future__ import annotations

import json
import random
from typing import Any

# ------------------------------------------------------------- affine Boolean identification

AFFINE_COHERENT = '''\
from qiskit import QuantumCircuit
from a2m_task import oracle


def build_circuits(spec):
    n = spec["n"]
    qc = QuantumCircuit(n + 1, n + 1)
    qc.x(n)
    qc.h(range(n + 1))
    qc.append(oracle(n + 1), range(n + 1))  # phase kickback (-1)^f(x)
    qc.h(range(n + 1))
    qc.append(oracle(n + 1), range(n + 1))  # second query, same register
    qc.measure(range(n + 1), range(n + 1))
    return [qc]


def postprocess(counts_list, spec):
    n = spec["n"]
    bits = max(counts_list[0], key=counts_list[0].get)[::-1]
    a = [int(bits[i]) for i in range(n)]
    parity = sum(a) % 2
    return {"a": a, "b": int(bits[n]) ^ 1 ^ parity}
'''

AFFINE_COHERENT_BITORDER_BUG = AFFINE_COHERENT.replace(
    "max(counts_list[0], key=counts_list[0].get)[::-1]", "max(counts_list[0], key=counts_list[0].get)"
)

AFFINE_INDEPENDENT_F0 = '''\
from qiskit import QuantumCircuit
from a2m_task import oracle


def build_circuits(spec):
    n = spec["n"]
    bv = QuantumCircuit(n + 1, n)
    bv.x(n)
    bv.h(range(n + 1))
    bv.append(oracle(n + 1), range(n + 1))
    bv.h(range(n))
    bv.measure(range(n), range(n))
    f0 = QuantumCircuit(n + 1, 1)          # evaluate f(0^n) on a fresh register
    f0.append(oracle(n + 1), range(n + 1))
    f0.measure(n, 0)
    return [bv, f0]


def postprocess(counts_list, spec):
    n = spec["n"]
    bits = max(counts_list[0], key=counts_list[0].get)[::-1]
    b = int(max(counts_list[1], key=counts_list[1].get))
    return {"a": [int(bits[i]) for i in range(n)], "b": b}
'''

AFFINE_BV_ONLY = '''\
from qiskit import QuantumCircuit
from a2m_task import oracle


def build_circuits(spec):
    n = spec["n"]
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.append(oracle(n + 1), range(n + 1))
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return [qc]


def postprocess(counts_list, spec):
    n = spec["n"]
    bits = max(counts_list[0], key=counts_list[0].get)[::-1]
    return {"a": [int(bits[i]) for i in range(n)], "b": 0}
'''

AFFINE_CLASSICAL = '''\
from qiskit import QuantumCircuit
from a2m_task import oracle


def build_circuits(spec):
    n = spec["n"]
    circuits = []
    for k in range(-1, n):                 # f(0), then f(e_k) for each k
        qc = QuantumCircuit(n + 1, 1)
        if k >= 0:
            qc.x(k)
        qc.append(oracle(n + 1), range(n + 1))
        qc.measure(n, 0)
        circuits.append(qc)
    return circuits


def postprocess(counts_list, spec):
    vals = [int(max(c, key=c.get)) for c in counts_list]
    b = vals[0]
    return {"a": [v ^ b for v in vals[1:]], "b": b}
'''

# ------------------------------------------------------------------------- modular adder

ADDER_QFT = '''\
from math import pi
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate


def build_circuit(spec):
    m = spec["m"]
    a, b = list(range(m)), list(range(m, 2 * m))
    qc = QuantumCircuit(2 * m)
    qc.append(QFTGate(m), b)                # Fourier (phase) encoding of b
    for i in range(m):
        for j in range(m):
            if i + j < m:                   # controlled phase rotation R_l from a_i
                qc.cp(2 * pi * 2 ** (i + j) / 2 ** m, a[i], b[j])
    qc.append(QFTGate(m).inverse(), b)      # inverse QFT
    return qc
'''

ADDER_QFT_SIGN_BUG = ADDER_QFT.replace("qc.cp(2 * pi", "qc.cp(-2 * pi")

ADDER_INCREMENT = '''\
from qiskit import QuantumCircuit


def build_circuit(spec):
    m = spec["m"]
    a, b = list(range(m)), list(range(m, 2 * m))
    qc = QuantumCircuit(2 * m)
    for i in range(m):                      # add 2^i controlled on a_i
        for j in reversed(range(i, m)):     # increment b[i:], top bit first
            qc.mcx([a[i]] + b[i:j], b[j])
    return qc
'''

ADDER_CARRY_QUBIT = '''\
from qiskit import QuantumCircuit


def build_circuit(spec):
    m = spec["m"]
    a, b = list(range(m)), list(range(m, 2 * m))
    carry = 2 * m
    qc = QuantumCircuit(2 * m + 1)
    reg = b + [carry]
    for i in range(m):
        for j in reversed(range(i, m + 1)):
            qc.mcx([a[i]] + reg[i:j], reg[j])
    return qc
'''

FAMILIES: dict[str, dict[str, dict[str, Any]]] = {
    "affine_boolean_id": {
        "coherent_two_query": {
            "sketch": ("Prepare n input qubits in |0> and an extra qubit in |1>; Hadamard all n+1. "
                       "The first query gives phase kickback (-1)^f(x); a second Hadamard layer "
                       "puts a in the inputs and returns the extra qubit to |1>. After one query b "
                       "is only a global phase, so apply the second query on the same register "
                       "(U_f H U_f H): the extra qubit becomes 1 xor b xor parity(a)."),
            "code": [AFFINE_COHERENT_BITORDER_BUG, AFFINE_COHERENT],
        },
        "bv_plus_f0_query": {
            "sketch": ("Bernstein-Vazirani: Hadamards and phase kickback reveal a in one query. "
                       "Because b is a global phase there, make an independent query of f(0^n) "
                       "on a fresh register and read b from the target qubit."),
            "code": [AFFINE_INDEPENDENT_F0],
        },
        "bernstein_vazirani_only": {
            "sketch": "Bernstein-Vazirani with one query reads a; assume b = 0.",
            "code": [AFFINE_BV_ONLY],
        },
        "classical_truth_table": {
            "sketch": "Query f(0) and f(e_k) for every unit vector e_k classically.",
            "code": [AFFINE_CLASSICAL],
        },
    },
    "modular_adder": {
        "qft_phase_adder": {
            "sketch": ("Apply a QFT to b for a phase encoding, add a with controlled phase "
                       "rotations R_l controlled by the bits of a, then inverse QFT. In place, no "
                       "ancilla; overflow wraps mod 2^m."),
            "code": [ADDER_QFT_SIGN_BUG, ADDER_QFT],
        },
        "controlled_increment_cascade": {
            "sketch": ("For each bit a_i, increment the upper part of b with a cascade of "
                       "multi-controlled X gates controlled on a_i."),
            "code": [ADDER_INCREMENT],
        },
        "ripple_carry_with_carry_qubit": {
            "sketch": "Ripple-carry addition into b with one extra carry qubit for the overflow.",
            "code": [ADDER_CARRY_QUBIT],
        },
    },
}


class MockBackend:
    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)

    def respond(self, tag: str, meta: dict[str, Any]) -> dict[str, Any]:
        handler = getattr(self, "_" + tag, None)
        if handler is None:
            raise ValueError(f"mock backend has no response for {tag!r}")
        return handler(meta)

    def _hypothesize(self, meta):
        pool = FAMILIES[meta["evaluator"]]
        existing = set(meta.get("existing_families", []))
        prefer, avoid = set(meta.get("prefer", [])), set(meta.get("avoid", []))
        names = [f for f in pool if f not in existing] or list(pool)
        weights = [3.0 if f in prefer else 0.3 if f in avoid else 1.0 for f in names]
        fam = self.rng.choices(names, weights=weights, k=1)[0]
        return {"family": fam, "sketch": pool[fam]["sketch"], "assumptions": []}

    def _implement(self, meta):
        pool = FAMILIES[meta["evaluator"]]
        fam = meta["family"] if meta["family"] in pool else self.rng.choice(list(pool))
        versions = pool[fam]["code"]
        attempt = int(meta.get("attempt", 0))
        if attempt == 0 and len(versions) > 1 and self.rng.random() < 0.5:
            code = versions[-1]  # sometimes right the first time
        else:
            code = versions[min(attempt, len(versions) - 1)]
        return {"code": code, "notes": f"mock implementation of {fam}, attempt {attempt}"}

    def _critique(self, meta):
        if self.rng.random() < 0.3 and meta.get("stress_params"):
            return {"verdict": "break", "reason": "may not generalise to a larger instance",
                    "stress_test": json.dumps(meta["stress_params"])}
        return {"verdict": "pass", "reason": "circuits and post-processing match the claim",
                "stress_test": ""}

    def _judge_rubric(self, meta):
        text = (meta["sketch"] + "\n" + meta["code"]).lower()
        hit = any(k.lower() in text for k in meta.get("keywords", []))
        return {"score": 1.0 if hit else 0.0, "rationale": "mock keyword judge"}

    def _plan(self, meta):
        return {"assignments": []}  # forces the planner's deterministic fallback

    def _recall(self, meta):
        return {"identified": False, "guess": "", "method_description": ""}

    def _draft_card(self, meta):
        raise ValueError("drafting claim cards needs a real model; run without --llm mock")
