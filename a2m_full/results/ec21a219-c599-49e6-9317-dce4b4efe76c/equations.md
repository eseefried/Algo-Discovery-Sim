# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Discrete-time coined quantum walk on a 4-site open chain with i.i.d. dynamic edge percolation. Each step applies U_omega = S_omega (I x C) for a random edge configuration omega in {0,1}^3. The averaged dynamics is the random unitary channel Phi, and the long-time limit of Phi^n is the projection onto its peripheral eigenspace. Predict the asymptotic state and position distribution, then compare with a finite-n circuit simulation.

Scope: One tiny instance: 4 positions (2 qubits), 1 coin qubit, 3 edge ancillas, 6 qubits total, Hadamard coin, localized initial walker, edge-open probability p. Covers (a) exact classical construction of U_omega and the superoperator with peripheral spectrum, and (b) a circuit simulation of n steps with fresh ancillas per step, reading the position distribution. Outside scope: the paper's general finite-graph theory, the detailed 1D chain classification, the numerical example in the paper, and the 2D lattice Grover-coin results. These cannot be reconstructed from the abstract.

## Symbols

- $x\in\{0,1,2,3\}$: walker position (binary-encoded in 2 qubits, little-endian); domain: integers 0..3
- $c\in\{0,1\}$: coin state; domain: bit
- $\omega=(\omega_0,\omega_1,\omega_2)$: edge configuration, where edge e joins sites e and e+1 and omega_e=1 means open; domain: {0,1}^3
- $p$: probability that an edge is open; domain: [0,1]
- $\theta$: Ry angle for the edge ancilla; domain: real, theta=2 arcsin(sqrt p)
- $C$: coin operator (Hadamard); domain: 2x2 unitary
- $S_\omega$: conditional shift with reflection at closed edges; domain: 8x8 unitary on position and coin
- $U_\omega$: one-step unitary for configuration omega; domain: 8x8 unitary
- $\Phi$: averaged one-step channel; domain: CPTP map on 8x8 density matrices

## eq_1: Random unitary channel

$$
\Phi(\rho)=\sum_{\omega}p(\omega)\,U_\omega\rho\,U_\omega^\dagger,\quad p(\omega)=\prod_e p^{\omega_e}(1-p)^{1-\omega_e}
$$

The one-step map averaged over independent edge configurations.

Provenance: `abstract_inferred`. The abstract says the long-time limit is treated with random unitary map methods. The explicit i.i.d. form is a modelling assumption taken from the sketch.

Abstract evidence: applying the asymptotic methods concerning random unitary maps

Equation assumptions:

- Edges are independent with equal p

## eq_2: Coined step with reflection

$$
S_\omega|x,c\rangle=\begin{cases}|x+s_c,c\rangle & \text{edge } e(x,c)\text{ open}\\ |x,1-c\rangle & \text{closed or boundary}\end{cases},\quad s_0=+1,\ s_1=-1,\ U_\omega=S_\omega(I\otimes C)
$$

The edge e(x,c) is the one between x and x+s_c. The shift moves the walker if the edge is open and reflects with a coin flip if it is closed. Boundary sites behave as closed edges, so the shift is a permutation and hence unitary.

Provenance: `assumption`. This is the proposed concrete implementation of reflecting dynamic percolation on the chain. The abstract does not specify it.

Equation assumptions:

- Reflection with coin flip
- Hadamard coin C=H
- Boundary acts as a closed edge

## eq_3: Ancilla preparation

$$
R_y(\theta)|0\rangle=\cos(\theta/2)|0\rangle+\sin(\theta/2)|1\rangle,\quad \sin^2(\theta/2)=p
$$

Each edge ancilla is prepared so that measuring it gives open with probability p. Fresh ancillas are used each step.

Provenance: `standard_background`. Standard single-qubit rotation.

Equation assumptions:

- Fresh ancilla per step, or ancillas reset to |0>

## eq_4: Peripheral eigen-condition and limit

$$
\Phi(X)=\lambda X,\ |\lambda|=1\iff U_\omega XU_\omega^\dagger=\lambda X\ \forall\omega;\quad \Phi^n\to P_{\rm per}\ (n\to\infty)
$$

For a random unitary channel on a finite-dimensional space, the peripheral eigenvectors are the common eigen-operators of all U_omega. The limit of Phi^n is the projection onto this peripheral space.

Provenance: `abstract_inferred`. This is the standard result for random unitary channels. The abstract only names the method, so the specific statement comes from background knowledge.

Abstract evidence: applying the asymptotic methods concerning random unitary maps

Equation assumptions:

- Finite dimension
- p(omega)>0 for the configurations used

## eq_5: Position readout

$$
P_n(x)=\sum_{c}\langle x,c|\Phi^n(\rho_0)|x,c\rangle,\quad \rho_0=|x_0,c_0\rangle\langle x_0,c_0|
$$

The position distribution after n steps equals the position-qubit measurement distribution in the circuit with ancillas traced out or refreshed each step. The comparison target is P_infty(x)=sum_c <x,c|P_per(rho_0)|x,c>. It is expected to be uniform (1/4) if the only peripheral element is the identity, which is a conjecture for the generic case.

Provenance: `assumption`. The readout follows from the sketch. Uniformity should be checked numerically and not assumed.

Equation assumptions:

- Generic p in (0,1)
- Initial state is localized

## Registers

- pos: 2 qubits; walker position, little-endian
- coin: 1 qubits; coin qubit
- edge: 3 qubits; edge-open ancillas, one per edge, refreshed each step

## Initial state

|x_0=0>|c_0=0> on pos and coin, with all edge ancillas in |0>

## Measurement

Measure only the 2 position qubits after n steps. Under the little-endian convention, bits[::-1][i] is position bit i. The ancillas are reset or averaged out.

## Classical postprocessing

Compute the peripheral spectrum and fixed points of the 64x64 superoperator. Compute P_infty and compare it with the empirical P_n(x) as n grows.

## Algorithm steps

1. Classically build the eight U_omega as 8x8 matrices, form the superoperator sum_omega p(omega) U_omega conj(U_omega), and find its eigenvalues of modulus 1 and their eigenvectors. (eq_1, eq_2, eq_4)
2. Per circuit step: apply Ry(theta) to each edge ancilla and the Hadamard on the coin. Then apply the shift controlled on the coin and the edge ancilla, using multi-controlled increment/decrement, with X on the coin for the reflection branch. (eq_2, eq_3)
3. Discard the ancillas, either with new ancillas per step (which needs more than 6 qubits) or by resetting them. Repeat for n steps and take the position distribution. Compare it with the classical Phi^n evolution and with P_infty. (eq_1, eq_5)

## Assumptions

- Chosen instance: 4-site open chain, Hadamard coin, independent edges with equal p (e.g. p=0.5), localized initial state
- The reflect-with-coin-flip convention is assumed
- The long-time limit is approximated by finite n
- Reusing the 3 ancillas by reset gives 6 qubits; fresh ancillas per step exceed the cap, so use mid-circuit reset or classical averaging over omega

## Missing information

- The paper's exact shift and coin conventions and boundary handling
- The paper's explicit asymptotic results and numerical example
- Whether the generic-case asymptotic state is truly maximally mixed
- Details of the 2D Grover case, which is not reconstructed
