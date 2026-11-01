# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate Shor order finding for a small N (N=15, a=7, order r=4) with gate-angle imperfections (systematic, random, combined), and measure the success probability versus epsilon or sigma. Then estimate an error threshold. The abstract states only the qualitative findings: robust to systematic errors, vulnerable to random errors, and an N-dependent threshold.

Scope: One instance: N=15, a=7, n=4 work qubits, t=8 counting qubits (12 qubits total; t could be reduced to fit a smaller cap). Ideal circuit plus an angle-perturbation noise model on QFT controlled-phase and Rz gates. Out of scope: the paper's actual error model, analytic threshold formula, and any numerical values. The abstract does not give them.

## Symbols

- $N$: integer to factor; domain: N=15 (odd composite)
- $a$: base coprime to N; domain: a=7, gcd(a,N)=1
- $n$: number of work qubits, ceil(log2 N); domain: positive integer, 4
- $t$: number of counting qubits; domain: positive integer, about 2n
- $r$: multiplicative order of a mod N; domain: positive integer, 4 for a=7
- $m$: integer read from counting register, with qubit 0 as the least significant bit; domain: 0..2^t-1
- $\epsilon$: systematic fractional angle error; domain: real
- $\sigma$: standard deviation of random angle error; domain: real, >=0
- $\delta_g$: relative angle shift on gate g; domain: real; equals epsilon, a Gaussian draw with std sigma, or the sum of both
- $G$: number of imperfect gates; domain: positive integer
- $P_s$: success probability; domain: [0,1]

## eq_1: Order-finding state

$$
U_a|y\rangle=|ay \bmod N\rangle,\quad \frac{1}{2^{t/2}}\sum_{x=0}^{2^t-1}|x\rangle|a^x \bmod N\rangle
$$

Modular multiplication unitary, and the state after H on the counting register and the controlled U_a^(2^k) gates, with the work register starting in |1>.

Provenance: `standard_background`. Textbook Shor construction; the abstract only names Shor's algorithm.

Equation assumptions:

- Work register starts in |1>
- U_a is defined as a permutation on y<N and identity on y>=N

## eq_2: Ideal peak distribution

$$
P(m)=\frac{1}{r}\left|\frac{1}{2^t}\sum_{x}...\right|^2\approx\text{peaks at } m\approx s\,2^t/r,\ s=0..r-1
$$

After the inverse QFT, the counting register is concentrated near multiples of 2^t/r. For r=4 and t=8 the ideal peaks are exactly m=0,64,128,192.

Provenance: `standard_background`. Standard result, applicable when r divides 2^t.

Equation assumptions:

- r=4 divides 2^8

## eq_3: Noisy gate model

$$
CP(\theta_k)\to CP\big(\theta_k(1+\delta_g)\big),\ \theta_k=\pi/2^k;\ \delta_g=\epsilon\ \text{(systematic)},\ \delta_g\sim\mathcal N(0,\sigma^2)\ \text{(random)},\ \delta_g=\epsilon+\mathcal N(0,\sigma^2)\ \text{(combined)}
$$

Angle perturbations applied to the QFT controlled-phase gates. Optionally an extra Rz(delta) is applied after each gate.

Provenance: `assumption`. The sketch proposes this model. The abstract gives only the three categories, not the form of the error.

Equation assumptions:

- Errors act on the QFT gates and Hadamards only, while modular multiplication is kept ideal
- Random errors are i.i.d. per gate

## eq_4: Success probability

$$
P_s=\mathbb E_{\delta}\sum_{m}P_\delta(m)\,\mathbf 1[\text{postprocessing}(m)\text{ yields a nontrivial factor}]
$$

Average over sampled noisy circuits, with the exact statevector distribution for each. For systematic error a single circuit suffices.

Provenance: `assumption`. Defines the metric. The abstract implies the algorithm's success is compared across error types.

Equation assumptions:

- Exact statevector probabilities are used, with no sampling shot noise

## eq_5: Threshold scaling heuristic

$$
F\approx 1-G\sigma^2,\quad \sigma_c\sim 1/\sqrt{G(N)}
$$

Heuristic: random errors add incoherently, so fidelity loss scales as G sigma^2. The threshold is the sigma at which P_s falls to a chosen fraction of its ideal value.

Provenance: `abstract_inferred`. The abstract implies an N-dependent threshold. The 1/sqrt(G) form is a heuristic from the sketch, not stated in the abstract.

Abstract evidence: Error threshold is given to the algorithm for a given number N to be factorized.

Equation assumptions:

- The drop criterion (e.g. 50% of ideal) is a free choice

## Registers

- count: t=8 qubits; phase-estimation counting register, measured; qubit i has weight 2^i
- work: n=4 qubits; holds a^x mod N, starting in |1>=|0001>; not measured

## Initial state

count=|0...0>, work=|0001> (integer 1, little-endian)

## Measurement

Measure only the t counting qubits into t classical bits. In Qiskit counts keys the last character is classical bit 0, so m=int(key,2) with bit order preserved.

## Classical postprocessing

phi=m/2^t. Use continued fractions (Fraction.limit_denominator(N)) to get a candidate r. Check a^r mod N = 1, and if r is even compute gcd(a^(r/2)±1, N), accepting nontrivial factors (3 and 5 for N=15).

## Algorithm steps

1. Apply H to all counting qubits. (eq_1)
2. For k=0..t-1, apply U_7^(2^k) controlled on counting qubit k. For a=7 mod 15, powers are 7, 4, 1, 1... so only k=0 and k=1 are nontrivial and the rest are identities. Build from CSWAP/CX and X gates. (eq_1)
3. Apply the inverse QFT to the counting register using H, CP and SWAP gates. In the noisy runs, perturb each CP angle per the noise model. (eq_2, eq_3)
4. Compute P_s versus epsilon, sigma and combined settings by averaging over sampled noisy circuits. Find sigma where P_s falls to the chosen fraction of the ideal value. (eq_4, eq_5)

## Assumptions

- Chosen instance N=15, a=7, t=8; a smaller t may be needed if the qubit cap is below 12
- Noise placement on QFT gates only; modular exponentiation is ideal
- Gaussian i.i.d. random errors, averaged over many trials
- Threshold defined by an assumed fractional drop in P_s

## Missing information

- Actual error model used in the paper
- Exact definition of the threshold
- Quantitative threshold formula as a function of N
- Whether errors also act on the modular exponentiation gates
