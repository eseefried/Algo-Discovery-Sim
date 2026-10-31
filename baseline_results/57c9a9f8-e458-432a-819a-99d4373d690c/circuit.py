"""Diagonal bipartite random-phase gate U on C^N (x) C^N (N = 2^n) as a Qiskit operation.

Implements eq_1 (diagonal unitary with phases phi_{jk}) via the exact decomposition of
eq_6, generalised from N = 2 to N = 2^n with a Mobius transform of the phase vector:
    phi_x = sum_{S subset of bits} c_S prod_{q in S} x_q ,
so that U = e^{i c_0} * prod_{|S|=1} P(c_S) * prod_{|S|=2} CP(c_S) * prod_{|S|>=3} MCP(c_S).
For n = 1 this is exactly eq_6:
    U = e^{i phi_00} (P(phi_10-phi_00)_A (x) P(phi_01-phi_00)_B) CP(phi_11-phi_10-phi_01+phi_00).

Qubit layout (index 0 = least significant basis bit):
    qubits 0 .. n-1      : register B  (least significant, index k)
    qubits n .. 2n-1     : register A  (most significant, index j)
    optional 2n .. 3n-1  : register B' (idle reference half, Choi construction eq_5)
    optional 3n .. 4n-1  : register A' (idle reference half, Choi construction eq_5)
The diagonal entry of U on basis state |j>_A |k>_B is e^{i phases[j*N + k]}, i.e. the
flat phase list is indexed by the Qiskit basis-state integer x = j*N + k, and reshaping
it row-major into an N x N matrix gives A_{jk} = e^{i phi_{jk}} (eq_2).

The circuit does NOT prepare Bell pairs or measure: the runner prepares
|Phi>_{AA'} |Phi>_{BB'} and performs tomography of the reduced state on A A' (eq_5);
its spectrum equals the eigenvalues of rho = A A^dagger / N^2 and its entropy equals
the Schmidt strength K_Sch(U) (eq_3, eq_4).
"""
from __future__ import annotations

import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

MAX_QUBITS = 12
TWO_PI = 2.0 * math.pi
PHASE_TOL = 1e-12


def _local_qubits(instance):
    """Return (N, n) with N = 2^n the local dimension, validated."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if "N" not in instance:
        raise ValueError("instance must provide the local dimension 'N'")
    N = instance["N"]
    if isinstance(N, bool) or not isinstance(N, int):
        raise ValueError("'N' must be an integer")
    if N < 2 or (N & (N - 1)) != 0:
        raise ValueError("'N' must be a power of two >= 2")
    n = N.bit_length() - 1
    return N, n


def _extract_phases(instance, N):
    """Flat real phase vector of length N^2 indexed by x = j*N + k (eq_1 / eq_2)."""
    if "phases" in instance:
        raw = instance["phases"]
        arr = np.asarray(raw, dtype=float)
        if arr.ndim == 2:
            if arr.shape != (N, N):
                raise ValueError("nested 'phases' must be an N x N array")
            arr = arr.reshape(N * N)
        elif arr.ndim != 1 or arr.shape[0] != N * N:
            raise ValueError("'phases' must have length N^2 or shape N x N")
        if not np.all(np.isfinite(arr)):
            raise ValueError("'phases' must be finite real numbers")
        return arr
    if "seed" in instance:
        seed = instance["seed"]
        if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
            raise ValueError("'seed' must be a non-negative integer")
        rng = np.random.default_rng(seed)
        # eq_1: i.i.d. uniform phases on [0, 2 pi)
        return rng.uniform(0.0, TWO_PI, size=N * N)
    raise ValueError("instance must provide either 'phases' or 'seed'")


def _mobius_coefficients(phases, m):
    """Inclusion-exclusion transform: c[S] = sum_{T subset S} (-1)^{|S|-|T|} phi[T].

    Afterwards phi[x] = sum_{S subset x} c[S], which is the multilinear expansion
    used by eq_6 (generalised to m = 2n qubits).
    """
    c = np.array(phases, dtype=float, copy=True)
    size = 1 << m
    for b in range(m):
        bit = 1 << b
        for x in range(size):
            if x & bit:
                c[x] -= c[x ^ bit]
    return c


def _wrap(angle):
    """Reduce an angle to (-pi, pi]."""
    a = math.fmod(angle, TWO_PI)
    if a > math.pi:
        a -= TWO_PI
    elif a <= -math.pi:
        a += TWO_PI
    return a


def build_circuit(instance):
    """Build the diagonal gate U = sum_{j,k} e^{i phi_{jk}} |j><j|_A (x) |k><k|_B (eq_1).

    instance keys:
      N      : int, local dimension (power of two, >= 2)
      phases : list of N^2 floats (index j*N + k) or N x N nested list, OR
      seed   : non-negative int to draw i.i.d. uniform phases (eq_1 ensemble)
      include_reference_registers : optional bool; if true, idle registers B', A'
                                    are appended for the Choi construction (eq_5)
    """
    N, n = _local_qubits(instance)
    include_ref = bool(instance.get("include_reference_registers", False))
    total = 4 * n if include_ref else 2 * n
    if total > MAX_QUBITS:
        raise ValueError("instance requires %d qubits, exceeding the cap of %d" % (total, MAX_QUBITS))

    phases = _extract_phases(instance, N)
    m = 2 * n

    qB = QuantumRegister(n, "B")
    qA = QuantumRegister(n, "A")
    if include_ref:
        qBp = QuantumRegister(n, "Bp")
        qAp = QuantumRegister(n, "Ap")
        qc = QuantumCircuit(qB, qA, qBp, qAp)
    else:
        qc = QuantumCircuit(qB, qA)

    # eq_6 (generalised): multilinear phase coefficients over the 2n qubits of A (x) B.
    coeffs = _mobius_coefficients(phases, m)

    # Global phase e^{i c_0} (= e^{i phi_00} for N = 2).
    c0 = _wrap(float(coeffs[0]))
    if abs(c0) > PHASE_TOL:
        qc.global_phase += c0

    for x in range(1, 1 << m):
        c = _wrap(float(coeffs[x]))
        if abs(c) <= PHASE_TOL:
            continue
        bits = [q for q in range(m) if (x >> q) & 1]
        if len(bits) == 1:
            # local phase gate P(c) on qubit (A or B side)
            qc.p(c, bits[0])
        elif len(bits) == 2:
            # controlled phase CP(c) = diag(1,1,1,e^{ic})
            qc.cp(c, bits[0], bits[1])
        else:
            # multi-controlled phase for higher-order interaction terms (n >= 2)
            qc.mcp(c, bits[:-1], bits[-1])

    return qc
