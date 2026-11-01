# Equation to Qiskit

Generalized Grover-type two-reflection iteration Q = D*O repeated k times on n data qubits (single marked item), with the oracle phase a = pi + delta1 and the diffusion phase b = pi + delta2. The oracle is a multi-controlled phase of angle a conjugated by X on the zero bits of the marked item. The diffusion is H^n X^n mcp(b) X^n H^n. The circuit applies the operation only: the runner prepares |s> and does all measurement, the P_k sweep and the comparison with Grover. The ancilla and any coin qubit are dropped, and the paper's optimized random-walk operator is not reconstructed.

Source equation run: `70491494-0e46-4658-ad72-341d5162660d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: data register 'data', little-endian (qubit 0 is the least significant bit); marked item w is the integer 'marked', with bit i of w on qubit i
- no ancilla and no coin qubit; total qubits = n, with 2 <= n <= 6
- input state |s> = H^n|0> must be prepared by the runner; the circuit contains only Q^k

## Assumptions

- Single marked item given as integer 'marked' in [0, 2^n-1], with bit i on qubit i
- Phase errors delta1 and delta2 are fixed real numbers (default 0) applied identically on every iteration
- The instance has keys n, marked, iterations, delta1 (optional), delta2 (optional)
- The iteration count is supplied by the instance, not derived from the k_opt formula
- The multi-controlled phase is built with qc.cp for n=2 and qc.mcp for n>2

## Unresolved issues

- The actual optimized random-walk operator, its tuned phases and any coin qubit are not recovered
- Closed forms for theta_eff, A, phi and offset are not provided, so eq_4 and eq_5 are not checked in the circuit
- The exact robustness comparison metric against Grover is not specified

## Equation mapping

- `eq_1`: implemented; build_circuit: oracle block (X on zero bits of marked, _phase_all_ones with angle a, X) and diffusion block (H^n X^n _phase_all_ones with angle b X^n H^n). O = I-(1-e^{ia})|w><w| and D = H^n(I-(1-e^{ib})|0><0|)H^n are implemented exactly with a = pi+delta1 and b = pi+delta2, using a multi-controlled phase without an ancilla.
- `eq_2`: implemented; build_circuit: the for-loop over k iterations. Q = D O is applied k times in sequence, oracle first and then diffusion. P_k is obtained by the runner from the output state on input |s>.
- `eq_3`: background; no code location. The reduced 2x2 matrix in span{|w>,|w_perp>} is an analytic description of the operation implemented. It is not built in the circuit.
- `eq_4`: out_of_scope; no code location. The eigen-decomposition and the A, phi, offset fit are classical analysis, not part of a unitary circuit.
- `eq_5`: out_of_scope; no code location. The P_max and k_opt sweep is classical post-processing. The circuit takes the iteration count k as an input parameter.

## Specification changes

- eq_1, eq_2: The circuit contains no state preparation. It is only the operator Q^k on n data qubits, and |s> is prepared by the runner. Reason: The task requires an operation without input-state preparation.
- eq_1: The ancilla in |-> and kickback oracle are dropped. The oracle is a direct multi-controlled phase of angle a on the marked basis state. Reason: This gives an exact adjustable phase a = pi+delta1 without needing a prepared ancilla, and it keeps the circuit measurement-free and unitary.
- eq_2, eq_4, eq_5: The model is the generic two-reflection Grover iteration with phase errors, not the paper's optimized quantum random-walk search. The tuned optimized phases are not implemented. Ideal Grover phases pi plus errors are used. Reason: The abstract does not give the optimized operator or its phases, as already stated in the specification.
- eq_1: The instance restricts n to 2..6 and iterations to 0..200, and diffusion is exactly I-(1-e^{ib})|s><s|. At b = pi this equals the usual Grover diffusion up to a global sign (-1). Reason: Qubit cap and size validation. The global sign is physically irrelevant.
- eq_4, eq_5: Analytic fits, the sweep over k and the Grover comparison are not part of the circuit. Reason: These are classical post-processing steps and the circuit must not contain experiments.
