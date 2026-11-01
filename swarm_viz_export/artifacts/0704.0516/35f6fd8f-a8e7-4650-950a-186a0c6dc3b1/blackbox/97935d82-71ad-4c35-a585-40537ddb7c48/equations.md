# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Order finding for Shor's algorithm with N=15, a=2 (order r=4), with the ideal circuit and three assumed gate-imperfection models (systematic, random, combined) on the QFT phase gates. The aim is to compare the success probability with the ideal value and define an operational error threshold sigma_c.

Scope: One tiny instance: t=4 counting qubits, 4 work qubits, N=15, a=2. The built unitary contains H, controlled modular multiplications, and an inverse QFT whose controlled-phase angles are perturbed by explicit numeric error values. Excluded: the paper's analytic threshold formula and precise error definitions, scaling with N beyond a numerical sigma_c, and classical decoding. Decoding is documented but is not part of the unitary.

## Symbols

- $N$: number to factor; domain: 15
- $a$: base coprime to N; domain: 2
- $r$: multiplicative order of a mod N; domain: 4
- $t$: number of counting qubits; domain: 4
- $x$: counting register integer, little-endian x=sum_k x_k 2^k; domain: 0..15
- $\theta_m$: ideal controlled-phase angle magnitude pi/2^m; domain: real
- $\epsilon,\delta$: fixed systematic relative and absolute angle errors; domain: real, small
- $\delta_j$: random angle offset of phase gate j, zero mean, width sigma; domain: real
- $\sigma$: random error width; domain: real >=0
- $P_{succ}$: probability mass on counting outcomes x with x/2^t within rounding of s/r; domain: [0,1]
- $\sigma_c$: largest sigma with averaged P_succ >= eta times ideal; domain: real >=0
- $\eta$: cutoff fraction; domain: (0,1), assumed 1/2

## eq_1: Modular multiplication unitary

$$
U|y\rangle=|a y \bmod N\rangle,\quad \Lambda|x\rangle|y\rangle=|x\rangle|a^{x}y \bmod N\rangle=\prod_k (c\text{-}U^{2^k})_k|x\rangle|y\rangle
$$

Controlled modular exponentiation for y in 0..14. Values y>=15 are left fixed so that U is a permutation and hence unitary.

Provenance: `standard_background`. Standard Shor order finding.

Equation assumptions:

- Compiled with explicit classical a and N
- Work register is 4 qubits, y=1 initially

## eq_2: Ideal output distribution

$$
P(x)=\frac{1}{r}\sum_{s=0}^{r-1}\left|\frac{1}{2^t}\sum_{j=0}^{2^t-1}e^{2\pi i j(s/r-x/2^t)}\right|^2
$$

Ideal outcome peaks at x/2^t near s/r. For t=4, r=4 the peaks are x=0,4,8,12 with probability 1/4 each.

Provenance: `standard_background`. Standard QFT phase estimation.

Equation assumptions:

- r divides 2^t exactly in this instance

## eq_3: Systematic error model

$$
\theta_m\to\theta_m(1+\epsilon)\ \text{or}\ \theta_m+\delta,\ \text{same at every gate}
$$

The same fixed angle error is applied to every controlled-phase gate.

Provenance: `assumption`. The abstract names systematic errors without defining them, so this is an assumed definition.

Equation assumptions:

- The paper's definition may differ

## eq_4: Random and combined error models

$$
\theta_{m,j}\to\theta_m+\delta_j,\ \delta_j\sim\mathcal{D}(0,\sigma^2);\quad \text{combined: }\theta_m+\delta+\delta_j
$$

Independent random offsets per gate, or a fixed offset plus random offsets. Several seeds are averaged.

Provenance: `assumption`. The abstract names the three categories without definitions.

Equation assumptions:

- The distribution (e.g. Gaussian or uniform) is my choice
- Seeds are fixed explicitly

## eq_5: Success probability and threshold

$$
P_{succ}=\sum_{x:\,|x/2^t-s/r|\le 2^{-t-1}\text{ for some }s}P(x),\quad \sigma_c=\max\{\sigma:\overline{P_{succ}}(\sigma)\ge \eta P_{succ}^{ideal}\}
$$

Operational numerical threshold with cutoff fraction eta, e.g. 1/2.

Provenance: `assumption`. The abstract says an error threshold is given for N but not its form; this is an operational stand-in.

Equation assumptions:

- eta=1/2
- This is not the paper's analytic threshold

## eq_6: Ideal inverse QFT gate decomposition

$$
\mathrm{QFT}^{-1}:\ \text{H on qubit } k \text{ and CP}(-\pi/2^{m}) \text{ between qubits separated by } m,\ \text{then bit-reversal swaps}
$$

The inverse QFT is built from H and controlled-phase gates with ideal angles -theta_m, which the error models perturb.

Provenance: `standard_background`. Standard QFT circuit decomposition.

Equation assumptions:

- Little-endian ordering with swaps included

## Registers

- count: 4 qubits; counting register, little-endian, qubits 0-3
- work: 4 qubits; holds y mod 15, little-endian, initial value 1

## Initial state

|0>^4 on count and |0001> (y=1) on work

## Measurement

Measure the counting register in the computational basis, outside the built unitary.

## Classical postprocessing

Continued fractions of x/2^t give r, then gcd(a^(r/2)±1, N) gives factors. Compute P_succ against the ideal value, and average over seeds for the random errors.

## Algorithm steps

1. Apply H to every counting qubit, giving a uniform superposition over x. This is the input preparation for the controlled exponentiation. (eq_2)
2. Apply controlled U^(2^k) from counting qubit k onto the work register, with U the multiplication by 2 mod 15 (a cyclic bit permutation). Optionally add small Rz rotations after these gates. (eq_1)
3. Apply the inverse QFT on the counting register with swaps, with the controlled-phase angles perturbed per the chosen error model using explicit numeric values. (eq_6, eq_3, eq_4)
4. Outside the unitary: simulate the output distribution, measure the counting register to get x, and evaluate P_succ against the ideal value and sigma_c, averaging over seeds for the random errors. (eq_2, eq_5)

## Assumptions

- The error models are my definitions, since the abstract does not define them
- N=15, a=2, t=4 chosen as the smallest instance
- The qualitative claim (robust to systematic, vulnerable to random errors) is only tested numerically on this single instance

## Missing information

- The paper's exact error definitions
- The analytic threshold formula as a function of N
- The error distributions and gate set used by the paper
