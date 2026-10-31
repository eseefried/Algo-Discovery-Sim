# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Describe the long-time asymptotic dynamics of a discrete-time quantum walk on finite dynamic percolation graphs, where edges appear and disappear randomly at each step. The evolution is a random unitary map, and the long-time limit is analyzed with asymptotic methods for such maps. The 1D chain is treated in detail, and the 2D integer lattice with a Grover coin is summarized.

Scope: Abstract-level reconstruction of the random-unitary-map formulation and a tiny finite example, such as a short 1D chain. It does not reproduce the paper's specific results, numerical example values, or 2D lattice findings.

## Symbols

- $U_\omega$: Unitary one-step walk operator for percolation edge configuration \omega; domain: unitary operator on the coin-position Hilbert space
- $\rho$: Density matrix of the walker; domain: positive trace-one operators
- $p_\omega$: Probability of edge configuration \omega in one step; domain: [0,1], summing to 1 over \omega
- $\Phi$: Random unitary channel describing the averaged one-step evolution; domain: completely positive trace-preserving map

## eq_1: Random unitary map

$$
\Phi(\rho)=\sum_{\omega} p_\omega\, U_\omega \rho U_\omega^\dagger
$$

Averaged one-step evolution over random edge configurations, with a fresh configuration drawn independently each step.

Provenance: `abstract_inferred`. The abstract names random unitary maps as the framework. The explicit form is standard background and assumes independent configurations per step.

Abstract evidence: applying the asymptotic methods concerning random unitary maps

Equation assumptions:

- Edge configurations are i.i.d. across steps
- Finite graph

## eq_2: Long-time evolution

$$
\rho_t=\Phi^t(\rho_0),\quad \rho_\infty=\lim_{t\to\infty}\Phi^t(\rho_0)
$$

Asymptotics of the averaged state. In general the limit may be a periodic or oscillating asymptotic behavior rather than a single fixed point.

Provenance: `abstract_inferred`. Directly follows from the stated long-time evolution goal. The limit may not exist in general.

Abstract evidence: solve the evolution on finite percolation graphs in the long time limit

Equation assumptions:

- Limit taken along a suitable subsequence if the dynamics is periodic

## Registers

- coin: 2 (1D chain; a 4-dimensional coin for the 2D lattice) qubits; Internal coin degree of freedom
- position: N sites (symbolic, finite graph) qubits; Walker vertex on the finite chain or graph

## Initial state

Assumed finite instance: a localized walker with an arbitrary coin state, rho_0 = |x_0,c_0><x_0,c_0|, on a short 1D chain.

## Measurement

Assumed: after t steps, measure the walker in the position basis (coin traced out) to get P_t(x)=sum_c <x,c|rho_t|x,c>. Repeat over many runs and edge-configuration samples. The averaged state rho_t is the ensemble average, so the statistics match Phi^t(rho_0).

## Classical postprocessing

Estimate P_t(x) from outcome frequencies for several large t. Compare with the asymptotic distribution from rho_infinity, or with its periodic or time-averaged version if the limit oscillates. Check convergence, for example by total variation distance between successive t.

## Algorithm steps

1. Prepare the initial coin-position state rho_0. (no equation reference)
2. At each time step, draw an independent edge configuration omega with probability p_omega. (eq_1)
3. Apply the coin operator and the conditional shift U_omega, which is blocked on missing edges. Averaging over omega gives the channel Phi. (eq_1)
4. Repeat for t steps and analyze the asymptotic behavior of Phi^t. (eq_2)

## Assumptions

- Independent identically distributed edge configurations per step
- Finite graph
- Coin dimension 2 for the 1D chain is assumed
- Shift is blocked on missing edges (assumed convention)
- Position-basis measurement is assumed; the abstract does not specify a measurement

## Missing information

- Specific coin operators for the 1D chain
- Percolation probabilities
- Numerical example details
- 2D Grover results
- Exact shift rule on missing edges (reflection vs. staying put)
- Observables used in the paper
