# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Equivalence checking of quantum states and circuits under several notions of equivalence (e.g., exact equality versus equality up to global phase). The abstract names these notions but gives no specific algorithm or equations.

Scope: Background definitions only, for a tiny instance: two n-qubit unitaries U and V given as circuits, checked for exact equivalence and equivalence up to global phase. The paper's actual algorithms, data structures, and scalability techniques for hundreds of qubits are outside scope and are not reconstructed.

## Symbols

- $n$: number of qubits; domain: positive integer
- $|\psi\rangle,|\phi\rangle$: pure n-qubit states as complex vectors; domain: unit vectors in C^{2^n}
- $U,V$: unitaries implemented by two circuits; domain: U(2^n)
- $\theta$: global phase; domain: [0,2\pi)
- $d$: Hilbert-space dimension, 2^n; domain: positive integer

## eq_1: Exact state equality

$$
|\psi\rangle=|\phi\rangle
$$

Strictest notion: equal complex vectors.

Provenance: `abstract_inferred`. States being complex vectors implies vector equality as the strictest equivalence notion; this is an inference.

Abstract evidence: quantum states, which are represented by complex-valued vectors

Equation assumptions:

- Pure states

## eq_2: State equivalence up to global phase

$$
|\psi\rangle=e^{i\theta}|\phi\rangle \iff |\langle\psi|\phi\rangle|=1
$$

Physical equivalence ignoring global phase, for normalized states.

Provenance: `standard_background`. Standard fact; the abstract only says several notions of equivalence exist and does not specify this one.

Equation assumptions:

- Normalized pure states

## eq_3: Exact circuit equivalence

$$
U=V \iff V^\dagger U=I_{d}
$$

Circuits are equivalent when their unitaries are identical.

Provenance: `standard_background`. Standard definition of functional equivalence of circuits.

Equation assumptions:

- Same qubit count and no ancillas or measurements

## eq_4: Circuit equivalence up to global phase

$$
U=e^{i\theta}V \iff \frac{|\mathrm{Tr}(V^\dagger U)|}{d}=1
$$

Equivalence ignoring an unobservable global phase.

Provenance: `standard_background`. Standard criterion via Cauchy-Schwarz equality in the Hilbert-Schmidt inner product.

Equation assumptions:

- U and V unitary of the same dimension

## Registers

- q: n qubits; data qubits on which U and V act

## Algorithm steps

1. Form the miter circuit V^\dagger U on n qubits for the two given circuits. (eq_3)
2. Test whether V^\dagger U is the identity exactly, or the identity up to a global phase. (eq_3, eq_4)
3. For state equivalence, compare the output states exactly or up to global phase. (eq_1, eq_2)

## Assumptions

- The abstract gives no equations, so all equations are generic background or inference.
- Only exact and global-phase notions are listed; the paper may define others (e.g., relative-phase or measurement-based equivalence).
- The tiny instance is two n-qubit circuits with no ancillas.

## Missing information

- The specific equivalence notions the paper defines
- The paper's algorithms and data structures
- Details of the quantum communication and search benchmark circuits
- How scalability to hundreds of qubits is achieved
- Any numerical results
