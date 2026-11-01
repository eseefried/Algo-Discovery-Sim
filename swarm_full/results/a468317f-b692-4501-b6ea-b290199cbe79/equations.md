# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Construct orthonormal bases of multi-term entangled Bell-like states, each a superposition of 2^m terms with amplitudes ±1/sqrt(2^m), using two multiple-qubit controlled-unitary gates together with existing quantum gates, and compare the quantum correlations (entanglement, monogamy score) of bases obtained from different controlled-unitaries.

Scope: Abstract-level reconstruction. The explicit gate definitions and circuits are not given in the abstract. Only the amplitude structure and orthonormality constraint are fixed. A small finite instance (for example m=1 or m=2) may be assumed later for illustration.

## Symbols

- $m$: Exponent giving the number of terms 2^m in each Bell-like state; domain: positive integer
- $\pm 1/\sqrt{2^{m}}$: Equal-magnitude amplitudes of each term in a Bell-like state; domain: real numbers

## eq_1: Bell-like state amplitudes

$$
|\psi\rangle=\frac{1}{\sqrt{2^{m}}}\sum_{k=0}^{2^{m}-1}s_k|x_k\rangle,\quad s_k=\pm1
$$

Each Bell-like state is a superposition of 2^m computational basis states with equal-magnitude amplitudes of ±1/sqrt(2^m).

Provenance: `abstract_inferred`. Direct restatement of the abstract. The basis states x_k and the sign pattern are not specified there.

Abstract evidence: superposition of $2^{m}$-terms with equal probabilities (that is, their amplitudes being $\pm 1/\sqrt{2^{m}}$)

Equation assumptions:

- x_k are distinct computational basis states

## eq_2: Orthonormality of basis

$$
\langle\psi_i|\psi_j\rangle=\delta_{ij}
$$

The generated Bell-like states form an orthonormal basis.

Provenance: `abstract_inferred`. Orthonormality is stated in the abstract. The delta form is standard background.

Abstract evidence: orthonormal entangled Bell-like bases

## Registers

- control: m (assumed) qubits; Qubits put in uniform superposition by Hadamards; they control the unitary gates
- target: unknown (assumed at least m) qubits; Qubits acted on by the multiple-qubit controlled-unitary; they carry the entangled Bell-like state

## Initial state

Computational basis state |i>, assumed to label the basis element (label bits set by X gates)

## Measurement

Assumed: to identify which basis element was produced, invert the circuit (the controlled-unitary, then the Hadamards) and measure all qubits in the computational basis, which returns the label i. For the correlation study, the entanglement and monogamy score are computed from the state or reduced density matrices, which would need tomography on an experiment.

## Classical postprocessing

Read the measured bitstring as the basis label. For the correlation analysis, compute the chosen entanglement measures and the monogamy score from the known state vectors or reconstructed density matrices, then compare the bases obtained from the different controlled-unitaries. The abstract does not define these measures.

## Algorithm steps

1. Apply Hadamard gates to the control qubits to create a uniform superposition of 2^m terms, with signs depending on the label bits. (eq_1)
2. Apply one of the two multiple-qubit controlled-unitary gates (the details are not given in the abstract) with the control qubits acting on the targets, which entangles them and spreads the terms over target basis states. (eq_1)
3. Repeat for all initial labels i to obtain the full set of states. The result should satisfy orthonormality, which holds because the circuit is unitary and the inputs are orthonormal. (eq_2)

## Assumptions

- Generic Hadamard plus controlled-unitary schematic assumed, not the paper's actual circuit
- Measurement by inverting the circuit and measuring in the computational basis is assumed, not stated in the abstract

## Missing information

- Definitions of the two multiple-qubit controlled-unitary gates
- Explicit circuit construction
- Definitions of the entanglement and monogamy score measures used
- Exact register sizes and the gate placement
- Whether the paper uses any measurement or tomography protocol
