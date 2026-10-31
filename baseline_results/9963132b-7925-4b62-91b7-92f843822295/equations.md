# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Fixed-point amplitude amplification: given a state-preparation unitary A with A|0> = sqrt(lambda)|t> + sqrt(1-lambda)|t_perp> and an oracle marking target states, amplify the target amplitude so that the success probability is at least 1-delta^2 for every unknown lambda >= w (a known lower bound), using O(log(1/delta)/sqrt(w)) oracle queries, i.e. retaining the Grover quadratic speedup while avoiding the souffle/overshoot problem of standard Grover search.

Scope: One smallest useful construction: a single-target search instance on n=2 qubits with A = H⊗H, target |11>, so lambda = 1/4, using one generalized Grover iteration (L = 3 oracle queries, l = 1 phase pair) with phases set by the Chebyshev-based fixed-point schedule for a chosen failure bound delta = 1/2 (so the guaranteed range w = 1 - gamma^2 ≈ 0.17 covers lambda = 1/4). Out of scope: the paper's optimality proof ('broadest possible range of lambda for a given number of queries'), the general-L derivation, oblivious/multi-target extensions, derandomization, and implementation of the generalized phase oracle via ancilla. The phase-schedule and success-probability formulas are recalled from knowledge of the published fixed-point method, not extracted from the abstract, and are unverified here.

## Symbols

- $\lambda$: Fraction (probability weight) of the initial state lying in the target subspace; unknown to the algorithm; domain: [0,1]
- $w$: Known lower bound on lambda for which the success guarantee must hold; domain: (0,1]
- $\delta$: Adjustable bound: failure probability is at most delta^2 whenever lambda >= w; domain: (0,1)
- $A$: State-preparation unitary, |s> = A|0>^{\otimes n}; domain: U(2^n)
- $|t\rangle, |t_\perp\rangle$: Normalized projection of |s> onto the target subspace and onto its orthogonal complement; domain: unit vectors in C^{2^n}
- $S_t(\beta), S_s(\alpha)$: Generalized (partial-phase) reflections about the target state and about the initial state; domain: U(2^n)
- $L = 2l+1$: Total number of oracle queries (odd); l is the number of generalized Grover iterations; domain: odd positive integers
- $\alpha_j, \beta_j$: Phase angles of the j-th generalized Grover iteration, j = 1..l; domain: real angles mod 2\pi
- $\gamma$: Chebyshev scale parameter, gamma^{-1} = T_{1/L}(1/delta); the guaranteed range is lambda >= 1-gamma^2; domain: (0,1)
- $T_L(x)$: Chebyshev polynomial of the first kind of degree L (cos(L arccos x) for |x|<=1, cosh(L arccosh x) for x>1); T_{1/L} denotes the fractional-order analogue; domain: real function
- $P_L(\lambda)$: Probability that measuring the final state yields a target state after L queries; domain: [0,1]
- $n$: Number of system qubits (n = 2 in the scoped instance); domain: positive integer

## eq_1: Initial state decomposition

$$
|s\rangle = A|0\rangle^{\otimes n} = \sqrt{\lambda}\,|t\rangle + \sqrt{1-\lambda}\,|t_\perp\rangle,\qquad \lambda = \|\Pi_{\mathrm{target}}|s\rangle\|^2
$$

The initial state splits into target and non-target components; lambda is the squared weight on targets, unknown to the algorithm.

Provenance: `abstract_inferred`. The abstract defines lambda as the target fraction of the initial state; the standard two-dimensional amplitude-amplification decomposition expresses this exactly.

Abstract evidence: what fraction $\lambda$ of the initial state is comprised of the target states

Equation assumptions:

- Multiple targets are collected into one normalized vector |t>; A is a unitary acting on n qubits.

## eq_2: Generalized phase reflections and Grover iterate

$$
S_t(\beta) = I - (1-e^{-i\beta})|t\rangle\langle t|,\quad S_s(\alpha) = I - (1-e^{-i\alpha})|s\rangle\langle s| = A\,S_0(\alpha)\,A^\dagger,\quad G(\alpha,\beta) = -\,S_s(\alpha)\,S_t(\beta)
$$

Partial-phase oracle about the target and partial-phase reflection about the initial state; beta = alpha = pi recovers the standard Grover iterate.

Provenance: `standard_background`. Standard generalized amplitude amplification operators (Grover/Hoyer/Long form) recalled from background; S_t(beta) is a phase oracle call counted as one query.

Equation assumptions:

- Sign and phase conventions as written; other conventions (e^{+i\beta}) give equivalent schedules with sign flips.

## eq_3: Fixed-point phase schedule (recalled, unverified)

$$
S_L = G(\alpha_l,\beta_l)\cdots G(\alpha_1,\beta_1),\quad \alpha_j = -\beta_{l-j+1} = 2\cot^{-1}\!\Big(\tan\tfrac{2\pi j}{L}\,\sqrt{1-\gamma^2}\Big),\quad \gamma^{-1} = T_{1/L}(1/\delta) = \cosh\!\Big(\tfrac{1}{L}\cosh^{-1}(1/\delta)\Big)
$$

Phase sequence of length l = (L-1)/2 determined entirely by (L, delta) through a Chebyshev scale parameter; this is the schedule of the fixed-point amplitude amplification method as recalled from knowledge.

Provenance: `standard_background`. The abstract does not state any phase formula; this is the published fixed-point schedule (Yoder–Low–Chuang) recalled from background knowledge, offered as the concrete construction to be implemented, and should be checked against the paper before use.

Equation assumptions:

- L is odd; the total query count is L = 2l+1 counting the oracle inside S_t only.
- The formula is recalled, not extracted or verified here.

## eq_4: Success probability (recalled, unverified)

$$
P_L(\lambda) = |\langle t|S_L|s\rangle|^2 = 1 - \delta^2\,T_L\!\big(T_{1/L}(1/\delta)\,\sqrt{1-\lambda}\big)^2
$$

Closed-form success probability as an L-th degree Chebyshev polynomial in sqrt(1-lambda); its oscillations are bounded by delta^2 for lambda in the guaranteed range.

Provenance: `standard_background`. Chebyshev characterization of the fixed-point response, recalled from knowledge of the method; this is the quantity whose minimax property underlies the 'broadest possible range' claim but that proof is outside scope.

Equation assumptions:

- Exact equality holds only under the phase conventions of eq_2 and eq_3.

## eq_5: Fixed-point guarantee and query complexity

$$
P_L(\lambda) \ge 1-\delta^2 \quad \forall\,\lambda \ge w := 1-\gamma^2,\qquad L \ge \frac{\ln(2/\delta)}{\sqrt{w}} \;\Rightarrow\; L = O\!\Big(\frac{\log(1/\delta)}{\sqrt{w}}\Big)
$$

For any lambda at least the known bound w, the failure probability is at most delta^2 (fixed point, no overshoot), with a number of queries scaling as 1/sqrt(w): the quadratic Grover speedup is retained up to a log(1/delta) factor.

Provenance: `abstract_inferred`. The abstract claims fixed-point behavior with an adjustable failure bound and preserved speedup; combined with eq_4 (|T_L| <= 1 on [-1,1]) this gives the stated inequality, and the 1/sqrt(w) scaling with a log(1/delta) prefactor is the recalled quantitative form.

Abstract evidence: achieves fixed-point behavior without sacrificing the quantum speedup. Our result incorporates an adjustable bound on the failure probability

Equation assumptions:

- The explicit prefactor ln(2/delta) is recalled from background and not established by the abstract.

## eq_6: Scoped tiny instance

$$
n=2,\; A = H\otimes H,\; |t\rangle = |11\rangle,\; \lambda = \tfrac14,\; \delta = \tfrac12,\; L = 3,\; l = 1,\; \gamma^{-1} = \cosh\!\big(\tfrac13\cosh^{-1}2\big),\; w = 1-\gamma^2,\; \alpha_1 = -\beta_1 = 2\cot^{-1}\!\big(\tan\tfrac{2\pi}{3}\sqrt{w}\big),\; S_0(\alpha)=I-(1-e^{-i\alpha})|00\rangle\langle 00|
$$

Concrete instance: uniform superposition on two qubits, single marked state |11>, one generalized Grover iteration with fixed-point phases; w evaluates to approximately 0.17 < lambda, so eq_5 guarantees P_3 >= 3/4 for this and for any lambda in [w,1].

Provenance: `assumption`. No experiment scope was supplied; this is the smallest instance exercising a non-trivial (non-pi) phase pair, chosen so the guaranteed range covers lambda = 1/4 and the circuit fits on two qubits without ancilla (controlled-phase gates realize S_t and S_0).

Equation assumptions:

- Numerical values of gamma, w, alpha_1 follow from the recalled eq_3 and are to be evaluated classically; they are not sourced from the abstract.

## Registers

- sys: n (= 2 in the scoped instance) qubits; System register holding |s> = A|0...0>; qubit ordering q_1 q_0 with |11> the target in the instance; the oracle S_t(beta) acts as a controlled phase on the target basis state and S_0(alpha) as a phase on |00>.

## Initial state

|0\rangle^{\otimes n} on sys, then A applied to give |s\rangle = \sqrt{\lambda}|t\rangle + \sqrt{1-\lambda}|t_\perp\rangle (eq_1); for the instance |s\rangle = (H\otimes H)|00\rangle, \lambda = 1/4.

## Measurement

Measure all n sys qubits in the computational basis; a shot succeeds if the outcome lies in the target set (outcome 11 in the instance). The empirical success frequency estimates P_L(lambda) of eq_4.

## Classical postprocessing

Optionally verify each outcome with a classical oracle check. Compare the observed success frequency with the guaranteed bound 1-delta^2 (eq_5) and, for the instance, with the value of eq_4 at lambda = 1/4; repeat the whole procedure O(1) times if a single-shot success probability of 1-delta^2 is insufficient.

## Algorithm steps

1. Classical preprocessing: choose failure bound delta and query budget L = 2l+1 (or choose w and set L from eq_5); compute gamma^{-1} = T_{1/L}(1/delta) and the phase pairs (alpha_j, beta_j), j = 1..l, from eq_3. Instance: delta = 1/2, L = 3, l = 1. (eq_3, eq_5, eq_6)
2. Prepare the initial state by applying A to |0>^{⊗n} on sys. (eq_1)
3. For j = 1..l: apply the generalized oracle S_t(beta_j) (phase e^{-i beta_j} on target states), then apply S_s(alpha_j) = A S_0(alpha_j) A^† (phase e^{-i alpha_j} on |0...0> conjugated by A), with the overall sign in G(alpha,beta) being a global phase that may be dropped. Instance: a single iteration with alpha_1 = -beta_1 from eq_6. (eq_2, eq_3, eq_6)
4. The resulting state S_L|s> has target weight P_L(lambda) given by eq_4, bounded below by 1-delta^2 whenever lambda >= w. (eq_4, eq_5)

## Assumptions

- No experiment scope was given; the n=2, single-target, L=3, delta=1/2 instance is a chosen smallest useful construction.
- Phase conventions of eq_2 (e^{-i beta}, e^{-i alpha}, overall minus sign) are assumed; alternative conventions change signs of alpha_j, beta_j.
- The phase schedule and Chebyshev success-probability formulas (eq_3, eq_4) are recalled from knowledge of the published fixed-point amplitude amplification method, not extracted from the abstract, and have not been verified here.
- The generalized phase oracle S_t(beta) is assumed to be available as a single query; in the instance it is a two-qubit controlled-phase gate with no ancilla.
- Query counting treats each S_t application as one oracle call and ignores the cost of A, A^†.

## Missing information

- The abstract gives no explicit phase formulas, Chebyshev construction, or closed-form success probability; these are supplied from background and must be checked against the paper.
- The precise statement and proof of optimality ('broadest possible range of lambda for a given number of oracle queries') and the exact query-count prefactor.
- Treatment of even L, multiple target states with phase oracles, and whether an ancilla is required for a general-phase oracle in the paper's construction.
- Any numerical results or benchmarks of the paper.
