# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Quantize an open quantum walk (OQW) with Kraus operators B_ij (sum_j B_ij^† B_ij = I) on a small graph into a Szegedy-type unitary walk W = SWAP·R, simulate P_t(x) and the Cesaro mean probability, and compare with the spectral formula for the asymptotic mean probability.

Scope: One tiny instance: a 4-node cycle (2 node qubits), internal dimension d=2 (1 qubit), a target-node register (2 qubits), 5 qubits total with no black box and no queries. Dilation ancillas, if needed, are extra. Covers the isometry T, the reflection R, the walk W, P_t(x), the Cesaro mean and the spectral limit. Excluded: the paper's exact construction, its proofs, lattices of infinite extent, general graphs, and any resource-optimal compilation.

## Symbols

- $B_{ij}$: Kraus operator for a jump from node i to node j on the internal space; domain: d x d complex matrices, sum_j B_ij^† B_ij = I
- $T$: isometry from node-internal space to node-target-internal space; domain: linear map H_n⊗H_d -> H_n⊗H_n⊗H_d
- $\Pi$: projector onto range(T); domain: orthogonal projector
- $R$: reflection 2\Pi - I; domain: unitary
- $S$: swap of node and target-node registers; domain: unitary
- $W$: one step of the unitary walk, W = S R; domain: unitary
- $\rho_0$: initial internal state; domain: density matrix on C^d
- $P_t(x)$: probability of finding the walk at node x after t steps; domain: [0,1]
- $\bar P_T(x)$: Cesaro mean probability over T steps; domain: [0,1]
- $e^{i\theta_k}, Q_k$: distinct eigenvalues of W and their spectral projectors; domain: unit circle; orthogonal projectors

## eq_1: Kraus normalization

$$
\sum_j B_{ij}^\dagger B_{ij}=I_d \quad \forall i
$$

Completeness of the Kraus operators, which makes T norm preserving.

Provenance: `standard_background`. Standard OQW definition, taken from the sketch rather than the abstract.

Equation assumptions:

- B_ij given classically

## eq_2: Isometry T

$$
T\,|i\rangle|\psi\rangle=\sum_j |i\rangle|j\rangle\otimes B_{ij}|\psi\rangle,\quad T^\dagger T=I,\quad \Pi=TT^\dagger
$$

Szegedy-type isometry whose Kraus action replaces the amplitudes sqrt(p_ij) of the classical case.

Provenance: `assumption`. Proposed generalization of Szegedy's construction from the sketch. The abstract only says the approach generalizes Szegedy's framework.

Equation assumptions:

- Ordering of the registers is |i>|j>|internal>
- The paper's isometry may differ

## eq_3: Walk operator

$$
W=S\,R,\quad R=U_T\,(2|0\rangle\langle0|_{tgt}\otimes I-I)\,U_T^\dagger=2\Pi-I,\quad S=\mathrm{SWAP}_{node,tgt}\otimes I_{int}
$$

Unitary walk. U_T is a unitary dilation of T acting on the target register starting in |0>. The reflection acts as 2Pi-I only if U_T maps |i>|0>|psi> to T|i>|psi>; the ancilla/dilation completes the unitary.

Provenance: `assumption`. Szegedy-like quantization, as proposed in the sketch.

Equation assumptions:

- U_T built from uniformly controlled gates, with the dilation ancilla returned to |0>
- Whether the target register carries the jump-edge state or is cleared afterwards is not specified

## eq_4: Probability and mean probability

$$
P_t(x)=\mathrm{Tr}\big[(|x\rangle\langle x|_{node}\otimes I)\,W^t(|i_0\rangle\langle i_0|\otimes|0\rangle\langle0|_{tgt}\otimes\rho_0)W^{\dagger t}\big],\quad \bar P_T(x)=\frac1T\sum_{t=0}^{T-1}P_t(x)
$$

Node probability after t steps, with the target and internal registers traced out, and its finite time average.

Provenance: `abstract_inferred`. The abstract says these are defined. The exact form here is my choice of definition.

Abstract evidence: we define the probability and the mean probability of finding the walk at a node

Equation assumptions:

- Initial target register is |0>
- Initial state is pure, or purified with an ancilla

## eq_5: Asymptotic mean probability

$$
\lim_{T\to\infty}\bar P_T(x)=\sum_k \big\|(\langle x|\otimes I)\,Q_k|\psi_0\rangle\big\|^2,\quad W=\sum_k e^{i\theta_k}Q_k
$$

Time averaging removes cross terms between distinct eigenvalues. The sum runs over distinct eigenvalues, and the I acts on all non-node registers. The result holds for a finite-dimensional unitary W.

Provenance: `abstract_inferred`. The abstract claims a derivation. The spectral form is standard for unitary dynamics and is not quoted from the paper. Written this way, the formula is the diagonal part of the density matrix, so the norm should be read as the expectation of the node projector in sum_k Q_k|psi0><psi0|Q_k.

Abstract evidence: then derive the asymptotic mean probability

Equation assumptions:

- Finite-dimensional W
- |psi_0> is the full initial state

## Registers

- node: 2 qubits (ceil(log2 n)) qubits; current node |i>
- target: 2 qubits qubits; edge partner node |j>, starts in |0>
- internal: 1 qubit (log2 d) qubits; internal state acted on by the Kraus operators
- dilation_ancilla: 0 or 1 qubit, unknown qubits; Stinespring/unitary completion of T, returned to |0>

## Initial state

|i_0> on node, |0> on target, internal in a pure state psi_0 (or a purified rho_0 with an extra ancilla)

## Measurement

Measure only the node register at the end of each t-step circuit, or read the statevector marginals. Qiskit is little-endian, so node bit k is qubit k of that register.

## Classical postprocessing

Average P_t(x) over t to get the mean probability. Eigendecompose W (a numerical unitary of the simulated circuit) to group eigenvalues, build the Q_k, evaluate eq_5, and compare with the finite-T average.

## Algorithm steps

1. Pick a tiny instance (4-node cycle, d=2) and Kraus operators B_ij satisfying eq_1 (e.g. B_{i,i±1} = a scaled unitary or a Kraus pair of a qubit channel). Check normalization classically. (eq_1)
2. Build U_T from multiplexed (uniformly controlled) gates conditioned on node i, acting on the target and internal registers, completed to a unitary so that U_T|i>|0>|psi> = T|i>|psi>. (eq_2)
3. Form R = U_T(2|0><0|_tgt - I)U_T^† and apply SWAP of node and target, giving W. Repeat W t times with no mid-circuit measurement. (eq_3)
4. Read the node distribution P_t(x) from the statevector or counts on the node qubits only, for t=0..T-1, and average to get the mean probability. Compute the spectral limit from the eigendecomposition of W classically and compare. (eq_4, eq_5)

## Assumptions

- The tiny instance and the isometry T are my choices, not from the abstract
- Dilation of T uses an ancilla returned to |0>
- Node count is a power of 2
- The mean probability is a finite average approximating the limit
- No black-box queries are used

## Missing information

- The exact construction of the paper's unitary walk, in particular how the coin/reflection acts on the internal space
- Which register the swap acts on in the paper, and how the walk starts
- Explicit Kraus operators for the target instance
- Eigenstructure results for the paper's walk (the asymptotic formula there may be closed form)
- Whether the walk acts on edge states, which could change the dimension
