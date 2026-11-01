# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate a single-qubit unitary U to error eps by a probabilistic protocol (PQF): a finite-step walk on a Markov chain of single-qubit unitaries over a universal gate set (Clifford+T primarily), in which each step applies a multi-qubit exact unitary W_k on data+ancilla, measures the ancilla, and moves to a next unitary determined by the outcome. U_eps is absorbing and the walk terminates after finitely many steps.

Scope: One smallest useful instance: 1 data qubit + 1 ancilla (2 qubits, under the 3-qubit cap), Clifford+T. A single PQF step with ancilla measured mid-circuit and classically controlled fallback correction, plus the final check that each measurement record yields a known data-qubit unitary and the expected T count is a probability-weighted sum. Outside scope: general norm-equation/factoring synthesis, the Clifford+V and Clifford+pi/12 constructions, the proof of the log_b(1/eps)+O(log log(1/eps)) bound, and explicit chain design for arbitrary U. The specific W_k, byproduct maps, and chain are not given in the abstract.

## Symbols

- $U$: target single-qubit unitary; domain: SU(2)
- $\varepsilon$: approximation error; domain: (0,1)
- $V_k$: chain state k: single-qubit unitary over the gate set, modulo Cliffords; domain: U(2)
- $W_k$: ancilla-assisted 2-qubit unitary exact over the gate set applied at state k; domain: U(4)
- $m$: ancilla measurement outcome; domain: {0,1}
- $p_{k,m}$: probability of outcome m at state k; domain: [0,1]
- $C_{k,m}$: known byproduct/correction unitary giving next chain state; domain: U(2)
- $b$: expansion-related quantity of the gate set; domain: real >1
- $c_k$: gate cost (T count) of step k; domain: nonnegative integer

## eq_1: Step transition

$$
W_k\,(|\psi\rangle\otimes|0\rangle)=\sum_{m\in\{0,1\}}\sqrt{p_{k,m}}\,\big(A_{k,m}|\psi\rangle\big)\otimes|m\rangle,\quad A_{k,m}\ \text{unitary up to scaling}
$$

Ancilla-assisted step; each outcome m implements a data-qubit unitary A_{k,m} with probability p_{k,m}. Requires each block be proportional to a unitary (assumed, to make the chain deterministic per outcome).

Provenance: `abstract_inferred`. Abstract says transitions come from multi-qubit unitaries followed by measurements; the block form is the standard consequence; the unitary-block requirement is an assumption.

Abstract evidence: transitions are induced by multi-qubit unitaries followed by measurements

Equation assumptions:

- Each outcome block is proportional to a unitary
- one ancilla qubit

## eq_2: Markov chain next state

$$
V_{k,m}=C_{k,m}\,A_{k,m}\,V_k\ \ (\text{up to global phase and Cliffords}),\quad \Pr[V_k\to V_{k,m}]=p_{k,m}
$$

Deterministic next state per outcome, random across outcomes; the walk on this chain is the protocol.

Provenance: `abstract_inferred`. Inferred from the Markov-chain-walk description; the explicit form of the update is an assumed construction.

Abstract evidence: implements a walk on a discrete Markov chain in which the target unitary is an absorbing state

Equation assumptions:

- Composition order and correction structure assumed

## eq_3: Absorbing target

$$
\Pr[V_{k}=V_{k'}]=\delta_{kk'}\ \text{for}\ V_k=U_\varepsilon,\quad \|U_\varepsilon-U\|\le\varepsilon
$$

The target state is absorbing; reaching it ends the protocol with the data qubit holding U_eps up to global phase.

Provenance: `abstract_inferred`. Direct reading of the absorbing-state claim; the error norm is an assumed measure.

Abstract evidence: the target unitary is an absorbing state

Equation assumptions:

- Distance measured up to global phase

## eq_4: Expected cost

$$
\mathbb{E}[\text{cost}]=\sum_{\text{paths }\gamma}\Pr[\gamma]\sum_{(k,m)\in\gamma}c_k,\quad \Pr[\gamma]=\prod_{(k,m)\in\gamma}p_{k,m}
$$

Expected gate count as a probability-weighted sum over the finite path DAG, computed from the branching probabilities.

Provenance: `standard_background`. Standard expectation over a finite absorbing Markov chain; abstract mentions expected gate counts.

Equation assumptions:

- Finite DAG so the sum is finite

## eq_5: Claimed scaling

$$
\mathbb{E}[\text{gates}]=\log_{b}(1/\varepsilon)+O(\log\log(1/\varepsilon))
$$

Asymptotic expected gate count to be checked only qualitatively; not verifiable on tiny instances.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: expected gate counts of $\log_{b}(1/\varepsilon)+O(\log(\log(1/\varepsilon)))$

## Registers

- data: 1 qubits; holds the single-qubit state being acted on by V_k
- anc: 1 (up to 2) qubits; ancilla measured mid-circuit; outcome selects the next W and correction

## Initial state

data in arbitrary |psi> (verify on basis states or via process fidelity), ancilla |0>

## Measurement

Ancilla measured mid-circuit each step (bit 0 in Qiskit little-endian ordering for that step's clbit); the data qubit is not measured, and is checked by simulation.

## Classical postprocessing

Feedforward selects the next W_k and correction from the outcome record; expected T count computed from the path probabilities.

## Algorithm steps

1. Classically choose a finite chain (DAG) of states V_k, exact gate-set unitaries W_k, and corrections C_{k,m}; this synthesis is assumed given for the small instance. (eq_2)
2. At the current state k, apply W_k to data+ancilla, measure the ancilla into a classical bit, and apply the classically controlled correction C_{k,m}. (eq_1, eq_2)
3. Repeat with the next state's W until reaching an absorbing state U_eps, which takes finitely many steps. (eq_3)
4. Compute the expected T count from the branch probabilities and check the data-qubit unitary per record against U_eps up to global phase. (eq_4)

## Assumptions

- Chosen instance: 1 data + 1 ancilla, Clifford+T, a one- or two-step chain
- Gate-set entries lie in a ring where norm equations are classically solvable
- Mid-circuit measurement and feedforward are available
- Byproduct unitaries stay in the ring so the chain is closed
- Success probability is bounded below and fallback states have strictly lower cost, ensuring termination
- The sketch's details (W_k, corrections, b=2 for T) are not in the abstract

## Missing information

- Explicit W_k construction and the norm-equation synthesis
- Definition of b and the chain's cost-reduction rule
- Fallback state definition and the explicit chain
- Details for the V and pi/12 gate sets
- Proof of the O(log log) term
