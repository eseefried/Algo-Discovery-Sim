# Equation to Qiskit

First-order Trotter circuit for a second-quantized molecular Hamiltonian under Jordan-Wigner encoding. The instance supplies sparse real one- and two-electron integrals, an evolution time and a step count r. The module maps each fermionic term to Pauli strings with its own Pauli algebra, checks that the result is Hermitian, then applies r repetitions of the product of Pauli-string exponentials exp(-i c_j t/r P_j) using H/S basis changes, CX ladders and RZ gates. No state preparation or measurement is included.

Source equation run: `0e2e4bff-71f8-4a36-8cff-023f0233d43e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit i (0..n_orbitals-1) = spin orbital i, Jordan-Wigner occupation encoding: |1> = occupied, |0> = empty
- qubit 0 is the least significant bit
- no ancilla qubits; total qubits = n_orbitals <= 12

## Assumptions

- Jordan-Wigner mapping with qubit p for spin orbital p
- Real integrals
- Two-body convention is H2 = 1/2 sum h_pqrs a_p^dag a_q^dag a_r a_s with no automatic symmetrization
- Identity-term energy is applied as a global phase

## Unresolved issues

- No explicit Trotter error bound or criterion for r is available
- The paper's alternative scheme and coalescing scheme are not reconstructed
- No specific molecule or fitted exponents are given; the example is an artificial toy Hamiltonian

## Equation mapping

- `eq_1`: implemented; _hamiltonian_paulis (with _ladder and _mul). One- and two-electron terms are built as products of Jordan-Wigner ladder operators and expanded into real-coefficient Pauli strings.
- `eq_2`: implemented; build_circuit loop over r steps with _pauli_rotation. First-order product formula with each Pauli string as one H_j. Each step applies exp(-i c_j t/r P_j) in sorted-key order.
- `eq_3`: background; no code location. G = r*G_step is a gate-count relation. The circuit repeats the step r times, but r is an input and is not derived from epsilon.
- `eq_4`: out_of_scope; no code location. The N^8 scaling is a reported result about random molecules, not an operation.
- `eq_5`: out_of_scope; no code location. The N^6 empirical worst-case scaling is a reported result and cannot be implemented as a circuit.

## Specification changes

- eq_1: Integrals are real and given as sparse lists. The Hamiltonian must come out Hermitian (all Pauli coefficients real), otherwise ValueError is raised. Jordan-Wigner is fixed as the encoding. Reason: The spec left the encoding open and gave no concrete molecule. Real sparse input keeps the instance small, and the Hermiticity check avoids silently changing the Hamiltonian.
- eq_2: Only first-order Trotter is implemented, with terms in sorted Pauli-string order (the identity term only adds a global phase). Each Pauli string is one H_j rather than each fermionic term, and r is supplied by the user. Reason: The ordering and step-size criterion were unspecified. Pauli-string splitting is the standard concrete choice.
- eq_3, eq_4, eq_5: Gate-count analysis, error bounds, choosing r from epsilon, and the scaling claims are not implemented. The paper's alternative scheme, coalescing and the complexity-bounding method are also excluded. Reason: They are analytic or empirical results rather than a single circuit operation, and the abstract gives insufficient detail.
