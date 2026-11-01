# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Convert an open quantum walk (quantum Markov chain) on a lattice or finite graph into a unitary quantum walk, generalizing Szegedy's quantization of Markov chains. Define the probability and mean probability of finding the walk at a node, and derive the asymptotic mean probability.

Scope: Abstract-level reconstruction of the unitary-walk construction and the node probability definitions. The explicit unitary, the OQW Kraus operators, and the asymptotic result are not given in the abstract; only a generic finite-graph instance can be sketched.

## Symbols

- $P_t(x)$: Probability of finding the unitary walk at node x after t steps; domain: [0,1]
- $\bar{P}_T(x)$: Mean (time-averaged) probability at node x over T steps; domain: [0,1]
- $\bar{P}_\infty(x)$: Asymptotic mean probability at node x; domain: [0,1]
- $U$: Unitary operator of the quantum walk (its explicit form is not given in the abstract); domain: unitary on the walk Hilbert space

## eq_1: Node probability

$$
P_t(x)=\mathrm{Tr}\left[\Pi_x U^t\rho_0 U^{\dagger t}\right]
$$

Probability of finding the walk at node x after t steps, where \Pi_x projects onto the subspace associated with node x

Provenance: `abstract_inferred`. The abstract says a node probability is defined; this projector form is an assumed standard realization, not the paper's definition.

Abstract evidence: we define the probability and the mean probability of finding the walk at a node

Equation assumptions:

- \Pi_x is the projector onto node x
- \rho_0 is the initial state

## eq_2: Mean probability

$$
\bar{P}_T(x)=\frac{1}{T}\sum_{t=0}^{T-1}P_t(x)
$$

Time-averaged probability at node x

Provenance: `abstract_inferred`. The standard Cesaro mean is assumed as the meaning of mean probability.

Abstract evidence: the mean probability of finding the walk at a node

Equation assumptions:

- The mean is taken over time steps

## eq_3: Asymptotic mean probability

$$
\bar{P}_\infty(x)=\lim_{T\to\infty}\bar{P}_T(x)
$$

Long-time limit of the mean probability

Provenance: `abstract_inferred`. The abstract states that the asymptotic mean probability is derived; the limit form is the natural definition.

Abstract evidence: then derive the asymptotic mean probability

Equation assumptions:

- The limit exists

## Registers

- node: ceil(log2 N) qubits for N nodes (assumed) qubits; Position/node register of the graph
- coin: ceil(log2 d) qubits for max degree d (assumed) qubits; Auxiliary register for edge/direction, Szegedy-style (assumed)

## Initial state

Assumed: a node-localized state |x0>|c0> on node and auxiliary registers, with rho_0 its density matrix; the actual initial state is not given in the abstract.

## Measurement

Assumed: after t applications of U, measure the node register in the computational basis (projectors Pi_x, tracing out the auxiliary register) to sample x with probability P_t(x); repeat over many runs and over t=0..T-1.

## Classical postprocessing

Estimate P_t(x) by outcome frequencies, average over t to get the mean probability (eq_2), and examine the large-T trend to estimate the asymptotic mean probability (eq_3). The paper's analytic derivation of the limit is not given in the abstract.

## Algorithm steps

1. Prepare the initial state on the node and auxiliary registers. (no equation reference)
2. Apply the unitary walk step U (a Szegedy-type construction built from the OQW transition data; explicit form unknown) t times. (eq_1)
3. Repeat for t=0..T-1 to build the time-averaged node distribution. (eq_2, eq_3)

## Assumptions

- Node probabilities are given by projector measurements on the unitary walk state
- Mean probability is the time average
- Projector-based probabilities and a Cesaro mean are assumed
- Register sizes and the two-register layout are assumed Szegedy-style
- Register layout is a generic node plus auxiliary register, assumed rather than taken from the abstract
- Measurement is a computational-basis readout of the node register

## Missing information

- Explicit unitary construction from the OQW Kraus operators
- Form of the Hilbert space and the node projectors
- Closed form of the asymptotic mean probability
- Initial state and the circuit realization
- Explicit Szegedy-type operator for OQWs
- Asymptotic mean probability formula
- Actual register structure and gate decomposition of U
