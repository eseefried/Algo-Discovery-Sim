# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Estimate the influence of each variable x_i on an n-variable Boolean function f using the quantum Bernstein-Vazirani circuit: after one run, the probability of reading 1 in position i equals the influence of x_i on f. Use repeated runs to approximate influences, and apply this to learning juntas.

Scope: Abstract-level reconstruction of the influence-estimation claim and approximation algorithm; the junta-learning algorithms and their complexity are not detailed. A small finite instance with n qubits plus an ancilla is assumed.

## Symbols

- $f$: Boolean function f:{0,1}^n -> {0,1}; domain: {0,1}^n -> {0,1}
- $y_i$: i-th bit of the Bernstein-Vazirani output y; domain: {0,1}
- $\mathrm{Inf}_i(f)$: influence (dependence degree) of x_i on f; domain: [0,1]
- $\hat f(s)$: Fourier coefficient of (-1)^{f}; domain: [-1,1]

## eq_1: Bit probability equals influence

$$
\Pr[y_i=1]=\mathrm{Inf}_i(f)
$$

One-run probability of a 1 in position i equals the influence of x_i on f.

Provenance: `abstract_inferred`. Directly stated in the abstract.

Abstract evidence: the probability of getting a 1 in each position $i$ is equal to the dependence degree of $f$ on the variable $x_{i}$, i.e. the influence of $x_{i}$ on $f$

## eq_2: BV output distribution

$$
\Pr[y=s]=\hat f(s)^2,\quad \hat f(s)=2^{-n}\sum_x(-1)^{f(x)+s\cdot x}
$$

Standard output distribution of the BV circuit applied to a phase oracle for f.

Provenance: `standard_background`. Standard Fourier sampling background.

Equation assumptions:

- Phase oracle (-1)^{f(x)}

## eq_3: Influence in Fourier form

$$
\mathrm{Inf}_i(f)=\sum_{s:\,s_i=1}\hat f(s)^2
$$

Standard Fourier expression for influence, consistent with eq_1 and eq_2.

Provenance: `standard_background`. Standard Boolean analysis with the normalization Inf_i = Pr[f(x)!=f(x xor e_i)]/2-type scaling; combining with eq_2 gives eq_1 under the paper's definition.

Equation assumptions:

- Influence normalized so that it equals the sum of squared Fourier weight on s_i=1

## eq_4: Empirical estimate

$$
\widehat{\mathrm{Inf}}_i=\frac{1}{N}\sum_{k=1}^N y^{(k)}_i
$$

Approximation from N repeated runs.

Provenance: `assumption`. Natural sampling estimator for the approximation algorithm; the exact scheme is not given in the abstract.

Equation assumptions:

- Independent runs

## Registers

- x: n qubits; Input register for the BV circuit, measured to give y
- anc: 1 qubits; Ancilla in |-> for phase kickback from the oracle U_f (assumed standard BV form)

## Initial state

|0>^{n} on x and |1> on anc (before Hadamards)

## Measurement

Measure the x register in the computational basis after the final Hadamards to obtain y; the bit y_i is a Bernoulli sample with mean Inf_i(f).

## Classical postprocessing

Over N independent runs, average y_i per position to estimate Inf_i(f) (eq_4); variables with estimate near 0 are treated as irrelevant when seeking juntas (assumed thresholding).

## Algorithm steps

1. Apply H^{\otimes n} to x and H to anc, giving uniform superposition on x and |-> on anc. (no equation reference)
2. Apply oracle U_f, imprinting phase (-1)^{f(x)} on x by kickback. (eq_2)
3. Apply H^{\otimes n} to x, so outcome y is distributed as the squared Fourier coefficients. (eq_2, eq_3)
4. Repeat the circuit N times independently to collect samples for estimation. (eq_4)

## Assumptions

- Phase-oracle form of BV
- Sampling estimator is the intended approximation
- Ancilla prepared in |1> then Hadamard to give |->
- Thresholding rule for junta identification is assumed, not given
- Thresholding on estimated influences is the assumed junta-identification step

## Missing information

- Sample complexity bounds
- Junta-learning algorithm details
- Exact definition of influence normalization
- Measurement and postprocessing are inferred, not stated in abstract
- Abstract does not specify error/confidence parameters for the approximation
