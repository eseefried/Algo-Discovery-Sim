# Equation to Qiskit

build_circuit(instance) returns the symmetric second-order Trotter-Suzuki unitary U_r (eq_2) for a Hamiltonian given as a list of real-coefficient Pauli strings, such as a Jordan-Wigner H2 Hamiltonian. Each Pauli exponential is a basis change, CNOT parity ladder, RZ, reverse ladder and basis undo. There is no state preparation, measurement or classical post-processing.

Source equation run: `bfa59ff7-5836-4be8-82cf-72181f7903b9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit i (0..n-1) = Jordan-Wigner spin orbital i; qubit 0 is the least significant bit
- Pauli label strings are written Qiskit-style: the rightmost character acts on qubit 0, the leftmost on qubit n-1
- No ancilla qubits; total qubits = n_qubits (<=12), 4 in the example
- Input state (e.g. the HF determinant with X on occupied qubits) is prepared by the runner

## Assumptions

- The Hamiltonian terms are real-coefficient Pauli strings, so each H_j is Hermitian.
- n_qubits <= 12, steps <= 1000 and at most 200 terms; anything else raises ValueError.
- The example uses n=4 qubits, t=1, r=2 with illustrative H2-like coefficients that are not claimed to be accurate integrals.
- Terms are applied in the order given, forward then reversed in each step.

## Unresolved issues

- Actual H2 integrals and the JW term ordering used in the paper are unknown.
- The paper's improved state preparation (Givens ladder angles) is not reconstructed.
- The eta-subspace error analysis and the C fit must be done outside this module.
- The paper's error bounds and the dependence on Z and eta/n are not reconstructed.

## Equation mapping

- `eq_1`: background; no code location. The Jordan-Wigner Pauli decomposition H = sum_j H_j is not computed here. The Pauli terms and coefficients are supplied through instance['terms'], and the integrals are external.
- `eq_2`: implemented; build_circuit: the loop over r steps (forward then reversed term sweep) and the nested apply_pauli_exp. Each Pauli term is exponentiated as exp(-i c_j P_j t/(2r)) by basis change, CNOT ladder, RZ(2*theta) and the reverse ladder. The forward sweep over terms is followed by the reverse sweep, and the whole sequence is repeated r times.
- `eq_3`: out_of_scope; no code location. HF state preparation is input-state preparation, which the runner handles. The returned circuit is only the evolution operation.
- `eq_4`: out_of_scope; no code location. The ground-state error in the eta-electron subspace, the effective Hamiltonian and the fit of C are classical post-processing that needs simulation. They are not part of the circuit.
- `eq_5`: out_of_scope; no code location. Choosing the step count by classical extrapolation is classical post-processing. Here r is just an input parameter.

## Specification changes

- eq_2: Time-order convention fixed: in the circuit the forward sweep j=1..L is applied first and the reverse sweep j=L..1 second. The operator-product reading of eq_2, where the rightmost factor acts first, would reverse this order. Reason: The product in eq_2 is ambiguous about operator versus time ordering. Both orderings are symmetric second-order formulas, but they are different unitaries. The convention chosen is disclosed.
- eq_1, eq_2: Hamiltonian terms are given as an explicit list of Pauli strings with real coefficients (H_j = c_j P_j) in the instance, instead of being built from h_pq and h_pqrs. Pauli labels follow the Qiskit convention (rightmost character = qubit 0). Reason: The integrals are not supplied and the JW term ordering is unspecified. A generic Pauli-term input keeps the operation valid for varying parameters. The example coefficients are illustrative placeholders, not verified H2 integrals.
- eq_1, eq_3, eq_4, eq_5: Scope narrowed to the Trotter evolution operator only. HF preparation, subspace-restricted error analysis and step-count estimation are excluded. Reason: The task requires an operation with no state preparation, measurement or classical analysis.
- eq_2: Identity Pauli terms are implemented as a global phase of -c*t/(2r) per occurrence. Pauli exponentials are built from explicit gates, not PauliEvolutionGate. Reason: An identity term only contributes a global phase. Explicit gates make the ordering and the CNOT-ladder structure transparent.
