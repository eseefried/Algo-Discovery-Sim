# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Long-time evolution of a discrete-time quantum walk on a finite graph with dynamic percolation (edges randomly present/absent at each step), modeled as a random unitary channel and analyzed via asymptotics of random unitary maps.

Scope: Smallest useful construction: a coined quantum walk on a tiny finite 1D chain (assumed N=3 sites, open boundary) with i.i.d. random edge configurations per step, written as a random unitary channel and its asymptotic (long-time) behavior in background form. The paper's specific solution method, the detailed 1D worked numerical example, the literature review and the 2D Grover-coin results are outside scope.

## Symbols

- $\rho_t$: density matrix of the walker after t steps; domain: positive semidefinite, trace one, on H
- $U_\omega$: unitary one-step operator for edge configuration omega; domain: unitary on H
- $\omega$: random edge configuration (subset of present edges); domain: finite set Omega
- $p_\omega$: probability of configuration omega; domain: [0,1], sum equals 1
- $\Phi$: random unitary channel; domain: CPTP map on operators on H
- $\mathcal{H}$: position-coin Hilbert space; domain: finite-dimensional complex
- $p$: probability an edge is present (assumed independent edges); domain: [0,1]

## eq_1: Random unitary channel

$$
\rho_{t+1}=\Phi(\rho_t)=\sum_{\omega\in\Omega}p_\omega U_\omega \rho_t U_\omega^\dagger
$$

One step of the walk averaged over random edge configurations drawn freshly each step.

Provenance: `abstract_inferred`. Per-step random connections with open system dynamics imply averaging unitary evolutions; the exact form is the standard random unitary map.

Abstract evidence: the connections appear and disappear randomly in each step during the time evolution

Equation assumptions:

- Configurations are i.i.d. across steps
- Finite graph

## eq_2: Edge configuration probability

$$
p_\omega=p^{|\omega|}(1-p)^{|E|-|\omega|}
$$

Probability of configuration omega under independent edge percolation.

Provenance: `assumption`. Proposed concrete percolation model; the abstract does not specify the distribution.

Equation assumptions:

- Independent edges with common probability p

## eq_3: Step operator

$$
U_\omega=S_\omega (I_{\mathrm{pos}}\otimes C)
$$

Coin then shift restricted to present edges; for blocked edges the walker is reflected (assumed rule).

Provenance: `assumption`. Standard coined-walk form; the blocked-edge rule is a choice.

Equation assumptions:

- Reflection at missing edges so U_omega is unitary
- C is a coin unitary, e.g. Hadamard in 1D

## eq_4: Asymptotic decomposition

$$
\lim_{t\to\infty}\Phi^{t}(\rho)=\mathcal{P}_{\mathrm{asym}}(\rho),\quad \mathrm{Fix}(\Phi)=\{X: U_\omega X U_\omega^\dagger=X\ \forall\omega\}
$$

For a random unitary channel, the asymptotic dynamics lives on the peripheral spectrum. The fixed-point set is the commutant of the set {U_omega} (the unital case). Peripheral eigenvalues give rotating components.

Provenance: `standard_background`. Known results on random unitary maps; the paper's specific treatment is not reconstructed here.

Equation assumptions:

- Finite dimension
- Possible non-fixed peripheral eigenvalues give a periodic limit, so the limit may be taken along subsequences

## eq_5: Peripheral eigen-equation

$$
\Phi(X)=e^{i\theta}X,\ \ \Leftrightarrow\ \ U_\omega X U_\omega^\dagger=e^{i\theta}X\ \ \forall\omega:p_\omega>0
$$

Peripheral eigenoperators of a random unitary channel satisfy a common covariance condition for all configurations.

Provenance: `standard_background`. Standard property of unital channels with Kraus unitaries; determines the asymptotic subspace.

Equation assumptions:

- Finite dimension
- Strictly positive weights on the included configurations

## Registers

- position: 3 sites (assumed instance) qubits; walker location on the chain
- coin: 1 qubit per site, or direction space of dimension 2 qubits; internal degree of freedom

## Initial state

Assumed localized state |x_0>|c_0> on the middle site with a fixed coin state, rho_0=|psi_0><psi_0|.

## Classical postprocessing

Numerical diagonalization of the superoperator Phi to obtain the peripheral eigenspace and the limiting position distribution; not a quantum measurement procedure.

## Algorithm steps

1. Fix the tiny instance, the coin, and the edge probability p, and enumerate the configurations Omega and their weights. (eq_2, eq_3)
2. Build the unitaries U_omega and the averaged channel Phi. (eq_1, eq_3)
3. Find the fixed points and the peripheral spectrum of Phi (commutant condition) to obtain the asymptotic state. (eq_4, eq_5)

## Assumptions

- No scope was given, so a 3-site open chain with a Hadamard coin and independent edge percolation is chosen as the smallest instance
- Blocked-edge reflection rule is assumed
- Equations eq_4 and eq_5 are textbook background, not the paper's results
- No claim is made about the paper's actual method or numerical example

## Missing information

- The paper's actual coin operators and boundary conditions
- The precise treatment of percolation correlations
- The explicit solution method and results for 1D chains
- The 2D Grover-coin results
- Any quantum circuit implementation
