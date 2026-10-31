# Equation to Qiskit

Implements the diagonal bipartite unitary U = diag(exp(i*phi_x)) on 2n qubits (N = 2^n per subsystem), whose diagonal vector reshaped to an N x N matrix is the unimodular matrix A of eq_2. Phases are supplied in the instance or generated from an integer seed. The diagonal is synthesized with standard gates by a Walsh-Hadamard expansion into parity phases (CX ladders and P gates) and a global phase, with no dense unitary. Computing rho and its entropy (eq_1, eq_3) is classical post-processing and is not implemented in the circuit.

Source equation run: `84cc3310-d1a5-4956-9c48-943c5dff14d5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0..n-1]: subsystem B, column index j of A (q0 least significant)
- q[n..2n-1]: subsystem A, row index i of A
- computational basis index x = i*N + j with N = 2^n; U|x> = exp(i*phi_x)|x>
- A[i,j] = exp(i*phi[i*N+j]) (row-major reshape); example n=2 uses 4 qubits, N=4
- no ancilla qubits

## Assumptions

- The diagonal vector is reshaped row-major: A[i,j] = d[i*N+j], with i on the high qubits and j on the low qubits.
- Phases are in radians and real-valued.
- If no phases are given, a seeded numpy uniform [0,2pi) generator provides them.
- The Walsh-Hadamard parity-phase decomposition is an exact synthesis of the diagonal, up to a global phase that is set explicitly.

## Unresolved issues

- The exact entangling power formula and its link to S(rho) are not given in the abstract and are not implemented.
- The Borel triangle moment formulas are not given in the abstract and are not implemented.
- The gate count grows as about 4^n parity terms, which is acceptable for n <= 6 but not optimized.

## Equation mapping

- `eq_1`: background; no code location. rho = A A^dagger / N^2 is classical post-processing of the diagonal of U and is not part of the circuit. The circuit only produces U, whose diagonal defines A.
- `eq_2`: implemented; build_circuit: phase vector phi, unit-modulus diagonal entries exp(i*phi_x), row-major reshape x = i*N + j. The gate has unimodular diagonal entries exp(i*phi_x), which form the unimodular matrix A under the stated qubit layout. Random phases come from the instance or from a seeded generator.
- `eq_3`: background; no code location. Von Neumann entropy is a classical functional of the spectrum of rho and is not a unitary operation.

## Specification changes

- eq_1, eq_3: Scope narrowed to constructing the diagonal gate U only. The spectrum of rho, its entropy, and ensemble averages are left to classical post-processing. Reason: The abstract gives no quantum protocol for estimating the entropy or the entangling power, and the operation must be measurement-free and unitary.
- eq_2: The random phases are deterministic inputs (explicit list or seed) rather than sampled inside an ensemble average. N is restricted to a power of 2 with n <= 6 so the circuit has at most 12 qubits. Reason: The circuit builder must be reproducible, and the qubit encoding needs a power-of-2 dimension.
