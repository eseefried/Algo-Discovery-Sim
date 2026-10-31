# Equation to Qiskit

Implements the scoped construction from the specification as a single unitary operation: coherent preparation of the product (mean-field) proposal state |psi_Q> on the visible+hidden register (eq_proposal_state), followed by the coherent rejection-sampling rotation that writes sqrt(e^{-E(v,h)}/(kappa' Q(v,h))) as the |1>-amplitude of a flag qubit (eq_rejection_rotation, with the energy of eq_energy evaluated classically per configuration), plus an optional number of amplitude-amplification rounds on flag=1 (the Grover operator underlying eq_postselect). Post-selecting flag=1 leaves the state register in the coherent Gibbs state of the RBM. The b-bit fixed-point ratio register of the specification is replaced by exact per-configuration multi-controlled R_y rotations (no ancilla, no rounding error), which is disclosed as a specification change. Measurement, post-selection, sampling and the classical gradient/update steps are left to the runner and are out of scope.

Source equation run: `732c7a45-7bad-4535-a262-8627f30fee8b`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0 (register v[0]): visible unit v_1, |1> = unit on (least significant bit)
- qubit 1 (register v[1]): visible unit v_2, |1> = unit on
- qubit 2 (register h[0]): hidden unit h_1, |1> = unit on
- qubit 3 (register f[0]): rejection-sampling flag; |1> marks acceptance (most significant bit of a measured bitstring)
- Total 4 qubits for the example; in general n_v + n_h + 1 <= 12, with qubits 0..n_v-1 = v_1..v_{n_v}, qubits n_v..n_v+n_h-1 = h_1..h_{n_h}, qubit n_v+n_h = flag
- For the example, kappa' = 8e is computed exactly by enumeration, so r(v,h) = e^{-E(v,h)-1}; post-selecting flag=1 (probability Z/(8e) ~ 0.40) gives outcome probabilities e^{-E(v,h)}/Z with Z = 6 + e + e^{-1} on qubits 0..2

## Assumptions

- The scoped construction (quantum rejection sampling from a product proposal to prepare the Gibbs state of an RBM) is a reconstruction choice; the abstract does not describe the algorithm.
- Binary {0,1} units, unit temperature, RBM (bipartite) energy; full-BM intra-layer couplings are not supported by the instance format.
- Proposal means mu_i, nu_j are strictly inside (0,1) so that Q > 0 and the ratio is finite.
- The Grover operator used for amplitude amplification is A S_0 A^dagger S_f with S_f = Z on the flag and S_0 = reflection about |0...0> on all qubits; its global sign is irrelevant.
- Total qubits n_v + n_h + 1 are capped at 12; the per-configuration multi-controlled rotations scale as 2^{n_v+n_h} gates and are intended only for tiny instances.

## Unresolved issues

- The actual quantum training algorithm of the paper, its complexity bounds, the treatment of full and multi-layer Boltzmann machines, and the amplitude-estimation variant for exact gradient estimation are not reconstructable from the abstract and are not implemented.
- The exact-enumeration encoding of the acceptance ratio is exponential in the number of units and does not reflect the scalable reversible-arithmetic circuit implied by the specification.
- No public validation contract was supplied; the example instance targets flag=1 post-selected frequencies e^{-E(v,h)}/Z with Z = 6 + e + e^{-1}, but this has not been verified here.

## Equation mapping

- `eq_energy`: implemented; _energy (classical evaluation of E(v,h) for each configuration inside build_circuit). The RBM energy is evaluated classically for every basis configuration; its exponential determines the per-configuration rotation angle encoded by _rejection_rotation.
- `eq_gibbs`: background; no code location. The normalised Gibbs distribution and Z define the target output statistics after post-selection, but the circuit only needs the unnormalised weights e^{-E}; Z is never computed (it is absorbed into kappa = kappa'/Z).
- `eq_gradient`: out_of_scope; no code location. The log-likelihood gradient is classical post-processing of measured samples (and a classically computed data term); the module returns only the state-preparation operation.
- `eq_proposal_state`: implemented; _proposal_prob (Q(v,h)) and _prepare_proposal (R_y(2 arcsin sqrt(mean)) on each state qubit). The product proposal distribution is computed classically for the ratios and prepared coherently by single-qubit R_y rotations; for means 1/2 this is R_y(pi/2) = H up to phase.
- `eq_rejection_rotation`: implemented; _rejection_rotation (multi-controlled RYGate(2 arcsin sqrt(r(v,h))) on the flag for each configuration). Implemented without the b-bit ratio register: the acceptance ratio exp(-E)/(kappa' Q) is computed classically per configuration and encoded exactly as a controlled R_y amplitude, which equals the specified map after uncomputation of the ratio register in the b -> infinity limit.
- `eq_postselect`: implemented; build_circuit loop over aa_rounds with _reflect_about_zero (Grover operator A S_0 A^dagger S_f); post-selection itself is left to the runner. The circuit produces the flagged state whose flag=1 branch is |psi_P>/sqrt(kappa); optional amplitude-amplification rounds are implemented as the Grover operator. The measurement/post-selection and the N_AA formula are not executed in the module (aa_rounds is an instance input).
- `eq_estimator`: out_of_scope; no code location. Sample-mean estimation, Hoeffding bound and the gradient-ascent update are classical post-processing of measurement outcomes, which the module does not perform.

## Specification changes

- eq_rejection_rotation: The b-qubit fixed-point ratio register and the reversible arithmetic that writes P/(kappa Q) into it are removed; the acceptance ratio is computed classically for every one of the 2^{n_v+n_h} configurations and encoded exactly with one multi-controlled R_y rotation per configuration (X-conjugation for zero-valued controls). Registers are therefore n_v + n_h + 1 qubits only. Reason: For the tiny instances allowed under the 12-qubit cap, direct enumeration is exact and avoids the 2^{-b} rounding error and the unspecified arithmetic circuit; the resulting unitary is the b -> infinity ideal of the specified map (with the ratio register already uncomputed). This does not scale to large models and is not the paper's claimed efficient method.
- eq_proposal_state, eq_rejection_rotation: Physical qubit ordering: v_1 is placed at Qiskit index 0 (least significant bit), followed by v_2..v_{n_v}, then h_1..h_{n_h}, then the flag at the highest index. The specification described v_1 as the first / most significant qubit of |v_1...v_{n_v}>|h_1...h_{n_h}>. Reason: Qiskit's little-endian convention; a measured bitstring reads (flag, h_{n_h}..h_1, v_{n_v}..v_1) from most to least significant bit.
- eq_rejection_rotation, eq_postselect: kappa' defaults to the exact maximum of exp(-E)/Q obtained by enumeration (so max r(v,h) = 1); an instance may supply a larger kappa' but not a smaller one. The number of amplitude-amplification rounds is an instance parameter aa_rounds (default 0) rather than being computed from the N_AA formula, since that formula requires Z (hence kappa = kappa'/Z), which the circuit never computes. Reason: Keeps the operation deterministic and exact for the tiny instance; the runner may choose aa_rounds using the known Z for the example.
- eq_postselect, eq_estimator, eq_gradient: Scope narrowed to the state-preparation unitary only: measurement of the flag, post-selection, sampling of the state register, the estimator and the gradient update are not part of the module. Reason: The required output is a measurement-free unitary operation; sampling and classical post-processing are performed by the runner.
