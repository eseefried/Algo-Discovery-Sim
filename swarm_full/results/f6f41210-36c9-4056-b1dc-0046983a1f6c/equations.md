# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Implement the oracle of Grover's quantum search over a real unstructured classical database as a simple circuit, where the oracle contains a quantumly accessible classical memory storing the database.

Scope: Abstract-level reconstruction only: oracle structure (classical memory queried in superposition) within Grover search; the specific gate-level circuit and memory design are not given in the abstract. Any finite instance is an assumed illustration.

## Symbols

- $N$: Number of database entries; domain: positive integer
- $x$: Database index; domain: {0,...,N-1}
- $f(x)$: Marking function; 1 if entry x satisfies the search criterion; domain: {0,1}
- $D_x$: Classical database content stored at address x; domain: bit string
- $O_f$: Grover oracle; domain: unitary on index register plus ancilla

## eq_1: Oracle phase action

$$
O_f|x\rangle=(-1)^{f(x)}|x\rangle
$$

Standard Grover oracle flips the phase of marked items.

Provenance: `standard_background`. Standard Grover search definition; the abstract only mentions an oracle for Grover search.

Equation assumptions:

- Phase-oracle form

## eq_2: Memory query

$$
U_M|x\rangle|0\rangle=|x\rangle|D_x\rangle
$$

Quantumly accessible classical memory loads the data at address x in superposition.

Provenance: `assumption`. Assumed model of the abstract's quantumly accessible classical memory; the exact construction is not stated.

Equation assumptions:

- Memory acts as a controlled-load of D_x into a data register

## eq_3: Oracle from memory

$$
f(x)=g(D_x)
$$

The marking bit is computed from the stored data via a predicate g, then memory is uncomputed.

Provenance: `assumption`. Assumed compute-phase-uncompute composition consistent with an oracle containing memory.

Equation assumptions:

- Predicate g is a fixed classical function

## Registers

- index: n=log2 N qubits (assumed) qubits; Address register holding superposition over database indices
- data: m qubits (assumed, entry width) qubits; Receives D_x from the classical memory
- flag: 1 qubit (assumed) qubits; Ancilla in |-> for phase kickback of g(D_x)

## Initial state

Index register in uniform superposition via Hadamards, data in |0>, flag in |->.

## Measurement

Measure the index register in the computational basis after the Grover iterations.

## Classical postprocessing

Read the outcome as candidate index x, classically check g(D_x) against the database, and repeat the run if it is not marked.

## Algorithm steps

1. Apply memory query U_M to load D_x into the data register, entangled with the index. (eq_2)
2. Compute predicate g(D_x) onto the flag in |-> so phase (-1)^{f(x)} is kicked back. (eq_1, eq_3)
3. Apply inverse memory query to uncompute the data register, leaving the net oracle action. Follow with the diffusion operator and repeat about (pi/4)sqrt(N/M) times for M marked items (sqrt(N) scale for M=1). (eq_1, eq_2)

## Assumptions

- Oracle is built as memory query, marking, and uncompute.
- Register sizes n, m, 1 and the single-flag layout are assumed, not from the abstract.
- Standard Grover iteration count is used.
- Equations are background or assumed; none are quoted from the abstract.

## Missing information

- Actual circuit design of the memory
- Gate counts and ancilla requirements
- Marking criterion details
- Number of marked items is not given, so the iteration count is unspecified.
- The abstract does not say how the classical memory is physically or logically realized as a circuit.
