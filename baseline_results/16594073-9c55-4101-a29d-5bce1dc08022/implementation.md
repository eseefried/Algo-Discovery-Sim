# Equation to Qiskit

Qiskit module implementing the explicitly scoped baseline construction of the specification (eq_5): an amplitude-amplified hypercube edge tester. The search register holds a hypercube vertex x (n qubits) and an edge direction i (ceil(log2 n) qubits); H gates prepare the uniform superposition over edges, a phase oracle S_{V_f} marks violated edges using four applications of the bit-flip query oracle O_f (two to compute f(x), f(x xor e_i) and two to uncompute), and the standard Grover diffusion -A S_0 A^dagger is applied; the iterate is repeated a user-chosen number of times. The example instance is n=4, f(x)=1-x_1, one iteration (8 qubits). This is the O(sqrt(n/eps)) stand-in, not the paper's O~(n^{1/4} eps^{-1/2}) algorithm, which cannot be reconstructed from the abstract.

Source equation run: `85ea3acb-0fb2-4a8f-a4b1-1c19a18abc8f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-3: register x, hypercube vertex; qubit j holds bit x_{j+1} (little-endian, x_1 on qubit 0)
- qubits 4-5: register i, edge direction as little-endian integer i in {0,1,2,3}; direction i flips qubit x[i] (i.e. coordinate x_{i+1}); for non-power-of-2 n values i >= n are padding and are never marked
- qubit 6: a[0], answer qubit receiving f(x) via O_f (temporarily f(x) xor x_i); returned to |0>
- qubit 7: a[1], answer qubit receiving f(x xor e_i) via O_f (temporarily f(x) xor f(x xor e_i)); returned to |0>
- total 8 qubits for the example (general: n + ceil(log2 n) + 2 <= 12, so n <= 7); all qubits start in |0>, no measurement

## Assumptions

- Instance format: {'n': int>=1, 'iterations': int>=0, 'f': {'type': 'negated_coordinate', 'index': j (1-based)} or {'type': 'truth_table', 'values': list of 2**n bits}}; total qubits n + ceil(log2 n) + 2 must be <= 12 (so n <= 7).
- For the example (n=4, f(x)=1-x_1, 4 directions) exactly 1/4 of the 64 basis states |x>|i> are marked (all x with i=0), so analytically a single Grover iteration should concentrate the amplitude on direction i=0; this is an expectation, not a verified result.
- Multi-controlled X gates are left to Qiskit's mcx (no ancilla); the circuit is unitary but not depth-optimised.
- Global phase of the diffusion operator (H X MCZ X H = I - 2|s><s|) differs from -A S_0 A^dagger by -1, which is irrelevant.

## Unresolved issues

- The paper's actual quantum algorithm achieving O~(n^{1/4} eps^{-1/2}) queries (underlying classical tester and quantum primitive) is unknown from the abstract and is not implemented.
- The truth-table oracle uses up to 2^n multi-controlled gates and is exponentially deep in n; acceptable only for the small n allowed here.
- No adaptive or exponential-guess iteration schedule is provided; the caller must choose 'iterations'.

## Equation mapping

- `eq_1`: background; no code location. Definition of monotonicity; it motivates the violated-edge predicate but is not itself a circuit element.
- `eq_2`: background; no code location. Definition of eps-farness and the rejection condition; only enters the iteration-count heuristic, which is left as the instance parameter 'iterations'.
- `eq_3`: implemented; _apply_oracle (bit-flip query oracle O_f) and _apply_marking (violated-edge predicate V_f realised as a CZ on the two answer qubits). O_f is implemented either as X+CX for f(x)=1-x_j or as a truth-table of multi-controlled X gates; V_f is detected via a0 = f(x) xor x_i and a1 = f(x) xor f(x xor e_i), which are both 1 exactly for violated edges.
- `eq_4`: background; no code location. Classical detection-probability lower bound p >= eps/n; it justifies the O(sqrt(n/eps)) iteration count but no gate depends on it (iterations is a user-supplied integer).
- `eq_5`: implemented; build_circuit (A = H on search register, loop over Grover iterates), _apply_marking (S_{V_f}), _apply_diffusion (-A S_0 A^dagger). The baseline amplitude-amplified edge tester; the number of iterations T is taken from the instance instead of a fixed schedule.
- `eq_6`: out_of_scope; no code location. The paper's O~(n^{1/4} eps^{-1/2}) query bound and its comparison with the classical bound describe an algorithm whose mechanism is not available from the abstract; the implemented baseline only achieves O(sqrt(n/eps)).

## Specification changes

- eq_5: Scope narrowed to the baseline amplitude-amplified edge tester; the paper's n^{1/4} eps^{-1/2} algorithm is not implemented. Reason: The abstract gives no construction; only the baseline from the math stage is explicitly specified.
- eq_3, eq_5: The dedicated marker qubit m from the register list is removed; the violated-edge predicate is written as a conjunction of two answer-qubit values (a0 = f(x) xor x_i, a1 = f(x) xor f(x xor e_i)) and the phase is applied with CZ(a0, a1). Reason: Both orientations of a violated edge are captured by this symmetric reformulation, saving one qubit under the 12-qubit cap while realising the same S_{V_f}.
- eq_5: The direction register has k = ceil(log2 n) qubits and the superposition is uniform over all 2^k direction values; values i >= n are padding directions that are never marked. Reason: Exact uniform superposition over n non-power-of-2 directions would need a non-standard state preparation; padding changes the marked fraction by at most a factor 2, i.e. constant overhead in T.
- eq_5: Bit ordering follows Qiskit little-endian: x_1 sits on qubit 0 (least significant), truth-table index bit j equals x_{j+1}; the specification's 'x_1 most significant' convention is replaced. Reason: Required to match the physical qubit order of Qiskit; disclosed so truth tables are interpreted consistently.
- eq_3, eq_5: Each Grover iteration uses four applications of O_f (compute f(x), f(x xor e_i), then uncompute both) rather than the two counted in the specification. Reason: Clean uncomputation of the answer qubits is needed to keep the search register unentangled; query count differs only by a constant factor.
- eq_4, eq_5: The iteration count T is an instance parameter instead of an exponential-guess schedule over unknown p. Reason: A schedule with random restarts is an experiment-level procedure; the module returns a single unitary operation.
- eq_1, eq_2, eq_3: Measurement of (x, i) and the classical verification/accept-reject step are omitted. Reason: The deliverable is a measurement-free unitary operation; measurement and post-processing belong to the runner.
