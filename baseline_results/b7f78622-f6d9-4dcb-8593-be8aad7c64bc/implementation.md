# Equation to Qiskit

Qiskit implementation of the 3-step trine-POVM quantum walk (eq_2-eq_4): one coin (polarisation) qubit plus a binary-encoded position register (default 2 qubits, positions x = 0..3). Each step applies position-controlled coin unitaries (RY(2*arccos(sqrt(2/3))) at x=0 and X at x=1 in step 2; H at x=1 in step 3) followed by the polarisation-dependent shift S that increments the position register (mod 2^n) when the coin is |V>=|1>. The returned circuit is the Naimark dilation unitary U3 U2 U1 of eq_3; reading out the position register (by the runner) realises the trine POVM E_k = (2/3)|psi_k><psi_k|. An optional trine_phase parameter rotates the trine plane about the Bloch z-axis via a phase gate on the coin before the walk.

Source equation run: `08660780-fdd4-49a1-b030-172647946c6e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin / polarisation qubit (|0> = |H>, |1> = |V>); holds the input state to be measured
- qubit 1: position bit x_0 (least significant), qubit 2: position bit x_1; position x = x_0 + 2*x_1, must be prepared in |0> (walker at x = 0)
- Total qubits for the example: 3. Outcome label = final value x of the position register (0, 1 or 2); x = 3 is never populated for an input with x = 0.
- For num_position_qubits = n, qubits 1..n form the position register (little-endian) and the shift increments mod 2^n.

## Assumptions

- Coin qubit 0 encodes |H> = |0>, |V> = |1>; coin matrices of eq_4 are in the ordered basis (|H>, |V>) and RY(theta) = [[cos(theta/2), -sin(theta/2)], [sin(theta/2), cos(theta/2)]] matches C2_0 for theta = 2 arccos(sqrt(2/3)).
- Position register is little-endian (qubit 1 = x_0); ctrl_state integers in _site_coin follow Qiskit's little-endian convention over the control list, so ctrl_state = x selects position |x>.
- The runner prepares the position register in |0...0>; outcomes are read from the position register only (coin traced out), as in eq_3.
- Ideal, noiseless gates; no optical loss or interferometric phase errors are modelled.
- Coins at unoccupied positions are identity and omitted from the circuit.

## Unresolved issues

- The coin schedule (eq_4) is a proposed construction consistent with the abstract, not the paper's actual wave-plate settings or walk layout.
- The SIC-POVM and unambiguous-discrimination constructions named in the abstract are not implemented (scope narrowed to the trine POVM).
- Correctness (E_x = (2/3)|psi_x><psi_x| for x = 0,1,2) follows from the algebra in eq_5 but has not been numerically verified here; validation software should check it.

## Equation mapping

- `eq_1`: background; no code location. Defines the target trine POVM; it is realised indirectly as the induced POVM of the walk (eq_3) under the coin schedule (eq_4) and is not coded directly.
- `eq_2`: implemented; _shift (conditional increment = S) and _site_coin (position-controlled coin C_x^(t)) in source_python. One walk step = position-dependent coins followed by the V-conditioned translation; the translation is a controlled incrementer on the binary position register (mod 2^n).
- `eq_3`: implemented; build_circuit (whole circuit = U_3 U_2 U_1; see closing comment). The circuit is the Naimark dilation unitary; the position-basis readout and the resulting Kraus/POVM elements arise when the runner prepares x = 0 and measures the position register.
- `eq_4`: implemented; build_circuit: theta/c2_0/c2_1/c3_1 definitions and the three step blocks. C2_0 is RY(2 arccos sqrt(2/3)), C2_1 is X at x=1, C3_1 is H at x=1; identity coins are omitted.
- `eq_5`: background; no code location. Algebraic consequence of eq_2-eq_4; not coded. Note the sign of K_2 in the specification is a global phase and the correct expression is K_2 = +sqrt(2/3)|V><psi_2| (see specification_changes).
- `eq_6`: background; no code location. Born-rule outcome statistics used for post-processing; outside the operation returned by build_circuit.

## Specification changes

- eq_2: The shift S is implemented on a finite binary position register of n >= 2 qubits as a V-conditioned increment modulo 2^n (positions 0..2^n-1) instead of an isometry on the infinite line. Reason: A unitary circuit on a finite register is required; since the walker starts at x = 0 and only reaches x <= 2 in three steps, the wrap-around is never populated and the induced POVM is unchanged.
- eq_5: K_2 = +sqrt(2/3)|V><psi_2| (no minus sign): direct evaluation of the step-3 Hadamard output at x=1 gives amplitude (beta - alpha/sqrt3)/sqrt2 = sqrt(2/3) <psi_2|psi> with psi_2 = (-1/2, sqrt3/2). Reason: Minor sign correction; it is a global phase of the Kraus operator and leaves E_2 = K_2^dag K_2 = (2/3)|psi_2><psi_2| unchanged.
- eq_1, eq_3: Added an optional instance parameter trine_phase phi: a phase gate P(-phi) on the coin before the walk, so the implemented POVM is E'_k = W E_k W^dag with W = diag(1, e^{i phi}) (trine plane rotated about the Bloch z-axis). Default phi = 0 reproduces the x-z plane trine of eq_1 exactly. Reason: Provides a family of valid instances as required, while preserving the specification's default construction.
- eq_3: Input-state preparation (coin in |psi>, position in |0>) and the position-basis measurement are not part of the returned circuit. Reason: The deliverable is the dilation operation only; preparation and readout are performed by the runner.
