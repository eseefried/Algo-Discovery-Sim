# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Evaluate a Boolean formula over an extended gate set (e.g. NAND, 3-majority) by encoding each gate as a span program, mapping it to a weighted bipartite graph, and using spectral estimation to detect an eigenvalue-zero eigenvector.

Scope: Scope: one tiny instance, a single 3-majority gate (a depth-1 formula) as a span program, with its associated bipartite graph and the eigenvalue-zero phase-estimation test. Out of scope: the full recursive formula-evaluation algorithm, the balance conditions, optimality and complexity proofs, the specific weights and graph construction for general gates, and the ternary majority tree analysis.

## Symbols

- $x$: input bit string to the gate; domain: x in {0,1}^3
- $f$: Boolean function computed by the gate; domain: f: {0,1}^3 -> {0,1}
- $P$: span program for f; domain: set of input vectors and a target vector in a vector space
- $t$: target vector of the span program; domain: nonzero vector in C^d
- $v_j$: span program input vectors indexed by literals; domain: vectors in C^d
- $G$: weighted bipartite graph associated with P; domain: graph with edge weights
- $A_G$: weighted adjacency (Hermitian) operator of G; domain: Hermitian matrix
- $\epsilon$: precision of spectral estimation; domain: positive real

## eq_1: 3-majority gate

$$
\mathrm{MAJ}_3(x_1,x_2,x_3)=1 \iff x_1+x_2+x_3\ge 2
$$

Definition of the example gate function.

Provenance: `standard_background`. Standard definition of 3-majority, named in the abstract.

## eq_2: Span program evaluation condition

$$
f(x)=1 \iff t \in \mathrm{span}\{v_j : \text{literal } j \text{ is satisfied by } x\}
$$

Generic span program acceptance rule: accept iff the target lies in the span of the vectors of satisfied literals.

Provenance: `standard_background`. Standard span-program definition recalled from background; the abstract only says span programs are a linear-algebraic model of computation.

Equation assumptions:

- Standard Karchmer-Wigderson-style definition; the paper's variant may differ

## eq_3: Evaluation as eigenvalue-zero eigenvector

$$
f(x)=1 \Leftrightarrow \exists\, \psi\neq 0 \text{ with } A_{G(x)}\psi=0
$$

The evaluation of the span program corresponds to an eigenvalue-zero eigenvector of the associated graph (precise eigenvector structure not specified here).

Provenance: `abstract_inferred`. Inferred loosely from the quoted claim; the abstract does not specify which outcome corresponds to the zero eigenvector, nor the exact eigenvector requirement, so the direction of the equivalence is an assumption.

Abstract evidence: A span program's evaluation corresponds to an eigenvalue-zero eigenvector of the associated graph.

Equation assumptions:

- Zero-eigenvector existence (suitably restricted to an input-dependent subspace) corresponds to one function value
- Exact graph construction is unspecified

## eq_4: Spectral estimation test

$$
\text{phase estimation of } e^{iA_G} \text{ to precision } \epsilon:\ |\lambda|<\epsilon \Rightarrow \text{declare eigenvalue }0
$$

Decide zero versus nonzero eigenvalue by estimating the spectrum of A_G, using a unitary such as exp(i A_G).

Provenance: `abstract_inferred`. Spectral estimation is named; the use of e^{iA_G} and the threshold rule are standard phase-estimation choices, not stated in the abstract.

Abstract evidence: A quantum computer can therefore evaluate the span program by applying spectral estimation to the graph.

Equation assumptions:

- Access to a method to implement e^{iA_G} or a similar unitary
- Threshold epsilon chosen below the gap of nonzero eigenvalues

## Registers

- graph: |V(G)| basis states (symbolic) qubits; Vertex register on which A_G acts; basis states are graph vertices
- phase: O(log(1/\epsilon)) qubits (symbolic) qubits; Phase-estimation ancilla register

## Initial state

Assumed: a fixed start state on a designated vertex of G (e.g. the root/output vertex) in the graph register, with phase register in |0>.

## Measurement

Measure the phase register; outcome near zero indicates overlap with the eigenvalue-zero eigenspace.

## Classical postprocessing

Threshold the measured phase against epsilon to output the Boolean value; repeat to amplify success probability (assumed).

## Algorithm steps

1. Choose the span program for the gate and build the bipartite graph G(x) with input-dependent structure. (eq_1, eq_2)
2. Prepare the start state on the graph register and apply phase estimation of a unitary derived from A_G. (eq_4)
3. Interpret a phase near zero as evidence for the zero-eigenvalue case that corresponds to the evaluation outcome. (eq_3, eq_4)

## Assumptions

- The 3-majority single gate is chosen as the smallest useful instance.
- Standard span program definition is used, not necessarily the paper's.
- Graph weights and eigenvector structure are unspecified and left abstract.

## Missing information

- Explicit span program for MAJ_3 and its weights
- Exact span-program-to-graph correspondence
- How the start state and zero-eigenvector relate to the function output
- Recursive composition for formulas and the balance condition
- Complexity and optimality results
