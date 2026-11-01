# Equation to Qiskit

Amplitude-estimation unitary for the mean of an explicit table f:{0..N-1}->[0,1]. The oracle is compiled into multi-controlled RY gates, A = H^n then U_f, and Q = -A S0 A^dagger S_chi. Controlled-Q^(2^j) is controlled by phase qubit j, followed by an inverse QFTGate on the phase register. The circuit has no input preparation and no measurement. The paper's novel, Aharonov-variant and median algorithms are not implemented.

Source equation run: `b37933ec-0d59-457a-8a54-96fefab7bc00`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..t-1: phase register, little-endian (qubit j has weight 2^j and controls Q^(2^j)); t=3 in the example gives qubits 0,1,2
- qubits t..t+n-1: idx register, little-endian x (bit i of x on qubit t+i); example qubits 3,4
- qubit t+n: ancilla flag (ancilla=1 is the good subspace); example qubit 5
- total qubits = t+n+1 <= 12; example uses 6

## Assumptions

- Standard amplitude estimation is the chosen construction. It does not implement the paper's own algorithms.
- f is an explicit table compiled into gates, so the circuit is not black-box.
- The phase register is little-endian and matches QFTGate's convention, so QFTGate(t).inverse() on qubits 0..t-1 decodes correctly.
- Multi-controlled RY and controlled composite gates are left to Qiskit's standard synthesis.

## Unresolved issues

- The paper's asymptotically optimal mean-estimation algorithm, the Aharonov variant and the median algorithm are not specified in the abstract and are not implemented.
- No query complexity is certified because the oracle is compiled from an explicit table.
- The circuit has not been simulated or verified; software checks follow generation.

## Equation mapping

- `eq_1`: implemented; _state_prep. For each x the ancilla gets a multi-controlled RY(2*asin(sqrt(f(x)))). X gates select idx=x. Angle-zero entries are skipped.
- `eq_2`: implemented; _state_prep (H on idx plus U_f) and its use in build_circuit. The A circuit prepares the uniform superposition with amplitude flags. Its ancilla=1 probability is the mean of f, but this is not checked in the circuit.
- `eq_3`: implemented; _grover_gate and the z(0) sign correction in build_circuit. Q' = A S0 A^dagger S_chi, with S_chi=Z on the ancilla and S0 built as X-layer, multi-controlled Z, X-layer. The global -1 is applied as Z on the phase control qubit for the j=0 controlled power, and cancels for the even powers at j>=1.
- `eq_4`: implemented; build_circuit. H on the phase qubits, A on the system, controlled-Q^(2^j) with j as the control, and QFTGate(t).inverse() on the phase qubits in little-endian order.
- `eq_5`: out_of_scope; no code location. Measurement, decoding a_hat = sin^2(pi*y/2^t) and the error bound are classical post-processing outside the unitary.

## Specification changes

- eq_3, eq_4: The global sign -1 of Q is implemented as a Z gate on phase qubit 0, after the single controlled-Q' application for j=0. It is not implemented as a global phase inside the gate. Reason: A global phase becomes a relative phase once Q is controlled. Q' is controlled directly and the sign is restored exactly on the control. The sign cancels for even powers.
- eq_1, eq_2, eq_4: The instance is parameterised by f_values (any power-of-two length >=2, entries in [0,1]) and t. The qubit order in the circuit is phase, idx, ancilla with phase on the lowest indices. Total qubits are capped at 12. Reason: The spec's tiny N=4, t=3 case was only an assumed example. The generalisation follows the same construction and obeys the qubit cap.
- eq_5: Decoding and error analysis are excluded from the circuit. Reason: The task requires a measurement-free unitary operation.
