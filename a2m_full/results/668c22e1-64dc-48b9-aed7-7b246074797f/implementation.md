# Equation to Qiskit

Builds the postselection-ready Gibbs-state preparation for a small Boltzmann machine. Each free unit gets an Ry(theta_i) mean-field rotation, then a classically tabulated multiplexed ancilla Ry whose |1> amplitude is sqrt(exp(-E(x))/(kappa Q(x))). Postselecting ancilla=1 gives sum_x sqrt(P(x))|x>. An optional clamp_visible vector fixes the visible units with X gates, so the hidden units get the conditional Gibbs state for the data term. No measurement, no amplitude estimation, no gradient update.

Source equation run: `10be5ce5-e847-408d-808e-84fca88d5c84`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: vis[0] (visible unit 0, little-endian bit 0)
- qubits 1..n_visible-1: further visible units
- qubits n_visible..n_visible+n_hidden-1: hidden units (example: qubit 1 = hid[0])
- qubit n_visible+n_hidden: ancilla anc[0], postselect on |1> (example: qubit 2)
- encoding: unit qubit |x_i> = binary unit value x_i; ancilla |1> marks accepted branch; basis index bit i = qubit i

## Assumptions

- Unit order is visible units first, then hidden units, then the ancilla, with little-endian qubit indexing.
- The builder knows b and w, so rotation angles are computed classically for tiny instances.
- Postselection on ancilla=1 and the Z/ZZ readout are done exactly by the runner outside this operation.
- Applying X gates to clamp visible units and Ry gates for the mean-field state are part of the state-preparation operation, since the qubits start in |0>.

## Unresolved issues

- No amplitude estimation, Grover amplification, QRAM data access or energy-oracle phase implementation is included.
- The O(sqrt(kappa)/epsilon) scaling and the speedup claims are not represented.
- Only small fully connected instances (at most 6 units) are supported.
- The mean-field fixed point is a heuristic and not guaranteed to minimise kappa.

## Equation mapping

- `eq_1`: implemented; _energy. Energy with biases and each pair counted once, evaluated classically to build the ancilla rotation table.
- `eq_2`: implemented; build_circuit: mean-field fixed point (q) and Ry(theta_i) loop. Q is the product of q_i factors with q_i=sin^2(theta_i/2), prepared by Ry(theta_i) on each free qubit. The typographical Q formula is not used.
- `eq_3`: implemented; build_circuit: ratios table and RYGate(phi).control(f, ctrl_state=m) loop. For every free assignment m the ancilla rotates with sin^2(phi/2)=exp(-E)/(kappa Q), so postselecting ancilla=1 gives sqrt(P(x)). Postselection itself is left to the runner.
- `eq_4`: background; no code location. Readout identity from Z and ZZ expectations. It is applied after the circuit and is not part of the operation.
- `eq_5`: implemented; build_circuit: clamp_visible handling (X gates, free-unit restriction). One training vector per circuit: visible qubits are clamped with X gates and the hidden units get the conditional Gibbs state. The sum over training vectors and the h_j readout are classical.
- `eq_6`: out_of_scope; no code location. The gradient combination and the gradient-ascent update with eta are classical postprocessing.

## Specification changes

- eq_2: Q(x) is the product of q_i^{x_i}(1-q_i)^{1-x_i} with q_i=sin^2(theta_i/2), not the garbled sin^{2(theta_i/2) x_i} latex. Reason: The latex is a typographical simplification, and Ry(theta)|0> gives P(1)=sin^2(theta/2).
- eq_2, eq_3: Mean-field marginals q are computed by a damped fixed-point iteration q_i=sigmoid(b_i+sum_j w_ij q_j), clipped to [1e-6,1-1e-6], unless the instance supplies q. Reason: The spec leaves the mean-field computation unspecified. The construction needs only that Q be a product distribution with q strictly inside (0,1).
- eq_3: kappa defaults to max_x exp(-E)/Q (the smallest valid value) and P_succ=Z/kappa because Q is normalized. A user-supplied kappa below that maximum raises ValueError. Reason: This guarantees exp(-E)<=kappa Q, so every ancilla rotation amplitude is at most 1.
- eq_3: The multiplexed rotation is built from 2^f multi-controlled RYGate instances with explicit ctrl_state, limited to at most 6 units. Reason: This uses standard gates only and stays tractable at small sizes.
- eq_5: In clamp mode the energy, mean-field and rotation table are restricted to the hidden units with the visible values fixed. Only one training vector is handled per circuit. Reason: This is the conditional Gibbs state P(h|v), and the data average is done classically.
- eq_1: Biases and weights are bounded in absolute value by 10, and weights are given as [i,j,w] triples over all units, with visible units first. Reason: This keeps the exponentials finite and defines full connectivity, including visible-visible and hidden-hidden couplings.
