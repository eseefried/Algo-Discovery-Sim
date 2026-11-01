# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Grover search over a classical database D[0..N-1] of m-bit words, N=2^n, to find an address i with D[i]=w, using an oracle built from a QRAM-like lookup (address-controlled X gates) with compute, mark and uncompute steps.

Scope: One tiny explicit instance, e.g. n=2, m=2, M=1, with the database and target known classically at build time. Includes load, mark via a |-> flag, uncompute, diffusion, iteration count and index readout. Paper-specific details beyond the abstract (exact gate-level QRAM design, resource counts, generalization to multiple matches or large databases) are outside scope.

## Symbols

- $n$: number of index (address) qubits; domain: positive integer
- $N$: database size, N=2^n; domain: positive integer
- $m$: word width in bits; domain: positive integer
- $D[i]$: classical database word at address i; domain: {0,1}^m
- $w$: target word being searched for; domain: {0,1}^m
- $M$: number of addresses i with D[i]=w; domain: integer 1..N-1 (M=1 assumed)
- $R$: number of Grover iterations; domain: non-negative integer
- $U_D$: QRAM load unitary; domain: unitary on index and data registers

## eq_1: QRAM load

$$
U_D|i\rangle_{I}|0\rangle_{R}=|i\rangle_{I}|D[i]\rangle_{R},\quad U_D=\prod_{i=0}^{N-1}\prod_{j:D[i]_j=1}\mathrm{C}^{n}_{i}X_{j}
$$

Coherent read of the classical memory, implemented as X on data qubit j controlled on the index register equal to i. Controls for 0 bits of i are flipped by X gates around the mcx.

Provenance: `abstract_inferred`. The abstract says the oracle contains quantumly accessible classical memory storing the database; the address-controlled X realization is an assumed implementation.

Abstract evidence: The oracle contains a kind of quantumly accessible classical memory, which stores the database.

Equation assumptions:

- Lookup uses only X, mcx gates
- Each gate toggles bits, so U_D is self-inverse

## eq_2: Flag phase marking

$$
\mathrm{MCX}_{R\to f}\,|x\rangle_R|-\rangle_f=(-1)^{[x=w]}|x\rangle_R|-\rangle_f,\quad \text{with X on data bits where }w_j=0\text{ before and after}
$$

Compare the data register to w via X conjugation, then an mcx onto the flag qubit in |->, giving a phase kickback.

Provenance: `assumption`. Standard phase-kickback marking, proposed as the oracle's comparison step.

Equation assumptions:

- Flag qubit prepared in |-> via X then H

## eq_3: Clean oracle

$$
O=U_D\,\mathrm{Mark}_w\,U_D,\quad O|i\rangle|0\rangle_R|-\rangle=(-1)^{[D[i]=w]}|i\rangle|0\rangle_R|-\rangle
$$

Load, mark, then uncompute so the data register returns to zero and the oracle acts as a phase oracle on the index.

Provenance: `assumption`. Compute-mark-uncompute follows from eq_1 and eq_2; the abstract only proposes a circuit implementation of the Grover oracle.

Equation assumptions:

- U_D is self-inverse

## eq_4: Diffusion operator

$$
G=\left(2|s\rangle\langle s|-I\right)O,\quad |s\rangle=H^{\otimes n}|0\rangle^{n},\quad 2|s\rangle\langle s|-I=H^{\otimes n}X^{\otimes n}\,\mathrm{C}^{n-1}Z\,X^{\otimes n}H^{\otimes n}\ \text{(up to global phase)}
$$

Grover iteration applied to the index register.

Provenance: `standard_background`. Standard Grover diffusion; the reflection is equal up to a global sign.

Equation assumptions:

- n>=2 for the multi-controlled Z, or use plain Z for n=1

## eq_5: Iteration count and success probability

$$
R=\left\lfloor \frac{\pi}{4}\sqrt{N/M}\right\rfloor,\quad P_{succ}=\sin^2\left((2R+1)\theta\right),\ \sin\theta=\sqrt{M/N}
$$

Number of iterations and resulting probability of measuring a marked address.

Provenance: `standard_background`. Textbook Grover analysis. For N=4, M=1, R=1 and P=1.

Equation assumptions:

- M known; M=1 assumed

## Registers

- index: n qubits; address register, searched over; qubit i is the i-th bit of the address (little-endian)
- data: m qubits; QRAM output word register, returned to |0> after each oracle
- flag: 1 qubits; phase kickback qubit in |->

## Initial state

index qubits H^{\otimes n}|0>, data |0>^m, flag |-> (X then H). Total n+m+1 qubits, plus an optional mcx ancilla.

## Measurement

Measure only the n index qubits, with measure(i,i) for index qubit i. In Qiskit counts keys the last character is classical bit 0, so bits[::-1][i] is index qubit i.

## Classical postprocessing

Take the most frequent bitstring, reverse it to little-endian, and read the integer address i. Optionally check D[i]=w classically.

## Algorithm steps

1. Prepare the uniform superposition on the index register and the flag in |->. (eq_4)
2. Load: apply the address-controlled X gates for every i and every bit j with D[i]_j=1. (eq_1)
3. Mark: X on data bits where w_j=0, mcx from data to flag, undo the X gates. (eq_2)
4. Uncompute: repeat the load step so the data register returns to |0>, giving the clean oracle O. (eq_3)
5. Apply diffusion on the index register. Repeat steps 2-5 R times. (eq_4, eq_5)

## Assumptions

- Smallest instance: n=2, m=2, M=1, with D and w chosen so that the target is unique
- D and w are known at build time
- The oracle is a standard-gate construction with no black box, and one oracle use is one query per iteration
- No initialize or state-prep gates

## Missing information

- Exact gate-level QRAM design and any optimizations in the paper
- Gate or depth counts from the paper
- Handling of multiple matches or unknown M
- Whether the paper uses a different mark or compare design
