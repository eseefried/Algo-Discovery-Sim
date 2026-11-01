# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximate a single-qubit unitary U to precision epsilon by a probabilistic protocol (PQF) over a universal gate set, modeled as an absorbing Markov chain whose transitions are multi-qubit unitaries followed by measurements, with finite termination and expected gate count log_b(1/eps)+O(log log(1/eps)).

Scope: Only the generic Markov-chain/expected-cost framework and the stated asymptotic gate-count scaling, plus a tiny assumed 3-state absorbing chain as illustration. Explicit PQF unitaries, measurement outcomes, fallback rules, and gate-set-specific constructions (Clifford+T, +V, +pi/12) and the definition of b are outside scope.

## Symbols

- $U$: target single-qubit unitary (absorbing state); domain: U(2)
- $\varepsilon$: approximation precision; domain: (0,1)
- $b$: constant related to expansion property of the gate set; domain: real, b>1 (assumed)
- $P$: transition matrix of the Markov chain over states (unitaries up to fallback); domain: row-stochastic matrix
- $Q$: sub-stochastic transition block among transient states; domain: real matrix
- $R$: transient-to-absorbing transition block; domain: real matrix
- $N$: fundamental matrix; domain: real matrix
- $c_i$: expected gate cost of one transition from transient state i (assumed); domain: nonnegative reals
- $E[G]$: expected gate count of the protocol; domain: nonnegative real

## eq_1: Expected gate count scaling

$$
E[G]=\log_b(1/\varepsilon)+O(\log\log(1/\varepsilon))
$$

Claimed expected gate count of the PQF decompositions.

Provenance: `abstract_explicit`. Directly stated in the abstract for the three gate sets.

Abstract evidence: expected gate counts of $\log_{b}(1/\varepsilon)+O(\log(\log(1/\varepsilon)))$

Equation assumptions:

- b depends on the gate set; its value is not given

## eq_2: Absorbing chain structure

$$
P=\begin{pmatrix}Q&R\\0&I\end{pmatrix}
$$

Canonical form of a Markov chain with absorbing states (target unitary absorbing).

Provenance: `abstract_inferred`. Absorbing-state chain implies canonical block form; the actual state space is not specified.

Abstract evidence: implements a walk on a discrete Markov chain in which the target unitary is an absorbing state

Equation assumptions:

- Finite state set
- Transitions induced by unitary plus measurement are probabilistic

## eq_3: Fundamental matrix

$$
N=\sum_{k\ge 0}Q^k=(I-Q)^{-1}
$$

Expected visits to transient states before absorption.

Provenance: `standard_background`. Standard absorbing Markov chain theory.

Equation assumptions:

- spectral radius of Q is less than 1

## eq_4: Expected cost

$$
E[G]=\sum_{i}\pi_i\,(Nc)_i
$$

Expected gate count from initial distribution pi over transient states with per-step costs c.

Provenance: `assumption`. Generic cost accounting; the paper's cost model is not given.

Equation assumptions:

- Cost additive per transition
- Initial distribution pi over transient states

## eq_5: Finite termination

$$
Q^{K}=0\ \text{for some finite }K
$$

Fallback ensures absorption in at most K steps, unlike RUS where Q^k only decays geometrically.

Provenance: `abstract_inferred`. Finite termination implies the transient block is nilpotent (acyclic transient structure) if termination is certain.

Abstract evidence: In contrast to RUS protocols, the presented PQF protocols terminate after a finite number of steps.

Equation assumptions:

- Termination holds with certainty, with fallback states counted as absorbing or leading to absorption

## Registers

- data: 1 qubits; qubit holding the state to which U is applied
- ancilla: unknown qubits; extra qubits for multi-qubit unitaries followed by measurement

## Measurement

Ancilla measurements after each multi-qubit unitary determine the transition; the measurement basis is not specified.

## Algorithm steps

1. Define the Markov chain with the target unitary as an absorbing state. (eq_2)
2. At each transient state apply a multi-qubit unitary from the gate set and measure ancillas; the outcome selects the next state (specific unitaries not given). (eq_2)
3. Fallback transitions guarantee absorption in a bounded number of steps. (eq_5)
4. Compute expected gate count via the fundamental matrix and compare to the stated scaling. (eq_3, eq_4, eq_1)

## Assumptions

- Generic absorbing-chain formalism used as illustration
- Cost model is additive per step
- b>1

## Missing information

- Explicit state space and transition unitaries
- Definition and values of b per gate set
- Fallback rule details
- Measurement bases and outcomes
- Ancilla count
- Proofs of the scaling and constants
