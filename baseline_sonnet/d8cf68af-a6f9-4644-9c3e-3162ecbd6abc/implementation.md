# Equation to Qiskit

Implements eq_5 for a small binary RBM: a unitary that maps |0...0> to the Gibbs-state encoding sum_{v,h} sqrt(P(v,h))|v>|h>. The energy (eq_1) and Gibbs weights (eq_2) are evaluated classically from the instance parameters W, b, d. The state is built with a standard binary tree of multi-controlled Ry rotations, so every amplitude is non-negative and no phases are needed. This is a classical-compute state-preparation circuit, not the paper's quantum training algorithm.

Source equation run: `9f0afa01-2b4f-4a6c-bce4-0ddf618bb6fb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n_v-1: visible units v_0..v_{n_v-1} (qubit i = v_i, qubit 0 least significant)
- qubit n_v..n_v+n_h-1: hidden units h_0..h_{n_h-1} (qubit n_v+j = h_j)
- Example: q0=v0, q1=v1, q2=h0, q3=h1; basis index x = v0 + 2 v1 + 4 h0 + 8 h1; no ancillas
- Encoding: computational basis, amplitude of |x> = sqrt(P(v,h)); intended input |0...0>

## Assumptions

- Binary units in {0,1} with temperature 1
- Visible unit i is qubit i and hidden unit j is qubit n_v+j
- The runner supplies |0...0> as input
- Parameters are bounded to |entries| <= 50 and must be finite

## Unresolved issues

- The paper's actual quantum training algorithm, state preparation and gradient estimation are not specified in the abstract and are not implemented
- The state-preparation cost is exponential in n_v+n_h, so it offers no speedup
- The full Boltzmann machine and multi-layer models are not covered
- The data-dependent (clamped visible) term of the gradient is not implemented

## Equation mapping

- `eq_1`: implemented; _gibbs_probs (energy loop E[x]). RBM energy computed classically for every basis configuration from W, b, d.
- `eq_2`: implemented; _gibbs_probs (exp(-(E-Emin)) normalized). Gibbs probabilities computed classically; the shift by E.min() cancels in the normalization and only aids numerical stability.
- `eq_3`: background; no code location. Log-likelihood objective is not part of the circuit; it is context for why the model distribution is needed.
- `eq_4`: background; no code location. Gradient is classical post-processing from samples and is not implemented. The circuit only prepares the state whose measurement would give the model term.
- `eq_5`: implemented; build_circuit (multiplexed Ry tree loop). Prepares sum sqrt(P(v,h))|v>|h> from |0...0> using controlled Ry rotations whose angles come from marginal probabilities.

## Specification changes

- eq_5: The Gibbs-state encoding is realized as an explicit state-preparation unitary from |0...0> with classically computed rotation angles. This is not a quantum Gibbs-sampling or paper-specific algorithm. Reason: The abstract gives no preparation method. A generic exact amplitude-encoding tree is the only defensible way to realize eq_5 with standard gates.
- eq_1, eq_2: The energy and Gibbs weights are evaluated classically at build time, so the circuit angles depend on the full distribution (including Z). Reason: eq_5 needs the amplitudes sqrt(P). A circuit without classical knowledge of P would require the unspecified quantum method.
- eq_3, eq_4, eq_5: Scope narrowed: total qubits n_v+n_h capped at 8, below the global cap of 12. Measurement, sampling, gradient estimation and training are excluded. Reason: The multi-controlled tree needs 2^n-1 gates, so a cap of 8 keeps it practical. Measurement and training are outside an operation-only module.
