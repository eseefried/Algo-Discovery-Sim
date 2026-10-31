# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Determine functional equivalence of quantum states and quantum circuits, where complex-valued state vectors admit several notions of equivalence (e.g. exact vs. up to global phase), and design equivalence-checking algorithms that stay fast and robust for circuits with hundreds of qubits, such as quantum communication and search circuits.

Scope: Abstract-level reconstruction of equivalence-checking definitions only. The specific algorithms, data structures and benchmarks are not given in the abstract, so only a small finite illustrative formulation of state and circuit equivalence is provided.

## Symbols

- $|\psi\rangle,|\phi\rangle$: quantum states as complex-valued vectors; domain: unit vectors in C^{2^n}
- $U,V$: unitary matrices of two circuits on n qubits; domain: U(2^n)
- $\theta$: global phase; domain: [0,2\pi)

## eq_1: Exact state equivalence

$$
|\psi\rangle=|\phi\rangle
$$

Strictest notion: the two state vectors are identical.

Provenance: `abstract_inferred`. The abstract says there are several notions of equivalence for vector states; the exact one is the strictest.

Abstract evidence: quantum states, which are represented by complex-valued vectors, exhibit subtle differences leading to several notions of equivalence

## eq_2: Equivalence up to global phase

$$
|\psi\rangle=e^{i\theta}|\phi\rangle
$$

Relaxed notion: states differ only by an unobservable global phase.

Provenance: `standard_background`. Standard physics background, taken as one plausible relaxed notion; the abstract does not name it.

Equation assumptions:

- The paper's relaxed notion is global-phase equivalence

## eq_3: Circuit equivalence up to phase

$$
U=e^{i\theta}V\iff V^\dagger U\propto I
$$

Two circuits are equivalent if their unitaries match up to a global phase.

Provenance: `assumption`. Assumed formalization of the circuit equivalence checking mentioned in the abstract.

Equation assumptions:

- Unitary circuits with no measurements or ancillas

## Registers

- q: n qubits; data qubits on which both circuits U and V act

## Initial state

Assumed finite instance: computational basis state |0^n> (or each basis state for full unitary comparison); the abstract gives no initial state.

## Measurement

Abstract specifies no measurement. Assumed illustration: apply V^\dagger U to |0^n> and measure q in the computational basis; equivalence up to phase predicts outcome 0^n with probability 1 (a necessary check only; for full equivalence repeat over basis or random input states). Equivalent algebraic/symbolic checking would need no measurement.

## Classical postprocessing

Assumed: declare 'not equivalent' if any shot returns a nonzero bitstring; otherwise report 'equivalent on tested inputs' (statistical evidence only). Global phase is not detectable by measurement, so phase-sensitive (exact) equivalence needs a non-measurement method such as a classical vector or matrix comparison. The paper's actual postprocessing is unknown.

## Algorithm steps

1. Build the composite circuit V^\dagger U on register q by applying U, then the inverse of V (circuit-level equivalence check, assumed formulation). (eq_3)
2. Check whether V^\dagger U acts as identity up to a global phase, i.e. is proportional to I. (eq_3)
3. For state equivalence, compare the output states of the two circuits exactly, then up to global phase. (eq_1, eq_2)

## Assumptions

- Equivalence notions are illustrated by exact and global-phase equality
- Global-phase equivalence is one of the notions considered
- The circuit plan is a generic miter-style check, not the paper's algorithm
- Circuit plan uses a generic V^dagger U identity check as an illustration
- Measurement scheme is a generic computational-basis test, not taken from the abstract

## Missing information

- Exact list of equivalence notions used
- Algorithm and data structure details
- Benchmark circuit specifics
- Algorithms are not described in the abstract
- Whether the paper's method uses simulation or a symbolic/decision-diagram-like representation is unknown
- Whether the paper uses measurement-based checks at all is unknown
