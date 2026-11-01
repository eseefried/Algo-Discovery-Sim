# Equation to Qiskit

One-qubit fixed-point amplitude amplification with Yoder-Low-Chuang Chebyshev phases. The circuit prepares A|0> = Ry(2*theta)|0> with sin^2(theta) = lambda and good state |1>. It then applies d pairs of S_t(beta_j) = P(beta_j) and S_s(alpha_j) = A X P(alpha_j) X A^dagger, so L = 2d+1 uses of A in total. The phases are computed classically from epsilon and d.

Source equation run: `aa0fa66b-5be1-4cf8-9a23-9c06bd86f21d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: search register S (single qubit, little-endian index 0); A = Ry(2*theta) with sin^2(theta)=lambda; good state |1>, bad state |0>
- no flag or control ancilla: S_t is a direct phase gate on |1> and S_s uses X-conjugated phase on |0> between A^dagger and A

## Assumptions

- The phase schedule and ordering are the Yoder-Low-Chuang form, not confirmed as the paper's own schedule
- lambda is in (0,1], epsilon is in [1e-12,1), and d is an integer in [1,500]
- Global phase conventions are irrelevant to the good-state probability
- Software later checks numerically that failure is at most epsilon over the intended lambda range

## Unresolved issues

- The paper's exact schedule for the quadratic-speedup version may differ from the Yoder-Low-Chuang phases used here
- Application order of the pairs (j increasing first) is assumed and is not verified here
- The relation between d and lambda_min (smallest sufficient L) is left to the caller
- The eq_4 normalization and sign conventions are not implemented

## Equation mapping

- `eq_1`: implemented; build_circuit (qc.p(betas[j],0) for S_t) and _start_reflection (S_s). S_t(b) = I-(1-e^{ib})|1><1| = P(b). S_s(a) = A (X P(a) X) A^dagger, with X P(a) X = diag(e^{ia},1) = I-(1-e^{ia})|0><0|.
- `eq_2`: implemented; build_circuit main loop. Applies A, then for j=1..d the sequence S_t(beta_j) followed by S_s(alpha_j), i.e. S_s(alpha_d)S_t(beta_d)...S_s(alpha_1)S_t(beta_1)A|0>. This is L=2d+1 uses of A/A^dagger, with d oracle S_t queries.
- `eq_3`: implemented; _phases. alpha_j = 2 arccot(tan(2 pi j/L) sqrt(1-gamma^2)) for j=1..d, with gamma = 1/cosh(arccosh(1/sqrt(eps))/L). beta_j = -alpha_{d-j+1}, replacing the specification's alpha_j = beta_{L-j+1}.
- `eq_4`: background; no code location. Chebyshev amplitude/failure formula is the analytic guarantee, not constructed in the circuit. The circuit realizes the phase sequence whose good amplitude is this polynomial type.
- `eq_5`: background; no code location. The L versus lambda_min scaling and the failure guarantee are targets for later checking. L is not computed from lambda_min; the caller supplies d.

## Specification changes

- eq_2: Oracle query count: S_t is applied d=(L-1)/2 times; L=2d+1 counts all uses of A and A^dagger (1 initial plus 2 per pair). The ordering is fixed as S_t(beta_j) then S_s(alpha_j) for j=1..d, applied to A|0>. Reason: Matches the Yoder-Low-Chuang fixed-point search structure; the specification's 'L applications of S_t' and ordering were unresolved.
- eq_3: Phase symmetry corrected to beta_j = -alpha_{d-j+1} with j=1..d (d=(L-1)/2), instead of alpha_j = beta_{L-j+1}. cot^{-1} is implemented as atan2(1,x), whose branch choice only changes alpha by multiples of 2 pi. Reason: The specification's indexing range and sign were flagged as unfixed. The sign and index form follows the recalled Yoder-Low-Chuang schedule.
- eq_5: L is not derived from lambda_min and epsilon. The instance supplies integer d directly, and lambda_min is not an input. Reason: The exact L formula was approximate and the specification said to choose the smallest odd L numerically, which this module cannot do without simulation.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to a single-qubit A = Ry(2 theta) and good state |1>, with no flag or control ancilla. The initial A is included in the operation, so the circuit is the full amplification unitary applied to |0>. Reason: The specification named a tiny instance. The extra registers are optional in the specification, and the multi-qubit general-n construction is out of scope.
