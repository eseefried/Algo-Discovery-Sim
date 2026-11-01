# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Quantized density classification: a Quantum Particle Automata (QPA) evolves under a unitary operator U (parameterized by theta), and after measurement the particle's position basis state falls on one side of a boundary partition, deciding whether a length-5 binary input has majority 0 or majority 1. A Genetic Algorithm searches for U and the boundary partition.

Scope: Finite instance with binary input length n=5 only; the abstract states that scaling to arbitrary n is future work. The exact form of U, the encoding of inputs into the QPA state, and the GA details are not given in the abstract.

## Symbols

- $n$: Length of binary input; domain: positive integer; n=5 in the study
- $U$: Unitary operator driving the QPA evolution, found by the GA; domain: unitary matrix on the particle position space
- $\theta$: Parameter of U controlling the particle's effective mass and evolution speed; domain: real number
- $B$: Boundary partition of basis states used to decide the majority; domain: partition of basis states into two sets

## eq_1: Evolution

$$
|\psi_{t}\rangle = U^{t}|\psi_0\rangle
$$

QPA state after t evolution steps under the unitary operator U

Provenance: `assumption`. The abstract says the QPA needs a unitary operator for its evolution; the power form is an assumed standard discrete-time model.

Equation assumptions:

- Discrete time steps with the same U applied at each step

## eq_2: Decision rule

$$
P_1=\sum_{x\in B_1}|\langle x|\psi_t\rangle|^2,\quad \text{decide majority 1 if } P_1>1/2
$$

Probability that the measured particle lands on the side B_1 of the boundary partition; used to decide the majority density

Provenance: `assumption`. The abstract says the particle is more likely to collapse to basis states on the correct side of the boundary partition; the threshold 1/2 is assumed.

Equation assumptions:

- B_1 is the side associated with majority 1
- The 1/2 threshold is an assumption

## Registers

- particle: unknown (position space dimension not given; assumed at least 2^5=32 basis states if inputs are encoded as positions) qubits; QPA particle position register holding the encoded input and evolving under U

## Initial state

Assumed: |psi_0> is the particle prepared in the basis state (or superposition) encoding the length-5 binary input; the encoding is not given in the abstract.

## Measurement

Measure the particle position in the computational (position) basis after the evolution. The outcome x is assigned to one side of the GA-found boundary partition B; the side containing x gives the decision (majority 0 or majority 1). Success probability is the mass on the correct side (eq_2).

## Classical postprocessing

Compare the measured basis state to the boundary partition and output the majority label. Repeating the run and taking the majority of outcomes, or estimating P_1 and thresholding it, is an assumed option. The GA fitness would presumably be the correct-side probability over all 32 inputs (assumed; not stated).

## Algorithm steps

1. Encode the length-5 binary input into the initial particle state |psi_0>. (no equation reference)
2. Apply the GA-found unitary U (parameterized by theta) for t steps to evolve the particle. (eq_1)
3. Compute the probability mass on each side of the GA-found boundary partition, to be used for the decision. (eq_2)

## Assumptions

- The equations are generic assumed models, not taken from the paper.
- Register size and input encoding are assumed.
- Particle register dimension and input encoding are assumed.
- Measurement in the position basis and the 1/2 threshold are assumed.

## Missing information

- Exact form of U and its dependence on theta
- Encoding of the binary input into the initial QPA state
- Number of evolution steps
- GA fitness function and parameters
- Boundary partition found
- Actual position space dimension of the QPA
- Handling of ties for inputs of length 5 (none exist, since n is odd)
