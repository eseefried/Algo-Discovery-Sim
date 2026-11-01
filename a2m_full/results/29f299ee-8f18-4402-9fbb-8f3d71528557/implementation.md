# Equation to Qiskit

Szegedy-type unitary walk W = SWAP(node,target) * R on a cycle of 2^m nodes, with R = 2*Pi - I = U_T (2|0><0|_tgt - I) U_T^dagger. The Kraus operators are B_{i,i+1} = cos(theta) Ry(alpha) and B_{i,i-1} = sin(theta) Rz(beta), which satisfy eq_1. U_T is built from standard gates (Ry, controlled rotations, a QFT-based modular adder) with no dilation ancilla. The circuit applies W for `steps` repetitions. It contains no state preparation or measurement, and the probabilities and the spectral limit are left to the runner.

Source equation run: `09e35c11-d79d-4913-81db-96edf9e1ca7c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1: node register |i> (little-endian, qubit 0 is the LSB); m=2 in the example, so qubits 0,1
- qubits m..2m-1: target-node register |j> (little-endian, starts in |0> for T); qubits 2,3 in the example
- qubit 2m: internal qubit (d=2) acted on by the Kraus operators; qubit 4 in the example
- no dilation ancilla; total qubits = 2m+1 (5 in the example, max 11 allowed for m<=5)
- node encoding: computational-basis integer i = sum_k 2^k * (qubit k), nodes on a cycle of 2^m sites

## Assumptions

- Register order is |node>|target>|internal>, in that qubit-index order
- Nodes are on a cycle of 2^m sites, indices mod 2^m, with m>=2 so that i+1 and i-1 are distinct
- Initial target register is |0...0>, as required for T
- steps is an integer from 0 to 64, and angles are finite reals
- The QFTGate adder uses the convention |j> -> 2^(-m/2) sum_k exp(2 pi i j k/2^m)|k> with little-endian bits

## Unresolved issues

- The paper's exact isometry and reflection may differ from this Szegedy-style proposal
- Initial internal state, initial node and the eq_4/eq_5 post-processing are left to the runner
- The circuit has not been simulated or verified at this stage

## Equation mapping

- `eq_1`: implemented; _build_ut: Kraus choice B_{i,i+1}=cos(theta)Ry(alpha), B_{i,i-1}=sin(theta)Rz(beta). Completeness holds by construction because cos^2+sin^2=1 and Ry, Rz are unitary; it is not checked numerically in the module.
- `eq_2`: implemented; _build_ut. U_T prepares cos(theta)|dir +> + sin(theta)|dir -> on the target, applies the direction-controlled internal rotation, and adds node+1 mod 2^m to the target. On target |0> it acts as T|i>|psi> = sum_j |i>|j> B_ij|psi>. The Kraus operators are specific instance choices.
- `eq_3`: implemented; build_circuit (reflection block, global phase, swap loop). Each step applies U_T, then 2|0><0|_tgt - I (X, multi-controlled Z, X, plus a pi global phase), then U_T^dagger, then SWAP of node and target. W is repeated `steps` times.
- `eq_4`: out_of_scope; no code location. P_t(x) and its Cesaro mean are post-processing of the circuit output. The runner prepares the initial state, and no measurement is included.
- `eq_5`: out_of_scope; no code location. The spectral limit is a classical eigendecomposition of the circuit unitary and is not part of the circuit.

## Specification changes

- eq_2, eq_3: Scope narrowed to a cycle graph with 2^m nodes (m=2..5). Kraus operators are the scaled unitaries cos(theta)Ry(alpha) for the jump to i+1 and sin(theta)Rz(beta) for the jump to i-1. This replaces the general B_ij. Reason: A general B_ij would need opaque dense multiplexed unitaries, which are disallowed. This family is built from standard gates.
- eq_3: No separate dilation ancilla is used. U_T is a concrete unitary on node, target and internal registers, and Pi is the projector onto U_T(|0>_tgt ⊗ everything else). Reason: For these Kraus operators the target register is enough to complete T to a unitary.
- eq_3: R is implemented as -(I - 2|0><0|) conjugated by U_T. The -1 is carried out as a global phase of pi per step. Reason: X, multi-controlled Z, X gives I - 2|0><0|. The exact sign 2|0><0| - I is restored with the global phase.
- eq_4, eq_5: Probability, Cesaro mean and spectral limit are not in the circuit. Reason: The task requires a measurement-free operation with the state prepared by the runner.
