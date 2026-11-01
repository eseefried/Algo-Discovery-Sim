# Equation to Qiskit

Implements a scoped, unitary version of the single-edge noisy hop (eq_2) on a hypercube-labelled vertex register: for an edge (source, source XOR 2^direction) it applies the two-level real orthogonal unitary |a> -> eps|a> + sqrt(1-eps^2)|b>, |b> -> sqrt(1-eps^2)|a> - eps|b>, and acts as identity on all other vertices. At eps=0 this is a perfect hop (a swap of a and b); at eps=1 the particle always stays. The asymptotic threshold (eq_1, eq_5), Grover iteration and the full walk are not built.

Source equation run: `e0d4e338-1c5f-4e62-ab09-1bc27e44813c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: vertex register, little-endian; qubit i holds bit i of the vertex index x (qubit 0 is least significant).
- Edge: vertex a=source and vertex b=source XOR (1<<direction), i.e. a hypercube edge flipping qubit 'direction'.
- No ancilla qubits; total qubits = n_qubits <= 12.

## Assumptions

- Vertex x is encoded as the computational basis state |x> with little-endian bit order.
- Failure amplitude epsilon is a real number in [0,1] and the hop is the real orthogonal two-level unitary described above.
- Applying the circuit once represents one noisy hop; repeated hops are left to the caller (the same-edge hop is an involution).

## Unresolved issues

- The paper's actual noisy-hop unitary, relative phases and barrier model are unknown, so this completion may differ from the paper's.
- The O(1/sqrt N) threshold claim is not encoded and eq_5's heuristic is inconsistent with it.
- No full noisy Grover quantum walk (marked-vertex step plus noisy hops, or the continuous-time case) is implemented.

## Equation mapping

- `eq_1`: out_of_scope; no code location. Asymptotic scaling statement (eps=O(1/sqrt N) gives T=O(sqrt N), otherwise O(N)); it is a runtime claim, not an operation, and cannot be encoded in a single circuit.
- `eq_2`: implemented; build_circuit (controlled RY(2*asin(eps)) followed by controlled X on the edge qubit). Single-edge noisy hop with stay amplitude eps and hop amplitude sqrt(1-eps^2), completed to a unitary by |b> -> sqrt(1-eps^2)|a> - eps|b>.
- `eq_3`: background; no code location. Standard Grover iterate; not built, since the paper's walk operator and its noisy form are not specified.
- `eq_4`: background; no code location. Ideal iteration count pi/4*sqrt(N); only informs how many steps a full search would use. No repetition is encoded.
- `eq_5`: out_of_scope; no code location. Heuristic cumulative no-failure amplitude; the spec itself notes it does not match the abstract's claim, and it is not a circuit operation.

## Specification changes

- eq_2: Chose the unitary completion M=[[eps, s],[s, -eps]] (real, Hermitian, M^2=I), with phase -eps on the b->b component and no relative phase between the two terms of the a->(b,a) image. Reason: eq_2 leaves the unitary completion and relative phase unspecified; a unitary circuit needs a definite choice. This reduces to a perfect hop (swap of a and b) at eps=0.
- eq_2: Narrowed scope from a generic graph hop to one hypercube edge (Hamming distance 1) between vertices a and b on a power-of-two vertex set 2^n. Reason: The graph and barrier model are not given; a hypercube edge is the simplest exactly implementable edge with standard controlled gates.
- eq_1, eq_3, eq_4, eq_5: No Grover walk, repeated steps, oracle, or scaling analysis is built; only the single noisy hop operation. Reason: The paper's walk operator, barrier model and proof are not available, so a faithful full construction cannot be resolved.
