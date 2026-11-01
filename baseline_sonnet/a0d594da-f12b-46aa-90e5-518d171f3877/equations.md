# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Quantized density classification with a Quantum Particle Automaton (QPA): for a binary input of length 5, evolve a single-particle state with a unitary U and decide majority 0 or 1 by the probability mass on either side of a boundary partition of position basis states. U and the partition are found by a genetic algorithm.

Scope: Smallest construction: n=5 binary input encoded as the initial particle amplitude on a 5-site line, evolution by an unspecified unitary U(theta), a boundary partition of basis states into two sets, and a GA fitness defined as classification accuracy. Not covered: the actual GA design details, the specific unitary form, the parameter theta's exact role, the found solutions, scaling to arbitrary n, and the QPA definition from the cited source.

## Symbols

- $n$: input length (here 5); domain: positive integer, n=5
- $x$: binary input string; domain: {0,1}^5
- $|\psi_0(x)\rangle$: initial particle state encoding x (encoding is assumed); domain: unit vector in C^5
- $U$: unitary evolution operator found by GA; domain: U(5)
- $t$: number of evolution steps; domain: nonnegative integer
- $\theta$: parameter of U that sets the evolution speed (small theta: small mass, fast evolution); domain: real, unspecified
- $B_0,B_1$: boundary partition of position basis states into the two decision sides; domain: disjoint subsets of {0,...,4} whose union is {0,...,4}
- $P_b(x)$: probability that the measured particle lies in B_b; domain: [0,1]
- $f(x)$: true majority label of x; domain: {0,1}
- $F$: GA fitness: classification accuracy over inputs; domain: [0,1]

## eq_1: Evolution

$$
|\psi_t(x)\rangle = U^t |\psi_0(x)\rangle
$$

Unitary evolution of the particle state for t steps

Provenance: `abstract_inferred`. The abstract says a unitary operator carries out the evolution; the power-t form assumes a discrete-time repeated application.

Abstract evidence: the QPA needed a unitary operator to carry out the QPA evolution

Equation assumptions:

- discrete time steps
- same U at each step

## eq_2: Side probability

$$
P_b(x)=\sum_{j\in B_b} |\langle j|\psi_t(x)\rangle|^2
$$

Born-rule probability that the particle collapses to a basis state in side B_b of the partition

Provenance: `abstract_inferred`. Collapse to basis states on a side of a partition implies Born-rule probabilities summed over that side.

Abstract evidence: when the particle was measured, it was more likely to collapse to the basis states that were on the correct side of the boundary partition

Equation assumptions:

- position-basis measurement

## eq_3: Decision rule

$$
\hat f(x)=\arg\max_{b\in\{0,1\}} P_b(x)
$$

Classify as majority 0 or 1 according to the more probable side

Provenance: `assumption`. A natural decision rule consistent with 'more likely to collapse' to the correct side; the exact rule is not given.

Equation assumptions:

- B_b is associated with majority-b label

## eq_4: GA fitness

$$
F(U,B_0,B_1)=\frac{1}{32}\sum_{x\in\{0,1\}^5}\mathbf 1[\hat f(x)=f(x)]
$$

Fraction of the 32 inputs classified correctly; the GA searches for U and the partition maximizing this

Provenance: `assumption`. Plausible fitness for the described GA search; the actual fitness is not stated.

Equation assumptions:

- accuracy-based fitness
- all 32 inputs used

## eq_5: Majority label

$$
f(x)=\mathbf 1\left[\sum_{i=1}^{5}x_i\ge 3\right]
$$

Majority density label for odd length 5 (no ties)

Provenance: `standard_background`. The standard definition of density classification; length 5 is odd so it is well defined.

## Registers

- position: 5 basis states (ceil(log2 5)=3 qubits if embedded) qubits; particle position on the 5-site lattice; qubit embedding is assumed

## Initial state

Not specified in the abstract; assumed |psi_0(x)> encodes the 5-bit input x as a function of site (e.g. amplitudes weighted by the bits), normalized.

## Measurement

Measure the particle in the position basis and assign the outcome to side B_0 or B_1 of the boundary partition.

## Classical postprocessing

Aggregate outcomes into side probabilities or a majority vote over shots; GA fitness evaluation and selection over candidate (U, partition) pairs.

## Algorithm steps

1. Encode input x into the initial particle state (encoding assumed). (no equation reference)
2. Apply the GA-found unitary U for t steps. (eq_1)
3. Measure the position and compute side probabilities for the partition. (eq_2)
4. Decide majority label from the more probable side. (eq_3, eq_5)
5. Outer classical loop: GA optimizes U and the partition using the fitness. (eq_4)

## Assumptions

- Input encoding, lattice geometry, number of steps t, and boundary structure are not given in the abstract and are assumed.
- The functional form of U(theta) is not given; U is treated as a general unitary.
- The GA's operators, population, and fitness are not given; the fitness is an assumed accuracy.

## Missing information

- QPA definition and the exact form of U including the role of theta
- Input encoding into the initial state
- Boundary partition structure
- GA representation, operators, and fitness
- Number of evolution steps
- Found solutions and success rates
- Scaling to arbitrary n
