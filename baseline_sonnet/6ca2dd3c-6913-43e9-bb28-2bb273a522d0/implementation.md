# Equation to Qiskit

Exact (not Clifford+T approximate) n-qubit diagonal unitary D = sum_x exp(i theta_x)|x><x|, built as a phase polynomial. The Walsh-Hadamard transform of the phase vector gives one parity phase rotation per nonzero Walsh coefficient. Each rotation uses a CNOT parity ladder, a P gate and the ladder uncompute. Phases can be given directly per basis state or as phase classes (the eq_3 grouping). No ancillas are used. The default example is the n=2, k=2 controlled-phase instance.

Source equation run: `39b67fb5-8e6b-46a3-8f59-49bceb3b7a8e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0..n-1]: system qubits, little-endian; basis index x = sum_i x_i 2^i with x_i on qubit i
- No ancilla qubits; total qubits = n <= 12

## Assumptions

- Little-endian basis encoding: qubit i carries bit i of x.
- Phases are taken modulo 2*pi.
- Walsh coefficients with magnitude below 1e-12 are skipped.
- Instance has key n plus exactly one of theta (list of 2^n reals) or classes (list of {phase, states} partitioning 0..2^n-1).

## Unresolved issues

- The paper's actual decomposition algorithm, E(n,k), C_0 and decision boundary are not reconstructed.
- The circuit's rotation count scales with the Walsh sparsity of the phase vector rather than with k, and no T-count is produced.

## Equation mapping

- `eq_1`: implemented; build_circuit / _parse: theta vector or classes define D; Walsh phase-polynomial synthesis. The circuit realizes D = sum_x exp(i theta_x)|x><x| exactly (up to float precision) with CNOT-parity P gates and a global phase theta_0.
- `eq_2`: background; no code location. The T-count bound is an abstract-level cost statement. E(n,k) and C_0 are unspecified, and the circuit uses continuous P gates, so no T-count is computed.
- `eq_3`: implemented; _parse: 'classes' input branch. Phase-class projectors P_j are accepted as input (a partition of the basis states with one phase each) and expanded into a theta vector. The synthesis does not use k as its cost parameter.
- `eq_4`: out_of_scope; no code location. Clifford+T rotation synthesis to precision epsilon is not implemented. Rotations are exact P gates, and approximation is left to a downstream transpiler.
- `eq_5`: implemented; example_instance_json. The n=2, k=2 instance diag(1,1,1,e^{i phi}) with phi=pi/3 is provided as the example instance.

## Specification changes

- eq_2, eq_4: Narrowed scope to an exact diagonal-unitary operation with continuous-angle P gates. There is no Clifford+T approximation, epsilon parameter, or T-count accounting. Reason: The abstract does not give the paper's algorithm, E(n,k), or C_0, and Clifford+T rotation synthesis cannot be done inside the allowed imports.
- eq_1, eq_3: The implemented construction is a Walsh-Hadamard phase-polynomial synthesis whose rotation count equals the number of nonzero Walsh coefficients (up to 2^n-1), not a k-rotation circuit. Reason: The paper's k-dependent decomposition is not specified. The assumed phase-class grouping is used only as an input format.
