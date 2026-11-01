# Equation to Qiskit

Unitary, measurement-free Qiskit implementation of the modified Tulsi-type search iterate with a single search-qubit register S (n qubits) and one control qubit C. Each iteration applies the oracle phase flip on marked item w controlled on C=1, then Ry(theta) on C, then Grover diffusion on S. Every tau iterations the Z-basis control measurement is realised by the deferred-measurement principle, a CNOT from C onto a fresh record qubit. Tracing out the record qubits gives the outcome-averaged dephased state of eq_3, and no reset is applied. The runner prepares the input state, so there is no H layer or measurement in the circuit.

Source equation run: `e2a5f85f-aff5-4cc6-9254-7f21c8b8a094`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: search register S, little-endian (qubit i holds bit i of x)
- qubit n: control qubit C
- qubits n+1..n+floor(k/tau): record qubits, one per control measurement in time order (CNOT copy of C in Z basis); absent if tau is null
- Example (n=3,w=5,tau=2,k=6): S=q0,q1,q2; C=q3; records=q4,q5,q6 (7 qubits)

## Assumptions

- Single marked item w
- Oracle is a phase flip on w controlled on C=1
- Gate order within an iteration is oracle, Ry(theta) on C, then diffusion
- theta is a free user-supplied real parameter
- The Ry(theta) angle convention is Qiskit's, Ry(theta)=exp(-i theta Y/2)
- Records are never reset, and the measurement count is floor(k/tau)
- n is capped at 10, k at 1000, and total qubits (n+1+floor(k/tau)) at 12

## Unresolved issues

- Exact Tulsi operators and the paper's standard and alternative angular parameter are not specified
- Cumulative Correlation Measure definition is missing
- Tested tau values and k ranges are not specified
- The paper's treatment of measurement outcomes (reset or kept) is unknown; no reset is assumed here
- Many measurement events with large k exceed the 12-qubit cap, which limits tau and k combinations

## Equation mapping

- `eq_1`: background; no code location. Initial state |s>|+> is prepared by the runner; the operation contains no state preparation. Qubit order convention is described in register_layout.
- `eq_2`: implemented; build_circuit loop body: _oracle (controlled phase oracle), qc.ry on control, _diffusion. G_theta = D (Ry(theta) Lambda_C(O_w)): oracle first, then Ry on the control, then diffusion on S. The global phase pi in _diffusion makes the diffusion exactly 2|s><s|-I.
- `eq_3`: implemented; build_circuit: qc.cx(ctrl, n + 1 + rec) when j % tau == 0. Dephasing of the control every tau iterations is implemented unitarily as a CNOT onto a fresh record qubit (deferred measurement). Tracing out the records gives the outcome-averaged state of eq_3; no reset is applied.
- `eq_4`: background; no code location. Success probability is a post-processing quantity computed by the runner on S; it is not part of the operation.
- `eq_5`: background; no code location. Mutual information is computed from reduced states by software after generation; not part of the circuit.
- `eq_6`: out_of_scope; no code location. Scaling fit of k* over n=3..8 needs many circuits and classical post-processing; only a single circuit builder is implemented.

## Specification changes

- eq_3: Mid-circuit measurement replaced by a CNOT from C to a fresh record qubit per measurement event, with no reset, no classical bits and no dynamic circuits. Reason: The circuit must be unitary and measurement-free; deferred measurement reproduces the outcome-averaged dephased reduced state on S and C when the records are traced out.
- eq_1: Input state preparation (H on S, |+> on C) is omitted from the circuit. Reason: The runner prepares inputs and the operation must not include state preparation.
- eq_2: The Grover diffusion is built as H X mcz X H with an explicit global phase of pi so that it equals 2|s><s|-I exactly. Reason: The sign convention of the diffusion is fixed to match eq_2.
- eq_3, eq_6: tau = infinity is represented by tau = null, which adds no records. Reason: JSON has no infinity value.
- eq_2, eq_3, eq_4, eq_5, eq_6: Scope narrowed to one circuit (fixed n, w, theta, tau, k) for the proposed stand-in iterate rather than Tulsi's exact construction. Mutual information, CCM and the order fit are not implemented. Reason: The exact Tulsi operators, the paper's theta choice and the CCM definition are not given in the specification.
