# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximate combinatorial optimization (MaxCut on regular graphs) with a depth-p parameterized quantum circuit built from gates whose locality is at most that of the objective function. This is the QAOA setting.

Scope: Smallest useful construction: p=1 circuit for MaxCut on a tiny explicit instance (assumed 3-vertex triangle... to keep it simple, 4-vertex cycle C4, 2-regular). Only the standard QAOA ansatz and the objective are given. Outside scope: the 0.6924 ratio derivation for 3-regular graphs, general-p analysis, classical parameter preprocessing, the strategy for p growing with input size, and the 2-regular analysis.

## Symbols

- $p$: number of circuit layers (integer); domain: p \geq 1
- $n$: number of vertices/qubits; domain: positive integer; n=4 in the assumed instance
- $C(z)$: MaxCut objective, the number of cut edges; domain: z \in \{0,1\}^n, integer values
- $E$: edge set of graph G; domain: subset of unordered vertex pairs
- $\gamma_k,\beta_k$: layer-k angles; domain: real numbers, k=1..p
- $B$: mixer operator, sum of Pauli X; domain: Hermitian operator on n qubits
- $C_{jk}$: edge term (1 - Z_j Z_k)/2; domain: operator, eigenvalues 0 or 1

## eq_1: MaxCut objective

$$
C(z)=\sum_{(j,k)\in E}\frac{1-z_j z_k}{2},\quad z_j\in\{+1,-1\}
$$

Cut size as a sum of 2-local clauses, one per edge.

Provenance: `standard_background`. Standard MaxCut definition; the abstract only names MaxCut and says gate locality is at most that of the objective.

Equation assumptions:

- Unweighted graph

## eq_2: Phase and mixer operators

$$
U(C,\gamma)=e^{-i\gamma C}=\prod_{(j,k)\in E}e^{-i\gamma C_{jk}},\quad U(B,\beta)=e^{-i\beta B}=\prod_{j=1}^n e^{-i\beta X_j}
$$

Layer unitaries. Each factor acts on at most the locality of the objective clauses (2 qubits for MaxCut), consistent with the abstract's locality claim.

Provenance: `standard_background`. Standard QAOA construction recalled from background. The abstract does not state these forms or the exact gate set.

Equation assumptions:

- The paper's algorithm is the standard QAOA ansatz

## eq_3: Depth-p state

$$
|\boldsymbol{\gamma},\boldsymbol{\beta}\rangle=U(B,\beta_p)U(C,\gamma_p)\cdots U(B,\beta_1)U(C,\gamma_1)|+\rangle^{\otimes n}
$$

Variational state with 2p angles.

Provenance: `abstract_inferred`. The abstract says the algorithm depends on p and the circuit depth grows linearly in p times the number of constraints, which is consistent with p repeated layers of clause-wise gates. The exact ansatz is background.

Abstract evidence: The algorithm depends on an integer $p\geq 1$

Equation assumptions:

- Initial state is the uniform superposition

## eq_4: Expected objective

$$
F_p(\boldsymbol{\gamma},\boldsymbol{\beta})=\langle\boldsymbol{\gamma},\boldsymbol{\beta}|C|\boldsymbol{\gamma},\boldsymbol{\beta}\rangle,\quad \max_{\gamma,\beta}F_p\ \text{is used to choose angles}
$$

Quantity to optimize classically over angles.

Provenance: `standard_background`. Standard QAOA objective. The abstract mentions classical preprocessing for fixed p, which is presumably angle selection, but this is not stated.

Equation assumptions:

- Angle selection by maximizing F_p

## eq_5: Approximation guarantee form

$$
\frac{C(z)}{C_{\max}}\geq 0.6924\quad (p=1,\ \text{3-regular graphs})
$$

The quoted guarantee, applying to the cut found by the algorithm.

Provenance: `abstract_explicit`. Directly stated in the abstract; the derivation is not reconstructed.

Abstract evidence: For $p=1$, on 3-regular graphs the quantum algorithm always finds a cut that is at least 0.6924 times the size of the optimal cut.

## Registers

- q: n (assumed n=4 for the C4 instance) qubits; one qubit per vertex; bit z_j encodes the side of the cut for vertex j, with qubit j labelled by vertex j

## Initial state

|+>^{\otimes n} (assumption from the standard ansatz)

## Measurement

Measure all qubits in the computational basis and keep the best cut found over repeated shots (assumed).

## Classical postprocessing

Evaluate C(z) classically for each sampled bitstring and return the largest. Angle optimization is as in eq_4 (assumed).

## Algorithm steps

1. Prepare the uniform superposition on all qubits using Hadamard gates. (eq_3)
2. For layer k=1..p apply the phase operator, i.e. a two-qubit ZZ-rotation for each edge with angle gamma_k, then the mixer, i.e. a single-qubit X-rotation per qubit with angle beta_k. (eq_2, eq_3)
3. Choose angles by classical optimization of the expected cut (assumed form of the classical preprocessing). (eq_4)

## Assumptions

- Algorithm taken to be the standard QAOA ansatz; the abstract does not give the explicit circuit.
- Tiny instance chosen: p=1 on the 4-cycle C4 (2-regular) as an illustration.
- The abstract's strategy for p growing with input size and its preprocessing details are not reconstructed.

## Missing information

- Explicit gate decomposition and parameter schedule
- The classical preprocessing procedure for fixed p
- The strategy for p growing with input size
- Derivation of the 0.6924 bound and the 2-regular analysis
