# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct Grover's quantum search as a Hamiltonian-evolution problem (as announced in the abstract) and contrast two discretisations of the same evolution: a Lie-Trotter product formula with small time steps (error decreasing only as a power law in the step count) versus steps of maximal size pi that turn each exponential into an exact reflection operator, recovering the standard Grover iteration.

Scope: Scoped to a single marked item in an unstructured database of N=2^n items, with the Farhi-Gutmann-type search Hamiltonian H=|s><s|+|t><t|. Tiny explicit instance: n=2 qubits (N=4), marked item t=3 (basis state |11>), for which the exact evolution time is T=pi, one reflection step of size delta=pi equals one Grover iteration, and the marked state is reached exactly. Outside scope: the paper's general theory of trajectory choice between fixed end-points, the derivation of the claimed logarithmic error dependence for reflection-based steps, applications to importance sampling and the analysis of overrelaxation algorithms, and any numerical results.

## Symbols

- $N$: Number of database items, N = 2^n; domain: positive integer power of 2 (instance: N = 4)
- $n$: Number of qubits in the search register; domain: positive integer (instance: n = 2)
- $|t\rangle$: Marked (target) computational basis state, integer t encoded in binary; domain: t in {0,...,N-1} (instance: t = 3, i.e. |11>)
- $|s\rangle$: Uniform superposition over all N basis states (initial state); domain: unit vector in C^N
- $H$: Search Hamiltonian H = |s><s| + |t><t|; domain: Hermitian operator on C^N
- $T$: Total evolution time needed to rotate |s> into |t>; domain: positive real (instance: T = pi)
- $\delta$: Time step of the discretised evolution, delta = T/m; domain: positive real
- $m$: Number of discretisation steps; domain: positive integer
- $\theta$: Half-angle of the Grover rotation, sin(theta) = 1/sqrt(N) = <s|t>; domain: (0, pi/2] (instance: theta = pi/6)
- $k$: Number of Grover iterations (reflection-pair steps); domain: non-negative integer (instance: k = 1)
- $\epsilon$: Target error (operator-norm deviation of the discretised unitary from exp(-iHT), or failure probability); domain: (0,1)
- $G$: Grover iteration, product of the two reflection operators; domain: unitary on C^N

## eq_1: Search Hamiltonian and initial state

$$
H = |s\rangle\langle s| + |t\rangle\langle t|,\qquad |s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle,\qquad \langle s|t\rangle = \frac{1}{\sqrt{N}} = \sin\theta
$$

The standard (Farhi-Gutmann) Hamiltonian formulation of unstructured search: a sum of projectors onto the uniform superposition and the marked state. The dynamics is confined to the 2D subspace spanned by |s> and |t>.

Provenance: `standard_background`. The abstract only states that Grover search is described as a Hamiltonian evolution problem; this specific H is the well-known analog-search Hamiltonian and is assumed to be the one used.

Equation assumptions:

- Single marked item
- The paper uses the projector-sum Hamiltonian H=|s><s|+|t><t| (not confirmed by the abstract)

## eq_2: Exact Hamiltonian evolution and evolution time

$$
\left|\langle t|e^{-iHt}|s\rangle\right|^2 = \sin^2\!\left(\tfrac{t}{\sqrt{N}}\right) + \tfrac{1}{N}\cos^2\!\left(\tfrac{t}{\sqrt{N}}\right),\qquad T = \frac{\pi\sqrt{N}}{2}\ \Rightarrow\ e^{-iHT}|s\rangle \propto |t\rangle
$$

Exact success probability under continuous evolution with H (eq_1); the marked state is reached with certainty (up to a global phase) at time T = pi*sqrt(N)/2. The end-points |s> and |t> are the fixed end-points between which different discretised trajectories are compared.

Provenance: `standard_background`. Follows from diagonalising H in span{|s>,|t>} (eigenvalues 1 +/- 1/sqrt(N)); standard Farhi-Gutmann result.

Equation assumptions:

- Hamiltonian of eq_1
- Units with hbar = 1

## eq_3: Lie-Trotter discretisation and power-law error

$$
e^{-iHT} \approx \left(e^{-i\delta|t\rangle\langle t|}\,e^{-i\delta|s\rangle\langle s|}\right)^{m},\quad \delta = \tfrac{T}{m},\qquad \left\|e^{-iHT} - \left(e^{-i\delta|t\rangle\langle t|}e^{-i\delta|s\rangle\langle s|}\right)^{m}\right\| \le \frac{T^{2}}{2m}\left\|[|s\rangle\langle s|,|t\rangle\langle t|]\right\| \ \Rightarrow\ m = O\!\left(\frac{T^{2}}{\epsilon}\right)
$$

First-order Lie-Trotter product formula splitting H into its two projector terms; the number of steps needed for operator error epsilon grows as a power law (here 1/epsilon) in the error. Each factor is implementable as a phase gate: exp(-i delta |t><t|) = 1 + (e^{-i delta}-1)|t><t| and exp(-i delta |s><s|) = H^{\otimes n} exp(-i delta |0><0|) H^{\otimes n}.

Provenance: `abstract_inferred`. The abstract states a power-law error dependence for Lie-Trotter; the explicit first-order product formula and its standard commutator error bound are background recalled to make that statement concrete. The abstract does not state the exponent, so O(T^2/epsilon) is the generic first-order bound, not a paper-specific result.

Abstract evidence: the computational complexity has a power-law dependence on error when a straightforward Lie-Trotter discretisation formula is used

Equation assumptions:

- First-order (symmetric or not) Lie-Trotter splitting into the two projector terms of eq_1
- Error measured in operator norm; the paper's exact error measure is unknown

## eq_4: Maximal step delta = pi gives exact reflections and the Grover iteration

$$
e^{-i\pi|s\rangle\langle s|} = 1 - 2|s\rangle\langle s|,\qquad e^{-i\pi|t\rangle\langle t|} = 1 - 2|t\rangle\langle t|,\qquad G = \left(2|s\rangle\langle s| - 1\right)\left(1 - 2|t\rangle\langle t|\right),\qquad G^{k}|s\rangle = \sin\!\big((2k+1)\theta\big)|t\rangle + \cos\!\big((2k+1)\theta\big)|t^{\perp}\rangle
$$

Because the projectors have eigenvalues 0 and 1, a step of size pi turns each exponential into an exact reflection (no approximation). The product of the two reflections is (up to sign) the Grover iteration, an exact rotation by 2 theta in the span of |s> and |t>, where |t^perp> is the normalised component of |s> orthogonal to |t>. The number of steps is k ~ pi*sqrt(N)/4, i.e. T/delta with delta = pi.

Provenance: `abstract_inferred`. The abstract says reflection operators replace the small Trotter steps and that the key idea is making steps as large as possible; the identity exp(-i pi P) = 1-2P for a projector P, and the resulting Grover rotation formula, are standard background that realise this. The abstract's claim that the error dependence then becomes logarithmic is reported but its mechanism is not reconstructible from the abstract.

Abstract evidence: it becomes logarithmic in error when reflection operators are used

Equation assumptions:

- The 'reflection operators' of the abstract are exp(-i pi |s><s|) and exp(-i pi |t><t|)
- Overall sign/global phase of G ignored

## eq_5: Explicit instance N = 4, t = 3

$$
n = 2,\ N = 4,\ \theta = \tfrac{\pi}{6},\ T = \pi,\ \delta = \pi \Rightarrow m = k = 1,\qquad G|s\rangle = \sin\!\left(\tfrac{\pi}{2}\right)|11\rangle = |11\rangle\ \text{(exactly)},\qquad 1 - 2|t\rangle\langle t| = CZ,\quad 2|s\rangle\langle s| - 1 = -\,H^{\otimes 2}\,(1 - 2|00\rangle\langle 00|)\,H^{\otimes 2}
$$

Smallest nontrivial instance: with two qubits the exact evolution time is T = pi, a single maximal step of size pi is one Grover iteration, and the marked state |11> is reached with probability exactly 1. For t = 3 the oracle reflection is a controlled-Z gate; the diffusion reflection is a conjugated reflection about |00>, implementable as H^{\otimes 2} X^{\otimes 2} CZ X^{\otimes 2} H^{\otimes 2} up to global phase.

Provenance: `assumption`. Chosen as the tiny explicit instance for the later circuit stage; not taken from the abstract.

Equation assumptions:

- Little-endian encoding |x> = |x_1 x_0>, qubit 0 least significant
- Marked item t = 3

## Registers

- search: n = 2 (general: n = log2 N) qubits; Holds the N-dimensional search space; basis state |x> encodes integer x with qubit 0 as least significant bit.

## Initial state

|0>^{\otimes n} on the search register; Hadamards on every qubit then prepare |s> = N^{-1/2} sum_x |x> (eq_1). For the instance: |00> -> (|00>+|01>+|10>+|11>)/2.

## Measurement

Computational-basis measurement of all n qubits of the search register. Success probability sin^2((2k+1) theta) for discretisation B (exactly 1 for N=4, k=1, outcome bit string 11); for discretisation A the success probability approaches the exact-evolution value of eq_2 as m grows.

## Classical postprocessing

Read the measured bit string as integer x (little-endian) and check it against the oracle/marked-item condition; repeat the circuit if the check fails. For the error study, compare the measured success frequency (or the simulated operator-norm error) against m for discretisation A and against k for discretisation B.

## Algorithm steps

1. Prepare the uniform superposition |s> by applying H^{\otimes n} to |0>^{\otimes n}. (eq_1)
2. Fix the end-points: the target of the whole procedure is to implement exp(-iHT)|s> ∝ |t> with T = pi*sqrt(N)/2 (instance T = pi). (eq_2)
3. Discretisation A (small steps, for comparison): apply m repetitions of the pair exp(-i delta |t><t|) (a controlled phase on the marked state) followed by exp(-i delta |s><s|) = H^{\otimes n} exp(-i delta |0><0|) H^{\otimes n}, with delta = T/m; the deviation from exp(-iHT) decreases only as a power law in m. (eq_3)
4. Discretisation B (maximal steps): choose delta = pi so each factor is an exact reflection; apply k = round(pi/(4 theta) - 1/2) Grover iterations G = (2|s><s|-1)(1-2|t><t|). For the instance, k = 1: apply CZ (oracle reflection), then H^{\otimes 2} X^{\otimes 2} CZ X^{\otimes 2} H^{\otimes 2} (diffusion reflection). (eq_4, eq_5)
5. Measure the search register in the computational basis. (eq_4, eq_5)

## Assumptions

- The paper's Hamiltonian is the projector-sum H = |s><s| + |t><t| (Farhi-Gutmann); the abstract does not state the Hamiltonian explicitly.
- The 'reflection operators' are the delta = pi exponentials of the two projectors, so that the reflection-based trajectory is the standard Grover iteration.
- Single marked item; N a power of 2; little-endian integer encoding of basis states.
- Instance choice N = 4, t = 3 is made here for concreteness and is not from the abstract.
- Error for the Trotter trajectory is quantified by the first-order operator-norm bound; the paper may use a different error measure and may obtain a different power-law exponent.

## Missing information

- The explicit Hamiltonian and splitting used in the paper (assumed here).
- The precise power-law exponent for the Lie-Trotter trajectory and the error measure used.
- The mechanism by which the reflection-based trajectory achieves logarithmic dependence of complexity on error (e.g. whether it refers to the exactness of each reflection step, residual rotation-angle mismatch when pi/(4 theta) is non-integer, or some additional correction scheme); the abstract gives no formula.
- The general criterion for choosing among trajectories between fixed end-points, and how it transfers to importance sampling and overrelaxation algorithms.
- Any numerical or analytical results on constants, scaling, or specific instances.
