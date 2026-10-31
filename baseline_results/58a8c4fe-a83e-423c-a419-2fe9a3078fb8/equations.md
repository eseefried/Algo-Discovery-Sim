# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Quantum state tomography of n qubits (dimension d=2^n) using a complete set of d+1 mutually unbiased bases (MUBs) that are generated cyclically by repeated application of a single unitary generator built from Hadamard and (controlled-)phase gates; the measured outcome statistics in all d+1 bases determine the density matrix.

Scope: Scoped to (i) the general cyclic-MUB framework (unbiasedness condition, cyclic generator of order d+1, MUB-based tomographic inversion) and (ii) one tiny explicit instance: n=1 qubit (d=2), where a verifiable order-3 generator U = S H (phase gate times Hadamard) cycles the computational basis through the Y- and X-eigenbases, giving the complete set of 3 single-qubit MUBs. Out of scope: the paper's explicit multi-qubit (two-, three-, four-qubit) generators built from Hadamard and controlled-phase gates, the classification of entanglement structures of the resulting MUB sets, and the circuits implementing the various entanglement classes; none of these are specified in the abstract and are not invented here.

## Symbols

- $n$: number of qubits; domain: positive integer; instance n=1
- $d$: Hilbert-space dimension, d=2^n; domain: positive integer; instance d=2
- $|j\rangle$: computational-basis state, j encoded as an n-bit string (little-endian: qubit 0 is the least significant bit when n>1); domain: j \in \{0,\dots,d-1\}
- $U$: cyclic MUB generator, a unitary with U^{d+1} proportional to the identity; domain: U \in \mathrm{U}(d)
- $\mathcal{B}_k$: k-th basis of the MUB set, \mathcal{B}_k=\{U^k|j\rangle\}_j; domain: k \in \{0,\dots,d\}
- $\Pi_{k,j}$: rank-one projector onto the j-th vector of basis \mathcal{B}_k; domain: Hermitian projector on \mathbb{C}^d
- $p_{k,j}$: probability of outcome j when the state is measured in basis \mathcal{B}_k; domain: [0,1], \sum_j p_{k,j}=1 for each k
- $\rho$: unknown n-qubit density matrix to be reconstructed; domain: positive semidefinite, trace one, d\times d
- $H$: single-qubit Hadamard gate; domain: 2\times 2 unitary
- $S$: single-qubit phase gate diag(1,i); domain: 2\times 2 unitary
- $CZ_{ab}$: controlled-phase (controlled-Z) gate between qubits a and b, diag(1,1,1,-1); domain: 4\times 4 unitary
- $\varphi$: global phase accumulated by U^{d+1}; domain: real

## eq_1: Mutual unbiasedness condition

$$
\left|\langle \psi^{(k)}_j | \psi^{(m)}_l \rangle\right|^2 = \delta_{jl}\,\delta_{km} + \frac{1}{d}\,(1-\delta_{km}), \qquad k,m\in\{0,\dots,d\},\; j,l\in\{0,\dots,d-1\}
$$

Two orthonormal bases are mutually unbiased when every overlap between a vector of one and a vector of the other has squared modulus exactly 1/d; a complete set for d=2^n contains d+1 such bases.

Provenance: `standard_background`. Standard definition of mutually unbiased bases; existence of d+1 MUBs in prime-power dimension is established background.

Equation assumptions:

- d is a prime power (true for qubits, d=2^n)

## eq_2: Cyclic generation of the MUB set

$$
\mathcal{B}_k=\{\,|\psi^{(k)}_j\rangle = U^k|j\rangle\,\}_{j=0}^{d-1},\quad k=0,\dots,d, \qquad U^{d+1} = e^{i\varphi}\,\mathbb{1}_d
$$

All d+1 bases are obtained by repeatedly applying one generator U to the computational basis; U has order d+1 up to a global phase, so the sequence of bases is cyclic. This is an exact (not approximate) relation; the bases are required to satisfy eq_1.

Provenance: `abstract_inferred`. The abstract states the method is based on cyclic generation of MUBs; the natural mathematical content of 'cyclic' is a single unitary whose powers produce all bases and which returns to the identity (up to phase) after d+1 steps. The specific choice of U in the paper is not given in the abstract.

Abstract evidence: cyclic generation of mutually unbiased bases

Equation assumptions:

- 'Cyclic' is interpreted as a single generator of order d+1 modulo global phase acting on the computational basis

## eq_3: Structure of the basic generator (Hadamard and controlled-phase gates)

$$
U = H^{\otimes n}\, D, \qquad D = \prod_{(a,b)\in E} CZ_{ab}\;\prod_{c\in V} P_c, \quad P_c\in\{\mathbb{1}, S\}
$$

Proposed form of the generator: a layer of Hadamards preceded by a diagonal network D of controlled-phase gates (edge set E) and possibly single-qubit phase gates (vertex set V). The abstract only states which gate types are needed; the precise sets E, V and the gate ordering that make U satisfy eq_1 and eq_2 for n=2,3,4 are NOT determined here.

Provenance: `abstract_inferred`. Inferred from the stated gate set; since controlled-phase gates are diagonal and Hadamards are the only non-diagonal element, the generator decomposes as Hadamards times a diagonal phase network. The explicit pattern is missing information, so this equation is a structural template, not a verified construction.

Abstract evidence: The basic generator requires only Hadamard and controlled-phase gates

Equation assumptions:

- Generator consists of a single Hadamard layer times a diagonal gate; multiple alternating layers are possible in the actual paper
- Single-qubit phase gates may or may not be part of the paper's construction

## eq_4: Explicit one-qubit instance (n=1, d=2)

$$
U_1 = S\,H = \frac{1}{\sqrt{2}}\begin{pmatrix}1 & 1\\ i & -i\end{pmatrix}, \qquad U_1^3 = e^{i\pi/4}\,\mathbb{1}_2, \qquad \mathcal{B}_0=\{|0\rangle,|1\rangle\},\; \mathcal{B}_1=\{|{+i}\rangle,|{-i}\rangle\},\; \mathcal{B}_2=\{|{+}\rangle,|{-}\rangle\}
$$

Smallest explicit instance: Hadamard followed by the phase gate S=diag(1,i) is a cyclic generator of order 3 (up to global phase e^{i\pi/4}) that maps the Z-eigenbasis to the Y-eigenbasis to the X-eigenbasis, which form the complete set of 3 single-qubit MUBs (all cross overlaps have squared modulus exactly 1/2). Uses a single-qubit phase gate rather than a controlled-phase gate because no two-qubit gate exists for n=1.

Provenance: `assumption`. Chosen as the smallest verifiable instance of eqs. 1-2; direct matrix multiplication gives (SH)^3 = ((1+i)/\sqrt{2})\,\mathbb{1} and the three bases are the standard Pauli eigenbases, which are mutually unbiased. This is not claimed to be the paper's generator.

Equation assumptions:

- Instance chosen by the reconstruction, not taken from the abstract
- Gate ordering: H applied first, then S

## eq_5: Outcome probabilities in basis k

$$
p_{k,j} = \mathrm{Tr}\left(\rho\,\Pi_{k,j}\right) = \langle j|\,(U^{\dagger})^{k}\,\rho\,U^{k}\,|j\rangle, \qquad \Pi_{k,j}=U^k|j\rangle\langle j|(U^\dagger)^k
$$

Measuring in basis \mathcal{B}_k is implemented by applying (U^\dagger)^k to the state and then measuring in the computational basis; outcome j occurs with probability p_{k,j}. In practice p_{k,j} is estimated from finite shot counts, so the estimated value approximates the exact probability.

Provenance: `standard_background`. Born rule and the standard equivalence between measuring in a rotated basis and un-rotating the state before a computational-basis measurement.

Equation assumptions:

- Projective (ideal) measurements; finite-sample estimates replace exact probabilities

## eq_6: MUB tomographic reconstruction

$$
\rho = \sum_{k=0}^{d}\sum_{j=0}^{d-1} p_{k,j}\,\Pi_{k,j} \;-\; \mathbb{1}_d
$$

For a complete set of d+1 MUBs the d(d+1) projectors form an informationally complete set and the density matrix is recovered exactly (as a linear inversion) from the outcome probabilities; with estimated probabilities the result is an estimate and may require a positivity-restoring post-processing step.

Provenance: `standard_background`. Standard MUB state-reconstruction formula following from \sum_j \Pi_{k,j}=\mathbb{1} and the unbiasedness condition eq_1.

Equation assumptions:

- Exact probabilities; with finite statistics this is a linear-inversion estimator

## Registers

- data: n (instance: 1) qubits; holds the unknown n-qubit state \rho to be reconstructed; for n>1 qubit 0 is the least significant bit of j in |j\rangle

## Initial state

Unknown state \rho on the data register, prepared identically for every repetition (for the n=1 instance, an arbitrary single-qubit density matrix).

## Measurement

Computational-basis projective measurement of all n data qubits after applying (U^\dagger)^k, for each k = 0,...,d; equivalent to measuring directly in basis \mathcal{B}_k. Total of d+1 measurement settings (3 for the n=1 instance).

## Classical postprocessing

Estimate p_{k,j} from outcome frequencies for each k and j; compute \rho via eq_6; optionally project onto the set of physical (positive semidefinite, unit-trace) states to correct finite-sample errors.

## Algorithm steps

1. Fix n and d=2^n; choose a cyclic MUB generator U satisfying eq_2 and producing bases satisfying eq_1 (for the n=1 instance take U_1 = S H from eq_4; for n>1 the generator has the Hadamard/controlled-phase form eq_3 whose explicit pattern is not provided by the abstract). (eq_1, eq_2, eq_3, eq_4)
2. For each k = 0, 1, ..., d: prepare \rho on the data register and apply the circuit (U^\dagger)^k, i.e. k repetitions of the inverse generator (for n=1: k applications of H S^\dagger). (eq_2, eq_4, eq_5)
3. Measure all n qubits in the computational basis, record outcome j; repeat many shots per k to estimate p_{k,j}. (eq_5)
4. Combine the estimated probabilities over all d+1 bases to reconstruct \rho via linear inversion. (eq_6)

## Assumptions

- No experiment_scope was supplied, so the reconstruction chose the smallest useful instance: a single qubit (d=2) with the order-3 generator U_1 = S H, verified by direct matrix multiplication; this instance is a choice of this reconstruction and is not stated in the abstract
- Cyclic generation is interpreted as a single unitary U of order d+1 (modulo global phase) acting on the computational basis
- The multi-qubit generator is assumed to decompose as a Hadamard layer times a diagonal controlled-phase network (eq_3); its exact structure is unknown
- Ideal gates and projective measurements; finite shot statistics make the reconstruction approximate
- Little-endian integer encoding of computational-basis labels when n>1

## Missing information

- Explicit n-qubit cyclic generator (which qubits receive Hadamards, which pairs receive controlled-phase gates, gate ordering and number of layers) for n = 2, 3, 4
- Definition and classification of the 'different entanglement structures' of the MUB sets and how the generator is modified to realize each class
- The quantum circuits implementing the various entanglement classes analyzed in the paper
- Any discussion of the global phase \varphi and of generators of order d+1 in the Clifford group that the paper may rely on
- Whether the paper's tomographic inversion uses the standard linear MUB formula (eq_6) or a different estimator
