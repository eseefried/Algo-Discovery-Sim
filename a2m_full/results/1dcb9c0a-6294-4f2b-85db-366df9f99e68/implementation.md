# Equation to Qiskit

Implements the unitary core of the truncated-Fock phase-encoding and readout-rotation model (eq_2 and the basis-rotation part of eq_3): the diagonal phase shift exp(-i*phi*n) as P(-2^j*phi) gates on little-endian qubit j, followed optionally by H on every Fock qubit. Squeezed-state preparation, measurement, ML phase estimation, Kalman/RTS smoothing and minimax design are not part of the circuit.

Source equation run: `d9dd0bd6-6f5b-41dd-9531-dfc8a57a8ce9`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n_qubits-1: Fock register 'fock', little-endian: qubit j is bit j of photon number n = sum_j 2^j b_j
- Example (n_qubits=3): qubit 0 = LSB (weight 1), qubit 1 = weight 2, qubit 2 = weight 4
- No classical bits; no measurements in the circuit

## Assumptions

- Register is little-endian: qubit j carries weight 2^j in Fock number n.
- Phase phi is in radians and is applied as exp(-i*phi*n) with the sign convention of eq_2.
- The runner supplies the truncated squeezed-state input and performs any measurement.

## Unresolved issues

- The paper's actual robust smoother, its uncertainty model and the continuous-mode homodyne model are not reconstructed.
- Squeezing parameter xi and the readout noise r are not used by the circuit.
- Phase periodicity (2π ambiguity) is not addressed.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Classical random-walk generation of the hidden phase trajectory with uncertain q; the circuit takes a single phi as an input parameter.
- `eq_2`: implemented; build_circuit: loop applying qc.p(-(2**j)*phi) on qubit j. The diagonal phase shift exp(-i*phi*n) is implemented exactly with P gates. The squeezed-vacuum amplitudes c_n are not prepared because the runner supplies the input state.
- `eq_3`: implemented; build_circuit: Hadamard loop under apply_readout_rotation. Only the H^{⊗n} basis rotation is implemented. Measurement, outcome statistics and ML phase estimation are left to the runner or classical postprocessing.
- `eq_4`: out_of_scope; no code location. Classical scalar Kalman filter; not a quantum circuit operation.
- `eq_5`: out_of_scope; no code location. Classical RTS fixed-interval smoother; not a quantum circuit operation.
- `eq_6`: out_of_scope; no code location. Classical minimax grid search for the robust design noise q_r.

## Specification changes

- eq_2: Squeezed-vacuum state preparation (RY ladder) is omitted from the circuit. The circuit contains only the phase-encoding unitary. Reason: The task requires an operation without input-state preparation; the runner prepares inputs.
- eq_3: Measurement is omitted. Only H on all Fock qubits is applied, and it can be disabled with apply_readout_rotation=false. Reason: The circuit must be measurement-free and unitary.
- eq_2, eq_3: The register size is generalized from a fixed 3 qubits to n_qubits in 1..12, and a single phi is a parameter of the instance. Reason: The operation must work for varying valid instance parameters, with a cap of 12 qubits.
- eq_1, eq_4, eq_5, eq_6: The classical smoothing and robust-design pipeline is excluded from the implemented scope. Reason: These equations have no circuit realization. Only one quantum construction is implemented.
