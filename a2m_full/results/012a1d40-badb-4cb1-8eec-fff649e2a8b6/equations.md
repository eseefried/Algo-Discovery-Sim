# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate the mean mu = (1/N) sum_x f(x) of a black-box function f:{0,1}^n->[0,1] using canonical amplitude estimation (the Heisenberg-limited O(1/eps) variant). The Aharonov-style phase-estimation variant and the median algorithm are only sketched or excluded.

Scope: One tiny instance: n=2 index qubits (N=4), one value qubit a, t=3 counting qubits (6 qubits total), f given as a direct rotation oracle with one query per controlled use. Excluded: variance-based rescaling for unbounded f, the Aharonov variant, the median/Durr-Hoyer algorithm, and all paper-specific details not in the abstract.

## Symbols

- $N=2^n$: number of index points; domain: positive integer power of two
- $f(x)$: black-box function value, rescaled; domain: [0,1]
- $p$: mean of f, equal to the probability of measuring a=1 after A; domain: [0,1]
- $A$: state-preparation unitary: Hadamards on the index register followed by the rotation oracle; domain: unitary on n+1 qubits
- $Q$: Grover iterate; domain: unitary on n+1 qubits
- $t, M=2^t$: number of counting qubits and the size of the counting register; domain: positive integers
- $y$: integer read from the counting register, with qubit j weighted 2^j (little-endian); domain: {0,...,M-1}
- $\theta_p$: angle with sin^2(\theta_p)=p; domain: [0,\pi/2]

## eq_1: Mean as amplitude

$$
A|0\rangle^{n}|0\rangle=\frac{1}{\sqrt N}\sum_x|x\rangle\left(\sqrt{1-f(x)}|0\rangle+\sqrt{f(x)}|1\rangle\right),\quad p=\frac1N\sum_x f(x)
$$

Uniform superposition followed by the rotation oracle, so the probability of a=1 equals the mean of f.

Provenance: `abstract_inferred`. The abstract states mean estimation. The sketch's use of amplitude estimation implies this encoding; the encoding itself is not stated in the abstract.

Abstract evidence: approximate the mean value of a black-box function

Equation assumptions:

- f in [0,1]
- N is a power of two
- rotation oracle with Ry(2 arcsin sqrt f(x)) controlled on x

## eq_2: Grover iterate

$$
Q=-A S_0 A^{-1} S_\chi,\quad S_\chi=I-2\,I\otimes|1\rangle\langle1|_a,\quad S_0=I-2|0\rangle\langle0|
$$

Q acts as a rotation by 2\theta_p in the plane spanned by the good and bad components.

Provenance: `standard_background`. Standard amplitude amplification, recalled from background knowledge.

Equation assumptions:

- good subspace is a=1

## eq_3: Eigenphases of Q

$$
Q|\psi_\pm\rangle=e^{\pm i2\theta_p}|\psi_\pm\rangle,\quad \sin^2\theta_p=p
$$

A|0> is an equal-weight superposition of the two eigenvectors, so phase estimation yields \theta_p.

Provenance: `standard_background`. Brassard-Hoyer-Mosca-Tapp amplitude estimation.

## eq_4: Estimator

$$
\hat p=\sin^2\left(\frac{\pi y}{M}\right),\quad |\hat p-p|\le \frac{2\pi\sqrt{p(1-p)}}{M}+\frac{\pi^2}{M^2}\text{ with probability}\ge 8/\pi^2
$$

Both y and M-y give the same estimate. The error is O(1/M) with M-1 applications of Q, hence O(1/eps) queries.

Provenance: `standard_background`. Standard amplitude estimation bound. The abstract only claims asymptotic optimality.

Equation assumptions:

- ideal oracle
- no noise

## eq_5: Counting register readout

$$
y=\sum_{j=0}^{t-1}b_j2^j,\quad b_j=\text{bits}[::-1][j]
$$

For a counts key over the counting register only, the last character is classical bit 0. The inverse QFT must be built so that qubit j carries weight 2^j.

Provenance: `assumption`. Needed to avoid the Qiskit bit-order error.

Equation assumptions:

- measure counting qubit j into classical bit j

## Registers

- x: n (2 in the tiny instance) qubits; index register, Hadamard to uniform superposition
- a: 1 qubits; value qubit that carries sqrt(p) as the |1> amplitude
- c: t (3 in the tiny instance) qubits; counting register for phase estimation of Q

## Initial state

All qubits in |0>.

## Measurement

Measure only the t counting qubits, with c_j into classical bit j.

## Classical postprocessing

Decode y with little-endian ordering, take the mode of y, and compute p_hat=sin^2(pi y/M). Rescale if f was rescaled.

## Algorithm steps

1. Apply H to every qubit of c. Prepare A|0> on x,a: H on x, then the rotation oracle onto a. (eq_1)
2. For j=0..t-1, apply controlled-Q^(2^j) with control c_j. Each Q uses A, A^-1, S_chi and S_0, so the oracle is queried twice per Q, plus once for the initial A. (eq_2, eq_3)
3. Apply the inverse QFT on c, with swaps handled so that c_j has weight 2^j, then measure only c. (eq_5)
4. Compute y from the counts, take the most frequent y, and set p_hat=sin^2(pi y/M). The mean estimate is p_hat, rescaled back to the original range of f. (eq_4)

## Assumptions

- The tiny instance is chosen by me: n=2, t=3, an explicit f table, a direct rotation oracle.
- Controlled-Q is built from the oracle placeholder, which requires a controlled version of the oracle, and each use counts as a query.
- f is in [0,1] with fixed-point precision sufficient for the rotation angles.
- No ancillas are needed in this version.

## Missing information

- The abstract does not give the paper's novel algorithm; this is the standard amplitude-estimation reconstruction.
- The unbounded-variance rescaling scheme is not specified.
- The Aharonov-style variant's details, including the exact phase-estimation unitary and the Hadamard test, are not specified.
- The median algorithm is not specified in the abstract; the sketch's Durr-Hoyer design is unverified.
- Whether the paper's algorithm avoids the QFT is unknown.
