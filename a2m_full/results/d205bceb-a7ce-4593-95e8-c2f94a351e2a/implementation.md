# Equation to Qiskit

Builds a measurement-free, Trotterized time-evolution unitary exp(-iHt) for a 1D open-boundary transverse-field Ising chain, H = sum J_j Z_j Z_{j+1} + sum h_j X_j, on a patch of 2 to 8 qubits. It uses RZZ(2 J dt) and RX(2 h dt) layers with first- or second-order Trotter splitting. An optional final Hadamard on the measured qubit rotates it for an X-basis readout. The runner supplies |+>^m and does the measurement; the classical Bayesian machinery is not implemented.

Source equation run: `f21006f5-d994-48a1-9e62-0220c95b0917`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: chain sites 0..n-1 of the patch (qubit index = site index, open boundaries)
- Input expected from runner: |+>^n (not prepared in the circuit)
- Measured qubit q (0-indexed) is read out in the computational basis by the runner; if basis is 'X', a final H on qubit q is included

## Assumptions

- Chain sites are mapped to qubits in order, with site j on qubit j.
- The patch is already chosen, so n is given directly (2 to 8).
- Evolution time t and Trotter step count are supplied per instance.
- The runner prepares |+>^n and performs any measurement.

## Unresolved issues

- The form of the epistemic Lieb-Robinson velocity v(sigma) and the margin are unspecified, so patch selection is not implemented.
- The Trotter error is not controlled automatically; the user must choose steps and order.
- Prior distribution, particle count and experiment design heuristic are unspecified, and the classical SMC loop is not part of this circuit.

## Equation mapping

- `eq_1`: implemented; _zz_layer and _x_layer, used in build_circuit. Trotterized exp(-iHt) for H = sum J_j Z_j Z_{j+1} + sum h_j X_j with open boundaries, using RZZ(2 J dt) and RX(2 h dt).
- `eq_2`: out_of_scope; no code location. Light-cone radius and patch extraction depend on the unspecified v(sigma) and margin and on classical posterior statistics. The patch size n is supplied directly, capped at 8.
- `eq_3`: implemented; build_circuit (evolution layers plus optional H on qubit q for the X basis). Only the unitary e^{-iHt} and the basis rotation are implemented. The |+>^m initial state, projective measurement and probability evaluation are left to the runner. The evolution is Trotterized, not exact.
- `eq_4`: out_of_scope; no code location. Classical Bayesian weight update; no quantum operation.
- `eq_5`: out_of_scope; no code location. Classical Liu-West resampling; no quantum operation.
- `eq_6`: out_of_scope; no code location. Classical expected-information-gain experiment selection; no quantum operation.

## Specification changes

- eq_1, eq_3: Exact evolution replaced by first- or second-order Trotter-Suzuki product formula with a user-chosen step count. Reason: A standard-gate circuit can only implement a product-formula approximation of e^{-iHt}; the specification allowed either exact or Trotter evolution.
- eq_3: The circuit omits the |+>^m preparation (H gates), the projector and the measurement. It includes only the evolution and an optional H on qubit q for X-basis readout. Reason: The task requires an operation without state preparation or measurement; the runner prepares inputs.
- eq_2, eq_4, eq_5, eq_6: Scope narrowed to a single-particle (single-theta) likelihood circuit on a patch of 2 to 8 qubits; all classical inference, resampling, experiment design and light-cone selection are excluded. Reason: These equations are classical or depend on unspecified functional forms and do not define a quantum circuit.
- eq_1: Sign and angle conventions fixed: RZZ(theta)=exp(-i theta/2 ZZ) and RX(theta)=exp(-i theta/2 X), hence theta=2J dt and 2h dt give exp(-i dt H). Reason: The specification left the Qiskit sign conventions to be checked.
