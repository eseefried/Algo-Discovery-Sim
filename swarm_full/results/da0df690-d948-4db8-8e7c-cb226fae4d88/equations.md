# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Synthesize a target single-qubit unitary into a Probabilistic Quantum Circuit with Fallback (PQF) protocol over universal gate sets (Clifford+T, Clifford+V, Clifford+pi/12). The protocol is a walk on a discrete Markov chain with the target unitary as an absorbing state, with transitions induced by multi-qubit unitaries followed by measurements. It terminates after finitely many steps, unlike RUS, and has expected gate count log_b(1/eps)+O(log log(1/eps)).

Scope: Abstract-level reconstruction of the PQF synthesis problem and its stated cost scaling. The explicit circuits, transition probabilities, fallback rules and the definition of b are not given in the abstract and are not reconstructed.

## Symbols

- $\varepsilon$: approximation precision for the target unitary; domain: (0,1)
- $b$: quantity related to the expansion property of the underlying universal gate set; domain: real, b>1 (assumed)
- $N_{\mathrm{exp}}$: expected gate count of the PQF decomposition; domain: positive reals

## eq_1: Expected gate count scaling

$$
N_{\mathrm{exp}}=\log_{b}(1/\varepsilon)+O(\log(\log(1/\varepsilon)))
$$

Expected gate count of PQF decompositions for Clifford+T, Clifford+V and Clifford+pi/12.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: expected gate counts of $\log_{b}(1/\varepsilon)+O(\log(\log(1/\varepsilon)))$

## Registers

- data: 1 qubits; Qubit on which the target single-qubit unitary is (probabilistically) implemented
- ancilla: unknown (multi-qubit unitaries imply at least 1) qubits; Ancilla qubits measured after each multi-qubit unitary to drive Markov chain transitions

## Initial state

Data qubit in arbitrary input state, ancillas in a fixed reference state (assumed |0>); Markov chain starts at an initial non-absorbing state.

## Measurement

Computational-basis measurement of the ancilla qubits after each multi-qubit unitary; the outcome determines the Markov chain transition (reaching the absorbing target state, moving to another state, or fallback). Outcome-to-transition map is not given in the abstract.

## Classical postprocessing

Classical controller maps each measurement outcome to the next Markov chain state and the next unitary, tracks the step count, and stops upon reaching the absorbing target state or the finite termination bound. Expected gate count is averaged over outcome probabilities.

## Algorithm steps

1. Pick a gate-set-specific multi-qubit unitary for the current Markov chain state and apply it to data and ancilla registers. (eq_1)
2. Measure ancillas; the outcome selects the transition: success moves toward the target (absorbing) state, other outcomes move to another state or fallback state with a correctable or alternative unitary. (no equation reference)
3. Repeat until the absorbing target state is reached or the finite step bound is hit; expected gate count scales as in eq_1. (eq_1)

## Assumptions

- N_exp denotes expected gate count as in the abstract; b>1 assumed.
- Register structure and ancilla reset to |0> are assumed, not from the abstract.
- Ancilla measured in the computational basis (assumed).
- Ancilla measured in the computational basis.

## Missing information

- Definition of b for each gate set
- Explicit multi-qubit unitaries, Markov chain transitions and fallback rules
- Number of ancilla qubits and exact step count per transition
- Outcome-to-transition mapping and the finite termination bound
- Outcome-to-transition mapping and the finite termination bound are not given.
