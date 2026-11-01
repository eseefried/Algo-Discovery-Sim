# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Full n-qubit state tomography via a complete set of 2^n+1 mutually unbiased bases, each realized by a Clifford circuit U_k (H, S/Z-type, CZ gates) before computational-basis measurement, followed by identity-subtracted linear inversion.

Scope: Smallest instance n=3 (qubit cap n, no ancillas, no black box). Generic MUB tomography structure and reconstruction formula are specified; the explicit CZ graph, local gates and generator W of the paper are NOT given in the abstract and must be supplied or searched by the builder (e.g. by verifying the MUB condition numerically). The n=4 case, the entanglement-class classification and the circuit-resource analysis are outside scope.

## Symbols

- $n$: number of qubits; domain: integer, 3 or 4 (scope: 3)
- $d$: Hilbert-space dimension 2^n; domain: integer
- $U_k$: Clifford circuit mapping basis k to computational basis; U_0=I; domain: unitary on n qubits, k=0..d
- $W$: basic generator built from H and CZ (plus local phase gates); domain: Clifford unitary on n qubits
- $|\psi_{k,j}\rangle$: j-th vector of basis k, U_k^\dagger|j\rangle; domain: unit vector in C^d
- $p_k(j)$: probability of outcome j when measuring in basis k; domain: [0,1], sum_j p_k(j)=1
- $\rho$: unknown n-qubit density matrix; domain: d x d, PSD, trace 1
- $j$: outcome integer, j=sum_i b_i 2^i with b_i from qubit i (little-endian; Qiskit key bits[::-1][i]); domain: 0..d-1

## eq_1: MUB condition

$$
|\langle\psi_{k,j}|\psi_{k',j'}\rangle|^2=\frac{1}{d}\quad (k\neq k'),\qquad \langle\psi_{k,j}|\psi_{k,j'}\rangle=\delta_{jj'}
$$

Defining property of the d+1 mutually unbiased bases that the circuits U_k must satisfy; can be checked numerically in simulation.

Provenance: `abstract_inferred`. The abstract refers to complete sets of mutually unbiased bases, whose standard definition is this overlap condition.

Abstract evidence: cyclic generation of mutually unbiased bases

Equation assumptions:

- Complete set has 2^n+1 bases

## eq_2: Cyclic generation

$$
U_0=I,\quad U_k=U_1 W^{k-1}\ \text{or equivalently basis } k \text{ obtained by } W^{k}\text{ applied to a Hadamard-type basis},\quad k=1,\dots,d
$$

Bases beyond the computational one are produced by repeated application of one generator W. The exact indexing and the order of W's action are an assumption and must be fixed by verifying eq_1.

Provenance: `assumption`. The abstract states cyclic generation with a generator using H and controlled-phase gates, but not the exact formula or the order of W.

Equation assumptions:

- W built from H, CZ and S/Z gates
- Cyclic structure of period 2^n+1 on non-computational bases, or an equivalent one
- Specific graph and local gates not given in the abstract

## eq_3: Born probabilities

$$
p_k(j)=\langle j|U_k\,\rho\,U_k^\dagger|j\rangle=\langle\psi_{k,j}|\rho|\psi_{k,j}\rangle
$$

Outcome distribution after applying U_k and measuring all qubits in the computational basis.

Provenance: `standard_background`. Born rule with the definition |psi_{k,j}> = U_k^dagger|j>.

Equation assumptions:

- Exact statevector probabilities or many shots

## eq_4: Linear-inversion reconstruction

$$
\rho=\sum_{k=0}^{d}\sum_{j=0}^{d-1}p_k(j)\,|\psi_{k,j}\rangle\langle\psi_{k,j}|-I
$$

Reconstruction from MUB probabilities; follows because the MUB projectors form a 2-design (sum_k sum_j P_{kj} tr(P_{kj} rho) = rho + I for tr rho=1).

Provenance: `standard_background`. Well-known MUB tomography identity for complete sets of d+1 MUBs.

Equation assumptions:

- Complete set of d+1 MUBs
- tr rho=1

## eq_5: Parameter count

$$
(d+1)(d-1)=d^2-1=4^n-1
$$

Each of the 2^n+1 bases gives 2^n-1 independent numbers, matching the free parameters of rho, so the measurement count is minimal.

Provenance: `abstract_inferred`. Counting inference; the abstract mentions only exponential growth, and the exact count follows from standard background.

Abstract evidence: The number of measurements necessary to perform the quantum state reconstruction of a system of qubits grows exponentially with the number of constituents

Equation assumptions:

- Complete MUB set

## Registers

- q: n (3 for scope) qubits; system qubits holding the state rho, prepared by a given circuit, then rotated by U_k and measured; no ancillas
- c: n qubits; classical bits recording outcome j little-endian: bit i from qubit i

## Initial state

|0>^{\otimes n} followed by a given preparation circuit for the test state rho (pure or mixed, supplied by the task)

## Measurement

Measure all n qubits in the computational basis after U_k for each k=0..2^n; measure(i,i) with outcome j=sum b_i 2^i.

## Classical postprocessing

Compute |psi_{k,j}> = U_k^dagger|j> from the circuit unitary, sum p_k(j)|psi_{k,j}><psi_{k,j}| over all k and j, subtract identity; optionally compare fidelity with the true state. No maximum-likelihood step.

## Algorithm steps

1. Fix n=3 and choose a CZ graph and local gates for W so that the d+1 bases satisfy the MUB condition (verify numerically via the statevector/unitary of the circuits). (eq_1, eq_2)
2. For each k=0..d build the circuit: state preparation, then U_k (k=0 is empty, k>=1 is W-based cyclic product from H, CZ, S/Z gates). (eq_2)
3. Obtain p_k(j) for all j from the computational-basis measurement (exact probabilities or counts), reading j little-endian from the counts key (last char is qubit 0). (eq_3)
4. Reconstruct rho using the identity-subtracted sum with |psi_{k,j}> = U_k^dagger|j> computed from the same circuits. (eq_4, eq_5)

## Assumptions

- n=3 chosen as the smallest instance within the paper's n=3,4 scope
- No ancillas; black box unused
- Builder must find W and the local gates itself; the abstract gives only that W uses H and controlled-phase gates
- Exact probabilities or large-shot counts are available

## Missing information

- Explicit CZ graph, local gates and form of W for each entanglement class
- Order of W and the exact indexing of cyclic bases
- Which bases are separable versus entangled for n=3, 4
- Circuit depth and gate counts per class
