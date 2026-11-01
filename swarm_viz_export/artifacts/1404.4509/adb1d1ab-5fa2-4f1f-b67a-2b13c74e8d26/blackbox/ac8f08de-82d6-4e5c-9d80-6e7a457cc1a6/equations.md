# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Dynamic percolation quantum walk on a 4-site cycle: each step draws a random edge-presence mask, giving a random unitary channel whose long-time limit is set by the peripheral spectrum. The circuit simulates one fixed mask sequence, a single trajectory, and averaging is classical.

Scope: Single trajectory of a coined Hadamard walk on a 4-cycle with T fixed classical mask configurations compiled into gates. The ensemble channel and its asymptotic attractor are given as background equations and computed classically. The 2D Grover-coin lattice, the paper's own asymptotic construction and the numerical example are outside scope.

## Symbols

- $x$: walker position on the cycle; domain: {0,1,2,3}
- $c$: coin value, 0=L, 1=R; domain: {0,1}
- $\omega$: edge mask; \omega_e=1 means edge e between sites e and e+1 mod 4 is open; domain: {0,1}^4
- $p$: probability that an edge is open, independent per edge and per step; domain: [0,1]
- $U_\omega$: one-step unitary for mask \omega; domain: unitary on C^4 tensor C^2
- $H$: Hadamard coin; domain: 2x2 unitary
- $T$: number of steps; domain: positive integer

## eq_1: Step unitary for fixed mask

$$
U_\omega=S_\omega\,(I_{pos}\otimes H),\quad S_\omega|x,R\rangle=\begin{cases}|x+1,R\rangle&\omega_x=1\\|x,L\rangle&\omega_x=0\end{cases},\quad S_\omega|x,L\rangle=\begin{cases}|x-1,L\rangle&\omega_{x-1}=1\\|x,R\rangle&\omega_{x-1}=0\end{cases}
$$

Coined shift with reflection (coin flip, no move) at closed edges. Position indices mod 4. It is unitary: the map is a permutation of basis states (a closed edge swaps the L and R states at the two ends consistently).

Provenance: `assumption`. Concrete choice of percolation shift for the minimal instance. The abstract does not specify the shift rule.

Equation assumptions:

- Reflecting rule at closed edges
- Hadamard coin H=(1/sqrt2)[[1,1],[1,-1]]
- Sites are labeled in cyclic order with edge e joining sites e and e+1 mod 4

## eq_2: Trajectory state

$$
|\psi_T\rangle=U_{\omega_T}\cdots U_{\omega_1}|x=0\rangle|c=+\rangle,\quad |+\rangle=(|0\rangle+|1\rangle)/\sqrt2
$$

Circuit output for a fixed mask sequence. Qubit ordering is x0,x1 (x=x0+2x1) and coin.

Provenance: `assumption`. Defines the implementable unitary for one realization.

Equation assumptions:

- Masks are classical parameters compiled into gates

## eq_3: Random unitary channel

$$
\Phi(\rho)=\sum_{\omega}P(\omega)\,U_\omega\rho U_\omega^\dagger,\quad P(\omega)=\prod_{e=0}^{3}p^{\omega_e}(1-p)^{1-\omega_e}
$$

Mask-averaged one-step dynamics. The state after T steps is Phi^T(rho_0).

Provenance: `abstract_inferred`. Random i.i.d. edge presence at each step gives a random unitary map. The product form of P assumes independence.

Abstract evidence: the connections appear and disappear randomly in each step during the time evolution

Equation assumptions:

- Edges are independent with identical p

## eq_4: Peripheral/attractor space

$$
\Phi^T(\rho)\to\Phi_\infty(\rho),\quad \text{peripheral eigenvectors }X:\ U_\omega X U_\omega^\dagger=\lambda X\ \forall\omega\text{ with }P(\omega)>0,\ |\lambda|=1
$$

Standard random unitary map asymptotics: the long-time limit lives on the span of the peripheral eigenoperators. Only these survive and everything else decays. This is recalled background, not the paper's specific formulas.

Provenance: `standard_background`. Known result for unital channels with Kraus operators proportional to unitaries.

Equation assumptions:

- Finite dimension
- All masks with positive probability, 0<p<1

## eq_5: Position distribution

$$
P_T(x)=\sum_{c}|\langle x,c|\psi_T\rangle|^2,\quad \bar P_T(x)=\frac1N\sum_{n=1}^{N}P_T^{(n)}(x)
$$

Per-trajectory distribution, averaged classically over N sampled sequences to approximate the channel.

Provenance: `assumption`. Output decoding for the trajectory circuit.

Equation assumptions:

- Monte Carlo averaging over N sampled mask sequences

## Registers

- pos: 2 qubits; position x in {0..3}, little-endian
- coin: 1 qubits; coin qubit, 0=L, 1=R

## Initial state

|x=0>|c=+> with |+>=(|0>+|1>)/sqrt2

## Measurement

Computational-basis position measurement on the final state, or equivalently exact probabilities from the simulated statevector, per trajectory.

## Classical postprocessing

Average position distributions over sampled sequences. Optionally diagonalize Phi (a 64x64 superoperator) to find the peripheral eigenspace.

## Algorithm steps

1. Prepare the initial state: Hadamard on the coin qubit. (eq_2)
2. For t=1..T, apply the Hadamard coin and then the shift S_omega_t compiled from the classical mask, using permutation gates (multi-controlled X, swaps or a permutation unitary). (eq_1, eq_2)
3. Classically sample mask sequences with probability P(omega), simulate each, compute position distributions and average them. Peripheral-space analysis is done by classical linear algebra on the channel. (eq_3, eq_4, eq_5)

## Assumptions

- The 4-cycle, Hadamard coin and reflecting closed-edge rule are choices of this reconstruction
- The circuit is a single trajectory with classical masks, not the open-system channel
- No black-box query complexity is claimed

## Missing information

- The paper's actual shift and coin definitions for chains
- The paper's asymptotic formulas and numerical example
- The 2D lattice Grover-coin results
