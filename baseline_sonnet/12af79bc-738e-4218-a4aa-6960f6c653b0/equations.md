# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Construct an orthonormal basis of entangled Bell-like states, each a superposition of 2^m terms with amplitudes ±1/sqrt(2^m), using multi-qubit controlled-unitary gates plus standard gates. The abstract does not define the two controlled-unitary gates, so only a generic stand-in can be specified.

Scope: Smallest useful instance (assumed): m=1 on 2 qubits, giving the standard Bell basis via Hadamard and CNOT, plus the general amplitude/normalization constraint from the abstract. The paper's two specific multi-qubit controlled-unitary gates, the general-m algorithms, the entanglement/monogamy-score analysis, and the qudit extension are outside scope.

## Symbols

- $m$: Number log2 of the number of terms in each Bell-like state; domain: positive integer
- $n$: Number of qubits (assumed n=2 for the tiny instance); domain: positive integer, n>=m
- $|\beta_{ab}\rangle$: Bell basis state labelled by bits a,b; domain: a,b in {0,1}
- $s_x$: Sign of the term |x> in a Bell-like state; domain: {+1,-1}
- $H$: Hadamard gate; domain: single-qubit unitary
- $\mathrm{CNOT}$: Controlled-NOT gate, control qubit 1, target qubit 2; domain: two-qubit unitary

## eq_1: Equal-amplitude form

$$
|\psi\rangle=\frac{1}{\sqrt{2^{m}}}\sum_{k=1}^{2^{m}} s_{x_k}|x_k\rangle,\quad s_{x_k}\in\{+1,-1\}
$$

Bell-like state as a superposition of 2^m computational basis states with amplitudes ±1/sqrt(2^m).

Provenance: `abstract_explicit`. Directly restates the amplitude form given in the abstract; the labels x_k are distinct n-bit strings.

Abstract evidence: The Bell-like states in any basis is superposition of $2^{m}$-terms with equal probabilities (that is, their amplitudes being $\pm 1/\sqrt{2^{m}}$).

Equation assumptions:

- The x_k are distinct computational basis strings

## eq_2: Orthonormality of basis

$$
\langle\psi_i|\psi_j\rangle=\delta_{ij}
$$

Basis states must be orthonormal, which is the stated reason arbitrary amplitudes are not allowed.

Provenance: `abstract_inferred`. Orthonormality is the basis requirement implied by the abstract; the explicit inner-product form is the standard definition.

Abstract evidence: The orthogonality of the basis does not permit arbitrary amplitudes.

Equation assumptions:

- Basis consists of orthonormal vectors in the n-qubit Hilbert space

## eq_3: Bell state preparation circuit (m=1)

$$
|\beta_{ab}\rangle=\mathrm{CNOT}_{1\to2}(H\otimes I)|a\rangle|b\rangle=\frac{1}{\sqrt2}\left(|0,b\rangle+(-1)^{a}|1,\,1\oplus b\rangle\right)
$$

Standard Bell basis from computational inputs; the simplest instance of the 2^m-term form with m=1.

Provenance: `standard_background`. Textbook construction used as a stand-in; it is not the paper's controlled-unitary method.

Equation assumptions:

- Qubit 1 is the control; ordering |q1 q2>
- Chosen as the tiny instance, not taken from the abstract

## eq_4: Generic multi-controlled unitary action

$$
C^{k}U=\,|1\rangle\langle1|^{\otimes k}\otimes U+\left(I-|1\rangle\langle1|^{\otimes k}\right)\otimes I
$$

Generic k-control unitary acting on target when all controls are 1. The paper's two gates are not specified by the abstract.

Provenance: `standard_background`. General definition of a multi-qubit controlled-unitary; the paper's specific gates and working principles are unknown.

Equation assumptions:

- Standard all-ones control condition
- May differ from the paper's two gates

## Registers

- q: 2 qubits; Two-qubit register, ordering q1 q2, for the Bell instance (assumed)

## Initial state

|a>|b> computational basis input with a,b in {0,1} (assumed)

## Algorithm steps

1. Prepare computational basis input |a>|b>. (no equation reference)
2. Apply H on qubit 1 then CNOT with qubit 1 as control and qubit 2 as target to obtain the Bell state. (eq_3)
3. Check that the four outputs are orthonormal and have the equal-amplitude form with m=1. (eq_1, eq_2)

## Assumptions

- No scope was given; m=1 on 2 qubits chosen as the smallest instance.
- The Bell construction is a generic stand-in and not the paper's controlled-unitary algorithm.
- Entanglement and monogamy-score analysis are not reconstructed.

## Missing information

- Definitions and working principles of the two multi-qubit controlled-unitary gates
- Algorithm for general m and the sign/term-selection patterns
- Definition of entanglement measures and monogamy score used
- Qudit generalization details
