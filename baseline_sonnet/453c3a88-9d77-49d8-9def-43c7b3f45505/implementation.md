# Equation to Qiskit

Lackadaisical quantum-walk search step U^t on the complete graph with N=2^n vertices, one marked vertex, phase-flip (Grover) coin, and l in {0,1} self-loops per vertex. Arcs are labelled by an XOR offset c, with the arc (v,c) leading to vertex v XOR c. c=0 is the self-loop, which exists only for l=1, so the shift is a bitwise CNOT from the coin register onto the vertex register. The coin is A (2|0><0|-I) A^dagger controlled on the vertex not being the marked vertex, and -I on the marked vertex. A is H^n for l=1 and a real-amplitude preparation of the uniform state over the nonzero offsets for l=0. The circuit contains no input-state preparation and no measurement.

Source equation run: `11944ef5-df97-4ea5-8a54-fbb671f49cb8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: vertex register, little-endian binary label v (bit i of v on qubit i)
- qubits n..2n-1: coin register, little-endian binary XOR offset c (bit i of c on qubit n+i); arc (v,c) leads to vertex v XOR c; c=0 is the self-loop
- example (n=2): qubits 0,1 = vertex; qubits 2,3 = coin
- total qubits = 2n <= 12

## Assumptions

- The 'phase flip coin' is the Grover diffusion coin on unmarked vertices with -I on the marked vertex, as in eq_2.
- The coin is applied before the shift, with one marked vertex.
- The runner prepares the initial state, which is uniform over vertices and over allowed coin states.
- The complete graph has N=2^n vertices with n between 1 and 6, so 2n <= 12 qubits.
- A global phase of pi per step is included for exactness and has no effect on probabilities.

## Unresolved issues

- The paper's exact phase-flip coin and shift definitions are not known, so this is an assumed reading of the abstract.
- The abstract's 1/2 and 1 success probabilities are asymptotic in N, so small instances will only approximate them.
- The optimal number of steps is not derived here; the user chooses steps.
- The SKW coin, continuous-time walks, multiple marked vertices and l>1 are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: per-step coin block (A^dagger, phase flips, A) followed by the shift loop of CNOTs from coin to vertex. U = S times (controlled coin), with the coin applied first. The shift is the XOR-offset arc pairing (v,c) <-> (v xor c,c), which fixes self-loops (c=0).
- `eq_2`: implemented; build_circuit: prep (A), the two multi-controlled phase flips and the global phase of pi. C_0 = A(2|0><0|-I)A^dagger on unmarked vertices, C_1 = -I on the marked vertex. Both are implemented as A D A^dagger with diagonal D = -(I - 2P[c=0, v!=w]). For l=1, A = H^n and |s_c> is uniform over all N offsets. For l=0, A is a real-amplitude preparation of the uniform state over nonzero offsets.
- `eq_3`: background; no code location. The task says the runner prepares the input state. The circuit is only the operation U^t, so the initial uniform state is not built here. For l=1 it is H on all 2n qubits. For l=0 the uniform vertex superposition is combined with the uniform state over nonzero offsets.
- `eq_4`: out_of_scope; no code location. Measurement of the vertex register and probability estimation are done by the runner, not by this circuit.
- `eq_5`: out_of_scope; no code location. This is the abstract's asymptotic claim, a target behaviour to compare against. It is not an operation and is not hardcoded.

## Specification changes

- eq_1: Restricted to N=2^n vertices and l in {0,1}. Arcs are labelled by an XOR offset c (target vertex = v XOR c). The shift is a CNOT layer instead of a generic arc-swap permutation. Reason: This keeps the coin vertex-independent on unmarked vertices and avoids padding the coin dimension N-1+l to a power of two. The labelling is a relabelling of the arcs, which does not change the walk.
- eq_2: For l=0 the coin dimension is N-1 but the register holds 2^n offset states. The reflection 2|s_c><s_c|-I acts on the full register and gives -1 on the unused offset c=0. Reason: The nonzero-offset subspace is invariant and c=0 is never populated by a valid initial state, so the walk dynamics are unchanged.
- eq_3: The initial state is not prepared inside the circuit. Reason: The task requires the circuit to be an operation only; the runner prepares inputs.
- eq_1: Added an integer parameter steps (0..100) giving the number of repeated applications of U, and the marked vertex is a parameter. Reason: The operation should be usable for several t and marked vertices; the cap bounds the circuit size.
- eq_2: Number of self-loops limited to l in {0,1}; larger l is rejected with ValueError. Reason: A larger l would need a multi-self-loop coin dimension that is not in the XOR-offset scheme. This narrows the scope but covers the abstract's l=0 versus l=1 comparison.
