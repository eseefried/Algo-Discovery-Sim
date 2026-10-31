# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Equivalence checking of quantum states and quantum circuits under several notions of equivalence (exact, up to global phase, up to relative/diagonal phase, and up to measurement outcome statistics), as needed for quantum CAD tasks such as simulation and synthesis verification. The abstract names the problem family and claims fast, robust algorithms on benchmarks with hundreds of qubits, but states no formulas, data structures, or complexity bounds.

Scope: Finite scope chosen here (assumption, no experiment_scope supplied): define the equivalence relations mathematically for two n-qubit pure states |psi>,|phi> in C^{2^n} and two n-qubit unitaries U,V in U(2^n); give the standard linear-algebraic decision criteria; and fix one tiny explicit instance with n=1: U = X·Z (Z applied first, then X) versus V = Y, which are equivalent up to global phase (XZ = -iY) but not exactly equal, together with the state pair |+> and |-> which are measurement-outcome equivalent but not phase equivalent. Outside scope: the paper's actual decision-diagram (compact vector/matrix representation) algorithms, their canonical forms, the specific benchmark circuits (communication and search), scalability claims, and any mixed-state or partial-trace equivalence notions.

## Symbols

- $n$: number of qubits of the states/circuits being compared; domain: positive integer; n=1 in the tiny instance
- $N$: Hilbert-space dimension, N = 2^n; domain: positive integer power of two
- $|\psi\rangle, |\phi\rangle$: the two pure quantum states under comparison, with computational-basis amplitudes psi_k, phi_k, k in {0,...,N-1} (binary index, qubit 0 most significant); domain: unit vectors in C^N
- $U, V$: the two quantum circuits (as unitary matrices) under comparison; domain: U(N), N x N unitary matrices
- $\theta$: global phase angle; domain: real number in [0, 2\pi)
- $D$: diagonal unitary of relative phases, D = diag(e^{i\theta_0},...,e^{i\theta_{N-1}}); domain: diagonal matrix in U(N)
- $\langle\psi|\phi\rangle$: complex inner product of the two states; domain: complex number with modulus at most 1
- $X, Y, Z, H$: single-qubit Pauli and Hadamard gates; domain: 2 x 2 unitary matrices

## eq_1: Exact equivalence of states and circuits

$$
|\psi\rangle \equiv_{\mathrm{exact}} |\phi\rangle \iff \psi_k = \phi_k \ \forall k \in \{0,\dots,N-1\}, \qquad U \equiv_{\mathrm{exact}} V \iff U_{jk} = V_{jk} \ \forall j,k
$$

Entrywise equality of amplitude vectors or of unitary matrices; the strictest notion.

Provenance: `abstract_inferred`. The abstract poses equivalence of states and circuits; exact vector/matrix equality is the baseline notion implied before relaxations are introduced.

Abstract evidence: determining if two states or circuits are functionally equivalent

Equation assumptions:

- States are pure and given as full amplitude vectors; circuits are given as unitaries in the computational basis with qubit 0 as the most significant index bit.

## eq_2: Equivalence up to global phase (states)

$$
|\psi\rangle \equiv_{\mathrm{gp}} |\phi\rangle \iff \exists\,\theta\in[0,2\pi): |\psi\rangle = e^{i\theta}|\phi\rangle \iff |\langle\psi|\phi\rangle| = 1
$$

Two normalized states that differ only by a unit-modulus scalar are physically indistinguishable; the inner-product criterion is an exact equivalence for unit vectors (Cauchy–Schwarz equality case).

Provenance: `standard_background`. Standard linear algebra; the abstract only says that complex-valued vectors admit 'several notions of equivalence' without stating this relation.

Equation assumptions:

- Both states are normalized to unit norm.

## eq_3: Equivalence up to global phase (circuits)

$$
U \equiv_{\mathrm{gp}} V \iff \exists\,\theta: U = e^{i\theta}V \iff U^{\dagger}V = e^{-i\theta} I_N \iff |\mathrm{Tr}(U^{\dagger}V)| = N
$$

Circuit equivalence modulo an unobservable global phase; the trace criterion is exact because |Tr(W)| <= N for any unitary W with equality iff W is a scalar multiple of the identity.

Provenance: `standard_background`. Standard unitary-matrix fact; not stated in the abstract.

Equation assumptions:

- U and V act on the same n qubits with identical qubit ordering.

## eq_4: Equivalence up to relative (diagonal) phase and measurement-outcome equivalence

$$
|\psi\rangle \equiv_{\mathrm{rp}} |\phi\rangle \iff \exists\,\theta_0,\dots,\theta_{N-1}: \psi_k = e^{i\theta_k}\phi_k \ \forall k \iff |\psi_k|^2 = |\phi_k|^2 \ \forall k; \qquad U \equiv_{\mathrm{rp}} V \iff \exists\, D=\mathrm{diag}(e^{i\theta_k}): U = D V
$$

For pure states, allowing an independent phase on each computational-basis amplitude is exactly the condition that computational-basis measurement statistics coincide. For circuits, left-multiplication by a diagonal unitary D models circuits that agree up to relative phases on outputs (note U = DV implies columnwise equal moduli, |U_{jk}| = |V_{jk}|, but the converse requires the phases to be consistent across columns, i.e. column-independent).

Provenance: `assumption`. The abstract says quantum states 'exhibit subtle differences leading to several notions of equivalence' but names none; relative-phase and measurement-outcome equivalence are proposed here as natural additional notions, not established from the abstract.

Equation assumptions:

- Measurement is in the computational basis.
- For circuits, phases are applied as a single output-diagonal D (column-independent); other paper-specific relaxations may differ.

## eq_5: Tiny explicit instance (n=1)

$$
U = XZ = \begin{pmatrix}0 & -1\\ 1 & 0\end{pmatrix}, \quad V = Y = \begin{pmatrix}0 & -i\\ i & 0\end{pmatrix}, \quad U = e^{-i\pi/2} V, \quad |\mathrm{Tr}(U^{\dagger}V)| = 2 = N; \qquad |+\rangle = \tfrac{1}{\sqrt2}(|0\rangle+|1\rangle),\ |-\rangle = \tfrac{1}{\sqrt2}(|0\rangle-|1\rangle),\ |\langle +|-\rangle| = 0 \neq 1,\ |\langle k|+\rangle|^2 = |\langle k|-\rangle|^2 = \tfrac12
$$

Concrete instance exercising the hierarchy: the circuit pair is not exactly equal (eq_1 fails) but is equivalent up to global phase (eq_3 holds since XZ = -iY); the state pair is not phase-equivalent (eq_2 fails) yet is measurement-outcome / relative-phase equivalent (eq_4 holds).

Provenance: `assumption`. Chosen as the smallest instance distinguishing the three equivalence notions; the identity XZ = -iY follows from Y = iXZ, verified by direct 2x2 multiplication.

Equation assumptions:

- Matrix convention: XZ means Z applied first, then X.
- This instance is a reconstruction choice, not a benchmark from the paper.

## Registers

- system: n qubits; the n qubits on which the compared states |psi>,|phi> or circuits U,V are defined (n=1 in the tiny instance); the equivalence check itself is a classical CAD computation on their representations, not a quantum circuit

## Initial state

For the state-check instance: |psi> = |+>, |phi> = |->. For the circuit-check instance: U = X·Z and V = Y acting on |0> (any input; circuit equivalence is input-independent).

## Classical postprocessing

Output the strongest satisfied relation in the chain exact ⇒ global-phase ⇒ relative-phase/measurement-outcome, or 'not equivalent'. Dense-matrix evaluation costs O(N) for states and O(N^2)–O(N^3) for circuits with N = 2^n; this does not scale to hundreds of qubits, so the paper's claimed scalability must come from a compact (decision-diagram-style) representation that is not recoverable from the abstract.

## Algorithm steps

1. Classical step: build the computational-basis representations of the two objects (amplitude vectors psi,phi or unitaries U,V) with qubit 0 as the most-significant index bit; in the paper this is where a compact decision-diagram representation would be used, which is outside the reconstructable scope. (eq_1)
2. Classical step: test exact equivalence by entrywise comparison (optionally with a numerical tolerance epsilon for floating-point amplitudes; tolerance choice is an assumption). (eq_1)
3. Classical step: if exact equality fails, test global-phase equivalence via |<psi|phi>| = 1 for states or |Tr(U^dagger V)| = N for circuits; equivalently, compute the ratio of the first nonzero corresponding entries to get e^{i theta} and check that all entries agree after rescaling. (eq_2, eq_3)
4. Classical step: if global-phase equivalence fails, test relative-phase / measurement-outcome equivalence by comparing squared moduli entrywise for states, or checking that U V^dagger is a diagonal unitary for circuits. (eq_4)
5. Report the strongest equivalence notion satisfied; on the tiny instance this yields 'global-phase equivalent' for (XZ, Y) and 'measurement-outcome equivalent only' for (|+>, |->). (eq_5)

## Assumptions

- No experiment_scope was given, so the scope is the three-tier equivalence hierarchy on pure states and unitaries with the n=1 instance in eq_5.
- The specific set of 'several notions of equivalence' used by the paper is not stated in the abstract; global-phase, relative-phase and measurement-outcome equivalence are proposed as plausible notions.
- Qubit ordering: qubit 0 is the most-significant bit of the basis-state index; gate products are read right-to-left in time.
- Floating-point comparisons would require a tolerance epsilon; its value is unspecified.

## Missing information

- The paper's actual algorithms and data structures (presumably a decision-diagram representation of vectors/matrices) and how equivalence tests are performed on them canonically.
- The exact list and formal definitions of the equivalence notions the paper identifies.
- The benchmark circuits (quantum communication and search circuits), their sizes, and runtime/robustness results.
- Any treatment of mixed states, density matrices, partial traces, or equivalence of circuits with ancillas/measurements.
- Numerical tolerance handling for approximate equivalence.
