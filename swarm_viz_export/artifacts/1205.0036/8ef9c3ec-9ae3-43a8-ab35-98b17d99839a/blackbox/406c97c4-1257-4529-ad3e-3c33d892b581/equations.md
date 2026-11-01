# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Implement fanout |x>|y_1,y_2,y_3> -> |x>|y_1^x,y_2^x,y_3^x> as a non-adaptive, ancilla-free, measurement-free nearest-neighbor circuit on a 2x2 grid (k=2). The same circuit gives a controlled product of X gates, the tiny instance of the controlled-operation/fanout family.

Scope: Tiny non-adaptive 2x2 instance only: control c at (0,0), targets t1=(0,1), t2=(1,0), t3=(1,1). Not covered: the adaptive classical-controller simulation theorem, constant-depth Shor, the Theta(k-th root n) depth and size/width constructions at scale, and the lower-bound proof. The 2x2 case does not show asymptotic scaling.

## Symbols

- $x$: control bit; domain: {0,1}
- $y_i$: target bit i; domain: {0,1}, i=1..3
- $m$: number of targets; domain: 3 in the instance
- $k$: grid dimension; domain: 2 in the instance
- $n$: number of qubits (sites); domain: 4 in the instance
- $U_i$: single-qubit gate applied to target i when x=1; domain: U(2)
- $\mathrm{CNOT}_{a\to b}$: CNOT with control a and target b, applied only on grid-adjacent sites; domain: 2-qubit unitary

## eq_1: Fanout truth table

$$
F|x\rangle|y_1,y_2,y_3\rangle=|x\rangle|y_1\oplus x,y_2\oplus x,y_3\oplus x\rangle
$$

Fanout copies the control bit by XOR onto every target.

Provenance: `standard_background`. Standard definition of fanout; the abstract only names fanouts.

Equation assumptions:

- Computational-basis encoding, bit 1 = |1>

## eq_2: Controlled product operation

$$
C(U_1\otimes U_2\otimes U_3)=|0\rangle\langle0|\otimes I+|1\rangle\langle1|\otimes(U_1\otimes U_2\otimes U_3)
$$

Controlled tensor-product unitary; U_i=X for all i gives eq_1.

Provenance: `standard_background`. Standard controlled-unitary definition, restricted to product operations.

Equation assumptions:

- U is a tensor product of single-qubit gates

## eq_3: Nearest-neighbor 2x2 fanout circuit

$$
F=\mathrm{CNOT}_{c\to t_2}\,\mathrm{CNOT}_{c\to t_1}\,\mathrm{CNOT}_{t_1\to t_3}\,\mathrm{CNOT}_{c\to t_1}\,\mathrm{CNOT}_{t_1\to t_3}\,\mathrm{CNOT}_{c\to t_1}
$$

Operators act right to left, so the first gate applied is c->t1, then t1->t3, c->t1, t1->t3, c->t1, c->t2. Edges used: c-t1, t1-t3, c-t2, all grid-adjacent; c and t3 are diagonal and never interact directly.

Provenance: `assumption`. Proposed explicit construction, checked by hand in eq_4. It replaces the previous eq_3 and eq_4 candidates, which were not verified.

Equation assumptions:

- Sites row-major: c=(0,0), t1=(0,1), t2=(1,0), t3=(1,1)

## eq_4: Trace of the diagonal target

$$
t_3:\ y_3\to y_3\oplus(y_1\oplus x)\to y_3\oplus(y_1\oplus x)\oplus y_1=y_3\oplus x,\quad t_1:\ y_1\to y_1\oplus x\to y_1\to y_1\oplus x
$$

Intermediate values: after the first four gates t3 holds y_3 xor x and t1 is back to y_1. The last c->t1 and c->t2 then XOR x onto t1 and t2, giving eq_1.

Provenance: `assumption`. Direct bitwise check of eq_3; the t1 copy of x is uncomputed, so no ancilla is needed.

Equation assumptions:

- Ideal noiseless gates

## eq_5: Grid-diameter depth scaling

$$
D=\Theta(k\,n^{1/k})
$$

The stated depth of the optimal non-adaptive circuits, matching the order of the grid diameter.

Provenance: `abstract_inferred`. Reads k√n as the k-th root of n, with a factor k from the diameter. The 2x2 instance is a constant-size case only.

Abstract evidence: These circuits have depth Θ( k√n), size Θ(n) and width Θ(n).

Equation assumptions:

- k√n means the k-th root of n

## Registers

- c: 1 qubits; control qubit at (0,0), qubit index 0
- t: 3 qubits; target qubits t1=(0,1), t2=(1,0), t3=(1,1), qubit indices 1,2,3

## Initial state

Arbitrary state on c and t; no ancillas are required. Basis index is little-endian in Qiskit with qubit 0 = c.

## Measurement

The circuit is a measurement-free unitary. Decoding is computational-basis readout of c and t, expected to match the fanout truth table.

## Algorithm steps

1. Fix the grid, the adjacency edges c-t1, c-t2, t1-t3, t2-t3, and the fanout target map. (eq_1)
2. Apply CNOT c->t1, CNOT t1->t3, CNOT c->t1, CNOT t1->t3 to XOR x onto the diagonal site t3 via t1, leaving t1 unchanged. (eq_3, eq_4)
3. Apply CNOT c->t1 and CNOT c->t2 (parallel) to finish the fanout. For a controlled product with general U_i, replace these by controlled-U_i from c, with a similar path-based copy for t3. (eq_3, eq_2)
4. Check the 16 basis inputs against the fanout truth table. Depth and size match the diameter-scaling claim only up to the constant for this tiny instance. (eq_1, eq_5)

## Assumptions

- Smallest construction chosen: a non-adaptive 2x2 fanout, not the paper's adaptive simulation theorem
- Qubit order is c,t1,t2,t3 with row-major grid sites
- The controlled product reduces to fanout when each U_i=X

## Missing information

- The paper's exact circuits achieving depth Theta(k-th root of n) at scale
- The adaptive classical-controller simulation construction
- The lower-bound proof
