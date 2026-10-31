# Equation to Qiskit

Implements the first-order (Lie-Trotter) product-formula circuit U_n(t) = (e^{-iAt/n} e^{-iBt/n})^n for a transverse-field Ising chain H = A + B with A = J sum_i X_i X_{i+1}, B = h sum_i Z_i (eq_1), on 2..12 qubits (default/spec instance: 2 qubits, J = h = t = 1). The Trotter number n is either supplied directly or chosen classically from the closed-form tradeoff optimum n* = sqrt(c_1/c_2) (eq_6) when a per-gate error strength epsilon is supplied. The noisy channel, trace distance and the D(n) scan (eq_3, eq_4, eq_5) are experiment/analysis steps, not part of the unitary operation, and are left to the runner.

Source equation run: `33fa8cde-dfa8-48ba-9597-555d895a8412`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'sys' has num_qubits = 2 qubits (cap 12).
- Qiskit qubit 0 (least significant bit) = specification qubit q_2.
- Qiskit qubit 1 (most significant bit) = specification qubit q_1 (the spec writes basis labels |q_1 q_2> with q_1 most significant).
- No ancillas; the circuit is the bare unitary U_n(t). The runner supplies the initial state |00> and any noise/measurement.

## Assumptions

- First-order product formula with two elementary evolutions (B-layer, A-layer) per Trotter step.
- Gate imperfection enters only through the scalar epsilon used to choose n*; the emitted circuit itself is noise-free, and the runner is expected to apply any noise model.
- 'Statistical distance' is interpreted as the trace distance, as in the specification.
- Trotter number is capped at 2000 to keep circuit size bounded; total qubits capped at 12.
- The example instance uses n = 4 explicitly; supplying {"epsilon": 0.01} instead of "n" for the same J = h = t = 1, N = 2 yields n* = sqrt(2/0.02) = 10.

## Unresolved issues

- The paper's actual gate-error model, distance measure, Trotter order and many-body Hamiltonian are unknown; the eq_6 optimum implemented here minimises an upper bound for the assumed additive per-gate trace-distance model and may differ from the paper's n*.
- For num_qubits > 2 the commutator-norm formula used in n* selection is an upper bound rather than the exact spectral norm.
- The integer rounding of n* is done on the bound, not on the exact D(n); the runner's scan over neighbouring n may select a different integer.

## Equation mapping

- `eq_1`: implemented; build_circuit: the `for _ in range(n_steps)` loop with the comment '# eq_1'; RZ(2 h tau) layer realises e^{-iB tau}, RXX(2 J tau) layer realises e^{-iA tau}. First-order Lie-Trotter product (e^{-iA t/n} e^{-iB t/n})^n built from standard RZ and RXX rotations (RZ(phi) = e^{-i phi Z/2}, RXX(theta) = e^{-i theta XX/2}). The B-layer is placed before the A-layer within each step because the rightmost operator factor acts first.
- `eq_2`: background; optimal_trotter_number: line computing c_1 (comment 'Trotter-error coefficient (eq_2)'). The operator-norm Trotter error bound is not an operation; only its coefficient c_1 = (t^2/2)||[A,B]|| enters classically, using the closed-form chain commutator norm bound 4|Jh|(N-1), exact for N = 2.
- `eq_3`: out_of_scope; no code location. The trace distance is a post-processing figure of merit computed by the runner from output states; it is not part of the unitary circuit.
- `eq_4`: out_of_scope; no code location. The imperfect-gate channel and its accumulated trace-distance bound describe noisy execution and analysis, which the runner performs; only its coefficient c_2 = 2 epsilon is used classically in optimal_trotter_number.
- `eq_5`: background; optimal_trotter_number: d_lo / d_hi evaluate the bound c_1/n + c_2 n for the two integer candidates. The total tradeoff bound is evaluated only classically to pick between floor and ceiling of n*; the actual distance D(n) must be obtained by the runner's simulation.
- `eq_6`: implemented; optimal_trotter_number (docstring cites eq_6; `n_real = math.sqrt(c_1 / c_2)`), invoked from build_circuit when 'epsilon' is supplied instead of 'n'. Closed-form continuous optimum n* = sqrt(c_1/c_2) = t sqrt(||[A,B]||/(4 epsilon)), rounded to the integer neighbour minimising the eq_5 bound, then used as the Trotter number of the emitted circuit.

## Specification changes

- eq_1: Generalised the 2-qubit instance A = X_1 X_2, B = Z_1 + Z_2 to an open transverse-field Ising chain A = J sum_k X_k X_{k+1}, B = h sum_k Z_k on 2..12 qubits with arbitrary real J, h, t; the spec instance is the default num_qubits = 2, J = h = t = 1. Reason: The task requires the operation to work for varying valid instance parameters; the 2-qubit TFIM is recovered exactly at num_qubits = 2.
- eq_1: Within each Trotter step the circuit applies the e^{-iB t/n} layer before the e^{-iA t/n} layer in time order. Reason: In the operator product (e^{-iA t/n} e^{-iB t/n})^n the rightmost factor acts first on the state; circuit order must be the reverse of the written matrix order.
- eq_1: Specification qubit k (MSB-first labelling |q_1 q_2 ... q_N>) is mapped to Qiskit index N - k. Reason: Qiskit index 0 is the least significant bit; for the symmetric chain this only relabels the bonds and does not change the unitary's action in the stated basis convention.
- eq_2, eq_6: The commutator norm ||[A,B]|| is replaced by the closed-form value 4|Jh|(N-1), which is exact for N = 2 (two commuting Pauli strings Y X + X Y have norm 2) and an upper bound (triangle inequality) for N > 2. Reason: Operator construction is disallowed inside the module; a closed form is needed for the classical n* selection. For N > 2 the resulting n* minimises a slightly looser bound.
- eq_3, eq_4, eq_5: Noisy gate channels, trace-distance evaluation and the D(n) scan are excluded from the generated module; only the ideal unitary U_n(t) is emitted. Reason: The deliverable is a measurement-free, unitary QuantumCircuit; noise injection, state comparison and minimisation over n are experiment steps for the runner.
- eq_6: When c_1 = 0 (J = 0, h = 0 or t = 0) the module returns n = 1 instead of n* = 0. Reason: The continuous optimum degenerates; one exact Trotter step is the minimal valid circuit.
