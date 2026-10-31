# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Exact synthesis of single-qubit unitaries over the Clifford-cyclotomic gate set (Clifford group plus a z-rotation by pi/n, n a positive even integer): given an exactly synthesizable unitary, output a gate sequence using the minimum number of pi/n z-rotations. Also characterize when exactly synthesizable unitaries equal those with entries over Z[e^{i pi/n},1/2].

Scope: Abstract-level problem statement and ring characterization only. The detailed synthesis algorithm, its proofs, and the list of exceptional n are not in the abstract and are not reconstructed. No measurement or sampling stage exists.

## Symbols

- $n$: even positive integer parameterizing the gate set; domain: positive even integers
- $R_n$: ring Z[e^{i pi/n},1/2] of candidate matrix entries; domain: subring of C
- $U$: single-qubit unitary to synthesize; domain: 2x2 unitary matrices

## eq_1: Gate set

$$
\mathcal{G}_n=\langle \mathrm{Clifford},\ R_z(\pi/n)\rangle
$$

Clifford-cyclotomic gate set generating the exactly synthesizable group.

Provenance: `abstract_inferred`. Direct restatement of the gate set definition in the abstract.

Abstract evidence: the Clifford group plus a $z$-rotation by $\frac{\pi}{n}$

## eq_2: Ring of entries

$$
R_n=\mathbb{Z}[e^{i\pi/n},1/2]
$$

Ring over which unitary entries are compared with exactly synthesizable unitaries.

Provenance: `abstract_explicit`. Ring named explicitly in the abstract.

Abstract evidence: $\mathbb{Z}[e^{i\frac{\pi}{n}},1/2]$

## Registers

- q: 1 qubits; single data qubit on which the target unitary U acts; the synthesis output is a gate sequence over this qubit

## Initial state

Not a state-preparation task; the input is a classical description of U (2x2 matrix with entries in R_n, assumed exactly synthesizable). Circuit acts on an arbitrary single-qubit input.

## Measurement

None. The task is a deterministic classical compilation of U into a gate sequence; no quantum measurement is part of the abstract's algorithm.

## Classical postprocessing

The whole algorithm is classical: arithmetic over R_n for the reductions, then inverting the recorded reductions to output the gate sequence and counting the pi/n rotations. The abstract gives no further details.

## Algorithm steps

1. Input classical matrix U and check its entries lie in R_n (necessary condition for exact synthesizability for the cases where the characterization holds). (eq_2)
2. Iteratively reduce U by multiplying by Clifford gates and one R_z(pi/n) factor per round, following a generalized KMM-style reduction that lowers a size measure of the entries, until reaching a Clifford. Details of the reduction are not given in the abstract. (eq_1, eq_2)
3. Invert the recorded reductions to output the gate sequence over G_n with the minimal number of pi/n z-rotations. (eq_1)

## Assumptions

- The reduction step is a generalization of the Kliuchnikov-Maslov-Mosca approach; its concrete form is assumed, not given in the abstract.

## Missing information

- Explicit synthesis algorithm steps
- Which n have the ring characterization hold
- Proof of optimality of the count of pi/n rotations
- Exceptional values of n
- Concrete size measure and reduction rule used in the synthesis
