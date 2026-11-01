# Equation to Qiskit

Reset-free, measurement-free Qiskit circuit for a second-order Trotterized single-qubit Lindblad semigroup exp(tL), with L = Hamiltonian (omega X/2) + pure dephasing (gamma) + amplitude damping (Gamma). The system is qubit 0. Each non-unitary factor uses its own fresh |0> ancilla, since reset is not allowed. The ancillas are left entangled, and the runner takes the partial trace over them. Narrowed scope: r is at most 5 because of the 12-qubit cap.

Source equation run: `eab3df43-4bc9-460f-b811-669405554bb8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system qubit (holds rho; input prepared by runner)
- qubits 1,3,5,...,2r-1: dephasing dilation ancillas for segments 0..r-1, each starting in |0>
- qubits 2,4,6,...,2r: amplitude-damping dilation ancillas for segments 0..r-1, each starting in |0>
- total qubits = 1 + 2r <= 12; output = reduced state of qubit 0 after tracing out all ancillas; Qiskit little-endian indexing

## Assumptions

- The input state on qubit 0 and |0> on all ancillas are prepared by the runner.
- Evaluation traces out ancilla qubits 1..2r and compares the system state with exp(tL) rho.
- The Lindblad convention is: dephasing multiplies rho01 by e^{-gamma t}, damping uses p = 1-e^{-Gamma t}, and the Hamiltonian is H = omega X/2.
- t, omega, gamma and Gamma are finite and nonnegative.

## Unresolved issues

- Only r <= 5 is reachable under the 12-qubit cap.
- Gate-count scaling O((||L|| t)^{3/2}/eps^{1/2}) is not demonstrated, since the paper's synthesis method is not reconstructed.
- Whether the paper's decomposition matches this one is unknown.

## Equation mapping

- `eq_1`: implemented; build_circuit (generator split into H = omega X/2, dephasing, amplitude damping; one qubit-0 operation per piece). The target is T_t = exp(tL) with L = L_H + L_deph + L_damp. The instance fixes this three-piece decomposition.
- `eq_2`: implemented; build_circuit (gate loop: rx half-step, then per-segment dephase + damp, rx full step between segments, rx half-step at the end). Symmetric second-order product formula with r segments, with exact merging of adjacent identical or commuting factors.
- `eq_3`: background; no code location. The error scaling and the choice of r from epsilon are not computed in the circuit. r is supplied directly in the instance, and epsilon is not an input.
- `eq_4`: implemented; _dephase and _damp (Stinespring dilation with one fresh |0> ancilla per non-unitary factor). Each Kraus-rank-2 channel is realized as a unitary on system plus ancilla. The ancilla is not reset and stays entangled, which implements the partial trace.
- `eq_5`: implemented; _dephase (RY + CZ), _damp (CRY + CNOT), build_circuit (rx for the Hamiltonian piece). Dephasing is a Z-mixture with probability q=(1-e^{-gamma s})/2. Amplitude damping uses p=1-e^{-Gamma s} with phi=2 asin sqrt(p). The Hamiltonian is exp(-i omega s X/2) = rx(omega s), with the X axis chosen so it does not commute with the dissipators.

## Specification changes

- eq_4: No ancilla reset between factors. Each dephasing or damping factor gets its own fresh ancilla qubit, giving 1+2r qubits in total. Reason: The task forbids reset and dynamic circuits. A single reused ancilla is not possible in a measurement-free unitary circuit.
- eq_2, eq_5: The three pieces are ordered H, D, A. The symmetric product is merged exactly: A(s/2)A(s/2)=A(s), D and A commute so D(s/2)A(s)D(s/2)=D(s)A(s), and neighbouring H(s/2) factors combine into H(s). D and A are still implemented as two separate rank-2 channels. Reason: This reduces the number of ancillas. The merged form is mathematically identical to the specified second-order product.
- eq_1, eq_5: The Hamiltonian is fixed as omega X/2 and the dephasing is a Z-type channel with rate gamma on the coherence. Rates are nonnegative reals. Reason: The specification left the axis open. A Hamiltonian that does not commute with Z gives a nontrivial Trotter structure.
- eq_3: The segment count r is an integer instance parameter limited to 1..5, and epsilon is not used. Reason: The 12-qubit cap with 2 ancillas per segment limits r. The error-to-r formula has unspecified constants.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to one exact-dilation, second-order Trotter instance. The paper's own decomposition/recombination technique and general channel approximation are not implemented. Reason: These details are not available in the supplied abstract or specification.
