# Equation to Qiskit

Small-RBM Gibbs-amplitude encoding: Hadamards on visible and hidden qubits, then for every configuration (v,h) a multi-controlled RY on one ancilla that gives the ancilla-|1> branch amplitude proportional to exp(-E(v,h)/2). After post-selecting ancilla=1, the vis/hid registers hold probabilities P(v,h)=exp(-E)/Z. Energies are computed classically from the instance parameters, and the energy shift is the minimum energy.

Source equation run: `e09a825c-1ef5-44dc-9296-4e43776876b8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n-1: vis register (v_i = qubit i)
- qubit n..n+m-1: hid register (h_j = qubit n+j)
- qubit n+m: ancilla (post-select |1> for Gibbs-weighted amplitudes)
- Example (n=2,m=1): q0=v0, q1=v1, q2=h0, q3=ancilla

## Assumptions

- The Hadamards that make the uniform superposition are part of the operation and act on a runner-prepared |0...0> state.
- Bit i of the visible register is v_i (qubit i), and bit j of the hidden register is h_j (qubit n+j).
- Post-selection on ancilla=1 and sampling are done outside the circuit.
- The construction is an assumed generic Gibbs-amplitude sketch, not the paper's algorithm.

## Unresolved issues

- The abstract does not give the paper's actual quantum training algorithm, circuits or ancilla count.
- Full Boltzmann machines and deep multi-layer models are not implemented. Only a single-layer visible-hidden energy is encoded.
- The post-selection success probability is not amplified.

## Equation mapping

- `eq_1`: implemented; _energy. The RBM energy is evaluated classically for each basis configuration (v,h) and used to set the rotation angles.
- `eq_2`: implemented; build_circuit: loop over k with multi-controlled RYGate. The ancilla rotation sets the |1> amplitude to exp(-(E-Emin)/2), so post-selected probabilities are exp(-E)/Z. Z is the normalization implied by the post-selection and is not computed in the circuit.
- `eq_3`: out_of_scope; no code location. The likelihood gradient needs sampling, data averages and classical post-processing. The circuit has no measurement and no gradient step.

## Specification changes

- eq_2: The ancilla amplitude uses a shift by the minimum energy, exp(-(E-Emin)/2), instead of exp(-E/2). Reason: The rotation amplitude must be at most 1. The shift is a constant factor, so it only changes the ancilla-|1> success probability and leaves the post-selected distribution unchanged.
- eq_1, eq_2: The scope is narrowed to a small RBM with n_visible + n_hidden <= 8 and one ancilla. Each configuration is encoded by an explicit multi-controlled RY, with 2^(n+m) of them. Reason: The abstract gives no efficient quantum algorithm. The qubit cap is 12, and the circuit size grows exponentially with n+m.
- eq_3: The gradient estimation is excluded. Reason: It is a classical post-processing step on measured samples, and the operation must not contain measurements.
