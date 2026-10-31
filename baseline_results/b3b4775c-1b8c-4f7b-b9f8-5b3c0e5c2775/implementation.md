# Equation to Qiskit

Qiskit module implementing the scoped construction: amplitude-estimation-based mean estimation of a black-box function F on N=2^n points. F is encoded as a basis-controlled RY rotation on one ancilla (U_F), A = U_F (H^n ⊗ I) prepares a state whose ancilla-1 probability equals the mean, Q' = A S_0 A† S_chi (= -Q) is built from standard gates, and m precision qubits run phase estimation (H, controlled Q^{2^k} with the -1 sign of Q realised as a Z on the control for the odd power, then inverse QFTGate). The returned circuit contains no measurement; measuring the precision register (little-endian integer y) and computing sin^2(pi*y/2^m) is the classical post-processing left to the runner.

Source equation run: `5cfce3bd-be4b-4c33-8932-d5eea3e5f132`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1: idx register (n=2), idx[k] = qubit k has weight 2^k in the index x (little-endian)
- qubit 2: anc, value ancilla; marked subspace is anc=|1>, Pr[anc=1] after A equals mu = 1/2
- qubits 3-5: prec register (m=3), prec[k] = qubit 3+k controls Q^(2^k) and holds bit of weight 2^k of y after the inverse QFT
- expected post-processing for the example: y in {2, 6} (theta = pi/4, M = 8), mu_tilde = sin^2(pi*y/8) = 1/2

## Assumptions

- The paper's novel algorithm is reconstructed only generically as BHMT amplitude estimation; the actual algorithm may differ.
- F is given explicitly as a table of 2^n real values in [0,1]; N is a power of two.
- The runner measures the precision register and computes sin^2(pi*y/2^m) with y read little-endian (qubit 3 = LSB in the example).
- Single-shot success probability >= 8/pi^2 without amplification; exact recovery for the example since M*theta/pi = 2 is an integer.
- Total qubits n + 1 + m <= 12 (e.g. n <= 8 with m = 3).

## Unresolved issues

- No mathematical description of the paper's actual optimal mean-estimation algorithm, the Aharonov-type variant, or the median-over-arbitrary-distance algorithm is available; these remain unimplemented.
- The controlled-RY oracle scales as 2^n multi-controlled gates, which is fine for the capped sizes but is not the query-efficient oracle model assumed by the complexity claim (eq_6).

## Equation mapping

- `eq_1`: background; _validate (enforces F(x) in [0,1] and |domain| = 2^n). Definition of the target quantity; only its normalisation assumptions are enforced in the code, the mean itself is realised implicitly through eq_3.
- `eq_2`: implemented; _oracle. U_F implemented as one RY(2*asin(sqrt(F(x)))) on the ancilla controlled on the index register being in basis state x (ctrl_state=x).
- `eq_3`: implemented; _prep_a and the first compose in build_circuit. A = U_F (H^n ⊗ I) applied to |0^n>|0>; ancilla-1 probability equals mu.
- `eq_4`: implemented; _grover_q_prime and the controlled-power loop in build_circuit. Q' = A S_0 A† S_chi built from Z, X, multi-controlled Z and A/A†; the overall minus sign of Q = -Q' is realised exactly as a Z gate on the control qubit of the odd power Q^(2^0).
- `eq_5`: implemented; build_circuit (H on prec, controlled Q^(2^k), QFTGate(m).inverse()). The quantum part of amplitude estimation is implemented; the measurement of y and the classical map mu_tilde = sin^2(pi y / M) are left to the runner as documented in the module docstring. The probabilistic error bound is a theorem, not code.
- `eq_6`: background; no code location. Query-complexity statement O(1/epsilon); the circuit uses 2^m - 1 controlled applications of Q (each with one U_F and one U_F†), consistent with M = 2^m, but no complexity analysis is implemented.

## Specification changes

- eq_5: Integer encoding of the precision register changed from the specification's big-endian convention to Qiskit little-endian: prec[k] (qubit 3+k in the example) controls Q^(2^k) and holds the bit of weight 2^k of y; QFTGate(m).inverse() is applied on [prec[0],...,prec[m-1]] in that order. Reason: QFTGate in Qiskit treats qubit index 0 as the least significant bit; using the big-endian ordering of the specification literally would require extra swaps.
- eq_4: Q is not built as a single gate with global phase pi; instead Q' = A S_0 A† S_chi (= -Q) is built and the sign (-1)^(2^k) is applied explicitly as a Z gate on the control qubit prec[0] for the odd power k=0 (even powers carry no sign). Reason: A global phase of Q becomes a relative phase under control and would shift the estimated phase by 1/2, yielding 1-mu instead of mu; realising it as a Z on the control makes the sign exact and independent of how Qiskit handles global phases under .control().
- eq_5, eq_6: Measurement of the precision register, the classical map mu_tilde = sin^2(pi y/M), and any repetition/median amplification are excluded from the returned circuit. Reason: The deliverable is a measurement-free unitary operation; post-processing is documented for the runner.
- eq_2: U_F is realised by explicit basis-state-controlled RY rotations (one multi-controlled gate per x with F(x) > 0), i.e. the black box is instantiated from the supplied value table rather than treated as an abstract oracle. Reason: A concrete circuit requires a concrete oracle; the instance supplies F as a list of 2^n values in [0,1].
