# Equation to Qiskit

Qiskit module implementing t steps of the Szegedy-type unitary quantum walk U = S R_A (eq_3) built from the Kraus isometry A (eq_2) of a finite-graph open quantum walk. The Kraus operators are restricted to the explicitly synthesisable family B_i^j = sqrt(p_ij) V_i^j with V_i^j a tensor product of single-qubit gates from {I,X,Y,Z,H,S,T}; the Kraus/trace-preservation constraint of eq_1 (sum_i p_ij = 1) is validated. The isometry is realised as a controlled Stinespring dilation U_A (controlled amplitude tree of RY rotations on node2 plus doubly-controlled internal gates), the reflection R_A = U_A (I x I x (2|0><0|-I)) U_A^dagger is built by uncompute/reflect/recompute, and S is a qubit-wise swap of the two node registers. The example instance is the 2-node, one-internal-qubit OQW of eq_6 (3 qubits). Probabilities and mean probabilities (eq_4, eq_5) are measurement/post-processing and are out of scope for the returned operation.

Source equation run: `de0d57fa-4b1d-4f15-82e9-c6027d3582dc`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: internal[0] - internal (coin-like) qubit of the OQW, d=2; Kraus unitaries V_i^j act here
- qubit 1: node1[0] - source/current node register j (|0>=node 0, |1>=node 1)
- qubit 2: node2[0] - destination node register i, the register whose computational-basis measurement defines p_t(i) in eq_4 (not included in the circuit)
- Tensor order internal x node1 x node2; qubit 0 is least significant. For general instances: internal = qubits 0..m-1, node1 = m..m+nb-1, node2 = m+nb..m+2nb-1 with nb = ceil(log2 nodes), little-endian within each register; total m+2nb <= 12.
- kraus[j][i] encodes B_i^j = sqrt(prob) * unitary; the example is eq_6: B_0^0=I/sqrt2, B_1^0=X/sqrt2, B_0^1=H/sqrt2, B_1^1=I/sqrt2.

## Assumptions

- Node labels are encoded in binary in each node register (little-endian), node count n need not be a power of two; unused basis states of node1 are acted on trivially by U_A, which keeps every circuit element unitary.
- The Kraus constraint tolerance is 1e-6 on sum_i p_ij; probabilities are clipped to [0,1] within 1e-9.
- Internal space dimension d = 2**m with m >= 1; the classical (d=1) Szegedy case is not exposed.
- ctrl_state integers follow Qiskit's convention that bit k of ctrl_state refers to the k-th qubit in the control list (node1 bits first, then the relevant node2 bits).

## Unresolved issues

- The paper's actual unitary construction (register layout, one- vs two-reflection step, which register defines the node position) is not available; the implemented U = S R_A is the reconstruction from the Szegedy analogy.
- General Kraus operators outside the scaled single-qubit-gate tensor-product family are not supported.
- Probability, mean probability and asymptotic mean probability (eq_4, eq_5) must be evaluated by the runner via measurement of node2 and classical post-processing.

## Equation mapping

- `eq_1`: background; _parse (Kraus constraint check sum_i p_ij = 1). The OQW map itself is not implemented; only its node-wise Kraus (trace-preservation) constraint is validated, which for the restricted family B_i^j = sqrt(p_ij) V_i^j reduces to sum_i p_ij = 1.
- `eq_2`: implemented; _append_dilation. Controlled Stinespring dilation U_A with U_A|xi>|j>|0> = sum_i (B_i^j|xi>)|j>|i> = A(|xi>|j>): controlled RY amplitude tree prepares sqrt(p_ij) on node2, then V_i^j is applied to internal controlled on node1=j, node2=i.
- `eq_3`: implemented; build_circuit (step loop) and _append_zero_reflection. R_A = U_A (I x I x (2|0><0|-I)) U_A^dagger built as compose(U_A^dagger), exact zero-reflection on node2 (Z for one qubit, X-MCZ-X with global phase pi otherwise), compose(U_A); S realised as qubit-wise swaps of node1 and node2; repeated steps times to give U^t.
- `eq_4`: out_of_scope; no code location. Probability p_t(i) requires measuring node2 after U^t; measurements are excluded from the returned operation and left to the runner.
- `eq_5`: out_of_scope; no code location. Mean and asymptotic mean probability are classical post-processing / spectral analysis of the 8x8 unitary, not part of the circuit.
- `eq_6`: implemented; example_instance_json; optional prepend_isometry branch in build_circuit. The example instance encodes exactly the four Kraus operators of eq_6; with prepend_isometry=true the circuit maps the runner-prepared |0>|0>|0> to |Psi_0> = A(|0>|0>) = (|000>+|101>)/sqrt2 before the walk steps.

## Specification changes

- eq_1, eq_2: Kraus operators restricted to B_i^j = sqrt(p_ij) V_i^j with V_i^j a tensor product of single-qubit gates from {I,X,Y,Z,H,S,T} and p_ij a stochastic matrix column (sum_i p_ij = 1). Reason: A general isometry A would require opaque dense-unitary synthesis, which is disallowed; this family admits an explicit standard-gate Stinespring dilation and contains the eq_6 instance and classical Szegedy walks.
- eq_3: For nb > 1 node qubits the reflection 2|0><0| - I is realised as -(X^{(x)nb} MCZ X^{(x)nb}) with the sign absorbed into qc.global_phase (+pi per step); for nb = 1 it is exactly Z. Reason: Standard gates give I - 2|0><0|; the global phase keeps the circuit exactly equal to U = S R_A rather than up to a sign.
- eq_3: The elementary step is taken to be U = S R_A; the two-reflection form W = R_B R_A is obtained by setting steps to an even number. Reason: The paper's normalization of the unit step is unknown; U is the finer operation from which W = U^2 follows.
- eq_6: Input-state preparation of |Psi_0> is not part of the default operation; an optional boolean prepend_isometry applies U_A first so the runner may supply |xi_0>|j_0>|0> instead. Reason: The task requires an operation without input-state preparation; the isometry itself is a unitary operation on the walk space and is offered as an opt-in.
