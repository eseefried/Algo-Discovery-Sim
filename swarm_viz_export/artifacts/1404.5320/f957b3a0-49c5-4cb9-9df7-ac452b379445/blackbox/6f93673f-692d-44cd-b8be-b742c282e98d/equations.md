# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate a single-qubit z-rotation Rz(theta) to operator-norm precision eps (up to global phase) by an ancilla-free Clifford+T circuit, via a number-theoretic exact synthesis baseline. This is a comparator, not the paper's RUS construction with one ancilla and measurement.

Scope: One data qubit, one tiny instance (e.g. theta=pi/8 style small angle with modest eps such as 0.1): sample u in Z[omega] near the scaled target entry, solve the norm equation for t, form the exact unitary, and synthesize it exactly into a Clifford+T word. Outside scope: the RUS circuit, ancilla and measurement, the paper's probabilistically polynomial RUS synthesis algorithm, the 2.5x expected T-count reduction, and the numerical evidence. A ZYZ extension to general U is only described, not built.

## Symbols

- $\theta$: target z-rotation angle; domain: real, [0,2\pi)
- $\varepsilon$: target precision; domain: (0,1)
- $\omega$: primitive 8th root of unity e^{i\pi/4}; domain: complex
- $u,t$: elements of Z[omega]; domain: Z[\omega]
- $k$: denominator exponent; domain: integer >= 0
- $U_{u,t}$: exact unitary built from (u,t), entries in Z[1/sqrt2,i]; domain: SU(2)
- $|0\rangle$: initial computational basis state of the data qubit; domain: C^2

## eq_1: Target and approximation criterion

$$
R_z(\theta)=\mathrm{diag}(e^{-i\theta/2},e^{i\theta/2}),\quad \min_{\phi}\|U_{\mathrm{circ}}-e^{i\phi}R_z(\theta)\|\le\varepsilon
$$

Target rotation and precision requirement, global phase ignored

Provenance: `abstract_inferred`. The abstract states approximation within precision eps; the operator norm is an assumed metric.

Abstract evidence: approximate any given single-qubit unitary within precision $\varepsilon$

Equation assumptions:

- Operator-norm metric up to global phase

## eq_2: Candidate and norm equation

$$
\left|u-e^{-i\theta/2}\sqrt2^{\,k}\right|\lesssim \varepsilon\sqrt2^{\,k}/2,\quad |u|^2+|t|^2=2^k
$$

Sample u near the scaled target entry and require 2^k-|u|^2 to be a norm from Z[omega] so t exists

Provenance: `assumption`. Standard number-theoretic approach recalled from background, not stated in the abstract. The plan omitted the sqrt2^k scaling; this is a correction. Here |.|^2 is the complex modulus squared, and for Z[omega] the equation is an exact equality in the real subring.

Equation assumptions:

- t found by randomized factoring with Miller-Rabin tests and sums of two squares over primes

## eq_3: Exact unitary

$$
U_{u,t}=\frac{1}{\sqrt2^{\,k}}\begin{pmatrix}u&-t^*\\ t&u^*\end{pmatrix}
$$

Exact unitary from the solved pair; unitary by the norm equation

Provenance: `standard_background`. Standard form of a Clifford+T-synthesizable matrix; determinant is (|u|^2+|t|^2)/2^k=1.

Equation assumptions:

- |u|^2+|t|^2=2^k

## eq_4: Initial state

$$
|\psi_0\rangle=|0\rangle,\quad |\psi_{\mathrm{out}}\rangle=U_{\mathrm{circ}}|0\rangle
$$

Data qubit starts in |0>; the circuit unitary is applied. Equivalent verification uses the full 2x2 unitary.

Provenance: `assumption`. A fixed input state is needed for implementation. This replaces the equation-specialist's prediction, which was rejected because its state includes an unjustified ancilla and does not follow from the cited relation.

Equation assumptions:

- Single data qubit, no ancilla

## eq_5: T-count reference

$$
T\text{-count}(\text{ancilla-free})\ge 3\log_2(1/\varepsilon)
$$

The abstract's ancilla-free reference bound; the comparator is expected near this order, with unverified O(log log) overhead

Provenance: `abstract_explicit`. Stated in the abstract; used only as a reference.

Abstract evidence: theoretical lower bound of $3\log_{2}(1/\varepsilon)$ for ancilla-free single-qubit circuit decomposition

## Registers

- q: 1 qubits; data qubit q0 on which the synthesized Clifford+T unitary acts; the only qubit

## Initial state

|0> on the single data qubit q0 (|psi_0> = |0>). The full unitary is compared to the target, so the choice of input state does not affect the check.

## Measurement

None. The circuit is a measurement-free unitary. Decoding compares the simulated 2x2 unitary to the target up to global phase using operator-norm distance.

## Classical postprocessing

Classical sampling, factoring and exact synthesis produce the gate word; the distance to the target is then evaluated.

## Algorithm steps

1. Fix theta and eps and prepare the data qubit in |0>. For a general U, ZYZ Euler angles would give three z-rotations with H/S conjugation (outside the built scope). (eq_1, eq_4)
2. Randomly sample candidate u in Z[omega] in the eps-disc; test solvability of the norm equation for t by randomized factoring; repeat until a solution is found. (eq_2)
3. Form the exact unitary U_{u,t}. (eq_3)
4. Apply Kliuchnikov-Maslov-Mosca exact synthesis to get a Clifford+T word using h, s, t, tdg, x as a measurement-free circuit; compare its T-count to the reference. (eq_3, eq_5)

## Assumptions

- The ancilla-free number-theoretic baseline is chosen as the smallest implementable construction; it does not reproduce the paper's RUS method.
- Metric is the operator norm up to global phase.
- Polynomial classical runtime relies on prime density about 1/log, an unverified expectation.
- Initial state |0> is a chosen convention.

## Missing information

- The paper's RUS circuit structure, ancilla use and measurement outcomes
- The paper's synthesis algorithm and runtime analysis
- The numerical evidence for the 2.5x reduction
