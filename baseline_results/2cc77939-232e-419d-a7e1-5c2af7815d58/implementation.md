# Equation to Qiskit

Implements, as a single-qubit Qiskit operation, the piecewise-constant singlet-triplet (S-T_0) control propagator of the specification: for a user-supplied exchange sequence {J_k, tau_k} with fixed Overhauser gradient h, each segment exp[-i tau_k/2 ((J_k+delta J_k) sigma_z + (h+delta h) sigma_x)] is compiled exactly into standard gates ry(-a_k) rz(Omega_k tau_k) ry(a_k) with a_k = atan2(h+delta h, J_k+delta J_k) and Omega_k the Rabi frequency. Optional quasi-static error parameters delta_h (nuclear-bath gradient shift) and epsilon_J (multiplicative voltage noise, delta J_k = epsilon_J J_k) let the runner build the noisy propagator U(T) of eq_1/eq_2 for any fixed noise realization, so DCG candidates can be compared against uncorrected gates externally. The classical numerical synthesis (eq_4, eq_5) that finds the DCG sequence is not performed inside the module.

Source equation run: `4225f4fe-c4d9-4c72-ab35-92ade22b8a76`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0]: the single logical singlet-triplet qubit; computational |0> = |S> (singlet), |1> = |T_0> (triplet-zero). Exchange J acts as sigma_z, Overhauser gradient h as sigma_x.

## Assumptions

- Basis |0>=|S>, |1>=|T_0> with J along sigma_z and h along sigma_x; sign conventions may differ from the paper.
- Nuclear-bath dephasing is modelled at leading order as a quasi-static c-number shift delta_h constant over the gate; voltage noise as multiplicative epsilon_J on every J_k, also constant over the gate.
- The example sequence (h=1, N=5, J in [0,10]) is a generic bounded piecewise-constant sequence illustrating the ansatz; it is NOT claimed to be an optimized DCG satisfying eq_4.
- Units are such that hbar=1 and h sets the frequency scale; tau_k are in units of 1/h.
- Only one logical qubit; leakage to |T_+>,|T_-> and two-qubit gates are ignored.

## Unresolved issues

- No optimized DCG sequence is available from the abstract, so the example instance does not implement a verified error-cancelling gate; an external optimizer (eq_5) must supply J_k, tau_k satisfying eq_4.
- The paper's actual perturbative non-Markovian framework, cost function, constraint set and device parameters are unknown; only the quasi-static leading-order model is represented.
- Global phase of the target gate and the paper's axis conventions cannot be confirmed.

## Equation mapping

- `eq_1`: implemented; build_circuit: lines computing hx = h + delta_h and jz = jk*(1+epsilon_J) (comment 'eq_1'); _append_segment realizes exp[-i tau/2 (jz sigma_z + hx sigma_x)]. The S-T_0 Hamiltonian with J on sigma_z and h on sigma_x is realized segment by segment; the error Hamiltonian is included as quasi-static (constant over the gate) shifts delta_h and delta J_k = epsilon_J J_k supplied in the instance (zero gives the ideal Hamiltonian).
- `eq_2`: implemented; _append_segment and the loop in build_circuit (comment 'eq_2'). Piecewise-constant control with bounds J_min <= J_k <= J_max is validated in _validate; the ordered product of segment unitaries is built with segment 1 first, each segment compiled exactly into ry(-a) rz(Omega*tau) ry(a).
- `eq_3`: background; no code location. The first-order Magnus/toggling-frame expansion is the analytic motivation; the circuit implements the full (non-perturbative) propagator for a given quasi-static noise realization rather than the truncated expansion.
- `eq_4`: out_of_scope; no code location. The DCG cancellation conditions Phi_1^(h)=Phi_1^(J)=0 and U_0(T)=G are classical constraints evaluated during synthesis; the module compiles a given sequence and does not test or enforce them.
- `eq_5`: out_of_scope; no code location. Numerical minimization of the cost function is classical post-processing not representable as a unitary circuit operation and is excluded (no optimizer or operator construction inside the module).

## Specification changes

- eq_4, eq_5: Scope narrowed from DCG synthesis (numerical search for J_k, tau_k) to compilation of a user-supplied piecewise-constant sequence into a circuit. Reason: Synthesis is a classical optimization; the deliverable is a measurement-free unitary operation with no simulation or operator construction.
- eq_1, eq_3: Noise is represented as fixed quasi-static instance parameters delta_h and epsilon_J (constant across all segments) and included exactly in each segment's rotation, instead of as the truncated first-order error operator Phi_1. Reason: A circuit must be unitary and bound; a fixed noise realization yields a unitary U(T) that an external runner can compare against the ideal gate to probe leading-order cancellation.
- eq_2: Each segment exp[-i tau_k/2 (J_k sigma_z + h sigma_x)] is decomposed as ry(-a_k) rz(Omega_k tau_k) ry(a_k), a_k = atan2(h, J_k), Omega_k = sqrt(J_k^2+h^2). Reason: Exact SU(2) identity using standard gates (no dense unitaries); global phase is preserved exactly.
- eq_2: Default lower bound J_min = 0 enforced; J_max optional (enforced only if supplied). Reason: The abstract gives no explicit constraint set; non-negative exchange is the assumed realistic constraint.
