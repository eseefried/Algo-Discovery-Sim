# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Fixed-point amplitude amplification with quadratic speedup: given A|0>=sqrt(lambda)|good>+sqrt(1-lambda)|bad>, a known lower bound lambda_min, and failure tolerance epsilon, use L=2d+1 oracle queries with Chebyshev-derived phases so the failure probability is <= epsilon for all lambda in [lambda_min,1].

Scope: One tiny instance: A is a single-qubit Ry(2 theta) with sin(theta)=sqrt(lambda), a single good state |1>, L=3 or 5, user-chosen epsilon. The oracle is a phase-parametrized marking, S_s is a phase on A|0>. Phases are computed classically in the Yoder-Low-Chuang form and sin-scan of lambda is run in simulation. The paper's proof of optimality and range-broadness, and the general-n multi-qubit construction, are out of scope.

## Symbols

- $\lambda$: initial overlap (success probability) with good subspace; domain: (0,1]
- $\lambda_{\min}$: known lower bound on lambda; domain: (0,1]
- $\epsilon,\ \delta=\sqrt{\epsilon}$: failure probability bound and its square root; domain: (0,1)
- $L=2d+1$: number of oracle queries (odd); domain: positive odd integer
- $T_L$: Chebyshev polynomial of the first kind of degree L; domain: polynomial
- $\gamma$: 1/T_{1/L}(1/\delta), where T_{1/L}(x)=cosh((1/L) arccosh x) for x>=1; domain: (0,1)
- $\alpha_j,\beta_j$: target and start reflection phases; domain: real, mod 2 pi
- $S_t(a),S_s(b)$: phase-controlled reflections about good state and about A|0>; domain: unitaries on S plus flag

## eq_1: Generalized reflections

$$
S_t(a)=I-(1-e^{ia})|good\rangle\langle good|,\quad S_s(b)=I-(1-e^{ib})A|0\rangle\langle0|A^\dagger
$$

Phase-parametrized target and start reflections; a=b=pi gives Grover.

Provenance: `standard_background`. Standard generalized amplitude amplification form, given in the sketch.

Equation assumptions:

- Good state marked by a flag or phase oracle, one query per S_t

## eq_2: Query sequence

$$
U=\prod_{j=1}^{d}\left[S_s(\beta_j)\,A\ldots\right]\ \text{with}\ L=2d+1\ \text{applications of}\ S_t,\ \text{final state}\ U|0\rangle
$$

Alternating S_t and S_s with phases chosen by the schedule. The exact ordering and the handling of the extra (L+1)/2 versus (L-1)/2 reflections need to be fixed when implementing, and the final good amplitude is a degree-L polynomial in sqrt(lambda).

Provenance: `assumption`. The ordering is not stated in the abstract; the sketch only gives L=2d+1 queries.

Equation assumptions:

- Ordering follows Yoder-Low-Chuang fixed-point search (S_s S_t pairs applied to A|0>)

## eq_3: Phase schedule

$$
\alpha_j=\beta_{L-j+1}=2\cot^{-1}\!\left(\tan(2\pi j/L)\sqrt{1-\gamma^2}\right),\ \gamma=1/T_{1/L}(1/\delta),\ \delta=\sqrt{\epsilon}
$$

Yoder-Low-Chuang style phases computed classically.

Provenance: `standard_background`. Recalled from the sketch; the paper's own schedule for the quadratic-speedup version may differ, and the indexing range for j is not fixed here.

Equation assumptions:

- j runs over 1..(L+1)/2 with the symmetric extension; verify numerically that failure <= epsilon

## eq_4: Chebyshev amplitude

$$
P_L(x)=T_L\big(T_{1/L}(1/\delta)\,x\big)\ \text{up to normalization},\ x=\sin\theta=\sqrt{\lambda},\ \text{failure}=1-|P_L|^2$
$$

The good amplitude is a Chebyshev-type polynomial; equiripple |P|>= sqrt(1-epsilon) for x>=sqrt(lambda_min).

Provenance: `abstract_inferred`. Inferred from the claim of an adjustable failure bound over a broadest range; the explicit Chebyshev form is from the sketch.

Abstract evidence: guarantees that this bound is satisfied over the broadest possible range of $\lambda$

Equation assumptions:

- Exact normalization and sign conventions to be fixed numerically

## eq_5: Query count and target

$$
L\approx \frac{\log(2/\sqrt{\epsilon})}{\sqrt{\lambda_{\min}}},\quad 1-P_{succ}(\lambda)\le\epsilon\ \ \forall\lambda\in[\lambda_{\min},1]
$$

Query scaling O(lambda_min^{-1/2} log(1/sqrt(epsilon))) and the guarantee to be tested.

Provenance: `abstract_inferred`. The adjustable failure bound and speedup are in the abstract; the exact L formula is from the sketch and is approximate. Choose the smallest odd L that gives the bound numerically.

Abstract evidence: Our result incorporates an adjustable bound on the failure probability

Equation assumptions:

- L rounded up to odd integer

## Registers

- S: 1 (tiny instance; n in general) qubits; search register holding A|0>, good state |1>
- a: 1 qubits; oracle flag qubit for phase-parametrized marking (may be dropped if phase is applied directly on S)
- c: 1 qubits; optional control/ancilla for multi-controlled phase in S_s

## Initial state

|0>^{n} on S, flag and control in |0>

## Measurement

Measure the S register (or flag) in the computational basis; the good-state probability is the success estimate. Mind Qiskit little-endian ordering.

## Classical postprocessing

Estimate P_succ per lambda, check >= 1-epsilon for lambda>=lambda_min.

## Algorithm steps

1. Classically compute L, gamma, and the phases alpha_j, beta_j from epsilon and lambda_min. (eq_3, eq_5)
2. Prepare A|0> with Ry(2 theta), theta=arcsin(sqrt(lambda)). (eq_4)
3. Apply L alternations of S_t(alpha_j) (one oracle query each, via controlled-phase on the flag) and S_s(beta_j) (A^dagger, phase on |0>, A). (eq_1, eq_2)
4. Scan lambda by varying the Ry angle and compare the good probability with 1-epsilon. (eq_4, eq_5)

## Assumptions

- lambda_min known; epsilon user-chosen
- A^dagger free; only S_t placements count as queries
- Tiny instance with single-qubit Ry A
- Phases are from the Yoder-Low-Chuang form, not verified to be the paper's schedule

## Missing information

- The paper's exact phase schedule and ordering for the quadratic-speedup version
- Precise relation between L and lambda_min
- Handling of sign and global-phase conventions
