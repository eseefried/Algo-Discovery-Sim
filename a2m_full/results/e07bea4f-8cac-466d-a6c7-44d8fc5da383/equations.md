# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a classical single-qubit target U in SU(2) and two non-parallel rotation controls (Rz at rate 1, Rn about n=(sin theta,0,cos theta) at rate r), find a minimum-time sequence of control rotations whose product equals U up to global phase, and build it as a one-qubit circuit.

Scope: One qubit, no ancilla, no black box, no measurement (statevector/unitary read). Only the five-segment Euler-like form Rz(a1)Rn(b1)Rz(a2)Rn(b2)Rz(a3) is built, with three free angles, plus a classical bounded grid or optimizer search over those angles. The paper's specific angle bounds, the five-concatenation proof and the clockwise-only length scaling laws are outside scope and not reconstructed.

## Symbols

- $\theta$: angle between the Rz axis and the second axis n in the xz-plane; domain: (0,\pi/2] assumed, non-parallel axes
- $r$: relative rotation speed of Rn versus Rz; domain: r>0
- $a_i$: Rz rotation angles; domain: real; in [0,2\pi) for clockwise-only case
- $b_j$: Rn rotation angles; domain: real; in [0,2\pi) for clockwise-only case
- $T$: total control time of a sequence; domain: nonnegative real
- $U$: target SU(2) unitary; domain: 2x2 unitary, given classically
- $V$: unitary produced by the sequence; domain: 2x2 unitary

## eq_1: Axis rotation

$$
R_n(b)=R_y(\theta)\,R_z(b)\,R_y(-\theta),\quad n=(\sin\theta,0,\cos\theta)
$$

Implements rotation about n using standard gates; Ry(theta) maps z to n.

Provenance: `standard_background`. Standard frame change; sign convention of Ry should be checked in simulation so that Ry(theta) takes z to n.

Equation assumptions:

- n lies in the xz-plane at angle theta from z

## eq_2: Five-segment decomposition

$$
U\simeq R_z(a_1)R_n(b_1)R_z(a_2)R_n(b_2)R_z(a_3)
$$

Time-optimal sequences are parametrized by three angles; at most five alternating segments when both rotation directions are allowed.

Provenance: `abstract_inferred`. Five concatenations is the stated maximum. The specific form with three free angles is inferred from 'parametrized by three rotation angles' and is not stated explicitly. Which three angles are free is not given.

Abstract evidence: any finite time-optimal sequence is composed at most of five control concatenations

Equation assumptions:

- Both rotation directions allowed
- The ordering and which angles are free are assumed

## eq_3: Total time

$$
T=\sum_i |a_i|+\frac{1}{r}\sum_j |b_j|
$$

Cost function: Rz at rate 1, Rn at rate r. For clockwise-only, angles are taken in [0,2\pi) so the absolute values are dropped.

Provenance: `assumption`. Follows from the constant-speed assumption and the relative speed ratio r mentioned in the abstract; the exact definition of r is assumed.

Equation assumptions:

- Constant rotation speeds
- r multiplies the Rn angular rate

## eq_4: Fidelity constraint

$$
F(U,V)=\tfrac12\left|\mathrm{Tr}(U^\dagger V)\right|=1
$$

Equality up to global phase.

Provenance: `standard_background`. Standard phase-insensitive check for SU(2).

## eq_5: Search problem

$$
\min_{\{a_i,b_j\}\in\mathcal{B}(\theta,r)}T\quad\text{s.t. } F(U,V)=1
$$

Bounded numerical search over the angle box B. The bounds come from the paper's results, which are not recoverable here.

Provenance: `abstract_inferred`. The abstract says the bounds constrain the structure so a numerical search is efficient. The box B itself is not given; the default is [0,2\pi) per angle.

Abstract evidence: allowing for an efficient numerical search of the time-optimal solution

Equation assumptions:

- Default box [0,2\pi) per angle if the true bounds are unknown

## Registers

- q: 1 qubits; single qubit on which the control sequence acts

## Initial state

|0> (the unitary is read from the circuit, so the input state is irrelevant)

## Classical postprocessing

Compute F from the simulated unitary and report T for the optimal angles. Keep the shortest-T solution among those with F near 1 (e.g. above 1-1e-8).

## Algorithm steps

1. Classically compute the target U and set theta and r. (eq_1)
2. Search the bounded angles for the minimum T with F=1, using a grid or optimizer with random restarts. (eq_3, eq_4, eq_5)
3. Build the circuit by applying rz(a1), the Rn gate (ry(theta) rz(b1) ry(-theta)), rz(a2), Rn(b2), rz(a3) in time order, skipping zero-angle gates. Qiskit applies gates in circuit order, so the matrix product is the reverse of the circuit order. (eq_1, eq_2)
4. Read the unitary, compare with U up to global phase, and report T. (eq_3, eq_4)

## Assumptions

- Second axis in the xz-plane at angle theta from z
- Rates are constant, with ratio r
- Both-direction case allows signed angles; the clockwise-only case uses angles in [0,2pi)
- Target U is given classically
- Equality is judged up to global phase
- Search is a classical grid or optimizer
- Five-segment form used as the parametrization

## Missing information

- The explicit angle bounds as functions of theta and r
- Which three angles are the free parameters and the closed-form solution
- Scaling-law constants for the clockwise-only maximum length
- The exact definition of r
- Whether shorter sequences than five segments need separate handling
