# Equation to Qiskit

Trotterized two-stage continuous-time quantum walk search operation U on an n-cube (hypercube, A = sum_j X_j) with n in {3,4}, one marked vertex w, and no ancillas. Stage k applies r first-order Trotter steps of RX mixing at rate gamma_k for total time T_k, interleaved with a phase oracle exp(i dt |w><w|) built from X-conjugated multi-controlled phase. Setting T2=0 gives the single-stage walk. The circuit contains no state preparation or measurement.

Source equation run: `9f37b962-29fc-4e99-9e11-eb124223bc1f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register 'v' with n qubits (n=3 or 4); qubit i (Qiskit index i) holds bit i of the vertex label, little-endian, so qubit 0 is the least significant bit of w.
- Marked vertex w is in {0,...,2^n-1} and uses the same little-endian encoding.
- No ancilla qubits. Input state (e.g. uniform superposition from Hadamards) must be prepared by the runner.

## Assumptions

- Adjacency-matrix Hamiltonian with the Childs-Goldstone sign convention H=-gamma A - |w><w|.
- Within each Trotter step the graph term is applied first, then the oracle phase.
- Little-endian vertex encoding, with qubit i corresponding to bit i of the vertex label.
- The global phase from the exact exp(i dt) convention is retained through the mcp gate, up to Trotter error.
- The runner prepares the initial state, typically the uniform superposition, and does the measurement.

## Unresolved issues

- The paper's actual two graph families and their critical gamma values are not reproduced.
- Appropriate gamma1, gamma2, T1, T2 and r must be chosen by an external scan; the example values are guesses near gamma ~ 1/n.
- First-order Trotter error is not controlled analytically, so results approximate the exact evolution.
- Whether the true oracle allows a free phase angle or only a fixed sign flip is unresolved.

## Equation mapping

- `eq_1`: implemented; _stage: RX mixing implements the -gamma*A term with A=sum_j X_j; mcp-based oracle implements the -|w><w| term. H(gamma)=-gamma A - |w><w| is split into hypercube hopping and a marked-vertex phase. The graph is fixed to the n-cube, which is a stand-in for the paper's graphs.
- `eq_2`: implemented; build_circuit: stage 1 (gamma1,T1) followed by stage 2 (gamma2,T2). Sequential composition U = exp(-iH(gamma2)T2) exp(-iH(gamma1)T1), each stage Trotterized. T2=0 reduces it to a single stage.
- `eq_3`: background; no code location. Success probability and the uniform start state are an experiment/readout concern. The circuit is the operation U only, with no state preparation or measurement.
- `eq_4`: implemented; _stage. First-order Trotter product of exp(i gamma A dt) and exp(i dt |w><w|). For the hypercube the first factor is the product of RX(-2 gamma dt) on each qubit. The oracle is a free-angle phase on |w> built from X conjugation and a multi-controlled phase gate.
- `eq_5`: out_of_scope; no code location. The T_opt versus sqrt(N) scan and fit is classical post-processing over many circuits, not part of one circuit.

## Specification changes

- eq_1, eq_4: Graph restricted to the hypercube on n=3 or 4 qubits with A=sum_j X_j; no complete-graph-pair or bridge graph is implemented. Reason: The paper's exact graphs are not given in the specification, and the hypercube factorization is the only one stated explicitly.
- eq_3: The Hadamard state preparation listed in the steps is omitted from the circuit. Reason: The task requires the circuit to be an operation with inputs prepared by the runner.
- eq_4: The oracle is realised as a phase exp(i dt) on |w> with a free angle, implemented in-circuit via X gates and a multi-controlled phase, rather than as an external black box. Reason: A black-box oracle is unavailable, and the free-angle oracle is needed to match exp(-iH dt).
- eq_2, eq_4: Trotter step count r is shared by both stages and capped at 200. A stage with T=0 is skipped. Reason: Bounds circuit size and keeps the single-stage case a special case.
- eq_5: Scan and fit are not implemented. Reason: They are classical scaling analysis, outside one circuit construction.
