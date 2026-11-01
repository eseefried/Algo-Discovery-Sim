# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Grover search for a single marked item |w> among N=2^n as evolution under H=|w><w|+|s><s|, |s>=H^{(x)n}|0>. Compare a first-order Lie-Trotter discretisation (power-law error in query count) with maximal-step reflections (dt=pi, exact Grover iterates). The error is 1 - P(w).

Scope: Tiny instance n=3 (N=8), one marked string w, black-box oracle O=I-2|w><w| used once per Grover or Trotter step. Build (A) a Trotter circuit with m steps of step size dt=T/m, and (B) k plain Grover iterations with k=round(pi/(4 theta)-1/2). Measure the n search qubits. The fixed-point/recursive scheme with eps_{j+1}=eps_j^3 and the Chebyshev/Yang phase schedule is out of scope: the abstract does not specify it and its phases are not invented here.

## Symbols

- $n$: number of search qubits; domain: integer, 3 to 6
- $N$: search space size 2^n; domain: integer
- $|w>$: marked basis state; domain: computational basis state
- $|s>$: uniform superposition H^{(x)n}|0>; domain: state
- $\theta$: Grover angle with sin(theta)=1/sqrt(N); domain: (0, pi/2)
- $dt$: evolution step size; domain: positive real
- $T$: total evolution time m*dt; domain: positive real
- $m$: number of Trotter steps (= number of oracle queries if the oracle is used as a pi-phase reflection); domain: positive integer
- $k$: number of Grover iterations; domain: nonnegative integer
- $\epsilon$: error 1 - |<w|psi>|^2; domain: [0,1]

## eq_1: Two-projector Hamiltonian

$$
H=|w\rangle\langle w|+|s\rangle\langle s|,\quad U(T)=e^{-iHT}
$$

Hamiltonian whose evolution realises Grover search; the abstract only states that Grover is cast as a Hamiltonian evolution.

Provenance: `abstract_inferred`. The specific two-projector form is the standard choice recalled from background knowledge, not stated in the abstract.

Abstract evidence: Grover’s quantum search algorithm is described as a Hamiltonian evolution problem.

Equation assumptions:

- single marked item
- start state |s>

## eq_2: Lie-Trotter step

$$
U_{LT}(dt)^m=\left(e^{-i\,dt|w\rangle\langle w|}e^{-i\,dt|s\rangle\langle s|}\right)^m,\quad dt=T/m
$$

First-order product formula; its error is polynomial in dt, so it is a power law in the step count.

Provenance: `abstract_inferred`. The power-law claim is stated in the abstract; the explicit product form is standard.

Abstract evidence: the computational complexity has a power-law dependence on error when a straightforward Lie-Trotter discretisation formula is used

Equation assumptions:

- the oracle supplies e^{-i dt|w><w|} only for dt=pi, so non-pi steps need an extra construction, e.g. a controlled-phase built from oracle queries (assumption)

## eq_3: Reflections at dt=pi

$$
e^{-i\pi|w\rangle\langle w|}=I-2|w\rangle\langle w|=O,\quad e^{-i\pi|s\rangle\langle s|}=I-2|s\rangle\langle s|=-D
$$

At the maximal step each factor is an exact reflection. With D=2|s><s|-I=H^n(2|0><0|-I)H^n, the Grover iterate is G=D*O up to a global sign.

Provenance: `abstract_inferred`. A direct identity for dt=pi; the abstract says only that reflection operators are used.

Abstract evidence: it becomes logarithmic in error when reflection operators are used

Equation assumptions:

- the sign (global phase) is irrelevant

## eq_4: Grover rotation success probability

$$
\sin\theta=1/\sqrt N,\quad P_k(w)=\sin^2((2k+1)\theta),\quad \epsilon_k=\cos^2((2k+1)\theta)
$$

Exact success probability after k iterations of G, used for the reflection arm.

Provenance: `standard_background`. Standard Grover analysis.

Equation assumptions:

- one marked item

## eq_5: Trotter error scaling (to fit)

$$
\epsilon_{LT}(m)\sim C\,m^{-p},\quad p>0
$$

Power-law error to be fitted numerically; p and C are not stated in the abstract.

Provenance: `assumption`. Only the qualitative power-law claim is available.

Equation assumptions:

- exponent p is determined by simulation

## Registers

- search: n qubits; search register, little-endian; the counts key is reversed to read w
- anc: 0 or 1 qubits; optional ancilla for the multi-controlled phase flip, returned to |0>

## Initial state

|0>^n, then H on every search qubit to give |s>

## Measurement

Measure the n search qubits into n classical bits. In Qiskit counts the rightmost character is bit 0, so reverse the string before comparing with w.

## Classical postprocessing

Estimate P(w) from counts or the statevector, set error=1-P(w), and tabulate error versus queries for both arms.

## Algorithm steps

1. Prepare |s> with H on all search qubits. (eq_1)
2. Arm B: apply k times O (black-box placeholder, one query each) then D = H^n X^n (multi-controlled Z) X^n H^n. (eq_3, eq_4)
3. Arm A: apply m Trotter steps with dt=T/m. The phase factor about |s> is done with H^n, X^n, a multi-controlled phase, X^n and H^n. The factor about |w> must come from oracle queries (assumed construction). (eq_2)
4. Measure the search qubits, compute the error 1-P(w), and compare the two arms at equal query counts. (eq_4, eq_5)

## Assumptions

- Scope chosen by the researcher: n=3, single marked item, known count
- The oracle is a phase-flip placeholder, with an ancilla if needed
- The Trotter arm's non-pi oracle rotations need an unspecified construction
- Exponential error control would require fixed-point or phase-generalised reflections, which are not constructed here

## Missing information

- Exact Hamiltonian normalisation and evolution time used in the paper
- How non-pi oracle rotations are implemented with the black-box oracle
- Explicit fixed-point or generalised-reflection phase schedule
- Error versus step-count formula for Trotter
