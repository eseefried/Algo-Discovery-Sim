# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given adjacency-matrix oracle access to an unweighted n-vertex graph G, find a triangle (u,v,w) with all three edges present. The abstract claims query complexity O~(n^{5/4}). The scoped reconstruction is only a small-n (4 to 6) Grover/amplitude-amplification skeleton over vertex triples. It uses the opaque edge oracle, with compute-AND-uncompute of three edge-query bits and a phase-kickback ancilla.

Scope: Only the scaled-down outer Grover search over candidate triples (u,v,w) with an oracle that marks triples whose three edges are present, plus classical verification and repetition. Outside scope: the combinatorial n^{5/4} algorithm itself (random subset sampling, edge-triangle classification, neighborhood search, balancing), the learning-graph comparison, and the lower bounds. Their details are not given in the abstract and are not reconstructed.

## Symbols

- $n$: number of vertices; domain: integer, 4<=n<=6 for simulation
- $m$: qubits per vertex index, ceil(log2 n); domain: positive integer
- $A[u][v]$: adjacency bit of the hidden graph; domain: {0,1}, symmetric, A[u][u]=0
- $O_G$: opaque adjacency oracle, one query per placement; domain: unitary on 2m+1 qubits
- $f(u,v,w)$: triangle indicator A[u][v] AND A[v][w] AND A[u][w], with u,v,w distinct and in [0,n); domain: {0,1}
- $N$: size of the search space, 2^{3m} basis states; domain: integer
- $M$: number of marked basis triples (ordered), unknown; domain: integer
- $k$: number of Grover iterations; domain: nonnegative integer

## eq_1: Edge oracle

$$
O_G|u,v,b\rangle=|u,v,b\oplus A[u][v]\rangle
$$

Opaque adjacency query, one query per placement.

Provenance: `assumption`. The sketch gives this adjacency-matrix oracle model; the abstract only implies unweighted edge queries.

Equation assumptions:

- Adjacency-matrix query model

## eq_2: Triangle predicate

$$
f(u,v,w)=A[u][v]\wedge A[v][w]\wedge A[u][w]\wedge[u,v,w\text{ distinct},<n]
$$

Marks the triples that the checker accepts.

Provenance: `abstract_inferred`. A triangle in an unweighted graph is three mutually adjacent vertices. The distinctness and range checks are assumed, so the invalid index values (>=n) must be handled.

Abstract evidence: triangle finding problem in unweighted graphs

Equation assumptions:

- Distinctness and range check done by ordinary gates, with no queries

## eq_3: Phase oracle via compute-AND-uncompute

$$
U_f|u,v,w\rangle=(-1)^{f(u,v,w)}|u,v,w\rangle
$$

Query three edge bits into ancillas, compute AND into a phase-kickback ancilla in |->, then uncompute the edge bits so the ancillas return to |0>. This costs 6 queries per use, 3 to compute and 3 to uncompute.

Provenance: `assumption`. A standard Grover oracle construction from the sketch, not from the abstract.

Equation assumptions:

- The ancillas are 3 edge-bit qubits and 1 kickback qubit
- The range and distinctness check may need an extra flag ancilla

## eq_4: Grover iteration

$$
G=(2|s\rangle\langle s|-I)\,U_f,\quad |s\rangle=N^{-1/2}\sum_x|x\rangle
$$

Diffusion about the uniform superposition over triples, applied after the phase oracle.

Provenance: `standard_background`. Standard Grover search, used as the scaled-down skeleton of amplitude amplification.

Equation assumptions:

- Uniform superposition over all 2^{3m} index strings, including invalid ones, which U_f leaves unmarked

## eq_5: Success probability and iteration count

$$
P_k=\sin^2((2k+1)\theta),\ \sin\theta=\sqrt{M/N},\ k\approx\frac{\pi}{4}\sqrt{N/M}
$$

Success probability after k iterations. If M is unknown, try k=1,2,4,... with verification after each try.

Provenance: `standard_background`. Standard amplitude amplification, matching the sketch's 1/sqrt(p) iteration count and the exponential guessing of iteration counts.

Equation assumptions:

- M>=1 for a graph that contains a triangle

## Registers

- u: ceil(log2 n) qubits; first vertex index
- v: ceil(log2 n) qubits; second vertex index
- w: ceil(log2 n) qubits; third vertex index
- e: 3 qubits; edge-bit ancillas for A[u][v], A[v][w], A[u][w], returned to 0
- kick: 1 qubits; phase-kickback ancilla in |-> (X then H)
- flag: 1 qubits; optional validity (distinct, <n) flag ancilla, returned to 0

## Initial state

All qubits in |0>. Hadamard on u,v,w to give the uniform superposition. The kick ancilla is set to |->.

## Measurement

Measure only the u,v,w registers (3m bits). In Qiskit counts keys the last character is classical bit 0. Map each register to its own classical bits and decode carefully.

## Classical postprocessing

Decode (u,v,w), check distinctness and that each index is <n, and verify with three direct edge queries. If verification fails, repeat with another k from the guessing schedule, O(log n) repetitions in total.

## Algorithm steps

1. Prepare the uniform superposition on the three vertex registers and put the kickback ancilla in |->. (eq_4)
2. Apply the phase oracle. Compute the 3 edge bits with O_G placeholders, check validity, and compute the AND into kick. Then uncompute everything so the ancillas return to 0. (eq_1, eq_2, eq_3)
3. Apply the diffusion on the u,v,w registers. Repeat for k iterations, with k chosen via the exponential guessing schedule. (eq_4, eq_5)
4. Measure the u,v,w registers, taking care over little-endian bit order, and verify the result classically. (eq_2)

## Assumptions

- Scaled-down instance: n in 4..6, so 3m=6 or 9 index qubits plus 5 ancillas, within the cap only if the cap allows it
- Ordered triples are searched, so M=6 times the number of triangles
- This is not the paper's n^{5/4} algorithm and has about n^{3/2} query cost, only a skeleton

## Missing information

- The abstract gives no details of the combinatorial algorithm: subset size, sampling, classification of edges by triangle count, or the neighborhood search
- The exact outer amplitude-amplification structure and parameter balancing for n^{5/4} are not given
- The qubit cap and the query budget are unknown
