# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Reconstruct two Grover-algorithm questions: (1) a quantum model of an unordered phone book (quantum database) with programmable queries to search for a number or a name; (2) how successful Grover search is when the number of database elements is not precisely known, analyzed via distinguishability of states arising during Grover's algorithm using unambiguous discrimination.

Scope: Small finite instance: standard Grover iteration on N items with one marked item, plus a mismatch analysis where the true database size differs from the guessed size. The detailed phone-book encoding and the discrimination success formula are not given in the abstract.

## Symbols

- $N$: number of database elements; domain: positive integer
- $k$: number of Grover iterations; domain: nonnegative integer
- $\theta$: Grover rotation angle with \sin\theta=1/\sqrt{N}; domain: (0,\pi/2)

## eq_1: Grover state after k iterations

$$
|\psi_k\rangle=\sin((2k+1)\theta)|w\rangle+\cos((2k+1)\theta)|w^\perp\rangle,\quad \sin\theta=1/\sqrt{N}
$$

Standard single-marked-item Grover state in the marked/unmarked-superposition basis.

Provenance: `standard_background`. Textbook Grover analysis; the abstract does not give formulas.

Equation assumptions:

- single marked item
- N known to define the oracle and diffusion

## eq_2: Optimal iteration count

$$
k_{opt}\approx\frac{\pi}{4}\sqrt{N}
$$

Approximate iteration count maximizing success probability for known N.

Provenance: `standard_background`. Standard background for the optimal guess in the size-uncertainty question.

Equation assumptions:

- large N

## eq_3: Distinguishability of states

$$
|\langle\psi_k^{(N)}|\psi_k^{(N')}\rangle|
$$

Overlap of Grover states for true size N versus guessed size N', which governs unambiguous discrimination success.

Provenance: `assumption`. The abstract says the question reduces to distinguishability of states; the overlap as the quantity is an assumed formalization.

Equation assumptions:

- pure states
- overlap controls unambiguous discrimination

## Registers

- index: n=\lceil\log_2 N\rceil qubits qubits; database address register searched by Grover
- anc: 1 qubit (assumed) qubits; oracle phase-kickback ancilla; phone-book data/query registers not specified in abstract

## Initial state

|0\rangle^{\otimes n} on index, ancilla in |-\rangle; Hadamards on index give uniform superposition over N items (assuming N=2^n).

## Measurement

Search: measure the index register in the computational basis after k iterations; the outcome is the address of the marked entry (then read out the name or number). Size-uncertainty: apply an unambiguous state discrimination POVM between the Grover states for candidate sizes, with outcomes 'state A', 'state B' or 'inconclusive'; for two equiprobable pure states the success probability is at most 1-|<psi|phi>| (assumed).

## Classical postprocessing

For search, verify the returned entry via a classical lookup and repeat on failure. For discrimination, tally conclusive vs inconclusive outcomes to estimate success rate and compare guessed N' against the true N using the overlap.

## Algorithm steps

1. Prepare uniform superposition over the index register with Hadamards. (eq_1)
2. Repeat k times: apply the programmable oracle marking the queried entry (by number or by name), then the diffusion operator about the uniform state. (eq_1, eq_2)
3. For the size-uncertainty analysis, choose k from a guessed size N' and compare the resulting state with the true-N state via their overlap. (eq_2, eq_3)

## Assumptions

- Single marked item.
- Overlap formalization of distinguishability.
- N=2^n and one oracle ancilla in the circuit sketch.
- Two-state equiprobable unambiguous discrimination (Ivanovic-Dieks-Peres bound) assumed for the measurement.

## Missing information

- Quantum phone book encoding and programmable query construction (number vs name oracle).
- Exact unambiguous discrimination setup, states discriminated, POVM and success rates.
- Prior distribution over database size.
