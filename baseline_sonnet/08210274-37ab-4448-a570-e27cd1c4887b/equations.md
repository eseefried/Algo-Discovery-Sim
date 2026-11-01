# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Trotterized simulation of exp(-i(A+B)t) with n Trotter steps where each elementary gate is imperfect; trade-off between Trotter (algorithmic) error decreasing with n and accumulated gate error increasing with n gives an optimum Trotter number n*.

Scope: Generic first-order Trotter formula with a simple assumed gate-error model (per-gate error epsilon, linear accumulation) yielding a toy n* scaling. Excludes the paper's actual error model, statistical-distance calculation, and exact n* result; higher-order formulas and specific Hamiltonians are out of scope.

## Symbols

- $H=A+B$: Hamiltonian split into two non-commuting parts; domain: Hermitian operators on a finite-dimensional space
- $t$: Total evolution time; domain: real, t>0
- $n$: Trotter number (number of stroboscopic steps); domain: positive integer
- $\epsilon$: Assumed error per elementary gate (imperfect application); domain: real, 0<\epsilon<<1
- $c_T$: Assumed constant of the Trotter error, proportional to ||[A,B]||; domain: real, >0
- $\delta(n)$: Assumed total error of the simulation as a function of n; domain: real, >=0
- $n^*$: Optimum Trotter number minimizing the total error; domain: positive real/integer

## eq_1: Trotter formula

$$
e^{-i(A+B)t}=\lim_{n\to\infty}\left(e^{-iAt/n}e^{-iBt/n}\right)^n
$$

Decomposition of the evolution into repeated elementary evolutions; the precision is controlled by n in the ideal case.

Provenance: `standard_background`. The abstract describes the Trotter formula as a stroboscopic sequence of elementary evolutions; this is the standard first-order form, not quoted from the abstract.

Equation assumptions:

- Two-term splitting, first order

## eq_2: Algorithmic error scaling

$$
\delta_{\mathrm{Trot}}(n)\le \frac{c_T t^2}{n},\quad c_T=\tfrac12\|[A,B]\|
$$

Standard first-order Trotter error bound in operator norm, decreasing with n.

Provenance: `standard_background`. Well-known bound; consistent with the abstract's claim that ideal precision improves with n.

Equation assumptions:

- Operator-norm error
- First-order product formula

## eq_3: Assumed gate error accumulation

$$
\delta_{\mathrm{gate}}(n)\approx 2n\epsilon
$$

Toy model: 2n gates each with error epsilon, adding linearly.

Provenance: `assumption`. The abstract only says each gate is applied imperfectly; the specific error model is a proposed assumption.

Equation assumptions:

- Two gates per step
- Independent errors adding linearly
- Fixed epsilon independent of n

## eq_4: Total error

$$
\delta(n)=\frac{c_T t^2}{n}+2n\epsilon
$$

Sum of the decreasing algorithmic error and increasing gate error; the trade-off creates a minimum.

Provenance: `abstract_inferred`. Inferred qualitatively: a trade-off implies one term decreasing and one increasing in n. The explicit functional form is assumed.

Abstract evidence: The resultant tradeoff in errors leads to an ultimate limit on the precision of the simulation.

Equation assumptions:

- Errors combine additively via eq_2 and eq_3

## eq_5: Optimum Trotter number (toy model)

$$
n^*=t\sqrt{\frac{c_T}{2\epsilon}},\quad \delta(n^*)=2t\sqrt{2c_T\epsilon}
$$

Minimizer of eq_4 from d\delta/dn=0.

Provenance: `abstract_inferred`. The abstract states that n* is calculated; this formula is the result for the assumed toy model only, not the paper's result and the paper's statistical-distance measure is not used.

Abstract evidence: We calculate the optimum Trotter number $n^{*}$ that achieves this limit

Equation assumptions:

- Continuous n, rounded to nearest integer in practice
- Validity of eq_2 to eq_4

## Registers

- sys: unknown qubits; System register holding the simulated many-body state

## Classical postprocessing

Compare the output distribution with the ideal one via a statistical distance and minimize over n; the exact distance and procedure are not given in the abstract.

## Algorithm steps

1. Split H into A and B and choose Trotter number n. (eq_1)
2. Apply n repetitions of e^{-iAt/n} then e^{-iBt/n}, each gate imperfect. (eq_1, eq_3)
3. Combine algorithmic and gate errors and minimize over n to find n*. (eq_2, eq_4, eq_5)

## Assumptions

- Two-term first-order Trotter splitting chosen as the smallest useful construction
- Linear gate-error accumulation model with constant epsilon
- Equations eq_3 to eq_5 are toy assumptions, not the paper's results

## Missing information

- Actual gate-error model (coherent, stochastic, or other)
- Definition of the statistical distance and measurement basis
- Hamiltonian and system size
- Actual formula for n* and its scaling in the paper
- Initial state and registers
