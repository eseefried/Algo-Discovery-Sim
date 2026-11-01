# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Evaluate a single ternary majority gate MAJ3(x1,x2,x3) on an explicit classical input x by building a span-program-derived weighted bipartite graph, compiling its adjacency matrix into a unitary, and running phase estimation to test for an eigenvalue-zero eigenvector with root support. The construction is tiny and explicit, and the abstract's recursive formula evaluation is not covered.

Scope: Depth-1 MAJ3 with explicit x compiled into gates, using a concrete span program and graph chosen here as background or assumption, not taken from the abstract. Covers only the single-gate case: no recursive composition, no optimality claim, no query complexity claim. Phase estimation is approximate, and a hard-coded tiny instance is used. Corrects the earlier build: the root state must be prepared explicitly, a consistent vertex encoding is needed, and the edge terms must be implemented by an exact matrix exponential of the whole A, not a Trotterization with mismatched indices.

## Symbols

- $x=(x_1,x_2,x_3)$: Classical input bits; domain: {0,1}^3
- $t$: Span program target vector; domain: R^2, t=(1,0)
- $v_1,v_2,v_3$: Input vectors, available iff x_i=1. Assumed choice with v_1=(1,1), v_2=(1,-1), v_3=(0,1) is not valid for MAJ3 (v_3 plus v_1 spans, but v_1 and v_2 span too, and the singleton cases need checking). A valid MAJ3 span program must be fixed in a later stage, e.g. a standard one with a 2-dim target space.; domain: R^2
- $B(x)$: Biadjacency matrix: rows are span-space coordinates plus a root row, columns are the available inputs; domain: real matrix
- $A(x)$: Graph adjacency matrix [[0,B],[B^T,0]]; domain: real symmetric
- $|r\rangle$: Root vertex basis state, prepared by explicit X gates on the vertex register; domain: vertex space
- $U$: exp(iAs), compiled exactly as a dense unitary for the tiny instance; domain: unitary
- $p_0$: Probability that the phase register reads 0; domain: [0,1]

## eq_1: MAJ3

$$
\mathrm{MAJ3}(x)=1\iff x_1+x_2+x_3\ge 2
$$

Target function

Provenance: `standard_background`. Definition of 3-majority, which the abstract names only by name.

Equation assumptions:

- Bits 0/1

## eq_2: Span program acceptance

$$
f(x)=1\iff t\in\mathrm{span}\{v_i:x_i=1\}
$$

Span program evaluation rule

Provenance: `standard_background`. Standard definition. The abstract names span programs only as a linear-algebraic model.

Equation assumptions:

- A valid MAJ3 span program is chosen and verified over all 8 inputs before building the circuit

## eq_3: Graph zero-eigenvector correspondence

$$
f(x)=1\iff \exists\psi\ne0:\ A(x)\psi=0,\ \langle r|\psi\rangle\ne0
$$

Evaluation corresponds to a zero-eigenvalue eigenvector of the graph, with root support as the test

Provenance: `abstract_inferred`. The abstract states the correspondence qualitatively. Root support is an assumed refinement, and the detailed graph construction is not given.

Abstract evidence: A span program's evaluation corresponds to an eigenvalue-zero eigenvector of the associated graph.

Equation assumptions:

- The root is a dedicated vertex joined to the target row, so the zero eigenvector must have root overlap, not merely lie in the kernel of B

## eq_4: Graph unitary

$$
U=e^{iAs},\quad A=\begin{pmatrix}0&B(x)\\B(x)^T&0\end{pmatrix}
$$

Compile the whole adjacency matrix exactly

Provenance: `assumption`. A standard way to do spectral estimation by phase estimation. The value of s is chosen so that s||A||<pi.

Equation assumptions:

- Exact dense unitary synthesis for the tiny instance, not Trotterization

## eq_5: Zero-bin probability

$$
p_0\approx\sum_{\lambda:|\lambda|\lesssim\epsilon}|\langle\psi_\lambda|r\rangle|^2
$$

Approximate probability of reading phase 0 in phase estimation on |r>

Provenance: `standard_background`. Standard phase estimation with finite-precision leakage ignored.

Equation assumptions:

- The smallest nonzero |eigenvalue|·s exceeds the precision

## Registers

- vertex: ceil(log2 |V|) qubits, with a single flat binary index over all vertices (rows first, then columns) qubits; Graph vertex space
- phase: m qubits qubits; Phase estimation register, left unmeasured

## Initial state

Vertex register prepared in |r> by X gates on the bits of the root index, phase register in |0^m>

## Measurement

The phase register is read externally; outcome 0 indicates a zero eigenvector with root support. The returned circuit is measurement-free.

## Classical postprocessing

Compare p_0 against a threshold, which is an assumption. Decode as 1 if p_0 exceeds the threshold.

## Algorithm steps

1. Fix a verified MAJ3 span program and build B(x) and A(x) with a single flat vertex index. Check that the zero-bin probability separates all 8 inputs by classical spectral simulation. (eq_1, eq_2, eq_3)
2. Prepare |r> on the vertex register, and Hadamards on the phase register. (eq_3)
3. Apply controlled U^(2^k) from phase qubit k, where each U is the exact exponential of A. (eq_4)
4. Apply the inverse QFT to the phase register, then read phase 0 externally. (eq_5)

## Assumptions

- Smallest useful construction: one MAJ3 gate on explicit x
- The span program and graph are chosen here and not taken from the abstract
- The adjacency matrix is compiled explicitly, with no black-box or query claim
- The root-overlap rule and the time s are assumptions

## Missing information

- The paper's exact graph construction and weights
- A verified MAJ3 span program (to be checked over all 8 inputs)
- Precision and gap analysis
- Recursive composition for formulas
- Optimality for balanced ternary majority
