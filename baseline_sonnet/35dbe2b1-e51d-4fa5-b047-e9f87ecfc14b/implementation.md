# Equation to Qiskit

Builds r steps of the first-order Trotter product formula S_1(t/r)^r = (prod_j exp(-i c_j P_j t/r))^r for a Hamiltonian H = sum_j c_j P_j given as a weighted Pauli sum, i.e. already Jordan-Wigner encoded. Each Pauli exponential uses basis changes, a CNOT parity ladder and one RZ. Term order is the input list order. No state preparation or measurement is included.

Source equation run: `9f806aac-6747-435e-9538-3e5e4eabcf20`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Single register 'system' with num_qubits qubits; qubit i is spin orbital i under an assumed Jordan-Wigner encoding (supplied by the caller through the Pauli terms).
- Qubit 0 is the least significant bit. In each Pauli label the leftmost character acts on qubit n-1 and the rightmost on qubit 0.
- No ancilla qubits. The input state is prepared by the runner.

## Assumptions

- The first-order product formula is the chosen construction, since the abstract does not specify the order.
- The Hamiltonian coefficients are real, so every term is Hermitian.
- Term ordering follows the order of the list in the instance.
- The Pauli label convention follows Qiskit: the rightmost character acts on qubit 0.
- The runner prepares any input state, such as a Hartree-Fock state.

## Unresolved issues

- The paper's actual error bounds and their dependence on maximum nuclear charge and filling fraction are not available in the abstract.
- The paper's term ordering and product-formula order are unknown.
- No molecular Hamiltonian is included, so the example is a small generic Pauli-sum, not a real molecule.
- The classical step-size strategies and improved state-preparation methods are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit (loop over r steps and ordered terms) and _term_step (exp(-i c_j P_j tau)). The ordered product of exponentials of the Pauli-decomposed Hamiltonian terms, applied r times with tau = t/r. The circuit is therefore S_1(t/r)^r.
- `eq_2`: out_of_scope; no code location. The operator-norm error compares against exact evolution exp(-iHt), a classical analysis that the circuit builder must not perform.
- `eq_3`: background; no code location. The commutator bound is a theoretical error bound. It motivates choosing r but does not enter the circuit.
- `eq_4`: out_of_scope; no code location. The state-specific error needs an input state and exact evolution for comparison, both of which are experiment and verification tasks outside the operation.

## Specification changes

- eq_1: The Hamiltonian is taken as a weighted sum of Pauli strings supplied in the instance. The terms H_j are c_j P_j, and their order is the list order. Reason: The abstract gives no molecule, no integrals and no term ordering. A generic Pauli-sum input keeps the Trotter construction meaningful for varying valid instances without a fermion-to-qubit mapper in the module.
- eq_1: The Jordan-Wigner transformation is not performed inside the module. The caller must supply already-mapped Pauli terms. Reason: This narrows the scope to the product-formula circuit. The chemistry-specific mapping is not specified in the abstract.
- eq_1: A Pauli string with all identities is implemented as a global phase. Reason: exp(-i c tau I) is a scalar phase.
- eq_1: Instance sizes are capped: at most 12 qubits, 1000 steps, 500 terms, and 5000 total term applications. Reason: This follows the required resource limits and avoids oversized circuits.
- eq_2, eq_3, eq_4: The error analysis, the commutator bound and the state-specific error comparison are excluded from the circuit. Reason: They are classical evaluation quantities, not part of the unitary operation. The paper's chemical-property scaling, step-size strategies and state-preparation methods are also out of scope.
