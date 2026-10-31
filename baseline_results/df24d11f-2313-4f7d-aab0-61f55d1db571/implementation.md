# Equation to Qiskit

Implements the ancilla-indicator factorization of an n-qubit diagonal unitary with k distinct phases (eq_1-eq_3): for every distinct nonzero phase theta_j, a reversible minterm network (X-conjugated multi-controlled-X gates) computes the indicator f_j(x) of the phase class S_j into one clean ancilla, a single phase gate P(theta_j) acts on the ancilla, and the network is uncomputed. The result equals D (x) I exactly on ancilla |0>. The Clifford+T approximation of P(theta_j) (eq_4) is replaced by the exact phase gate, which is disclosed as a scope narrowing.

Source equation run: `d93106a3-ee0d-437e-8203-073d1ff294d3`

Generation: **generated**; validation: **failed**.

Generated source was not executed: ValueError: Module constants must be literals or small numeric expressions.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1 = data register (instance: qubits 0,1); basis label x has bit i stored on qubit i, qubit 0 least significant
- qubit n = anc (instance: qubit 2); clean ancilla receiving the indicator f_j(x), restored to |0> after each factor
- example: D = diag(1,1,1,e^{i pi/5}) on data; circuit = Toffoli(data0,data1->anc), P(pi/5) on anc, Toffoli uncompute; total 3 qubits

## Assumptions

- Instance phases are given as a dense list of 2^n real angles theta(x) indexed little-endian (qubit 0 = least significant bit).
- Phases are considered equal (same class) when they agree mod 2 pi after rounding to 10 decimal places of theta/(2 pi).
- The ancilla is prepared in |0> by the runner; on other ancilla states the circuit implements the phase on the complementary class instead.
- Multi-controlled X gates (qc.mcx) with up to 11 controls are acceptable standard-library gates for the reversible logic; their internal decomposition is left to the transpiler.
- Qubit cap: n + 1 <= 12, hence n <= 11.

## Unresolved issues

- Actual Clifford+T synthesis of the phase rotations (eq_4) and the resulting per-rotation precision budget (eq_5) are not realised; the circuit is exact rather than epsilon-approximate.
- The paper's entanglement cost E(n,k) and its optimized indicator/phase-context circuitry are unknown; the minterm network used here may have far higher T-count for large classes S_j.
- How the log_2 k overhead from uniform error allocation is handled in the paper is not addressed.

## Equation mapping

- `eq_1`: implemented; _group_phases. Scans the 2^n phases, reduces them mod 2 pi, and groups equal values into (theta_j, S_j) classes forming the partition sum_j Pi_j = I.
- `eq_2`: implemented; build_circuit loop over _group_phases (comment 'eq_2'). Applies the commuting factors exp(i theta_j Pi_j) sequentially; factors with theta_j = 0 are the identity and skipped.
- `eq_3`: implemented; _apply_indicator and the qc.p call in build_circuit. O_j is a minterm network of X-conjugated multi-controlled-X gates XORing f_j(x) into the ancilla; P(theta_j) is applied on the ancilla; O_j is reapplied as its own inverse.
- `eq_4`: out_of_scope; no code location. No Clifford+T Rz synthesis is performed; the exact phase gate P(theta_j) stands in for the approximant tilde P_j. Only the module's docstring records this substitution.
- `eq_5`: background; no code location. epsilon is validated to lie in (0,1) but, because rotations are exact, no per-rotation budget epsilon/k is consumed; the bound is informational.
- `eq_6`: background; no code location. Headline T-count bound is a resource statement about the synthesized circuit; it is not an operation and E(n,k) is not reconstructable from the abstract.
- `eq_7`: implemented; example_instance_json consumed by build_circuit. n=2, phases [0,0,0,pi/5] yields one class S_2={11} with f_2 = x1 AND x0 realised by ccx, one P(pi/5), and the ccx uncompute.

## Specification changes

- eq_4, eq_5: The Clifford+T approximation tilde P_j of each phase gate is replaced by the exact Qiskit phase gate qc.p(theta_j); the epsilon parameter is validated but not used for synthesis. Reason: Clifford+T Rz synthesis (e.g. number-theoretic gridsynth) cannot be implemented with the allowed imports in a compact module; the exact gate preserves the construction's meaning (the circuit equals D (x) I exactly rather than to precision epsilon).
- eq_2: No phase is dropped as a global phase; every distinct nonzero phase class gets its own indicator+rotation stage, so between k-1 and k rotations are applied. Reason: Keeps the returned operation exactly equal to D (x) I (not merely equal up to a global phase), avoiding ambiguity for downstream validation.
- eq_3: The indicator network O_j is a naive disjoint-minterm ESOP (one n-controlled X per element of S_j, X-conjugated for zero bits), with the constant-1 indicator special-cased to a single X on the ancilla. Reason: The paper's optimized predicate circuitry and entanglement-cost function E(n,k) are unknown; the minterm network is exact for arbitrary S_j but is not T-count optimal and is only a surrogate for E(n,k).
