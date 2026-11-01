# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Convert an open quantum walk (OQW, quantum Markov chain) on a graph into a unitary quantum walk generalizing Szegedy's quantization of Markov chains, and define the node probability, mean (time-averaged) probability, and its asymptotic limit. The abstract gives no explicit construction.

Scope: Background-level reconstruction of (i) the OQW update rule, (ii) the standard Szegedy walk for a classical Markov chain, and (iii) the definition of node probability and Cesaro mean probability, on a tiny assumed instance (2-node graph with 2-dim internal space). The paper-specific OQW-to-unitary conversion, its Kraus-operator-dependent isometry, and the asymptotic mean probability result are outside scope and not reconstructed.

## Symbols

- $V$: set of graph nodes; domain: finite or countable set; assumed {0,1} in tiny instance
- $\mathcal{H}_V$: node (position) Hilbert space with basis |i>; domain: span{|i>: i in V}
- $\mathcal{H}_C$: internal (coin) Hilbert space; domain: C^d, d=2 assumed
- $B_{ij}$: OQW Kraus operator on H_C for a transition from node j to node i; domain: d x d complex matrices
- $\rho_i(t)$: unnormalized internal state at node i at step t; domain: positive semidefinite d x d matrices
- $p_{ij}$: Markov chain transition probability from i to j; domain: [0,1], rows sum to 1
- $|\phi_i\rangle$: Szegedy state sum_j sqrt(p_ij)|i>|j>; domain: unit vector in H_V⊗H_V
- $\Pi$: projector onto span{|\phi_i>}; domain: projector
- $R$: Szegedy reflection 2Π - I; domain: unitary on H_V⊗H_V
- $S$: swap operator on H_V⊗H_V; domain: unitary
- $P_t(i)$: probability of finding the walk at node i at step t; domain: [0,1]
- $\bar P_T(i)$: mean probability over first T steps; domain: [0,1]

## eq_1: OQW update

$$
\rho_i(t+1)=\sum_{j} B_{ij}\,\rho_j(t)\,B_{ij}^{\dagger},\qquad \sum_i B_{ij}^{\dagger}B_{ij}=I\ \ \forall j
$$

Standard open quantum walk dynamics with completeness condition per source node.

Provenance: `standard_background`. Recalled definition of OQWs; the abstract only says OQWs on lattices/graphs are converted.

Equation assumptions:

- Kraus-operator form of OQW of Attal et al.

## eq_2: Szegedy walk operator

$$
|\phi_i\rangle=\sum_j\sqrt{p_{ij}}\,|i\rangle|j\rangle,\quad \Pi=\sum_i|\phi_i\rangle\langle\phi_i|,\quad W=S\,(2\Pi-I)
$$

Szegedy quantization of a classical Markov chain; the abstract says the work generalizes this framework.

Provenance: `standard_background`. The abstract names Szegedy's framework but states no formulas; this is the recalled classical form, not the OQW generalization.

Equation assumptions:

- Szegedy walk operator as commonly written; the paper's variant may differ

## eq_3: Node probability

$$
P_t(i)=\mathrm{Tr}\,\rho_i(t)\ \text{(OQW)};\quad P_t(i)=\langle\psi_t|\,(|i\rangle\langle i|\otimes I)\,|\psi_t\rangle\ \text{(unitary walk, assumed position-first register)}
$$

Probability of finding the walk at node i.

Provenance: `abstract_inferred`. The abstract says a node probability is defined; the specific form is the natural projective one, assumed.

Abstract evidence: we define the probability and the mean probability of finding the walk at a node

Equation assumptions:

- Register ordering with node register first; the paper's unitary walk Hilbert space is unknown

## eq_4: Mean probability and limit

$$
\bar P_T(i)=\frac{1}{T}\sum_{t=0}^{T-1}P_t(i),\qquad \bar P_\infty(i)=\lim_{T\to\infty}\bar P_T(i)
$$

Cesaro mean probability and its asymptotic value.

Provenance: `abstract_inferred`. A mean probability and its asymptotic limit are mentioned; the time-average form is the standard reading, assumed. The limit value is not derived here.

Abstract evidence: then derive the asymptotic mean probability

Equation assumptions:

- Mean means a uniform time average

## Registers

- node: ceil(log2|V|) qubits (1 qubit for the assumed 2-node graph) qubits; graph node label
- internal/aux: unknown (d=2 assumed: 1 qubit) qubits; OQW internal space or Szegedy second register; paper's actual extended space unknown

## Measurement

Measure the node register in the computational basis at step t to estimate P_t(i); the paper's measurement is not stated.

## Classical postprocessing

Average the node distributions over t=0..T-1 to estimate the mean probability.

## Algorithm steps

1. Fix a tiny instance: 2-node graph, d=2, with chosen Kraus operators B_ij satisfying completeness, and an initial internal state at one node. (eq_1)
2. Evolve the OQW classically-mixed dynamics as the reference to be reproduced by the unitary construction. (eq_1, eq_3)
3. For the underlying Markov chain, build the Szegedy walk operator as a background comparison; the paper's OQW-specific unitary is not specified. (eq_2)
4. Compute node probabilities and the time-averaged mean probability over T steps. (eq_3, eq_4)

## Assumptions

- No scope provided; chose a tiny 2-node, d=2 instance as the smallest useful construction.
- Equations 1 and 2 are background recollections, not evidence of the paper's construction.

## Missing information

- The explicit OQW-to-unitary construction (Hilbert space, isometry, coin/reflection operators).
- How Kraus operators B_ij enter the unitary walk.
- The formula and conditions for the asymptotic mean probability.
- The initial states and graph/lattice specifics used.
