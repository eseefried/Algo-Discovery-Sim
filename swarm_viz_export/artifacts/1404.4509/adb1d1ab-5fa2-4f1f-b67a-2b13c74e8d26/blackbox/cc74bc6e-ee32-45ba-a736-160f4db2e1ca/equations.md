# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Dynamic percolation quantum walk on a 4-site cycle: each step draws a random edge-presence mask, giving a random unitary channel whose long-time limit is set by the peripheral spectrum. The circuit simulates one fixed mask sequence (a single trajectory); averaging over sequences is classical.

Scope: Single trajectory of a coined Hadamard walk on a 4-cycle, T fixed classical masks compiled into gates, with explicit initial-state preparation |x=0>|c=+> and an explicit permutation convention for the shift. The ensemble channel and its asymptotic attractor are background, computed classically. The 2D Grover-coin lattice, the paper's own asymptotic construction and its numerical example are out of scope.

## Symbols

- $x$: walker position on the cycle; domain: {0,1,2,3}
- $c$: coin value, 0=L, 1=R; domain: {0,1}
- $\omega$: edge mask; \omega_e=1 means edge e joining sites e and e+1 mod 4 is open; domain: {0,1}^4
- $p$: probability an edge is open, independent per edge and step; domain: [0,1]
- $U_\omega$: one-step unitary for mask \omega; domain: unitary on C^4 tensor C^2
- $H$: Hadamard coin; domain: 2x2 unitary
- $T$: number of steps; domain: positive integer
- $\pi_\omega$: permutation of basis labels (x,c) realized by S_\omega; domain: bijection on {0..3}x{0,1}

## eq_1: Step unitary for fixed mask

$$
U_\omega=S_\omega\,(I_{pos}\otimes H),\quad S_\omega|x,R\rangle=\begin{cases}|x+1,R\rangle&\omega_x=1\\|x,L\rangle&\omega_x=0\end{cases},\quad S_\omega|x,L\rangle=\begin{cases}|x-1,L\rangle&\omega_{x-1}=1\\|x,R\rangle&\omega_{x-1}=0\end{cases}
$$

Coin first, then shift with reflection (coin flip, no move) at closed edges. Positions mod 4. S_\omega is a basis permutation: |x,R> goes to |x+1,R> if edge x is open, else to |x,L>; |x,L> goes to |x-1,L> if edge x-1 is open, else to |x,R>. Closed edge x: |x,R>->|x,L> and |x+1,L>->|x+1,R>. These are images distinct from the others, so S is a bijection.

Provenance: `assumption`. Concrete percolation shift for the minimal instance; the abstract does not give the shift rule.

Equation assumptions:

- Reflecting rule at closed edges
- H=(1/sqrt2)[[1,1],[1,-1]]
- Edge e joins sites e and e+1 mod 4

## eq_2: Permutation convention

$$
S_\omega|s\rangle=|\pi_\omega(s)\rangle,\quad \text{matrix }(S_\omega)_{\pi_\omega(s),s}=1
$$

The circuit must map basis state s to pi(s) (forward direction, not its inverse). Index s=x+4c... with little-endian qubits: x0,x1 are qubits 0,1 and coin is qubit 2, so index = x+4c. Verify the compiled circuit by comparing its Operator with the dense matrix of eq_1 for several masks, including the full product in eq_3.

Provenance: `assumption`. Addresses the review: fixes direction and encoding so the permutation decomposition can be checked.

Equation assumptions:

- Little-endian qubit ordering, index = x + 4c

## eq_3: Trajectory state

$$
|\psi_T\rangle=U_{\omega_T}\cdots U_{\omega_1}\,(I_{pos}\otimes H)\,|x=0\rangle|c=0\rangle=U_{\omega_T}\cdots U_{\omega_1}|x=0\rangle|c=+\rangle
$$

Circuit output for a fixed mask sequence. The circuit must begin with an explicit H on the coin qubit (qubit 2) before the step loop, since the circuit starts in |0,0>.

Provenance: `assumption`. Defines the implementable unitary for one realization, including the initial-state preparation missing from the earlier build.

Equation assumptions:

- Masks are classical parameters compiled into gates
- |+>=(|0>+|1>)/sqrt2

## eq_4: Random unitary channel

$$
\Phi(\rho)=\sum_{\omega}P(\omega)\,U_\omega\rho U_\omega^\dagger,\quad P(\omega)=\prod_{e=0}^{3}p^{\omega_e}(1-p)^{1-\omega_e}
$$

Mask-averaged one-step dynamics; state after T steps is Phi^T(rho_0).

Provenance: `abstract_inferred`. Random edge presence at each step gives a random unitary map; the product form of P assumes independent identical edges.

Abstract evidence: the connections appear and disappear randomly in each step during the time evolution

Equation assumptions:

- Edges independent with identical p

## eq_5: Peripheral/attractor space

$$
\Phi^T(\rho)\to\Phi_\infty(\rho),\quad \text{peripheral eigenoperators }X:\ U_\omega X U_\omega^\dagger=\lambda X\ \forall\omega\text{ with }P(\omega)>0,\ |\lambda|=1
$$

Standard random-unitary-map asymptotics: the long-time limit lives on the span of peripheral eigenoperators; the rest decays. Recalled background, not the paper's formulas.

Provenance: `standard_background`. Known result for finite-dimensional unital channels with unitary Kraus operators.

Equation assumptions:

- Finite dimension
- 0<p<1

## eq_6: Position distribution

$$
P_T(x)=\sum_{c}|\langle x,c|\psi_T\rangle|^2,\quad \bar P_T(x)=\frac1N\sum_{n=1}^{N}P_T^{(n)}(x)
$$

Per-trajectory distribution, averaged classically over N sampled sequences to approximate the channel (Monte Carlo, approximate).

Provenance: `assumption`. Output decoding for the trajectory circuit.

Equation assumptions:

- Monte Carlo averaging over N sampled sequences

## Registers

- pos: 2 qubits; position x in {0..3}, qubits 0,1 little-endian
- coin: 1 qubits; coin qubit 2, 0=L, 1=R

## Initial state

|x=0>|c=0> from the circuit start, then an explicit Hadamard on the coin qubit gives |x=0>|c=+>.

## Measurement

Computational-basis position measurement on the final state, or exact probabilities from the statevector, per trajectory.

## Classical postprocessing

Average position distributions over sampled sequences. Optionally diagonalize Phi (64x64 superoperator) for the peripheral eigenspace.

## Algorithm steps

1. Prepare the initial state: apply H on coin qubit 2 before any step. (eq_3)
2. For t=1..T apply the Hadamard coin on qubit 2, then the shift S_omega_t as the basis permutation pi_omega_t (forward direction, index=x+4c), compiled from the classical mask with multi-controlled X/swap gates or a permutation unitary. (eq_1, eq_2, eq_3)
3. Validate: compare the circuit Operator against the dense product of eq_1 matrices applied after the initial H for several masks; fix permutation order or direction if they differ. (eq_2, eq_3)
4. Classically sample mask sequences with P(omega), simulate each, compute position distributions and average. Peripheral analysis is done classically on the 64x64 superoperator. (eq_4, eq_5, eq_6)

## Assumptions

- The 4-cycle, Hadamard coin and reflecting closed-edge rule are choices of this reconstruction
- The circuit is a single trajectory with classical masks, not the open-system channel
- No black-box query complexity is claimed

## Missing information

- The paper's actual shift and coin definitions for chains
- The paper's asymptotic formulas and numerical example
- The 2D lattice Grover-coin results
