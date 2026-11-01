# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Describe Grover search as Hamiltonian evolution and compare two discretisations of the evolution operator: Lie-Trotter product formula (cost scaling as a power law in error) versus reflection-operator steps (cost logarithmic in error).

Scope: Smallest useful construction: Grover search on n=2 qubits (N=4) with one marked item, using the standard two-term Hamiltonian H=|w><w|+|s><s| style evolution, Lie-Trotter step form, and reflection-based Grover iteration as background. The paper's actual error analysis, the specific reflection construction that attains logarithmic error dependence, and the importance sampling and overrelaxation applications are outside scope.

## Symbols

- $N$: Size of the search space; domain: N=2^n, positive integer
- $|w\rangle$: Marked basis state; domain: computational basis state
- $|s\rangle$: Uniform superposition state; domain: N^{-1/2}\sum_x|x\rangle
- $H$: Search Hamiltonian (assumed form); domain: Hermitian operator on n qubits
- $t$: Evolution time; domain: real, t\ge0
- $m$: Number of Lie-Trotter steps; domain: positive integer
- $\epsilon$: Target error; domain: (0,1)
- $R_w,R_s$: Reflections about the marked state and the uniform state; domain: unitary operators

## eq_1: Hamiltonian for Grover search (assumed)

$$
H=|w\rangle\langle w|+|s\rangle\langle s|
$$

Assumed two-projector Hamiltonian whose evolution rotates |s> toward |w>.

Provenance: `standard_background`. Common Hamiltonian form of Grover search; the abstract does not state the Hamiltonian.

Equation assumptions:

- The paper may use a different but equivalent Hamiltonian form.

## eq_2: Exact evolution operator

$$
U(t)=e^{-iHt}
$$

Target unitary for evolution time t, which can be built along different trajectories.

Provenance: `abstract_inferred`. The abstract implies a unitary determined by H and t.

Abstract evidence: the corresponding unitary evolution operator can be constructed in many different ways

Equation assumptions:

- Units with \hbar=1.

## eq_3: Lie-Trotter discretisation

$$
U(t)\approx\left(e^{-i|w\rangle\langle w|t/m}\,e^{-i|s\rangle\langle s|t/m}\right)^m
$$

First-order product formula; the approximation error decreases only polynomially in m, so cost is power-law in 1/\epsilon.

Provenance: `standard_background`. The abstract mentions a straightforward Lie-Trotter formula with power-law error dependence; this is the standard form.

Equation assumptions:

- Error is O(t^2/m) in operator norm, giving m=O(1/\epsilon) (standard first-order bound, not taken from the paper).

## eq_4: Reflection operators

$$
R_w=I-2|w\rangle\langle w|,\quad R_s=2|s\rangle\langle s|-I
$$

Reflection operators used as large steps.

Provenance: `standard_background`. Standard Grover oracle and diffusion operators; the abstract only says reflection operators are used.

## eq_5: Grover iteration and success probability

$$
G=R_sR_w,\quad P_{\mathrm{succ}}(k)=\sin^2\!\big((2k+1)\theta\big),\ \sin\theta=N^{-1/2}
$$

Each reflection step rotates by 2\theta; with N=4, \theta=\pi/6 and k=1 gives P=1.

Provenance: `standard_background`. Standard Grover analysis. The paper's specific scheme for achieving logarithmic error scaling is not reconstructed here.

Equation assumptions:

- Single marked item.

## Registers

- q: n=2 qubits (N=4) qubits; Search register; basis index x encoded as a binary integer with q_0 least significant (assumed)

## Initial state

|s\rangle=H^{\otimes n}|0\rangle^{\otimes n}

## Measurement

Measure q in the computational basis; success if the outcome is w.

## Algorithm steps

1. Prepare the uniform superposition |s>. (no equation reference)
2. Define target evolution U(t) with the assumed Hamiltonian. (eq_1, eq_2)
3. Option A: approximate U(t) with m Lie-Trotter steps. (eq_3)
4. Option B: apply reflection-based Grover iterations. (eq_4, eq_5)

## Assumptions

- Chose n=2, single marked item, as the tiny instance, since no scope was given.
- Hamiltonian form and units are assumed, not taken from the abstract.
- Equations are textbook background and do not reproduce the paper's error analysis.

## Missing information

- Paper's exact Hamiltonian and evolution-time convention
- Construction of the reflection-based scheme achieving logarithmic error scaling, including any phase schedule
- Error bounds and complexity derivations
- Details of the importance sampling and overrelaxation applications
