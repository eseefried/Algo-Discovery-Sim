# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Discrete-time coin quantum walk on a cycle of N=2^n sites. An unknown qubit a|0>+b|1> starts as the coin state with the walker at site 0. After t steps, a fixed state-independent single-qubit correction D on the coin should leave the walker at site d with coin state a|0>+b|1>. The task is to test for which (coin, t, d) this succeeds, and to check periodicity of the walk.

Scope: Small circle with n=3 (N=8, 4 qubits total). Coins are identity, X, Hadamard and Ry(theta). The statevector gives the transfer fidelity at a fixed site d for the basis inputs |0>, |1>, |+>, |+i> (which fixes the map on the coin by linearity), and the minimal T with U^T=I is found on that subspace. Outside scope: the paper's line-walk theorems, proofs of 'arbitrary distance' versus 'finite distance', the exact definition of D for biased coins, and the exact arbitrary-distance construction for the line.

## Symbols

- $N=2^n$: number of sites on the cycle; domain: positive integer power of 2
- $a,b$: amplitudes of the unknown qubit; domain: complex, |a|^2+|b|^2=1
- $C$: single-qubit walk coin (I, X, H or Ry(theta)); domain: U(2)
- $D$: final correction coin on the coin qubit, independent of a,b; domain: U(2)
- $T_\pm$: increment/decrement shift on the position register; domain: T_\pm|x>=|x\pm1 \bmod N>
- $t,d$: number of walk steps and target site; domain: t>=0 integer, d in {0..N-1}
- $U$: one-step walk operator; domain: unitary on 2N-dim space
- $\psi$: unknown coin state a|0>+b|1>; domain: normalized qubit state

## eq_1: Shift operator

$$
S=|0\rangle\langle0|\otimes T_+ + |1\rangle\langle1|\otimes T_-,\quad T_\pm|x\rangle=|x\pm1 \bmod N\rangle
$$

Coin-conditioned shift on the cycle, with coin 0 moving right and coin 1 left. Implemented with controlled increment/decrement circuits.

Provenance: `assumption`. Convention taken from the method sketch; the abstract names only a walk on a line or circle.

Equation assumptions:

- Power-of-two cycle so the shift is a modular adder
- Coin-0=right convention

## eq_2: Walk step and transfer state

$$
U=S\,(C\otimes I_{pos}),\quad |\Phi_t\rangle=(D\otimes I_{pos})\,U^{t}\,|0\rangle_{pos}\,(a|0\rangle+b|1\rangle)
$$

Coin is applied first, then the shift. After t steps D is applied to the coin qubit only.

Provenance: `abstract_inferred`. The abstract states a final state-independent coin operator; the step ordering is an assumption.

Abstract evidence: we introduce an additional coin operator which is applied at the end of the walk. This operator does not depend on the state to be transferred.

Equation assumptions:

- Coin acts before the shift

## eq_3: Perfect transfer criterion

$$
|\Phi_t\rangle=|d\rangle_{pos}\otimes(a|0\rangle+b|1\rangle)\ \ \forall a,b\iff \big\|(\langle d|\otimes\langle\psi|)|\Phi_t\rangle\big\|^2=1\ \text{for}\ \psi\in\{|0\rangle,|1\rangle,|+\rangle,|+i\rangle\}
$$

Success is checked on four inputs; by linearity, fidelity 1 on all four (with consistent phases) gives transfer for every a,b. Checking the two basis states alone would miss relative-phase errors. Read from the statevector with no measurement.

Provenance: `abstract_inferred`. Perfect transfer means the output equals the input state at the target site for all inputs.

Abstract evidence: perfect transfer of an unknown qubit state via the discrete-time quantum walk on a line or a circle

Equation assumptions:

- Walker starts at site 0
- Fixed known d

## eq_4: Identity coin on the circle

$$
U^t|0\rangle(a|0\rangle+b|1\rangle)=a|t\bmod N\rangle|0\rangle+b|-t\bmod N\rangle|1\rangle;\ \text{components meet iff } 2t\equiv0\ (\mathrm{mod}\ N),\ \text{e.g. } t=N/2,\ d=N/2,\ D=I
$$

With C=I the two coin components move in opposite directions and coincide on a cycle only at t=N/2, giving transfer to site N/2 with D=I. On an infinite line they never coincide, so the paper's 'any distance' result for this coin must rely on a different definition than the one here.

Provenance: `assumption`. Direct computation from eq_1 with C=I; related to the abstract only through its identity-coin claim.

Equation assumptions:

- Circle geometry
- Coin-0=right convention

## eq_5: Flip coin

$$
C=X:\ U^t|0\rangle(a|0\rangle+b|1\rangle)=|0\rangle(a|0\rangle+b|1\rangle)\ (t\ \text{even});\ \ a|-1\rangle|1\rangle+b|{+}1\rangle|0\rangle\ (t\ \text{odd})
$$

Computed under the coin-then-shift order. For even t the walker is back at site 0 with the original state (D=I), i.e. trivial transfer at distance 0. For odd t the components sit at sites ±1 and are separated, so D cannot merge them. A different shift or coin ordering may give nonzero distances.

Provenance: `assumption`. Direct computation from eq_1 and eq_2 with C=X; this contradicts the sketch's claim of arbitrary-distance transfer under these conventions.

Equation assumptions:

- Coin-then-shift ordering

## eq_6: Periodicity

$$
U^{T}|0\rangle|\psi\rangle=|0\rangle|\psi\rangle\ \forall\psi,\ T=\min\{t>0\}
$$

Check numerically for each coin that a minimal T exists on the reachable subspace, for example N or 2N for I and X on the cycle. Compare the states for several ψ, including phases.

Provenance: `abstract_inferred`. The abstract claims periodicity of walks that end in perfect transfer; the exact form of the check is chosen here.

Abstract evidence: we show that quantum walks ending with a perfect state transfer are periodic

Equation assumptions:

- Periodicity tested on the subspace reached from |0>⊗coin

## Registers

- pos: n (n=3) qubits; walker position, little-endian integer x=sum x_i 2^i, qubits 0..n-1
- coin: 1 qubits; coin qubit (index n) carrying the unknown state, supplied as input by the runner

## Initial state

|0>_pos ⊗ (a|0>+b|1>)_coin; the unknown state is supplied by the runner, with no initialize

## Measurement

None. Read the final statevector for the fidelity; the circuit contains no measurement gates.

## Classical postprocessing

Project the position onto |d>, compute the reduced coin fidelity with ψ for the four test inputs, and report the minimal period T.

## Algorithm steps

1. Take the coin qubit in state ψ and the position register in |0>. (eq_3)
2. Repeat t times: apply coin C (I, X, H or Ry(theta)) on the coin qubit, then the coin-controlled modular increment/decrement S built from cx/ccx/mcx. (eq_1, eq_2)
3. Apply the fixed correction D on the coin qubit (D=I for the identity and flip coins; for H/Ry choose D as the inverse of the coin-block unitary found by simulation). (eq_2)
4. Scan (t,d) from the statevector for fidelity 1. Check against the identity-coin circle prediction t=N/2, d=N/2, and find the minimal period T. (eq_3, eq_4, eq_5, eq_6)

## Assumptions

- Walker starts at site 0 with the unknown qubit as the coin state
- Target d is fixed and known
- D is a single-qubit unitary on the coin only
- Instance n=3 (4 qubits), cyclic shift mod 8
- Coin-then-shift ordering and coin-0=right convention are assumed, not from the abstract

## Missing information

- Exact coin and shift ordering used in the paper
- Explicit D for Hadamard and biased coins
- Paper's definition of 'distance' on the line and its target-site convention
- The construction that makes identity and flip coins work at arbitrary distance on a line
- Explicit periods of the walk
