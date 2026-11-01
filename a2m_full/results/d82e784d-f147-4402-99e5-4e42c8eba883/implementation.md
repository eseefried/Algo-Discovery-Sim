# Equation to Qiskit

Builds the unitary part of a p-layer (p=1..3) QAOA MaxCut circuit on an unweighted regular graph with one qubit per vertex and no ancillas. Each layer applies RZZ(-gamma) on every edge, then RX(2*beta) on every qubit. The initial |+>^n state and the readout are left to the runner.

Source equation run: `1a68c3aa-7dbf-46e5-b8b5-e2d38d84a339`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[i] = qubit index i = graph vertex i, for i in 0..n-1 (Qiskit little-endian, qubit 0 is the least significant bit)
- No ancilla qubits; total qubits = n <= 12
- Intended input state |+>^n, prepared by the runner
- Bitstring readout: vertex i is bits[::-1][i] in Qiskit counts keys

## Assumptions

- Vertex i maps to qubit i.
- The instance dict has keys n, edges (list of [i,j] pairs), gammas and betas (equal-length lists with length p in 1..3).
- The runner prepares |+>^n as input.
- Regularity is enforced as a scope restriction.
- Angles are in radians.

## Unresolved issues

- Optimal angles are not specified, so the caller must supply gammas and betas.
- The p=1 closed-form 3-regular result, the large-p strategy, and the classical local-subgraph preprocessing are not implemented.
- The optional ring-ratio sanity check was recalled from the literature and has not been verified.

## Equation mapping

- `eq_1`: implemented; build_circuit: per-edge loop over edges (each term C_ij=(1-Z_iZ_j)/2 realized as RZZ plus global phase). The MaxCut cost operator is exponentiated edge by edge. The edges are validated as an unweighted, simple, regular graph.
- `eq_2`: implemented; build_circuit: loop over layers zip(gammas, betas), phase layer then RX mixer layer. Layer 1 is applied first and layer p last, with the mixer B=sum X_i as RX(2*beta). The H^{(x)n} state preparation is omitted because inputs are prepared by the runner.
- `eq_3`: implemented; build_circuit: qc.rzz(-g, a, c), qc.global_phase update, qc.rx(2*b, i). exp(-i g (1-ZZ)/2) = exp(-i g/2) exp(+i g ZZ/2) = exp(-i g/2) RZZ(-g). The sign is therefore -g, and the global phase -g/2 per edge is tracked exactly. The mixer is exp(-i b X) = RX(2b).
- `eq_4`: out_of_scope; no code location. Expectation-value estimation, sampling and best-cut selection are readout and postprocessing. The circuit is measurement-free and the runner handles readout.
- `eq_5`: background; no code location. The ring ratio (2p+1)/(2p+2) is a recalled literature result that could serve as a sanity check. It is not implemented, and it needs a ring with n>2p+1 and optimized angles.

## Specification changes

- eq_2: The initial H^{(x)n} layer is not included. The circuit implements only the unitary prod_l exp(-i beta_l B) exp(-i gamma_l C), which the runner applies to |+>^n. Reason: The task requires an operation with no input-state preparation.
- eq_1, eq_3: The edge gate is RZZ(-gamma) with an explicit global phase of -gamma/2 per edge, which makes it exactly exp(-i gamma (1-ZZ)/2). The abstract spec's 'RZZ(gamma)' was only up to sign and phase. Reason: RZZ(theta)=exp(-i theta ZZ/2), so the sign has to be corrected to match exp(-i gamma C).
- eq_1, eq_2, eq_3: Scope is narrowed to unweighted simple regular graphs with 2<=n<=12 and 1<=p<=3, given explicitly as an edge list, with rejection of other inputs via ValueError. Reason: This matches the specified scope of tiny regular graphs and the 12-qubit cap.
- eq_4, eq_5: Readout, angle optimization, and the closed-form ring and 3-regular results are not implemented. Reason: They are classical postprocessing or background results, not part of the circuit operation.
