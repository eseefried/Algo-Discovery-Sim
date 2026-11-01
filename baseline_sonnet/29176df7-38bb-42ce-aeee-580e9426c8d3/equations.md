# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Reconstruct a minimal model of a 2D discrete-time quantum walk (DTQW) with link cuts and disorder, to study transport from site A to site B along a line of cut links. The abstract gives only qualitative claims, so only generic background walk dynamics are specified.

Scope: One tiny instance: a generic split-step DTQW on a small L x L periodic square lattice with a 4-state coin, a cut line of removed links, and a site-dependent disorder phase. Out of scope: the paper's actual walk operator, disorder model, cut geometry, Floquet Hamiltonian realization, quasienergy winding invariant calculation, and edge-state proof.

## Symbols

- $L$: Linear lattice size (assumed tiny, e.g. 4); domain: integer >= 2
- $\vec{x}=(x,y)$: Lattice site; domain: \{0,\dots,L-1\}^2
- $c$: Coin/direction index (right, left, up, down); domain: \{0,1,2,3\}
- $C$: Coin unitary (assumed Grover coin); domain: 4x4 unitary
- $S$: Conditional shift that reflects (stays in place with flipped direction) on cut links; domain: unitary on position and coin space
- $D$: Diagonal disorder phase operator; domain: diagonal unitary
- $\theta_{\vec{x}}$: Random on-site phase; domain: [0,2\pi)
- $U$: One-step walk operator; domain: unitary
- $A,B$: Source and target sites; domain: lattice sites
- $P_B(t)$: Probability at B after t steps; domain: [0,1]

## eq_1: Walk step

$$
U = S\,D\,(I_{pos}\otimes C)
$$

One step of the DTQW: coin, disorder phase, then shift.

Provenance: `assumption`. Abstract names a disordered 2D DTQW but gives no operator; this is a generic proposed form.

Equation assumptions:

- Operator ordering and the form of disorder are assumed

## eq_2: Disorder

$$
D=\sum_{\vec{x}}e^{i\theta_{\vec{x}}}|\vec{x}\rangle\langle\vec{x}|\otimes I_4
$$

Site-dependent random phases.

Provenance: `assumption`. Simplest disorder model; the paper's model is not given in the abstract.

Equation assumptions:

- Uniform random phases

## eq_3: Shift with cut links

$$
S|\vec{x},c\rangle = \begin{cases}|\vec{x}+\hat{e}_c,c\rangle & \text{link }(\vec{x},\vec{x}+\hat{e}_c)\text{ intact}\\ |\vec{x},\bar{c}\rangle & \text{link cut}\end{cases}
$$

Shift hops along intact links and reflects at cut links, where \bar{c} is the opposite direction.

Provenance: `assumption`. Abstract states links are cut; the reflecting-boundary implementation is an assumption.

Equation assumptions:

- Cut links are the set along a line from A to B
- Reflection convention is assumed

## eq_4: Evolution and transport probability

$$
|\psi_t\rangle=U^t|\psi_0\rangle,\quad P_B(t)=\sum_c|\langle B,c|\psi_t\rangle|^2
$$

State after t steps and probability to be at target B.

Provenance: `standard_background`. Standard definition of discrete-time quantum walk evolution and site probability.

## eq_5: Floquet quasienergy

$$
U|\phi_n\rangle=e^{-i\varepsilon_n}|\phi_n\rangle
$$

Quasienergy eigenproblem for a periodically driven system; the winding invariant is built from the quasienergy bands (details not given).

Provenance: `standard_background`. Abstract mentions a periodically driven Hamiltonian and quasienergy winding; this is only the generic Floquet eigenproblem, not the invariant.

Equation assumptions:

- Unit period

## Registers

- pos: 2*log2(L)=4 qubits for L=4 qubits; Position (x,y) in binary encoding, x register first
- coin: 2 qubits qubits; Direction index c in binary encoding

## Initial state

Assumed localized at source A with a fixed coin state: |\psi_0\rangle=|A\rangle\otimes|c_0\rangle

## Measurement

Measure the position register in the computational basis after t steps to estimate P_B(t).

## Classical postprocessing

Average P_B(t) over disorder realizations and compare cut versus uncut lattices.

## Algorithm steps

1. Choose a tiny L, positions A and B, the cut line of links, and a disorder phase sample. (eq_2, eq_3)
2. Build U from coin, disorder, and shift with cuts, then apply it t times. (eq_1, eq_4)
3. Compute P_B(t) and compare cut versus no-cut cases. Optionally diagonalize U for quasienergies. (eq_4, eq_5)

## Assumptions

- Grover coin, periodic boundaries, reflecting cuts and random phase disorder are all proposed choices
- Single instance with small L
- The abstract's actual walk is not reproduced

## Missing information

- Actual coin and shift operators
- Disorder model and strength
- Cut geometry and boundary conditions
- Floquet Hamiltonian realization
- Definition of the quasienergy winding invariant
- Edge-state construction
