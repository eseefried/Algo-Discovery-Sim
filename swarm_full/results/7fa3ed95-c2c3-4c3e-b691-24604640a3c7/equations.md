# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Analyze Trotterized quantum simulation of unitary dynamics when each elementary gate is applied imperfectly: Trotter (algorithmic) error decreases with Trotter number n, while accumulated gate error grows with n, giving a tradeoff and an optimum n* that minimizes the statistical distance between actual and ideal simulation outcomes.

Scope: Abstract-level reconstruction of the Trotter-vs-gate-error tradeoff with a small finite illustrative model; the specific error model, Hamiltonian, and closed-form n* from the paper are not given in the abstract.

## Symbols

- $n$: Trotter number (number of repeated elementary-evolution steps); domain: positive integers
- $n^{*}$: optimum Trotter number minimizing statistical distance; domain: positive integers
- $t$: total simulated evolution time (assumed symbol); domain: real, t>0
- $H=A+B$: Hamiltonian split into two non-commuting parts (assumed example); domain: Hermitian operators
- $D(n)$: statistical distance between actual and ideal simulated outcome distributions; domain: [0,1]

## eq_1: Trotter formula

$$
e^{-i(A+B)t}\approx\left(e^{-iAt/n}e^{-iBt/n}\right)^{n}
$$

First-order Trotter decomposition of the time evolution into n repeated elementary evolutions.

Provenance: `standard_background`. Standard first-order Trotter formula; abstract only describes a stroboscopic sequence of elementary evolutions.

Equation assumptions:

- Two-term Hamiltonian, first-order product formula

## eq_2: Error tradeoff model

$$
D(n)\approx \frac{a}{n}+b\,n
$$

Assumed total error: Trotter error ~ a/n decreasing in n plus gate-error accumulation ~ b n increasing in n.

Provenance: `assumption`. Illustrative model of the tradeoff described in the abstract; coefficients a,b not given.

Equation assumptions:

- a,b>0 constants
- Leading-order scaling only

## eq_3: Optimum Trotter number

$$
n^{*}=\sqrt{a/b}
$$

Minimizer of the assumed D(n), giving the minimal distance 2\sqrt{ab}.

Provenance: `assumption`. Calculus on eq_2; the paper's actual n* is not stated in the abstract.

Equation assumptions:

- n treated as continuous

## Registers

- sys: N (symbolic number of simulated qubits) qubits; Simulator register holding the evolving many-body state

## Initial state

Assumed generic product state |0>^{\otimes N} on sys (abstract does not specify)

## Measurement

Assumed computational-basis measurement of all N qubits of sys after the n Trotter steps, repeated over many shots to estimate the outcome distribution; the abstract does not specify the observable.

## Classical postprocessing

Compare the empirical outcome distribution p_actual(n) with the ideal distribution p_ideal, computing statistical distance D(n)=1/2 sum_x |p_actual(x)-p_ideal(x)|; scan n and choose the minimizer as the estimate of n*.

## Algorithm steps

1. Prepare the assumed initial state on sys. (no equation reference)
2. Choose Trotter number n and split H=A+B (assumed two-term example). (eq_1)
3. Repeat n times: apply imperfect gate approximating e^{-iAt/n}, then imperfect gate approximating e^{-iBt/n}. (eq_1, eq_2)
4. Select n near n* to balance Trotter error and accumulated gate error. (eq_2, eq_3)

## Assumptions

- Error model D(n)=a/n+bn is an illustrative assumption, not the paper's result.
- Two-term Hamiltonian and a/n + b n error scaling
- Generic product initial state and single system register assumed; no ancillas
- Computational-basis measurement assumed; statistical distance is taken as total variation distance
- Computational-basis measurement and total variation distance assumed for postprocessing

## Missing information

- Actual Hamiltonian, gate error model, and exact n* formula
- Paper's actual measurement and observable
- Actual register structure and initial state used in the paper
