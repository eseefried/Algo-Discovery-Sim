# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Estimate how a continuous-time quantum walk searches on a graph by sketching small weighted graphs with self-loops and applying degenerate perturbation theory, including a case where evolution occurs in a subspace whose dimension grows with N.

Scope: Abstract-level reconstruction of the search model only: continuous-time quantum walk search with a marked-vertex oracle Hamiltonian and degenerate perturbation theory on effective small weighted graphs. Specific graphs, results and circuits are not given in the abstract.

## Symbols

- $N$: Number of vertices of the graph; domain: positive integer
- $H$: Search Hamiltonian, a graph term plus an oracle term; domain: Hermitian operator on N-dimensional space
- $H_0$: Unperturbed Hamiltonian whose degenerate subspace is treated perturbatively; domain: Hermitian operator
- $V$: Perturbation coupling the degenerate subspace to the rest; domain: Hermitian operator

## eq_1: Search Hamiltonian

$$
H = -\gamma L - |w\rangle\langle w|
$$

Standard continuous-time quantum walk search Hamiltonian with graph Laplacian L, hopping rate gamma and marked vertex w; assumed form, not stated in the abstract.

Provenance: `standard_background`. Common CTQW search model; the abstract mentions a randomly walking particle searching a graph but gives no formula.

Equation assumptions:

- Marked vertex w; Laplacian-type hopping term

## eq_2: Degenerate perturbation theory

$$
H_{\mathrm{eff}} = P V P + \sum_{k\notin D} \frac{P V |k\rangle\langle k| V P}{E_0-E_k}
$$

Effective Hamiltonian on degenerate subspace D of H_0 with projector P, up to second order.

Provenance: `standard_background`. Standard degenerate perturbation theory background, which the abstract says is used.

Equation assumptions:

- Perturbative regime

## Registers

- vertex: ceil(log2 N) qubits (assumed vertex-basis encoding) qubits; Position of the walker on the graph vertices; the walk is simulated as Hamiltonian evolution, not a gate-based circuit

## Initial state

Assumed uniform superposition over all vertices, (1/sqrt(N)) sum_v |v>, the usual CTQW search start; not stated in the abstract.

## Measurement

Assumed: after evolution for time t, measure the vertex register in the computational (vertex) basis and read out the marked vertex w with probability |<w|psi(t)>|^2. Not specified in the abstract.

## Classical postprocessing

Assumed: repeat the evolve-and-measure procedure, check whether the outcome is the marked vertex using the oracle, and repeat if not. The evolution time is chosen near the peak success probability from the effective small-graph analysis. Not specified in the abstract.

## Algorithm steps

1. Prepare the assumed uniform superposition on the vertex register. (no equation reference)
2. Evolve under the search Hamiltonian H for a time t, which is assumed to be implemented via Hamiltonian simulation. (eq_1)
3. Analyze the dynamics by restricting to the degenerate subspace and using the effective Hamiltonian, which corresponds to a small weighted graph with self-loops. (eq_2)

## Assumptions

- Search Hamiltonian form is the standard CTQW search model, not given in abstract.
- Uniform initial state and vertex-register encoding are assumed, not given in abstract.
- Computational-basis vertex measurement and repeat-until-success postprocessing are assumed, not given in abstract.
- Computational-basis vertex measurement and repeat-until-success postprocessing are assumed.

## Missing information

- Specific graphs, weights and self-loop values
- Scaling results and runtime
- Circuit implementation details
- Optimal gamma and evolution time
- Explicit measurement protocol and success probability from the paper
