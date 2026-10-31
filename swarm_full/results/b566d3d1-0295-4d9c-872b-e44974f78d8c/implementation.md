# Equation to Qiskit

Qiskit implementation of the p-layer QAOA operation for MaxCut on an arbitrary simple graph with at most 12 vertices. Each layer applies the phase separator exp(-i*gamma_l*C) with C = sum over edges of (1 - Z_i Z_j)/2, using one RZZ(-gamma_l) per edge plus the exact global phase, then applies the mixer exp(-i*beta_l*sum_j X_j) as RX(2*beta_l) on every qubit. The |+>^n preparation is not included, because the runner prepares inputs. The circuit is measurement-free and bound.

Source equation run: `11acfd05-4e8d-47d9-be65-7836e97cf55d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Single register 'q' with n qubits; qubit index i = graph vertex i (Qiskit qubit 0 is the least significant bit of the computational-basis string z).
- Bit value 0 corresponds to Z=+1 and bit value 1 to Z=-1.
- Example: n=4, qubits q0..q3 are the vertices of K4, which is 3-regular.

## Assumptions

- The objective is the MaxCut cut-size operator C = sum over edges of (1 - Z_u Z_v)/2, with the cut maximized.
- The mixer is B = sum_j X_j, implemented as RX(2*beta) on every qubit.
- The input state is |+>^n, prepared externally by the runner.
- Instance keys: n (1..12), edges (list of distinct [u,v] pairs with u != v), gammas and betas (equal-length lists of finite reals, p between 1 and 20).
- Registers use the Qiskit little-endian convention: vertex i maps to qubit i.

## Unresolved issues

- The abstract does not give the paper's exact gate decomposition, so the standard QAOA gates are assumed.
- The optimal angles for p=1 on 3-regular graphs are not given in the abstract, and the user must supply them.
- The 0.6924 guarantee cannot be checked from the circuit alone, and it is unclear whether it refers to the expectation value or to sampled outcomes.
- Regularity of the graph is not enforced, so 2-regular or 3-regular instances must be supplied by the caller.

## Equation mapping

- `eq_1`: implemented; build_circuit: edge loop applying qc.rzz(-g,u,v) and the global_phase update (C = sum over edges of (1-Z_u Z_v)/2). The objective is realized as a sum of 2-local MaxCut clause terms, one per edge. The clause form (1-ZZ)/2 is the standard MaxCut choice and is an assumption, since the abstract only implies a sum over constraints.
- `eq_2`: background; no code location. The depth scaling is a property of the construction and is not computed. The circuit has p*(m+n) gates, which is consistent with O(p*m) depth.
- `eq_3`: out_of_scope; no code location. The 0.6924 approximation-ratio guarantee is a performance claim about optimized angles and sampled or expected cuts. It is not a circuit operation, and the circuit performs no angle optimization or measurement.
- `eq_4`: implemented; build_circuit: loop over layers; qc.rx(2.0*b, j) is the mixer, and the layer order is gamma_1 first. The layered unitary prod_{l=p..1} exp(-i beta_l B) exp(-i gamma_l C) is implemented with B = sum_j X_j. Layer 1 is applied first. The |+>^n factor is excluded because the runner prepares the input.

## Specification changes

- eq_4: The initial state |+>^{\otimes n} (Hadamard layer) is omitted from the circuit. The circuit implements only the operator prod_l exp(-i beta_l B) exp(-i gamma_l C). Reason: The task requires an operation without input-state preparation. The runner must supply |+>^n to reproduce the QAOA state.
- eq_1, eq_4: Scope is narrowed to MaxCut on arbitrary simple graphs (not only regular ones) with explicit user-supplied angles. C is fixed to sum (1-Z_u Z_v)/2 and the mixer to sum X_j. Weighted edges and higher-locality clauses are not implemented. Reason: The abstract gives no explicit gate forms, so the standard QAOA MaxCut construction is used. Angle optimization is not part of the circuit.
- eq_1, eq_4: The phase separator exp(-i gamma (1-ZZ)/2) is implemented as RZZ(-gamma) per edge, with the global phase -gamma*m/2 added to the circuit. Reason: Qiskit's RZZ(theta) equals exp(-i theta ZZ/2), so theta = -gamma reproduces the sign. The global phase keeps the unitary exact.
- eq_2, eq_3: These equations are not turned into circuit logic. The depth statement is treated as background and the approximation ratio as out of scope. Reason: They are performance statements, not gate-level operations.
