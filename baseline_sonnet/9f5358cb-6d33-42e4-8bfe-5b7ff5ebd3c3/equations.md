# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Decompose an n-qubit diagonal Hermitian gate into multiple-controlled Z gates by mapping the gate to a binary vector over GF(2) and expressing it in the basis given by binary representations of multiple-controlled Z gates.

Scope: Tiny instance: n=2 qubits. Diagonal Hermitian gate D=diag((-1)^{f(x)}) with f:{0,1}^2->{0,1}. Binary representation is the vector of f values; basis is the set of multiple-controlled Z gates (Z on qubit 1, Z on qubit 2, CZ). Out of scope: general n, cost optimization, CZ vs CNOT library cost comparison, experimental results, and the paper's exact binary representation and basis construction.

## Symbols

- $D$: diagonal Hermitian gate; domain: 2^n x 2^n unitary matrix
- $d_x$: diagonal entry for basis state x; domain: {+1,-1}
- $f(x)$: binary exponent with d_x=(-1)^{f(x)}; domain: {0,1}
- $\mathbf{b}(D)$: binary representation vector of D (assumed to be the f values); domain: \mathbb{F}_2^{2^n}
- $S$: subset of qubits acted on by a multiple-controlled Z gate; domain: nonempty subset of {1,...,n}
- $c_S$: coefficient indicating whether MCZ_S is included; domain: {0,1}
- $n$: number of qubits; domain: positive integer

## eq_1: Diagonal Hermitian form

$$
D=\sum_{x\in\{0,1\}^n} d_x |x\rangle\langle x|,\quad d_x\in\{+1,-1\}
$$

A diagonal gate is Hermitian and unitary iff its diagonal entries are real and of unit modulus, hence +-1.

Provenance: `standard_background`. D=D^dagger needs real entries and unitarity needs modulus 1, so entries are +-1. The abstract only says these gates can be decomposed into MCZ gates.

Equation assumptions:

- Gate is both Hermitian and unitary

## eq_2: Binary representation

$$
d_x=(-1)^{f(x)},\quad \mathbf{b}(D)=(f(x))_{x\in\{0,1\}^n}\in\mathbb{F}_2^{2^n}
$$

Assumed binary vector encoding of D, with x ordered as an integer with qubit 1 as most significant bit.

Provenance: `assumption`. The abstract mentions a binary representation but does not define it; this is the natural choice.

Equation assumptions:

- The paper's encoding may differ

## eq_3: MCZ gate action

$$
\mathrm{MCZ}_S|x\rangle=(-1)^{\prod_{i\in S}x_i}|x\rangle
$$

A Z gate controlled on all other qubits in S applies a phase of -1 only when all qubits in S are 1.

Provenance: `standard_background`. Standard definition of multiple-controlled Z, which is symmetric in its qubits.

## eq_4: Decomposition as GF(2) linear combination

$$
\mathbf{b}(D)=\sum_{S\neq\emptyset}c_S\,\mathbf{b}(\mathrm{MCZ}_S),\quad D=\prod_{S:c_S=1}\mathrm{MCZ}_S
$$

Decomposition is writing b(D) in the MCZ basis over GF(2). Diagonal gates commute and their phases add mod 2.

Provenance: `abstract_inferred`. Directly follows from the stated mapping, with the GF(2) field being an inference given the binary vectors.

Abstract evidence: the problem of decomposing a given diagonal Hermitian gate is mapped to the problem of writing its binary representation in the specific basis mentioned above

Equation assumptions:

- Vector space is over GF(2)
- f(0)=0 so the global phase is +1 (otherwise a global -1 is needed)

## eq_5: n=2 instance

$$
f(x_1,x_2)=c_{1}x_1\oplus c_{2}x_2\oplus c_{12}x_1x_2,\quad (f(00),f(01),f(10),f(11))=(0,c_2,c_1,c_1\oplus c_2\oplus c_{12})
$$

Triangular system solved by c_2=f(01), c_1=f(10), c_12=f(11)⊕f(01)⊕f(10).

Provenance: `assumption`. Worked tiny instance of the mapping with an invertible basis matrix.

Equation assumptions:

- n=2
- f(00)=0

## Registers

- q: n (n=2 in the instance) qubits; qubits on which the diagonal gate acts

## Classical postprocessing

Solve the GF(2) linear system, with the matrix entries given by products of bits, to obtain the coefficients c_S.

## Algorithm steps

1. Given a diagonal Hermitian D, read off the signs d_x and form f(x) and b(D). (eq_1, eq_2)
2. Solve the GF(2) linear system in the MCZ basis for the coefficients c_S. (eq_4, eq_5)
3. Emit one MCZ_S gate for each S with c_S=1; for n=2 these are Z on qubit 1, Z on qubit 2, and CZ. (eq_3, eq_4)

## Assumptions

- Chosen scope is the n=2 instance.
- The binary representation is taken to be the f-vector, which may differ from the paper.
- Global phase is ignored or f(0)=0.

## Missing information

- The paper's exact binary representation definition
- Its basis ordering and construction
- Its cost model and the CZ versus CNOT library cost comparison
- Its experimental benchmarks
- Any optimization of the gate ordering or synthesis of MCZ gates into CZ
