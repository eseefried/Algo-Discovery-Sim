# Equation to Qiskit

Builds a measurement-free first-order randomized-Trotter circuit for fast-signal-assisted AQC on an EC3 instance. Each of N steps applies the driver H_B=-sum X_i with weight (1-s_k), the EC3 penalty H_P with weight s_k, and one supplied signal rotation xi_k*sigma_j. The signal sequence is passed in the instance, so the circuit is deterministic. The runner must prepare |+>^n.

Source equation run: `692ef7a4-3ad5-459d-b5a0-c1bf082dc679`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1 (n=3 in the example): qubit i encodes EC3 bit z_i = (1-Z_i)/2, with qubit 0 the least significant bit of the computational-basis index
- Expected runner input: |+>^n, the ground state of H_B=-sum X_i
- No ancilla qubits; no measurements

## Assumptions

- Driver H_B=-sum_i X_i, so the initial state is |+>^n, prepared by the runner
- Linear schedule with s_k=k/N and dt=T/N
- The EC3 clauses are chosen by the caller; the example uses the single clause (0,1,2)
- Signal operators are single-qubit Paulis X, Y or Z with caller-specified amplitude
- The Trotter order is first and the Hamiltonian is closed-system

## Unresolved issues

- The paper's actual signal form, statistics and randomized Trotter formula are unknown
- The specific EC3 instance and driver in the paper are unknown
- No decoherence or system-bath model is included, so the runtime-reduction claim cannot be tested with this circuit
- The Trotter error and the effect of the signals on the final ground-state overlap are not characterised in the module

## Equation mapping

- `eq_1`: implemented; build_circuit: driver RX(-2 dt (1-s_k)) layer and problem-phase layer weighted by s_k. The linear interpolation H(s)=(1-s)H_B+sH_P is exponentiated per step, with H_B=-sum X_i as an assumed driver and a linear schedule.
- `eq_2`: implemented; build_circuit: signal rotation at the end of each step. The fast-signal term is reduced to one Pauli term xi_k*sigma_j per step, with all values supplied through instance['signals']. It is a placeholder form.
- `eq_3`: implemented; build_circuit: loop over k=1..N with s_k=k/N and dt=T/N. Generic first-order randomized product step. The split terms (driver, problem, signal) are applied sequentially in each step, and the sampling of xi_k and j_k is delegated to the caller.
- `eq_4`: background; no code location. The adiabatic condition is a runtime criterion. It is not an operation, and the code does not check it.
- `eq_5`: implemented; build_circuit: clause loop using rz and rzz. Each clause penalty (z_a+z_b+z_c-1)^2 is expanded as 1 - (Za+Zb+Zc)/2 + (ZaZb+ZaZc+ZbZc)/2 and exponentiated with RZ and RZZ gates. The constant 1 is dropped as a global phase.

## Specification changes

- eq_2, eq_3: The signal sequence is a deterministic instance input, one single-qubit Pauli rotation per step, instead of randomness sampled inside the module. Reason: The abstract does not give the signal distribution, and the module must return a bound, deterministic, unitary circuit without hidden randomness.
- eq_3: The exponential of the sum H(s_k)+xi_k*sigma_j is replaced by a first-order sequential split, with driver, problem and signal factors applied one after another in each step. Reason: This is the simplest standard product formula. The paper's randomized Trotter formula is unknown.
- eq_1, eq_5: The driver is fixed to H_B=-sum X_i, the schedule is linear, and a concrete clause list is required as input. The constant term of each clause penalty is dropped (global phase). Reason: The abstract does not specify these choices, and they are the smallest self-consistent assumptions.
- eq_4: The adiabatic condition is background only and is not enforced by the circuit. Reason: It is a diagnostic inequality, not a gate sequence.
- eq_1, eq_2, eq_3, eq_4, eq_5: The scope is narrowed to a unitary closed-system circuit with n between 3 and 12. Open-system decoherence, the paper's specific signals, the trapped-ion implementation and the runtime-reduction analysis are not implemented. The spec's 'q_1 most significant' convention is replaced by clause index i mapping directly to Qiskit qubit i. Reason: These details are missing from the abstract. Clause indices are 0-based.
