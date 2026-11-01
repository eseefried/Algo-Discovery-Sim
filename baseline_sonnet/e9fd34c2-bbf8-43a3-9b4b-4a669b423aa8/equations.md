# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Grover search over an unstructured classical database of N items, where the oracle reads the database from a quantumly accessible classical memory (QRAM-like lookup). The abstract gives no gate-level construction, so only a generic, assumed oracle is specified.

Scope: One smallest construction: N=4 database of 1-bit entries d(x), with a memory-lookup oracle that computes d(x) into an ancilla, applies a phase flip, and uncomputes. Outside scope: the paper's specific simple circuit implementation, its memory design, gate counts, resource analysis, and general N or multi-bit entries.

## Symbols

- $N=2^n$: number of database entries; domain: positive integer power of 2; n=2 in the instance
- $x$: address/index of database entry; domain: {0,...,N-1}
- $d(x)$: classical database entry at address x, marking function; domain: {0,1}
- $M$: number of marked entries with d(x)=1; domain: integer, 1<=M<N
- $\theta$: Grover angle; domain: (0,\pi/2)
- $U_M$: memory lookup unitary; domain: unitary on address and data registers
- $O$: Grover phase oracle; domain: unitary on address register

## eq_1: Memory lookup

$$
U_M|x\rangle_A|b\rangle_D=|x\rangle_A|b\oplus d(x)\rangle_D
$$

Quantumly accessible classical memory that stores the database and XORs the entry into a data qubit.

Provenance: `abstract_inferred`. The abstract says the oracle contains a quantumly accessible classical memory storing the database; the XOR-lookup form is the standard way to model this, but is inferred, not stated.

Abstract evidence: The oracle contains a kind of quantumly accessible classical memory, which stores the database.

Equation assumptions:

- Entry is 1 bit
- Lookup is of XOR type

## eq_2: Phase oracle via lookup and phase kickback

$$
O|x\rangle_A=(-1)^{d(x)}|x\rangle_A,\quad O=(\mathbb{1}_A\otimes\langle -|)\,U_M\,(\mathbb{1}_A\otimes|-\rangle)
$$

With data qubit in |-> = (|0>-|1>)/sqrt2, the lookup gives a phase (-1)^{d(x)} on the address register.

Provenance: `standard_background`. Standard phase kickback; the paper's actual circuit may differ.

Equation assumptions:

- Data qubit prepared in |->and returned unchanged

## eq_3: Grover iterate

$$
G=(2|s\rangle\langle s|-\mathbb{1})\,O,\quad |s\rangle=\frac{1}{\sqrt N}\sum_{x=0}^{N-1}|x\rangle
$$

Grover iteration with oracle O and diffusion about the uniform state.

Provenance: `standard_background`. Textbook Grover search.

## eq_4: Success probability

$$
\sin\theta=\sqrt{M/N},\quad P_k=\sin^2((2k+1)\theta)
$$

Probability of measuring a marked item after k iterations; exact for the ideal noiseless algorithm.

Provenance: `standard_background`. Standard Grover analysis.

Equation assumptions:

- Ideal noiseless gates

## eq_5: Tiny instance

$$
n=2,\ d=(0,0,1,0),\ M=1,\ \theta=\pi/6,\ k=1,\ P_1=\sin^2(\pi/2)=1
$$

Explicit N=4 example: marked address 2 is found with certainty after one iteration.

Provenance: `assumption`. Chosen as smallest useful instance; not from the abstract.

Equation assumptions:

- Database contents chosen arbitrarily

## Registers

- A: n=2 qubits qubits; address/search register, x encoded as big-endian binary integer
- D: 1 qubit qubits; data/ancilla qubit receiving d(x), kept in |->
- memory: unknown qubits; classical memory storing d(x); physical realization not specified in the abstract

## Initial state

|0>_A|1>_D, giving |0>_A|-> after Hadamard on D

## Measurement

Measure register A in the computational basis to obtain a candidate address.

## Classical postprocessing

Check the candidate x by classically reading d(x); repeat if d(x)=0.

## Algorithm steps

1. Apply H to every qubit of A to form |s>, and X then H to D to form |->. (eq_3)
2. Apply the oracle: memory lookup U_M with data qubit in |-> giving phase (-1)^{d(x)}. (eq_1, eq_2)
3. Apply diffusion 2|s><s|-1 on A. (eq_3)
4. Repeat the oracle and diffusion for k iterations (k=1 for the instance). (eq_4, eq_5)

## Assumptions

- No scope was provided; chose N=4, 1-bit entries, XOR-lookup oracle
- The lookup unitary is treated as a black box
- Ideal noiseless gates

## Missing information

- Actual circuit implementation of the oracle
- Design and gate decomposition of the quantumly accessible classical memory
- Entry width and database format
- Resource counts and any error analysis
