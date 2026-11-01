# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Generate an orthonormal basis of n=3 qubit Bell-like states, each a 2^m-term superposition with amplitudes ±1/sqrt(2^m), by applying Hadamards on m qubits and a multi-qubit controlled-X fan-out to computational basis inputs. The input index x labels the output basis state.

Scope: Single instance n=3, m=2 (also valid for m=1): H on m control qubits followed by a CNOT-type controlled-X fan-out with a fixed GF(2)-linear map f onto the n-m target qubits. The paper's two specific controlled-unitary gates, the qudit extension, and the entanglement and monogamy analysis are outside scope. This is a generic family member, not the paper's exact construction.

## Symbols

- $n$: total number of qubits; domain: integer, n=3
- $m$: number of Hadamard (control) qubits; states have 2^m terms; domain: integer, 1<=m<n
- $x=(a,y)$: input basis label; a in {0,1}^m sets the sign pattern, y in {0,1}^{n-m} sets the target offset; domain: bit strings
- $f$: fixed GF(2)-linear map from {0,1}^m to {0,1}^{n-m}, implemented as CNOT fan-out; domain: linear over GF(2)
- $|B_x\rangle$: output Bell-like basis state; domain: n-qubit pure state
- $U$: circuit unitary CU(H^{\otimes m}\otimes I); domain: unitary on 2^n dimensions
- $P_A$: projector onto the |1> state of a control qubit, as in the predicted multi-controlled-X form; domain: projector

## eq_1: Bell-like state

$$
|B_{a,y}\rangle=2^{-m/2}\sum_{c\in\{0,1\}^m}(-1)^{a\cdot c}\,|c\rangle\,|f(c)\oplus y\rangle
$$

Output of the circuit on input |a>|y>; a 2^m-term superposition with amplitudes ±2^{-m/2}.

Provenance: `abstract_inferred`. The equal-magnitude amplitude claim is explicit in the abstract; the specific form via H and CNOT fan-out is an assumed realization.

Abstract evidence: The Bell-like states in any basis is superposition of $2^{m}$-terms with equal probabilities (that is, their amplitudes being $\pm 1/\sqrt{2^{m}}$).

Equation assumptions:

- f linear over GF(2)
- controls are the first m qubits

## eq_2: Circuit unitary

$$
U=\Big(\sum_{c}|c\rangle\langle c|\otimes X^{f(c)}\Big)\,(H^{\otimes m}\otimes I^{\otimes (n-m)})
$$

H on the control qubits, then a multi-target controlled-X fan-out. X^{f(c)} is a bitwise X on the targets according to the bits of f(c).

Provenance: `assumption`. Proposed concrete controlled-unitary; the paper's two gates are not stated in the abstract.

Equation assumptions:

- X-type controlled unitary only

## eq_3: Orthonormality

$$
\langle B_{x}|B_{x'}\rangle=\langle x|U^\dagger U|x'\rangle=\delta_{x,x'}
$$

The 2^n outputs form an orthonormal basis because U is unitary.

Provenance: `standard_background`. A unitary maps an orthonormal basis to an orthonormal basis.

## eq_4: Instance f

$$
f(c_1,c_2)=c_1\oplus c_2\quad(n=3,m=2)
$$

Explicit map for the tiny instance, realized by CNOT c1->t and CNOT c2->t. It is linear but not injective; the offset y still labels states uniquely.

Provenance: `assumption`. Chosen as a smallest concrete example.

Equation assumptions:

- qubit order (c1,c2,t)

## eq_5: Multi-controlled-X form (predicted)

$$
\mathcal{U}_{C^mX}=(I-P_A)\otimes\cdots\otimes(I-P_M)+P_A\otimes\cdots\otimes P_M\,X
$$

Predicted general form of a multiple-qubit controlled-X: X acts on the target only when all controls are in |1>. Kept as a background-style gate definition, not used in the n=3 CNOT instance.

Provenance: `assumption`. Equation-specialist prediction, unverified. The form is plausible as a standard multi-controlled gate, but the abstract does not state it and the paper's two gates are unknown. As written, the product-of-projectors structure is schematic since the target factor is absorbed into X.

Equation assumptions:

- P_k=|1><1| on control k
- the target operator is X

## Registers

- c: m=2 qubits; control qubits that receive H, the first qubits in ordering
- t: n-m=1 qubits; target qubits that receive the controlled-X fan-out

## Initial state

Computational basis state |a>|y> loaded by X gates, with index x=(a,y). Qubit 0 is the most significant bit in the label; Qiskit's little-endian ordering must be mapped accordingly.

## Classical postprocessing

Decoding: apply U^dagger and read the computational basis to recover x. Entanglement comparisons (concurrence, negativity, monogamy score) are done offline and are not implemented.

## Algorithm steps

1. Load basis input x=(a,y) with X gates, giving the state |a>|y> on which U acts (this is the input of eq_2). (eq_2)
2. Apply H to the m control qubits (the first factor in U). (eq_2)
3. Apply CNOT fan-out from controls to targets according to f (the multi-controlled X-type gate). (eq_2, eq_4, eq_5)
4. Output is |B_x>; orthonormality over all x can be checked via the Gram matrix of the columns of U. (eq_1, eq_3)

## Assumptions

- n=3, m=2 chosen as the smallest instance
- only X-type fan-out is implemented; phase-type gates are not

## Missing information

- The paper's two specific multiple-qubit controlled-unitary gates
- Qudit generalization
- Entanglement and monogamy score definitions and results
