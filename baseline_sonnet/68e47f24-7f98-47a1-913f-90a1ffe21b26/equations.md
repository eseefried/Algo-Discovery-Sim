# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Estimate systematic amplitude and off-resonance errors of single-qubit gates with Heisenberg-scaling precision, robustly to SPAM errors, using only single-qubit experiments; the abstract names a robust version of Higgins et al. phase estimation as the key tool but gives no explicit formulas.

Scope: Smallest useful construction: a background single-qubit amplitude-error model (rotation angle pi(1+epsilon)) and repeated-gate Ramsey-style phase-estimation likelihood with depth-m sequences, in one tiny instance (m in {1,2,4,8}). The robust phase estimation theorem, off-resonance error estimation, SPAM-robust protocol details, and error bounds are outside scope.

## Symbols

- $\epsilon$: fractional amplitude error of the nominally pi rotation; domain: real, |epsilon| small
- $m$: number of gate repetitions in an experiment; domain: positive integer, e.g. powers of 2
- $\theta$: accumulated phase/rotation angle to estimate, theta = pi*epsilon; domain: real
- $p_m$: probability of measurement outcome 0 after m repetitions; domain: [0,1]
- $N$: number of shots per depth m; domain: positive integer
- $\hat p_m$: empirical frequency of outcome 0; domain: [0,1]

## eq_1: Amplitude-error gate model

$$
U(\epsilon)=\exp\left[-i\frac{\pi(1+\epsilon)}{2}X\right]
$$

Nominal pi rotation about X with fractional over/under-rotation epsilon.

Provenance: `assumption`. The abstract mentions amplitude errors in single-qubit gates but gives no model; this is a standard parametrization chosen for the instance.

Equation assumptions:

- Pure rotation about X with no other errors

## eq_2: Repeated gate

$$
U(\epsilon)^m=\exp\left[-i\frac{m\pi(1+\epsilon)}{2}X\right]
$$

Applying the gate m times multiplies the rotation angle by m, amplifying epsilon linearly in m (the source of Heisenberg scaling).

Provenance: `standard_background`. Commuting powers of the same rotation; Heisenberg scaling in general arises from phase amplification by depth.

Equation assumptions:

- Coherent error identical in every repetition

## eq_3: Outcome probability

$$
p_m=\Pr(0)=|\langle 0|U(\epsilon)^m|0\rangle|^2=\cos^2\!\left(\frac{m\pi(1+\epsilon)}{2}\right)
$$

Ideal-SPAM probability of measuring 0 starting from |0> in the Z basis.

Provenance: `standard_background`. Direct computation from eq_2. For m even, the dependence on epsilon is cos^2(m pi epsilon/2); for m odd it is sin^2(m pi epsilon/2).

Equation assumptions:

- Perfect state preparation and measurement

## eq_4: Empirical frequency

$$
\hat p_m=\frac{n_0(m)}{N},\quad \mathbb{E}[\hat p_m]=p_m,\quad \mathrm{Var}[\hat p_m]=\frac{p_m(1-p_m)}{N}
$$

Binomial estimate of p_m from N shots.

Provenance: `standard_background`. Standard binomial statistics.

Equation assumptions:

- Independent identically distributed shots

## eq_5: Heisenberg-scaling target

$$
\Delta\epsilon=O\left(\frac{1}{m_{\max}}\right)\ \text{with}\ m_{\max}\ \text{total depth}
$$

Error shrinking inversely with total gate applications, rather than as 1/sqrt of the count.

Provenance: `abstract_inferred`. Abstract claims Heisenberg scaling; the specific form in terms of m_max is an inference, not a stated bound or constant.

Abstract evidence: our estimates achieve the optimal efficiency, Heisenberg scaling

Equation assumptions:

- Constants and robustness conditions unspecified

## Registers

- q: 1 qubits; single data qubit; no ancilla or entanglement

## Initial state

|0> (assumed ideal; the actual protocol is claimed robust to SPAM errors, details not given)

## Measurement

Computational (Z) basis measurement of the single qubit after m gate applications.

## Classical postprocessing

Invert p_m for epsilon at increasing depths, using coarse estimates to resolve ambiguity at larger m. The robust Higgins-type procedure and its SPAM-robust analysis are not specified in the abstract.

## Algorithm steps

1. Choose depths m in {1,2,4,8} and shot count N per depth. (eq_4)
2. Prepare |0>, apply the gate U(epsilon) m times. (eq_1, eq_2)
3. Measure in the Z basis and compute the empirical frequencies. (eq_3, eq_4)
4. Combine results across depths to refine the estimate of epsilon, coarse to fine, as in phase estimation; the robust combination rule is not given. (eq_5)

## Assumptions

- Amplitude-error model on an X rotation was chosen by me
- Ideal SPAM used for the tiny instance
- Depths 1,2,4,8 are illustrative

## Missing information

- Robust phase estimation theorem statement, depth schedule, and error bounds
- Off-resonance error model and the universal gate-set sequences used
- How SPAM robustness is achieved
- Estimator and confidence guarantees
- Control correction step
