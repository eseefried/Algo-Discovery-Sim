# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Success probability and optimal iteration count of a Grover-like two-reflection search (stand-in for the optimized quantum random-walk search) when the oracle and diffusion inversion phases carry systematic offsets: a = pi + d1, b = pi + d2, for one marked item among N = 2^n.

Scope: Single marked item, small n (<= 6, so n+1 <= 7 qubits). Build the generalized Grover iteration with phase-error offsets, one oracle query per iteration. Compute P_k from the exact 2x2 reduced matrix and compare it with the simulated marked-state frequency. Sweep k to find the maximizing k. The paper's specific optimized random-walk operator and tuned phase values are NOT recovered. Comparison with the Grover baseline uses the ideal Grover phases plus the same errors.

## Symbols

- $N$: database size, N=2^n; domain: integer power of 2, N>=4
- $n$: number of data qubits; domain: positive integer, n<=6
- $|s\rangle$: uniform superposition over all N items; domain: state in C^N
- $|w\rangle$: marked basis state; domain: computational basis state
- $\lambda$: overlap sin of the initial angle, \langle w|s\rangle=1/\sqrt{N}; domain: real in (0,1)
- $a,b$: oracle and diffusion inversion phases; domain: real, radians
- $\delta_1,\delta_2$: systematic phase errors, a=\pi+\delta_1, b=\pi+\delta_2; domain: real, small radians
- $k$: number of iterations (equals number of oracle queries); domain: nonnegative integer
- $P_k$: marked-state probability after k iterations; domain: [0,1]
- $Q$: one-iteration operator, diffusion times oracle; domain: unitary on span{|w>,|w_perp>}

## eq_1: Phase-inversion oracle and diffusion

$$
O=I-(1-e^{ia})|w\rangle\langle w|,\quad D=I-(1-e^{ib})|s\rangle\langle s|=H^{\otimes n}\big(I-(1-e^{ib})|0\rangle\langle 0|\big)H^{\otimes n}
$$

Generalized phase-inversion oracle and diffusion. Ideal Grover uses a=b=pi, with a global sign on D.

Provenance: `standard_background`. Standard generalized amplitude-amplification operators. The abstract names phase inversions with errors but gives no formulas.

Equation assumptions:

- Single marked item
- Diffusion phase b is the same on every iteration

## eq_2: Iteration operator and state

$$
Q=D\,O,\quad |\psi_k\rangle=Q^k|s\rangle,\quad P_k=|\langle w|Q^k|s\rangle|^2
$$

Success probability after k iterations, with a=pi+delta_1 and b=pi+delta_2.

Provenance: `abstract_inferred`. This relationship implies that P_k is a function of N, k and the errors. The explicit form here is my own construction.

Abstract evidence: the relationship between the success rate of the algorithm, the database size, the number of iterations and the phase error is depicted

Equation assumptions:

- Optimized random-walk search is modeled as this two-reflection iteration

## eq_3: Reduced 2x2 matrix in basis {|w>,|w_perp>}

$$
|s\rangle=\lambda|w\rangle+\sqrt{1-\lambda^2}|w_\perp\rangle,\ \lambda=1/\sqrt N;\ Q=\big(I-(1-e^{ib})|s\rangle\langle s|\big)\,\mathrm{diag}(e^{ia},1)
$$

Q restricted to the invariant 2D plane, where |s> has real components (lambda, sqrt(1-lambda^2)).

Provenance: `standard_background`. The geometric picture in the abstract is the 2D invariant subspace. The matrix follows from eq_1.

## eq_4: Eigen-decomposition form of P_k

$$
Q\sim e^{i\gamma}\exp\!\big(-i\,\theta_{\rm eff}\,\hat n\cdot\vec\sigma\big),\quad P_k=\Big|\sum_{j=\pm}c_j e^{-ik\theta_j}\Big|^2=A\sin^2(k\theta_{\rm eff}+\phi)+\text{offset}
$$

Q is an SU(2) rotation times a phase, with eigenphases e^{-i theta_j}. P_k oscillates at theta_eff. A, phi and offset are computed numerically from the eigenvectors of eq_3, with cos(theta_eff)=Re tr(Q)/2 up to the phase.

Provenance: `assumption`. The sketch proposes this form via Chebyshev/Bloch analysis. The abstract does not give it.

Equation assumptions:

- Exact closed forms for A, phi, offset are not supplied; use numerical diagonalization

## eq_5: Maximum success and optimal iteration count

$$
P_{\max}=\max_{k\in\mathbb Z_{\ge0}}P_k\approx A+\text{offset},\quad k_{\rm opt}=\mathrm{round}\!\big((\pi/2-\phi)/\theta_{\rm eff}\big)
$$

Maximum success rate and the iteration count that achieves it, found by a sweep over k.

Provenance: `abstract_inferred`. The abstract claims both quantities are given. The formula is inferred from the sin^2 form, and the rounding is an approximation.

Abstract evidence: we give both the maximum success rate of the algorithm and the required number of iterations when the algorithm is in the presence of phase errors

Equation assumptions:

- k_opt from the formula is approximate; verify with the sweep

## Registers

- data: n qubits; indexes N=2^n items, little-endian integer encoding, marked item w as bitstring
- anc: 1 qubits; oracle ancilla in |-> for phase kickback; optional. Total qubits n+1 <= 7

## Initial state

All qubits |0>, then H on each data qubit gives |s>. The ancilla is prepared in |-> by X then H if used.

## Measurement

Measure the n data qubits (not the ancilla) after k iterations. The frequency of the marked bitstring estimates P_k. Respect Qiskit little-endian bit order in the counts keys.

## Classical postprocessing

Sweep k, compare the simulated marked-state frequency or exact probability with the eq_2/eq_3 prediction, and select k maximizing P_k. Compare P_max(optimized) with P_max(Grover) for each error value.

## Algorithm steps

1. Prepare |s> with H on the data qubits. Prepare the ancilla in |-> if the oracle is a kickback black box. (eq_2)
2. Repeat k times: apply the oracle with phase a=pi+delta_1 (one black-box query per iteration, or a controlled-phase with an adjustable angle). (eq_1)
3. Apply the diffusion: H^n, X^n, multi-controlled phase mcp(b) with b=pi+delta_2, X^n, H^n. (eq_1, eq_3)
4. Classical sweep over k=0..K and over d. Compute the analytic P_k from the 2x2 matrix, find P_max and k_opt, and compare with the Grover baseline (ideal phases plus the same errors). (eq_4, eq_5)

## Assumptions

- Phase errors are systematic and fixed on every application, with no random noise
- Single marked item, N=2^n, n<=6
- Optimized random-walk search is modeled as a two-reflection iteration with a tunable diffusion phase, possibly plus a coin qubit
- Oracle is queryable as a phase oracle or controlled phase with an adjustable angle
- The tuned optimized phases are not known from the abstract and must be chosen by the implementer, e.g. by numerically maximizing the ideal P at about (pi/4)sqrt(N) iterations

## Missing information

- The actual optimized random-walk operator and its tuned phases
- Closed forms for theta_eff, A, phi and offset
- Numeric robustness results and the exact comparison metric against Grover
- Whether the coin qubit is part of the model
