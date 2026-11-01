# Equation to Qiskit

build_circuit(instance) returns the random-phase diagonal gate U = sum_{jk} exp(i phi_jk)|j><j| (x) |k><k| on two n-qubit registers (A = qubits 0..n-1 holding j, B = qubits n..2n-1 holding k). The phases come from an explicit list or from a seed. U is synthesized exactly from standard gates by a Moebius (subset) transform of the phase table, which gives one phase or multi-controlled-phase gate per qubit subset plus a global phase. Hadamard input preparation, statevector reshaping, entropy and averaging are left to the runner.

Source equation run: `495e379e-fe93-4add-86f0-9937db72b209`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1: register A (index j, qubit 0 least significant)
- qubits 2-3: register B (index k, qubit 2 is least significant bit of k)
- basis index x = k*N + j; phase applied to |x> is phases[j*N+k] = phi_jk
- no ancillas for n=2 (2n qubits in general, n<=6)

## Assumptions

- Phases are real numbers in radians; uniform sampling on [0,2pi) is used only when a seed is given.
- Register A holds j on qubits 0..n-1 and register B holds k on qubits n..2n-1.
- The global phase of U is included in the circuit's global_phase.
- Valid n is an integer from 1 to 6.

## Unresolved issues

- The proportionality between entangling power and S(rho) is not specified, so it is not used.
- Gate count grows as 2^(2n), and the n=6 case needs many high-order multi-controlled phase gates; this is acceptable only for small instances.

## Equation mapping

- `eq_1`: implemented; build_circuit (Moebius transform + p/mcp gates); _get_phases. The diagonal gate with unimodular entries exp(i phi_jk) is built exactly from a global phase, single-qubit phase gates and multi-controlled phase gates.
- `eq_2`: implemented; build_circuit (index mapping x = k*N + j; U layer only). Only the U part of U H^{2n}|0> is implemented, together with the A=low qubits, B=high qubits layout and the reshape index j*N+k. The Hadamard layer is input preparation and is supplied by the runner.
- `eq_3`: background; no code location. Property of the resulting state (rho_jj = 1/N for unimodular A), not a circuit element.
- `eq_4`: out_of_scope; no code location. Entropy from the SVD of the reshaped statevector is classical postprocessing, excluded from the operation.
- `eq_5`: out_of_scope; no code location. Purity is a classical check or a swap-test extension; not implemented.
- `eq_6`: out_of_scope; no code location. Monte Carlo averaging over phase draws is done outside the circuit, by the runner calling build_circuit with different phases or seeds.

## Specification changes

- eq_2: The Hadamard layer H^{2n}|0> is excluded from build_circuit; only the diagonal gate U is returned. Reason: The task requires an operation without input-state preparation; the runner prepares |+>^{2n}.
- eq_2, eq_4: Amplitude matrix index convention: with A on the low qubits, basis index is x = k*N + j. The code maps phases[j*N+k] to x = k*N + j, so M[j,k] = psi[k*N+j] corresponds to A_{jk}/N. Reason: Qiskit is little-endian, and the spec's reshape j*N+k would be wrong if applied directly to Qiskit basis indices.
- eq_1, eq_6: Phases are supplied via instance ('phases' list or integer 'seed') rather than sampled internally with hidden state; n is capped at 6. Reason: Makes the operation deterministic and reproducible per instance, and respects the 12-qubit cap.
- eq_3, eq_4, eq_5, eq_6: Scope narrowed to the gate construction. Entropy, purity, ensemble averaging, moments and Borel triangle claims are not implemented. Reason: They are classical postprocessing or analytic results, not part of a unitary operation.
