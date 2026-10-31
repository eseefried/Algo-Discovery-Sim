# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Given a target Hamiltonian H = A + B with non-commuting terms, simulate U(t) = e^{-iHt} by the first-order Trotter formula with Trotter number n, where every elementary gate is applied imperfectly. Determine the total deviation (statistical distance) between the noisy Trotterized simulation and the ideal evolution as a function of n, and find the optimum Trotter number n^{*} that minimizes it.

Scope: Smallest useful construction chosen (no experiment_scope supplied): a 2-qubit transverse-field Ising Hamiltonian H = A + B with A = J X_1 X_2, B = h (Z_1 + Z_2), J = h = 1, evolution time t = 1, first-order (Lie-Trotter) product formula, initial state |00>, and a generic per-gate error model in which each elementary gate adds at most epsilon to the trace distance. The reconstruction covers the n-dependence tradeoff D(n) <= c_1/n + c_2 n and the resulting continuous-optimum n^{*} = sqrt(c_1/c_2). Outside scope: the paper's specific gate-error model, its exact definition of statistical distance, any higher-order Trotter formulas, its specific many-body model, and the exact (non-bound) expression it derives for n^{*}.

## Symbols

- $H$: Target Hamiltonian to be simulated, H = A + B; domain: Hermitian operator on (C^2)^{\otimes 2}
- $A, B$: Non-commuting elementary Hamiltonian terms whose exponentials are the elementary evolutions; domain: Hermitian operators on (C^2)^{\otimes 2}
- $t$: Total simulated evolution time; domain: t > 0, instance value t = 1
- $n$: Trotter number: number of repetitions of the elementary evolution sequence; domain: positive integer
- $n^{*}$: Optimum Trotter number minimizing the total statistical distance; domain: positive integer (or positive real before rounding)
- $U(t)$: Ideal unitary e^{-iHt}; domain: unitary on (C^2)^{\otimes 2}
- $U_n(t)$: First-order Trotter approximation to U(t) with n steps; domain: unitary on (C^2)^{\otimes 2}
- $\epsilon$: Per-gate error strength (upper bound on trace-distance increment caused by one imperfect elementary gate); domain: 0 \le \epsilon \ll 1
- $\rho_{\mathrm{ideal}}, \rho_n$: Output state of the ideal evolution and of the noisy n-step Trotter simulation, respectively; domain: density operators on (C^2)^{\otimes 2}
- $D(\rho,\sigma)$: Statistical (trace) distance between two states; domain: [0,1]
- $c_1, c_2$: Coefficients of the Trotter-error term (∝1/n) and the accumulated gate-error term (∝n) in the total distance bound; domain: non-negative reals

## eq_1: First-order Trotter (Lie-Trotter) decomposition

$$
U(t) = e^{-i(A+B)t} \approx U_n(t) = \left(e^{-iAt/n}\, e^{-iBt/n}\right)^{n}
$$

The desired evolution is replaced by n repetitions of two elementary evolutions, each for time t/n; the relation is approximate for [A,B] \neq 0 and exact as n \to \infty.

Provenance: `abstract_inferred`. The abstract names the Trotter formula and describes it as a repeated sequence of elementary evolutions with repetition count n; the first-order form is the simplest instance consistent with that description (the order used in the paper is not stated).

Abstract evidence: The Trotter formula, which decomposes a desired unitary time evolution of the simulator into a stroboscopic sequence of repeated elementary evolutions

Equation assumptions:

- First-order product formula
- Two-term splitting H = A + B

## eq_2: Trotter (algorithmic) error bound

$$
\left\| U(t) - U_n(t) \right\| \le \frac{t^{2}}{2n}\,\left\| [A,B] \right\| \equiv \frac{c_1}{n}
$$

Operator-norm bound on the first-order Trotter error; it decreases as 1/n, which is the ideal-case statement that precision can be controlled by increasing n.

Provenance: `standard_background`. Standard first-order product-formula error bound; consistent with the abstract's claim that in the ideal case precision is arbitrarily controlled by increasing n.

Equation assumptions:

- Operator (spectral) norm
- Bound, not exact equality

## eq_3: Trace (statistical) distance

$$
D(\rho,\sigma) = \tfrac{1}{2}\left\| \rho - \sigma \right\|_{1}
$$

Figure of merit used to compare the noisy simulated state with the ideal one.

Provenance: `standard_background`. The abstract speaks of 'statistical distance' without defining it; the trace distance is the standard quantum generalization of classical statistical distance and is assumed here.

Equation assumptions:

- 'Statistical distance' is interpreted as the trace distance; the paper may use a different (e.g. fidelity-based) measure

## eq_4: Accumulated gate-error contribution

$$
D\left(\rho_n,\; U_n(t)\rho_0 U_n(t)^{\dagger}\right) \le 2n\,\epsilon \equiv c_2\, n
$$

With 2n imperfect elementary gates each adding at most epsilon in trace distance, the accumulated gate error grows linearly in n (triangle inequality and contractivity of CPTP maps).

Provenance: `assumption`. The abstract states each gate is applied imperfectly but does not give the error model; a generic per-gate additive trace-distance bound is the simplest model exhibiting the stated tradeoff.

Equation assumptions:

- Each imperfect gate is a CPTP map within trace distance epsilon of the ideal gate
- Errors accumulate at most additively
- Two elementary gates per Trotter step

## eq_5: Total error tradeoff

$$
D(n) \equiv D\left(\rho_n, \rho_{\mathrm{ideal}}\right) \le \frac{c_1}{n} + c_2\, n, \qquad c_1 = \frac{t^{2}}{2}\left\|[A,B]\right\|,\; c_2 = 2\epsilon
$$

The Trotter error decreases with n while the gate error increases with n, giving a total distance bound with a non-trivial minimum.

Provenance: `abstract_inferred`. The abstract asserts a tradeoff between Trotter precision and gate imperfection that sets an ultimate precision limit; combining eq_2 (converted to trace distance via the triangle inequality, since ||U-U_n|| bounds the trace distance of pure outputs up to a constant) with eq_4 yields this form.

Abstract evidence: The resultant tradeoff in errors leads to an ultimate limit on the precision of the simulation.

Equation assumptions:

- Operator-norm Trotter bound converts to a trace-distance bound with an O(1) constant absorbed into c_1
- Bound rather than exact distance

## eq_6: Optimum Trotter number (continuous relaxation of the bound)

$$
n^{*} = \sqrt{\frac{c_1}{c_2}} = t\,\sqrt{\frac{\left\|[A,B]\right\|}{4\epsilon}}, \qquad D(n^{*}) \le 2\sqrt{c_1 c_2} = 2t\sqrt{\epsilon\left\|[A,B]\right\|}
$$

Minimizing the bound c_1/n + c_2 n over real n > 0 gives n^{*}; the integer Trotter number is the floor or ceiling of this value that gives the smaller D(n). The resulting minimum value is the ultimate precision limit for this model.

Provenance: `abstract_inferred`. The abstract states an optimum n^{*} minimizing the statistical distance exists; this is the minimizer of the assumed bound eq_5. The paper's exact expression may differ because its error model and distance measure are not given.

Abstract evidence: We calculate the optimum Trotter number $n^{*}$ that achieves this limit, which is the minimum statistical distance from the actual simulation to the ideal one.

Equation assumptions:

- Minimization of the upper bound, not of the exact distance
- n^{*} must be rounded to an integer; floor/ceiling chosen by direct comparison of D(n)

## Registers

- sys: 2 qubits; System qubits on which H = A + B acts; qubit 1 is the most significant bit in the computational-basis label |q_1 q_2>

## Initial state

|\psi_0\rangle = |00\rangle on sys (rho_0 = |00><00|), chosen as a tiny explicit instance; any fixed product state would serve.

## Measurement

To estimate D(n) on hardware, perform full state tomography of the 2-qubit output rho_n (Pauli-basis measurements, 3^2 settings) and compute the trace distance to the classically computed rho_ideal; alternatively, measure in the computational basis and use the classical total-variation distance of the outcome distributions as a lower bound on D(n).

## Classical postprocessing

Reconstruct rho_n from tomography data, compute D(n) = (1/2)||rho_n - rho_ideal||_1 for each n, fit or scan D(n) over n, and report n^{*} = argmin_n D(n) and D(n^{*}); compare with the analytic prediction sqrt(c_1/c_2).

## Algorithm steps

1. Fix the instance: A = X_1 X_2, B = Z_1 + Z_2, t = 1, per-gate error epsilon; compute c_1 = (t^2/2)||[A,B]|| and c_2 = 2 epsilon, and evaluate the candidate optimum n^{*} = sqrt(c_1/c_2), rounding to the neighbouring integers. (eq_2, eq_4, eq_6)
2. For each candidate n, prepare |00> and apply n repetitions of the elementary gates exp(-iA t/n) followed by exp(-iB t/n), each realized imperfectly (noisy channel), producing rho_n. (eq_1, eq_4)
3. Compare rho_n to the ideal state rho_ideal = U(t)|00><00|U(t)^dagger using the trace distance D(n) and verify the 1/n versus n tradeoff. (eq_3, eq_5)
4. Select n^{*} = argmin_n D(n) over the integer candidates; D(n^{*}) is the ultimate precision limit for this gate-error strength. (eq_6)

## Assumptions

- No experiment_scope was given, so a 2-qubit transverse-field Ising instance (A = X_1 X_2, B = Z_1 + Z_2, J = h = 1, t = 1) was chosen as the smallest useful construction
- First-order Trotter formula with two elementary evolutions per step
- Gate imperfection modelled as a generic per-gate trace-distance increment epsilon, accumulating additively
- 'Statistical distance' interpreted as trace distance
- n^{*} obtained by minimizing an upper bound on D(n), then rounding to an integer

## Missing information

- The paper's specific gate-error model (e.g. depolarizing, over-rotation, stochastic) and how it enters the distance
- The precise definition of 'statistical distance' used in the paper
- The exact (not bound-based) functional form of D(n) and n^{*} derived in the paper
- The Trotter order and the many-body Hamiltonian studied in the paper
- Any numerical values or scaling results reported in the paper
