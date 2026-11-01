# Equation to Qiskit

Implements the permutation operator P_sigma|j> = |sigma(j)> for a chosen sigma in S_4 on one ququart encoded as two qubits (j = 2*spatial + polarization). It is built only from X, CX and the identity, via a decomposition of sigma into basis-state transpositions; each transposition is realised with CX/X gates. The circuit contains no state preparation or measurement. The paper's input state, measurement and linear-optical implementation are out of scope.

Source equation run: `89611e00-bc7f-43fb-87f7-02d748f8e295`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 = polarization bit p (least significant)
- qubit 1 = spatial-mode bit s
- ququart basis label j = 2*s + p, so |j> = |q1 q0> in Qiskit little-endian ordering

## Assumptions

- The ququart is encoded as two qubits with j = 2*spatial + polarization, so qubit 0 is polarization and qubit 1 is spatial.
- The permutation sigma is given as a list with sigma[j] being the image of j, and P_sigma|j> = |sigma(j)>.
- The ancilla-free construction uses only X and CX gates; global phases are trivial.

## Unresolved issues

- The paper's actual input state, measurement basis and any ancillary degrees of freedom are not reconstructed.
- The linear-optical implementation of the permutations is not modeled.
- The circuit does not itself perform the one-step parity determination, because the abstract gives no explicit construction.

## Equation mapping

- `eq_1`: implemented; build_circuit (with helpers _transposition and _single_bit_swap). P_sigma|j> = |sigma(j)> is built as a sequence of basis-state transpositions, each implemented with X and CX gates.
- `eq_2`: background; no code location. sgn(sigma) = det P_sigma is a standard group-theory fact. It is not a circuit element, and the circuit does not compute or output parity.
- `eq_3`: out_of_scope; no code location. The illustrative Fourier-type input state is input preparation. It is left to the runner, and the circuit does not prepare it.
- `eq_4`: out_of_scope; no code location. The single-query distinguishability criterion involves an unspecified measurement observable M. No measurement is included and no parity-testing scheme is reconstructed.

## Specification changes

- eq_1: The scope is narrowed to the permutation oracle P_sigma alone, acting on a 2-qubit ququart. The permutation is a runtime parameter of the instance. Reason: The abstract gives no explicit parity-determining circuit, input state, or measurement, so only the well-defined permutation operation can be implemented faithfully.
- eq_3, eq_4: The input state, the measurement and the parity read-out are excluded from the circuit. Reason: The task requires an operation without state preparation or measurement. The paper's actual input state and measurement basis are unknown.
- eq_2: The determinant/parity relation is treated as background only and is not computed in the circuit. Reason: Parity is a classical property of sigma. No unitary circuit element is specified for it.
