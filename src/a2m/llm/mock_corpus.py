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


# --------------------------------------------------------------- materials: cluster search

CLUSTER_BASIN_HOPPING = '''
import time
import numpy as np
from scipy.optimize import minimize
import a2m_task


def _relax(x):
    def fun(flat):
        e, f = a2m_task.energy_forces(flat.reshape(-1, 3))
        return e, -f.ravel()
    r = minimize(fun, x.ravel(), jac=True, method="L-BFGS-B", options={"maxiter": 2000})
    return float(r.fun), r.x.reshape(-1, 3)


def search(spec):
    n, seed = spec["n"], spec["seed"]
    deadline = time.time() + spec["time_budget_s"] * 0.9
    rng = np.random.default_rng(seed)
    cur_e, cur_x = _relax(a2m_task.random_cluster(n, seed))
    best_e, best_x, step = cur_e, cur_x.copy(), 0.38
    while time.time() < deadline:
        e, x = _relax(cur_x + rng.uniform(-1, 1, cur_x.shape) * step)
        if e < cur_e or rng.random() < np.exp(-(e - cur_e) / 0.8):   # Metropolis on minima
            cur_e, cur_x = e, x
            if e < best_e:
                best_e, best_x = e, x.copy()
    return best_x.tolist()
'''

CLUSTER_RANDOM_RESTART = '''
import time
import numpy as np
from scipy.optimize import minimize
import a2m_task


def search(spec):
    n = spec["n"]
    deadline = time.time() + spec["time_budget_s"] * 0.9
    best_e, best_x, k = 1e9, None, 0
    while time.time() < deadline:
        x0 = a2m_task.random_cluster(n, spec["seed"] * 1000 + k); k += 1
        r = minimize(lambda v: (lambda ef: (ef[0], -ef[1].ravel()))(
            a2m_task.energy_forces(v.reshape(-1, 3))), x0.ravel(), jac=True, method="L-BFGS-B")
        if r.fun < best_e:
            best_e, best_x = float(r.fun), r.x.reshape(-1, 3)
    return best_x.tolist()
'''

# ------------------------------------------------------------------ chemistry: molecule opt

CHEM_GA = '''
import time
import numpy as np
import selfies as sf
import a2m_task

PHENYL = "[C][=C][C][=C][C][=C][Ring1][=Branch1]"


def _mutate(s, alphabet, rng):
    if rng.random() < 0.04:
        return s + PHENYL
    toks = list(sf.split_selfies(s)) or ["[C]"]
    i = int(rng.integers(len(toks) + 1))
    t = alphabet[int(rng.integers(len(alphabet)))]
    if rng.random() < 0.5:
        toks.insert(i, t)
    else:
        toks[min(i, len(toks) - 1)] = t
    return "".join(toks)


def run(spec):
    rng = np.random.default_rng(spec["seed"])
    deadline = time.time() + spec["time_budget_s"] * 0.85
    start, thr = spec["start"], spec["similarity_threshold"]
    alphabet = sorted(sf.get_semantic_robust_alphabet())
    pool = [sf.encoder(start)] * 60
    keep = {}
    while time.time() < deadline:
        smiles = [sf.decoder(s) for s in pool]
        fit = []
        for s in smiles:
            j = a2m_task.score(s)
            ok = np.isfinite(j) and a2m_task.similarity(s, start) >= thr
            if ok:
                keep[a2m_task.canonical(s)] = j
            fit.append(j if ok else -1e6)
        order = np.argsort(-np.array(fit))
        surv = [pool[i] for i in order[:30]]
        pool = list(surv) + [_mutate(surv[int(rng.integers(len(surv)))], alphabet, rng)
                             for _ in range(30)]
    return sorted(keep, key=lambda s: -keep[s])[: spec["n_return"]]
'''

CHEM_APPEND_CARBONS = '''
import a2m_task


def run(spec):
    out = []
    for k in range(1, spec["n_return"] + 1):
        out.append(spec["start"] + "C" * k)     # blind chain extension, ignores similarity
    return [s for s in out if a2m_task.is_valid(s)]
'''

# -------------------------------------------------------------------- biology: RNA design

RNA_THRESHOLD_GREEDY = '''
import numpy as np


def _onehot(seqs, alphabet, length):
    idx = {c: i for i, c in enumerate(alphabet)}
    x = np.zeros((len(seqs), length * len(alphabet)))
    for r, s in enumerate(seqs):
        for p, c in enumerate(s):
            x[r, p * len(alphabet) + idx[c]] = 1.0
    return np.hstack([x, np.ones((len(x), 1))])


def propose(measured, spec):
    a, L, B = spec["alphabet"], spec["length"], spec["batch_size"]
    rng = np.random.default_rng(spec["seed"] + spec["round_index"])
    if not measured:
        return ["".join(a[i] for i in rng.integers(len(a), size=L)) for _ in range(B)]
    seqs = [m[0] for m in measured]; ys = np.array([m[1] for m in measured])
    X = _onehot(seqs, a, L)
    w = np.linalg.solve(X.T @ X + np.eye(X.shape[1]), X.T @ ys)
    seen = set(seqs)
    best = ys.max()
    parents = [s for s, y in zip(seqs, ys) if y >= best * 0.95] or [seqs[int(ys.argmax())]]
    pool = {}
    for _ in range(400):
        if len(pool) >= 20 * B:
            break
        for p in parents:
            base = float(_onehot([p], a, L) @ w)
            child = p
            for _ in range(20):
                c = list(child)
                for i in range(L):
                    if rng.random() < 1.0 / L:
                        c[i] = a[int(rng.integers(len(a)))]
                nxt = "".join(c)
                sc = float(_onehot([nxt], a, L) @ w)
                if sc < base:
                    break
                child = nxt
                if child not in seen:
                    pool[child] = sc
    while len(pool) < B:
        c = "".join(a[i] for i in rng.integers(len(a), size=L))
        if c not in seen:
            pool[c] = 0.0
    return sorted(pool, key=lambda s: -pool[s])[:B]
'''

RNA_RANDOM = '''
import numpy as np


def propose(measured, spec):
    rng = np.random.default_rng(spec["seed"] + spec["round_index"])
    a, L, B = spec["alphabet"], spec["length"], spec["batch_size"]
    return ["".join(a[i] for i in rng.integers(len(a), size=L)) for _ in range(B)]
'''

# ----------------------------------------------------------------- dynamics: transition path

STRING_NORMAL_FORCE = '''
import numpy as np
import a2m_task


def _reparam(path):
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    t = np.linspace(0, s[-1], len(path))
    return np.stack([np.interp(t, s, path[:, k]) for k in range(2)], axis=1)


def find_path(start, end, spec):
    start, end = np.array(start, float), np.array(end, float)
    m = max(6, spec["n_images"])
    path = start + np.linspace(0, 1, m)[:, None] * (end - start)
    for _ in range(20000):
        g = a2m_task.gradient(path)
        t = np.gradient(path, axis=0)
        t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-12)
        perp = g - (g * t).sum(axis=1, keepdims=True) * t      # normal component only
        perp[0] = perp[-1] = 0.0
        step = 1e-4 * perp
        n = np.linalg.norm(step, axis=1)
        big = n > 0.05
        if big.any():
            step[big] *= (0.05 / n[big])[:, None]
        path = _reparam(path - step)
        if np.abs(step).max() < 1e-6:
            break
    path[0], path[-1] = start, end
    return path.tolist()
'''

STRING_PLAIN_DESCENT = '''
import numpy as np
import a2m_task


def find_path(start, end, spec):
    start, end = np.array(start, float), np.array(end, float)
    m = max(6, spec["n_images"])
    path = start + np.linspace(0, 1, m)[:, None] * (end - start)
    for _ in range(4000):                       # no tangent projection: images fall in
        g = a2m_task.gradient(path)
        g[0] = g[-1] = 0.0
        path = path - 1e-4 * np.clip(g, -500, 500)
    return path.tolist()
'''

FAMILIES.update({
    "cluster_global_opt": {
        "minimize_then_metropolis": {
            "sketch": ("Score a configuration by the energy of the local minimum reached from "
                       "it, then run a Metropolis walk on those minimized energies at a finite "
                       "temperature, continuing from the relaxed coordinates after an accepted "
                       "step."),
            "code": [CLUSTER_RANDOM_RESTART, CLUSTER_BASIN_HOPPING],
        },
        "random_restart_minimization": {
            "sketch": "Locally minimize from many random starting configurations and keep the best.",
            "code": [CLUSTER_RANDOM_RESTART],
        },
    },
    "molecule_opt": {
        "selfies_mutation_ga": {
            "sketch": ("Evolve a population in a string encoding where every mutation stays a "
                       "valid molecule, keeping the fittest that still satisfy the similarity "
                       "constraint."),
            "code": [CHEM_APPEND_CARBONS, CHEM_GA],
        },
        "blind_chain_extension": {
            "sketch": "Append carbons to the starting molecule to raise logP.",
            "code": [CHEM_APPEND_CARBONS],
        },
    },
    "sequence_design": {
        "threshold_greedy_rollouts": {
            "sketch": ("Keep every measured sequence close to the best as a parent, mutate each "
                       "while a surrogate fitted on the measurements says it is still "
                       "improving, and measure only the top of the resulting pool."),
            "code": [RNA_RANDOM, RNA_THRESHOLD_GREEDY],
        },
        "random_batches": {
            "sketch": "Propose uniformly random sequences each round.",
            "code": [RNA_RANDOM],
        },
    },
    "transition_path": {
        "normal_force_string": {
            "sketch": ("Discretize the path into images, move each by the force component "
                       "perpendicular to the path, and redistribute the images to equal "
                       "spacing after every step."),
            "code": [STRING_PLAIN_DESCENT, STRING_NORMAL_FORCE],
        },
        "plain_gradient_descent": {
            "sketch": "Move every interior image down the gradient until the path settles.",
            "code": [STRING_PLAIN_DESCENT],
        },
    },
})


# ------------------------------------------------------- quantum: fixed-point amplification

FIXED_POINT_CHEBYSHEV = '''
import numpy as np
from qiskit import QuantumCircuit
from a2m_task import oracle


def _phases(L, delta):
    l = (L - 1) // 2
    gamma = 1.0 / np.cosh(np.arccosh(1.0 / delta) / L)
    root = np.sqrt(1.0 - gamma * gamma)
    alpha = [2.0 * np.arctan2(1.0, np.tan(2 * np.pi * j / L) * root) for j in range(1, l + 1)]
    return alpha, [-alpha[l - 1 - k] for k in range(l)]      # palindromic phase matching


def _reflect(qc, q, alpha):
    qc.h(q); qc.x(q)
    qc.p(-alpha, q[0]) if len(q) == 1 else qc.mcp(-alpha, q[:-1], q[-1])
    qc.x(q); qc.h(q)


def build_circuits(spec):
    n = spec["n"]; q = list(range(n))
    alpha, beta = _phases(spec["L"], spec["delta"])
    qc = QuantumCircuit(n)
    qc.h(q)
    for j in range(len(alpha)):
        qc.append(oracle(n, beta[j]), q)
        _reflect(qc, q, alpha[j])
    return [qc]
'''

FIXED_POINT_PLAIN_GROVER = '''
import numpy as np
from qiskit import QuantumCircuit
from a2m_task import oracle


def build_circuits(spec):
    n = spec["n"]; q = list(range(n))
    qc = QuantumCircuit(n)
    qc.h(q)
    for _ in range(spec["max_queries"]):        # full inversions, tuned to one lambda only
        qc.append(oracle(n, np.pi), q)
        qc.h(q); qc.x(q)
        qc.mcp(np.pi, q[:-1], q[-1])
        qc.x(q); qc.h(q)
    return [qc]
'''

FAMILIES.update({
    "fixed_point_search": {
        "chebyshev_phase_sequence": {
            "sketch": ("Run a sequence of generalized Grover iterates whose two phases per "
                       "iterate are computed from the tolerated failure probability through a "
                       "Chebyshev relation and matched in reverse order, so the success "
                       "probability stays flat across the whole range of marked fractions."),
            "code": [FIXED_POINT_PLAIN_GROVER, FIXED_POINT_CHEBYSHEV],
        },
        "plain_grover_iterations": {
            "sketch": ("Apply the standard Grover iterate as many times as the query budget "
                       "allows, using full inversions about the mean."),
            "code": [FIXED_POINT_PLAIN_GROVER],
        },
    },
})
