# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Evaluate a single ternary majority gate MAJ3(x1,x2,x3) on an explicit classical input x by building a span-program-derived weighted bipartite graph, compiling its adjacency matrix into a unitary, and applying a phase-estimation-style spectral test for the eigenvalue-zero eigenvector with root support.

Scope: Single depth-1 MAJ3 gate with explicit classical input x compiled into gates. No recursive formula composition, no balanced-formula optimality, no query-complexity claim. The exact MAJ3 span program and graph weights are background or assumption, not given in the abstract. A concrete weighted graph and phase-estimation schedule are not fully fixed here.

## Symbols

- $x=(x_1,x_2,x_3)$: Classical input bits; domain: {0,1}^3
- $P$: Span program with target t and input vectors v_i; domain: vectors over R^d
- $t$: Target vector of the span program; domain: R^d
- $v_i$: Vector available when x_i=1; domain: R^d
- $G(x)$: Weighted bipartite graph built from P and x; domain: finite graph
- $A(G)$: Symmetric weighted adjacency matrix of G(x); domain: real symmetric matrix
- $|r\rangle$: Root vertex basis state; domain: vertex Hilbert space
- $U$: Unitary exp(iA s) with s a gap-scale time (assumption); domain: unitary on vertex space
- $\epsilon$: Phase-estimation precision, below the smallest nonzero |eigenvalue| scale; domain: positive real

## eq_1: MAJ3 definition

$$
\mathrm{MAJ3}(x)=1\iff x_1+x_2+x_3\ge 2
$$

Function to be evaluated

Provenance: `standard_background`. Definition of 3-majority, named in the abstract only by name.

Equation assumptions:

- Bits 0/1

## eq_2: Span program acceptance

$$
f(x)=1\iff t\in\mathrm{span}\{v_i : x_i=1\}
$$

Span program evaluates to 1 when the target lies in the span of the available input vectors

Provenance: `standard_background`. Standard span-program definition; abstract mentions span programs only as a linear-algebraic model of computation.

Equation assumptions:

- A valid MAJ3 span program P is chosen, e.g. any two available inputs span t and a single one does not

## eq_3: Graph eigenvector correspondence

$$
f(x)=1\iff \exists\,\psi\neq0:\ A(G(x))\psi=0,\ \langle r|\psi\rangle\neq0
$$

Evaluation corresponds to a zero-eigenvalue eigenvector of the graph, with root overlap as the decision criterion

Provenance: `abstract_inferred`. The abstract states the correspondence qualitatively. The root-overlap criterion is an assumed refinement, and the precise graph construction is not given.

Abstract evidence: A span program's evaluation corresponds to an eigenvalue-zero eigenvector of the associated graph.

Equation assumptions:

- Root-support formulation; exact graph weights are a modeling choice

## eq_4: Unitary from graph

$$
U=e^{iA s},\quad A=\begin{pmatrix}0&B(x)\\B(x)^{T}&0\end{pmatrix}
$$

Bipartite adjacency block form compiled into a unitary; eigenvalue 0 gives phase 0

Provenance: `assumption`. Hamiltonian simulation of the adjacency matrix is a standard route to spectral estimation; the choice of s and the simulation method are assumed.

Equation assumptions:

- Explicit classical matrix compiled to gates, e.g. exact matrix exponential synthesis for a tiny instance
- s*||A||<pi so phases do not alias

## eq_5: Zero-phase probability

$$
p_0=\sum_{\lambda:\,|\lambda|<\epsilon'}|\langle\psi_\lambda|r\rangle|^2
$$

Probability that phase estimation on |r> reads the zero-eigenvalue bin

Provenance: `standard_background`. Standard phase estimation applied to |r> decomposed in the eigenbasis of A, ignoring leakage from finite precision. The abstract states only that spectral estimation is used.

Equation assumptions:

- Gap between 0 and the smallest nonzero |eigenvalue| exceeds the precision

## Registers

- vertex: ceil(log2 |V|) qubits, basis states indexed by graph vertices qubits; Holds the graph vertex state; initial state is the root vertex
- phase: m qubits with 2^m large relative to 1/epsilon qubits; Phase estimation register, left unmeasured by the measurement-free circuit

## Initial state

vertex register in |r> (root vertex basis state), phase register in |0^m>

## Measurement

Read the phase register externally; outcome 0 (zero-eigenvalue bin) indicates a zero eigenvector with root overlap, i.e. formula value per the correspondence. The returned circuit itself is measurement-free.

## Classical postprocessing

Threshold p_0 compared with a constant, with repetition if needed; the threshold is an assumption.

## Algorithm steps

1. Fix the MAJ3 span program P (background or assumption) and build the bipartite graph G(x) by keeping only edges for inputs with x_i=1. (eq_1, eq_2, eq_3)
2. Form the adjacency matrix A and compile U=exp(iAs) classically into gates, with controlled powers U^(2^k). (eq_4)
3. Apply Hadamards to the phase register, controlled powers of U, and the inverse QFT on the phase register. (eq_4, eq_5)

## Assumptions

- The smallest useful construction is a single MAJ3 gate with explicit x
- The span program and graph weights are a chosen standard construction, not from the abstract
- Adjacency compiled explicitly into gates, with no black-box or query-count claim
- Root-overlap decision rule and the time s are assumptions

## Missing information

- Exact graph construction and edge weights from the paper
- Precise gap and precision analysis
- Recursive composition for formulas
- Handling of the case where the root has small overlap on the zero eigenspace
- Optimality claims for the balanced ternary majority formula, not reproduced
