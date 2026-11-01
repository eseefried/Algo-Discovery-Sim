# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Additive approximation of the Ising partition function Z = sum_s exp(sum_<ij> J_ij s_i s_j + sum_i h_i s_i) on a small square lattice, via the Van den Nest-Duer-Briegel overlap with a cluster/graph state, estimated by a Hadamard test.

Scope: One tiny instance: a 2x2 (or 2x3) lattice with a single-qubit-per-site overlap form of the mapping. Prepare the cluster state with H and CZ, apply the product-state rotation, and read Re and Im of the overlap with a Hadamard test. Out of scope: the BQP-completeness proof, the explicit approximation scale for real parameters, the exponential-improvement comparison, and the classical-hardness evidence.

## Symbols

- $J_{ij}, h_i$: Ising couplings and magnetic fields (complex in the BQP-hard regime, real physically); domain: complex or real numbers
- $s_i$: Ising spin; domain: {+1,-1}
- $|\psi_G\rangle$: graph (cluster) state on the chosen graph G; domain: n-qubit stabilizer state
- $|a\rangle$: product state whose local weights are set by J and h; domain: unnormalized product state
- $N$: classically computable normalization factor relating Z to the overlap; domain: positive real
- $\epsilon$: additive precision of the overlap estimate; domain: (0,1)
- $V$: cluster-state preparation unitary, CZ over edges times H^{\otimes n}; domain: unitary on n qubits
- $U_a$: product of single-qubit unitaries mapping |0> to the normalized |a>; domain: unitary on n qubits

## eq_1: Partition function

$$
Z=\sum_{s\in\{\pm1\}^n}\exp\Big(\sum_{\langle ij\rangle}J_{ij}s_is_j+\sum_i h_i s_i\Big)
$$

Ising partition function to be approximated.

Provenance: `abstract_inferred`. The abstract names Ising partition functions on square lattices; the explicit form is the standard definition.

Abstract evidence: calculating partition functions of Ising models

Equation assumptions:

- Square-lattice graph with open boundaries on a tiny instance

## eq_2: Overlap mapping

$$
Z=N\,\langle a|\psi_G\rangle,\qquad |a\rangle=N^{-1}\text{-normalized product state}
$$

Z is proportional to the overlap of a product state with a graph state. The details of the decorated lattice and the weight formulas are not reconstructed here.

Provenance: `abstract_inferred`. The abstract cites the overlap mapping, and the sketch states Z is proportional to the overlap. The exact constants and weights come from my recollection of the mapping, not from the abstract.

Abstract evidence: we utilize the overlap mapping developed by Van den Nest, Dür, and Briegel

Equation assumptions:

- For this instance the qubit-per-site graph state and local weights are chosen so the identity holds
- N is computed classically

## eq_3: Cluster state and overlap circuit

$$
|\psi_G\rangle=\prod_{(ij)\in E}CZ_{ij}\,H^{\otimes n}|0\rangle^{\otimes n}=V|0^n\rangle,\quad \langle a|\psi_G\rangle=\langle 0^n|U_a^\dagger V|0^n\rangle
$$

The overlap is a vacuum-to-vacuum amplitude of the circuit U_a^dagger V.

Provenance: `standard_background`. Standard graph-state construction; this is the circuit form of the MBQC interpretation.

Equation assumptions:

- |a> normalized so that U_a exists; non-unitary weights are absorbed into N

## eq_4: Hadamard test readout

$$
\langle X\rangle_{anc}=\mathrm{Re}\,A,\quad \langle Y\rangle_{anc}=\mathrm{Im}\,A \ \text{(for the Y-basis convention that gives +Im)},\quad A=\langle 0^n|U_a^\dagger V|0^n\rangle
$$

A control ancilla in |+> controls U_a^dagger V on the |0^n> register, which is the unitary-circuit Hadamard test.

Provenance: `standard_background`. Standard Hadamard test identity; the sign of Im depends on the convention and should be checked in simulation.

Equation assumptions:

- Controlled-(U_a^dagger V) is built from controlled standard gates, and the |0^n> reference register is used with a controlled-V then controlled-U_a^dagger structure
- Alternative: a controlled-V against an uncontrolled U_a ensures the reference state is the same for both branches

## eq_5: Estimator and additive error

$$
\hat Z=N(\hat x+i\hat y),\quad |\hat Z-Z|\lesssim \epsilon N \text{ with } O(1/\epsilon^2)\text{ shots}
$$

Z is estimated as N times the estimated overlap, with error scaling set by N, which is the approximation scale.

Provenance: `abstract_inferred`. The abstract mentions an approximation scale; the sampling form is the standard shot-noise argument.

Abstract evidence: an approximation scale, which determines the accuracy of the approximation

Equation assumptions:

- The scale is N times epsilon in this sketch, not the paper's explicit scale

## Registers

- anc: 1 qubits; Hadamard test control ancilla
- lat: n = L*L (e.g. 4 for 2x2, 6 for 2x3) qubits; cluster-state qubits, one per lattice site, index = r*L + c in little-endian order

## Initial state

All qubits in |0>.

## Measurement

Measure only the ancilla, once in the X basis and once in the Y basis, over many shots. The lattice qubits are left unmeasured. Mind Qiskit's little-endian bit order when reading counts.

## Classical postprocessing

<X> = (n0 - n1)/shots and <Y> likewise, giving A = <X> + i<Y>. Then Z_hat = N*A.

## Algorithm steps

1. Classically compute the local weights, the normalized product state |a>, and N from J and h. Determine the single-qubit rotations U_a. (eq_2)
2. Put the ancilla in |+>. Apply controlled-V to the lattice register (controlled-H on each qubit plus CCZ for each edge, or any equivalent construction), then controlled-U_a^dagger. Alternatively compute the test in the usual form with an uncontrolled reference. (eq_3, eq_4)
3. Measure the ancilla in the X basis (apply H) and then in the Y basis (apply Sdg then H), in separate runs. (eq_4)
4. Form the estimate of the overlap A from the two expectation values and multiply by N to get Z. Compare with brute-force enumeration. (eq_5, eq_1)

## Assumptions

- Tiny 2x2 or 2x3 lattice with the qubit count under the cap including the ancilla
- Complex parameters are realized via unitary rotations; real parameters need non-unitary weights whose normalization goes into N
- The decorated-lattice overlap form is simplified to a form where the identity in eq_2 holds for the chosen instance

## Missing information

- The exact weight formulas for |a> in terms of J and h, and the exact form of N
- The precise graph (decorated lattice) used in the paper's overlap mapping
- The explicit approximation scale for real parameters and the algorithmic domain
- The BQP-completeness construction
- Whether controlled-V is needed or a cheaper circuit is used
