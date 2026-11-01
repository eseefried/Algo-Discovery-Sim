# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Effect of systematic phase-inversion errors on success rate and iteration count of an optimized quantum random-walk search algorithm, compared with Grover's algorithm. The abstract gives no explicit formulas.

Scope: Smallest useful construction: Grover-type search in a 2D geometric subspace with both phase inversions replaced by phases e^{i(pi+delta)}, for N=4 and a small delta. This is a background/assumed Grover baseline only. The paper's optimized random-walk algorithm, its error model, closed-form success rate, maximum success rate and optimal iteration count are outside this scope.

## Symbols

- $N$: database size; domain: positive integer, N>=2
- $\delta$: systematic phase error in each phase inversion; domain: real, small
- $k$: number of iterations; domain: non-negative integer
- $\theta$: Grover rotation half-angle, sin(theta)=1/sqrt(N); domain: (0,pi/2)
- $P_k(\delta)$: success probability after k iterations with phase error; domain: [0,1]
- $|w\rangle$: marked state; domain: computational basis state
- $|s\rangle$: uniform superposition; domain: N-dimensional Hilbert space

## eq_1: Initial state geometry

$$
|s\rangle=\sin\theta\,|w\rangle+\cos\theta\,|w^\perp\rangle,\quad \sin\theta=1/\sqrt{N}
$$

Standard two-dimensional geometric picture of search starting from the uniform state.

Provenance: `standard_background`. Background Grover geometry; the abstract only mentions a geometric description without giving it.

Equation assumptions:

- Uniform initial state
- single marked item

## eq_2: Phase-error iteration

$$
G(\delta)=-\,U_s(\delta)\,U_w(\delta),\quad U_w(\delta)=I-(1-e^{i(\pi+\delta)}\cdot(-1))|w\rangle\langle w|\ \text{i.e.}\ I+(e^{i\delta}-1)\,(-1)\cdots
$$

Placeholder form is replaced by the cleaner equation eq_3; do not use this equation.

Provenance: `assumption`. Superseded by eq_3.

Equation assumptions:

- Superseded

## eq_3: Phase-inversion with error

$$
U_w(\delta)=I-(1-e^{i\delta})\,|w\rangle\langle w|\cdot(-1)^{0}-2|w\rangle\langle w|\ \ \text{(not used)}
$$

Not used; kept out of the algorithm steps.

Provenance: `assumption`. The specific error model of the paper is unknown, so none is asserted.

Equation assumptions:

- Not used

## eq_4: Assumed generalized phase rotation

$$
R_\phi(|a\rangle)=I+(e^{i\phi}-1)|a\rangle\langle a|,\quad \phi=\pi+\delta
$$

Assumed model of an erroneous phase inversion about a state |a>; delta=0 gives the ideal reflection.

Provenance: `assumption`. A common way to model a systematic phase error, not stated in the abstract.

Equation assumptions:

- Same delta for both inversions

## eq_5: Iteration with errors and success rate

$$
G_\delta=-R_{\pi+\delta}(|s\rangle)\,R_{\pi+\delta}(|w\rangle),\quad P_k(\delta)=|\langle w|G_\delta^k|s\rangle|^2
$$

Assumed iteration operator and success probability for the Grover baseline with phase errors.

Provenance: `assumption`. Abstract states that the success rate depends on N, iterations and phase error, but not the formula; this is a proposed construction.

Equation assumptions:

- Grover baseline instead of the paper's optimized random-walk operator

## Registers

- search: 2 qubits (N=4) qubits; database index register, basis state encoded as integer 0..3

## Initial state

Uniform superposition |s> = H^{\otimes 2}|00>, with marked item assumed to be |11>.

## Measurement

Measure the search register in the computational basis; success if the marked item is observed.

## Classical postprocessing

Estimate P_k(delta) from repeated shots or exact simulation and select k maximizing it for given delta; compare against the random-walk variant if its operator becomes available.

## Algorithm steps

1. Prepare the uniform superposition on the search register. (eq_1)
2. Apply k iterations of the phase-error iteration operator, using assumed erroneous phase inversions about the marked state and |s>. (eq_4, eq_5)
3. Compute P_k(delta) for several delta and k to find maximum success rate and best k (numerical, outside circuit). (eq_5)

## Assumptions

- No scope was supplied; chose a Grover baseline with N=4 and a uniform phase error delta.
- The error model is assumed, not taken from the paper.
- eq_2 and eq_3 are discarded drafts and not used in the algorithm.

## Missing information

- Definition of the optimized quantum random-walk search operator and graph/coin
- Exact phase error model used in the paper
- Closed-form success rate, maximum success rate and optimal iteration number
- Numerical simulation parameters and robustness comparison details
