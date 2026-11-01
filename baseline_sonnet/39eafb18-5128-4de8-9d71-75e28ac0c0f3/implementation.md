# Equation to Qiskit

Implements the discrete-time search operator U=(W^m O)^k on an n-qubit vertex register (N=2^n vertices), with O=I-2|w><w| and W a walk step for the complete graph K_N, W=2|s><s|-I (reflection about the uniform state). No state preparation or measurement. The continuous-time Hamiltonian and the asymptotic speedup claims are not implemented.

Source equation run: `1ecfa2cf-0679-4690-b488-df025f681a7f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: vertex register, little-endian computational basis: vertex v = sum_q b_q 2^q with qubit 0 the least significant bit
- Example: n=2 gives N=4 vertices on qubits 0,1; marked vertex 2 corresponds to qubit0=0, qubit1=1
- No ancilla or coin qubits

## Assumptions

- Single marked vertex w in {0,...,2^n-1}, with N a power of two.
- The vertex index is encoded in little-endian binary on qubits 0..n-1.
- A global phase of pi per W step makes W exactly 2|s><s|-I.
- Parameter bounds: n_qubits 1..12, m 1..64, k 0..64, to cap circuit size.
- Input state preparation (e.g. uniform superposition) is done by the runner.

## Unresolved issues

- The paper's graph families, W operator, and values of m are unknown.
- On the complete graph W^2=I, so m>1 carries no extra algorithmic content here and does not reproduce the paper's cubic speedup.
- The continuous-time algorithm is not implemented, so no comparison between the two models is built.

## Equation mapping

- `eq_1`: out_of_scope; no code location. The continuous-time Hamiltonian evolution exp(-iHt) is not built. The chosen scope is the discrete-time construction only.
- `eq_2`: implemented; build_circuit: loop over k rounds, each calling _oracle once then _walk_step m times. The operator (W^m O)^k is built with O acting first in each round, followed by m walk steps. W is the concrete complete-graph step defined in _walk_step.
- `eq_3`: implemented; _oracle. The phase oracle I-2|w><w| is built from X conjugation on the zero bits of w and a multi-controlled Z.
- `eq_4`: background; no code location. An asymptotic quadratic-speedup claim. It is not an operation and cannot be implemented in a fixed circuit.
- `eq_5`: background; no code location. An asymptotic cubic-speedup claim. It is not an operation, and the paper's graph families and schedules are not given.

## Specification changes

- eq_2: The walk step W is concretely chosen as W=2|s><s|-I on the vertex register, the reflection about the uniform state, which is the walk on the complete graph K_N with N=2^n. The scope is narrowed to this graph, and no coin register or Szegedy-type walk is used. Reason: The specification leaves W unspecified. The complete graph is the only graph that can be defined from the given information with standard gates and no dense unitaries.
- eq_2: The circuit is the operator product W^m O applied in the order O then W^m, repeated k times. The m steps are applied literally as m repeated gate sequences, with no reduction of W^2=I. Reason: This preserves the specified product form and matches the intended meaning of m walk steps between oracle queries.
- eq_1: The continuous-time variant is dropped from this artifact. Reason: Exactly ONE construction is implemented. Scope is narrowed to the discrete-time walk.
- eq_4, eq_5: The asymptotic speedup relations are treated as background context, not as circuit content. Reason: They are statements about scaling and have no unitary realization.
