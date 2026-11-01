# Equation to Qiskit

build_circuit returns a 4-qubit unitary for one of two scoped operations on two qutrits embedded in qubit pairs (0->00, 1->01, 2->10, level 3 acted on by identity). The operations are the controlled shift CX3 (or its inverse, in either orientation) and the ternary SWAP3. The qutrit Fourier gate F is synthesized from standard gates by a numerical Givens decomposition. CZ3 is built from X-conjugated multi-controlled phase gates. CX3 = (I x F^dag) CZ3^(+-1) (I x F), and SWAP3 = N_a CX(a->b) CX(b->a)^-1 CX(a->b), where N is a qubit SWAP of the two qubits of qutrit a.

Source equation run: `773c9b8d-1eb7-4d7e-a7ad-024c4b6a1f0a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: qutrit a, LSB of level index (level j = q0 + 2*q1)
- qubit 1: qutrit a, MSB of level index
- qubit 2: qutrit b, LSB of level index
- qubit 3: qutrit b, MSB of level index
- encoding: level 0->00, 1->01, 2->10, level 3 (11) unused and acted on by identity; global index = a + 4*b
- instance options: operation 'cx3' (optional 'control' in {0,1} = control qutrit index, 'inverse' bool) or 'swap3'

## Assumptions

- TCZ is taken to be the standard generalized controlled-Z with phase w^{ab}.
- Inputs lie in the span of |a,b> with a,b in {0,1,2}. Level 3 is mapped to itself by every gate.
- Qiskit's little-endian order applies: qubit 0 is the LSB of qutrit a.
- The numerical Givens decomposition is done in numpy at build time with fixed deterministic arithmetic. No Qiskit operators or simulation are used.

## Unresolved issues

- The earlier stage reported a status of 'partial', which this schema does not allow. This artifact reports 'generated' for the narrowed scope only.
- Correctness on the 9-dimensional subspace and on the identity sector has not been simulated here. It is left to downstream verification.

## Equation mapping

- `eq_1`: implemented; _fourier_circuit (F and F^dagger via Givens decomposition); N=F^2 realised as qc.swap(0,1) in build_circuit. F is synthesized from standard controlled rotations, CX and phase gates by a numerical Givens decomposition of the 3x3 Fourier matrix, with identity on level 3. N=F^2 is realised directly as the qubit SWAP that exchanges levels 1 and 2. The relation F X F^dag = Z is a background identity that justifies eq_3 and is not built as a gate.
- `eq_2`: implemented; _cz3. Diagonal phases w^{ab} (or w^{-ab} for the dagger) on levels a,b in {1,2}, each applied as an X-conjugated multi-controlled phase gate. The phase is 1 elsewhere, including level 3.
- `eq_3`: implemented; _cx3. CX3 = (I x F^dag) CZ3 (I x F) acting on the target qutrit. The inverse uses CZ3^dagger. Orientation is chosen by selecting which qutrit is the target, since CZ3 is symmetric.
- `eq_4`: implemented; build_circuit, operation 'swap3' branch. Time order: CX(a->b), CX(b->a)^-1, CX(a->b), then N on qutrit a (qubit SWAP of qubits 0,1).
- `eq_5`: implemented; register layout; level-3 identity handled throughout (_phase_level, _two_level, _cz3). 4-qubit embedding with qubit 0 as LSB of qutrit a and global index a+4b. Every sub-gate leaves level 3 untouched.

## Specification changes

- eq_1: The one-qutrit F gate is synthesized from standard gates (Givens two-level rotations as controlled Rz/Ry/phase, plus diagonal phases) rather than inserted as a dense 4x4 unitary. Reason: Opaque dense unitaries are not allowed. The synthesis computes the same F matrix with identity on level 3.
- eq_4: SWAP3 includes the final N on qutrit a, as in the specification's correction. N is implemented as a qubit SWAP, equal to F^2 on the embedded levels. Reason: The three controlled shifts alone give (a,b)->(-b,a). The specification added N to obtain the exact swap.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to CX3 (either orientation, optional inverse) and SWAP3 in the Weyl-Heisenberg F+CZ3 variant. The Cartan one-qutrit gates, Toffoli and Muthukrishnan-Stroud synthesis, physical implementation, qudit generalization and universality are not implemented. Reason: These are outside the single scoped construction in the specification.
