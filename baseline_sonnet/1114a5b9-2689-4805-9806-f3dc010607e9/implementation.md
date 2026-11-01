# Equation to Qiskit

Scoped Qiskit implementation of one Grover building block from the trivial quantum APSP baseline: r Grover iterations that amplify intermediate vertices k with d1(u,k)+w(k,v) < threshold for a fixed pair (u,v). The cost table is classical data compiled into a phase oracle of multi-controlled phase flips with no ancillas. The runner supplies the uniform superposition over k. The paper's nontrivial algorithms are not implemented.

Source equation run: `0edbc907-4725-4b92-8231-da599378a333`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1 form register 'k' with m = log2(n); qubit i holds bit i of the candidate intermediate vertex index k (qubit 0 is the least significant bit)
- example: n=8, so 3 qubits; qubit 0..2 encode k in 0..7
- no workspace or ancilla qubits; the d(u,k)+w(k,v) values are classical data compiled into the oracle
- the runner is expected to prepare the uniform superposition over k before the circuit

## Assumptions

- The marked condition is strict: cost < threshold.
- A null weight denotes infinity, so that k is never marked.
- The weights are nonnegative.
- The oracle phase is -1 on marked basis states and the diffusion is I-2|s><s| up to a global phase.
- The runner prepares the uniform superposition over k.

## Unresolved issues

- The paper's nontrivial algorithms for geometric weights, small integer weights, few weights per vertex, and earliest arrivals are not described in the abstract and are not implemented.
- A reversible arithmetic oracle for d1(u,k)+w(k,v) from quantum-accessible data is not implemented.
- The full Durr-Hoyer adaptive minimum finding and the n^2 pair repetition are not implemented.
- Non-power-of-two n is rejected.

## Equation mapping

- `eq_1`: background; no code location. Runtime statement about trivial classical and quantum algorithms; it is not a circuit operation.
- `eq_2`: out_of_scope; no code location. Target subcubic and nontrivial quantum bounds. The abstract gives no algorithm achieving them.
- `eq_3`: implemented; build_circuit: costs = d1_row[k] + w_col[k]; marked = {k : cost < threshold}; _phase_flip_basis. The min-plus term d1(u,k)+w(k,v) is evaluated classically per k. A threshold phase oracle marks the k that improve on the threshold, which is one comparison step of Durr-Hoyer minimum finding.
- `eq_4`: background; no code location. The O(sqrt n) query count and n^2*sqrt(n) total motivate Grover use. The circuit exposes the iteration count as a parameter and does not implement the n^2 pair repetition or the full adaptive Durr-Hoyer loop.

## Specification changes

- eq_3, eq_4: Narrowed from full Durr-Hoyer minimum finding to a fixed number of Grover iterations with a threshold oracle for one pair (u,v). Reason: Minimum finding is adaptive and needs mid-circuit measurement and classical updates, which are not allowed in a unitary circuit.
- eq_3: Dropped the quantum 'val' workspace register. Costs d1(u,k)+w(k,v) are precomputed classically and the oracle is compiled as phase flips on basis states. Reason: The data oracle and precision are unspecified, and no ancillas are needed for a sparse marked set.
- eq_4: The number of vertices n must be a power of two (2 to 4096) so the uniform superposition over all index states is exactly over the vertices. The iteration count is a user parameter capped at 64. Reason: Avoids padded invalid indices and keeps the circuit size bounded.
- eq_1, eq_2: Complexity equations are not implemented. Reason: They are asymptotic statements, not operations.
- eq_3, eq_4: The initial uniform superposition is not prepared in the circuit. The circuit contains the Grover iterate (oracle then diffusion) repeated r times. Reason: Inputs are prepared by the runner.
