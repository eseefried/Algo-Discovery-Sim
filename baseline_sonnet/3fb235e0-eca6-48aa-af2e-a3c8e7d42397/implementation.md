# Equation to Qiskit

Qiskit implementation of the p-layer QAOA operation for unweighted MaxCut: each layer applies exp(-i*gamma_k*C) as an RZZ per edge, then exp(-i*beta_k*B) as an RX per qubit. The |+>^n preparation, measurement, angle optimization and the 0.6924 guarantee are excluded. The example is p=1 on the 4-cycle C4.

Source equation run: `0c57350d-2be7-4db8-895e-777a56855325`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubit i (Qiskit index i, i=0..n-1, little-endian) encodes vertex i; computational-basis bit z_i=0/1 labels the side of the cut (Z eigenvalue +1/-1).
- Example: q0,q1,q2,q3 are the vertices of the 4-cycle C4 with edges 0-1, 1-2, 2-3, 3-0.
- No ancillas; total qubits = n <= 12.

## Assumptions

- The algorithm is the standard QAOA ansatz with a ZZ phase separator and an X mixer.
- The graph is unweighted and simple, with no self-loops or duplicate edges.
- Edges are given as vertex index pairs and vertex i maps to qubit i.
- Angles are real and finite, with len(gammas) == len(betas) = p.
- The runner prepares |+>^n as the input state.

## Unresolved issues

- The abstract gives no explicit gate decomposition or parameter schedule, so the standard QAOA form is assumed.
- The classical preprocessing for fixed p and the strategy for p growing with input size are not implemented.
- The derivation of the 0.6924 bound and the 2-regular analysis are not reconstructed.

## Equation mapping

- `eq_1`: background; no code location. MaxCut objective with edge clauses (1 - Z_j Z_k)/2. It defines the edge list and the phase-separator generator but is not itself a gate. The cut value is never evaluated in the circuit.
- `eq_2`: implemented; build_circuit: per-edge qc.rzz(-gamma, j, k) with global_phase -= gamma/2 (phase operator), and qc.rx(2*beta, j) per qubit (mixer). exp(-i*gamma*C_jk) = exp(-i*gamma/2) * exp(+i*gamma/2 Z_j Z_k), and RZZ(theta) = exp(-i*theta/2 Z Z), so RZZ(-gamma) is used with the scalar phase tracked. exp(-i*beta*X) = RX(2*beta).
- `eq_3`: implemented; build_circuit: loop over zip(gammas, betas), applying the phase layer then the mixer layer in order k=1..p. Implements the ordered product U(B,beta_p)U(C,gamma_p)...U(B,beta_1)U(C,gamma_1). The |+>^n preparation is deliberately left out because the runner prepares inputs.
- `eq_4`: out_of_scope; no code location. Expected objective and classical angle optimization is a classical/measurement-level procedure. Angles are supplied by the instance.
- `eq_5`: out_of_scope; no code location. The 0.6924 approximation guarantee for p=1 on 3-regular graphs is an analytical result and is not part of the circuit.

## Specification changes

- eq_3: Hadamard preparation of |+>^n is excluded from the returned circuit; the circuit is only the layered unitary applied to a runner-prepared input. Reason: The task requires an operation with no input-state preparation.
- eq_2, eq_3, eq_4: Angles gamma_k, beta_k are explicit instance inputs. Optimization and selection of angles are not implemented. Graph, p and angles are taken from the instance and the circuit is validated for general p <= 50, n <= 12. Reason: Classical preprocessing is not specified, and the circuit must be a bound, unitary operation.
- eq_1, eq_2: The edge phase factor exp(-i*gamma/2) is retained as circuit global_phase so the unitary equals exp(-i*gamma*C) exactly, not just up to a phase. Reason: The spec writes the exact operator exp(-i*gamma*C). Dropping the phase would only change a global phase.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope is narrowed to the standard QAOA ansatz for unweighted MaxCut on a user-given simple graph, with the C4 example. The 3-regular analysis and the large-p strategy are not covered. Reason: The abstract gives no explicit circuit, so the standard QAOA ansatz is assumed. The status is 'generated' because the schema has no 'partial' value.
