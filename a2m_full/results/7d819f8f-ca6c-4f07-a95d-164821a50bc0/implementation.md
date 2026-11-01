# Equation to Qiskit

Grover block for min-plus witness search over one (u,v) pair: k repetitions of the threshold phase oracle O_tau (compiled from a classical cost table as X-conjugated multi-controlled-Z gates on the marked indices) followed by the diffusion operator 2|s><s|-I on the q-qubit index register. The runner prepares the uniform superposition and does measurement and threshold updates. Max 3 qubits.

Source equation run: `d1fb08e7-1d1c-4d0a-8d5e-b57e5c5ae687`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..q-1 = register idx, q=ceil(log2 n), n=len(costs) in 2..8 (so q in 1..3)
- Qubit i holds bit i of witness index w (little-endian, qubit 0 is least significant)
- Example: n=8, q=3, qubits 0,1,2 = bits 0,1,2 of w
- No ancilla, value or flag qubits; the oracle is compiled from the classical table
- Input state expected from runner: uniform superposition H^q|0> (or any state); no measurement in the circuit

## Assumptions

- instance keys: 'costs' (list of 2..8 nonnegative ints, c(w)=D[u,w]+W[w,v]), 'threshold' (nonnegative int tau), 'iterations' (int 0..64, Grover repetitions k)
- Marking is strict: w is marked iff costs[w] < threshold
- q = max(1, ceil(log2 n)); indices w in [n, 2^q) are not marked but are included in the uniform superposition if the runner prepares it
- If no witness is marked (m=0) the oracle is the identity and only diffusion is applied
- With n=2 the multi-controlled Z reduces to a single Z

## Unresolved issues

- Choice of the iteration count k (about floor(pi/(4 theta)) with sin^2 theta = m/N) and of the random schedule is left to the caller
- When N=2^q > n and m is large (e.g. m=N/2) Grover rotation can be degenerate, which is inherent in the specified iterate
- The paper's subcubic algorithms (small integer weights, geometric weights, earliest arrivals) are not reconstructed because the abstract gives no construction

## Equation mapping

- `eq_1`: background; no code location. Definition of the target minimum d'(u,v). The caller supplies the candidate costs c(w)=D[u,w]+W[w,v] as the 'costs' list; the circuit does not evaluate the minimum.
- `eq_2`: implemented; _oracle (called from build_circuit). Phase oracle for the marked set S_tau={w<n: costs[w]<threshold}, built as X-conjugated multi-controlled-Z gates on each marked basis state. Indices w>=n are never marked.
- `eq_3`: implemented; _diffusion and the loop in build_circuit. Grover iterate G=(2|s><s|-I)O_tau applied k times. The diffusion is H X MCZ X H with a global phase of pi to match 2|s><s|-I exactly. The success probability formula P_k is analysis only and is not coded.
- `eq_4`: out_of_scope; no code location. The Durr-Hoyer loop (measure, classical verify, threshold update, random k schedule) is classical post-processing across many circuits. Each circuit takes the threshold and k as instance parameters.
- `eq_5`: out_of_scope; no code location. Asymptotic complexity statement; there is no circuit content.

## Specification changes

- eq_2, eq_3: build_circuit returns only the operation (G)^k on the idx register. It has no initial H^q state preparation, no measurement and no classical creg. Reason: The task requires an operation with inputs prepared by the runner and no measurements. The runner should apply H^q to |0> to obtain |s>.
- eq_2: The oracle is compiled from the classical cost table and threshold into multi-controlled-Z gates. There are no val or flag ancillas, no adder, and no QRAM lookup. Reason: This is the tiny-instance option explicitly allowed in the specification. No hidden black box is supplied.
- eq_3: The diffusion operator is implemented as H X MCZ X H plus an explicit global phase of pi, so it equals 2|s><s|-I exactly rather than only up to a sign. Reason: The product H X MCZ X H equals I-2|s><s|, which is the negative of the stated reflection.
- eq_4, eq_1, eq_5: Scope is narrowed to one Grover round with fixed threshold and iteration count. The Durr-Hoyer loop, the minimum finding, and the complexity claims are not circuit-implemented. Reason: Threshold updating depends on measurement outcomes and is classical. Dynamic circuits are disallowed.
