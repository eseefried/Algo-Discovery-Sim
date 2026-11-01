# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Evaluate formulas over an extended gate set (all 2- and 3-bit binary gates, e.g. NAND, 3-majority) with a quantum algorithm, by mapping span programs to weighted bipartite graphs so that span program evaluation corresponds to an eigenvalue-zero eigenvector of the graph, and applying spectral estimation.

Scope: Abstract-level reconstruction of the span-program-to-graph correspondence and the spectral-estimation evaluation idea; circuit details, weights, and complexity proofs are not reconstructed.

## Symbols

- $P$: span program computing a Boolean function; domain: classical linear-algebraic model
- $G_P$: weighted bipartite graph associated with P; domain: weighted bipartite graph
- $x$: input bit string to the formula; domain: {0,1}^n
- $f$: formula value; domain: {0,1}
- $A_{G}$: weighted adjacency operator of the graph; domain: Hermitian operator

## eq_1: Span program evaluation as zero eigenvector

$$
f(x)=1 \iff A_{G_P(x)}\,|\psi\rangle=0 \text{ for some nonzero } |\psi\rangle \text{ supported near the output vertex}
$$

Schematic statement that evaluation corresponds to an eigenvalue-zero eigenvector of the graph; the exact support condition is an assumption.

Provenance: `abstract_inferred`. Schematic formalization of the abstract sentence; precise condition not given.

Abstract evidence: A span program's evaluation corresponds to an eigenvalue-zero eigenvector of the associated graph.

Equation assumptions:

- Support condition and the 0/1 direction convention are assumed

## eq_2: Spectral estimation

$$
U=e^{iA_G t},\quad \text{phase estimation of } U \text{ distinguishes eigenvalue } 0 \text{ from gap } \ge \Delta
$$

Spectral estimation applied to the graph operator via phase estimation of a unitary built from it.

Provenance: `standard_background`. Standard way to realize spectral estimation; the abstract only names it.

Equation assumptions:

- Spectral gap Delta around zero in the relevant case

## Registers

- vertex: ceil(log2 |V(G_P)|) qubits (symbolic) qubits; Position register: basis states are graph vertices, the space on which A_G acts
- phase: m qubits, m ~ log(1/Delta) (symbolic) qubits; Ancilla register holding the phase estimation output for the eigenvalue of A_G

## Initial state

Vertex register in the basis state of a designated input/output vertex of G_P(x); phase register in |0>^m.

## Measurement

Measure the phase register in the computational basis. Outcome 0 (eigenvalue within the estimation precision of zero) indicates the zero-eigenvector overlap, i.e. f(x)=1 under the assumed convention; a nonzero outcome indicates f(x)=0.

## Classical postprocessing

Repeat the run a constant number of times and take a majority vote on whether the phase outcome is within the threshold of zero. Threshold and precision are assumed to be of order Delta; output the Boolean f(x) accordingly.

## Algorithm steps

1. Build the graph G_P(x) from the span program and input x, with oracle queries to x determining which edges are present. (eq_1)
2. Prepare the vertex register at the designated vertex and apply Hadamards to the phase register. (no equation reference)
3. Apply controlled powers of U=e^{iA_G t} (implemented by a Hamiltonian simulation or walk) from the phase register onto the vertex register, then the inverse QFT. (eq_2)

## Assumptions

- Equations are schematic, not the paper's exact construction
- Phase estimation is used as the spectral estimation method
- Initial vertex and register sizes are assumed, not given in the abstract
- Initial state is the designated input vertex of the graph; register sizes are symbolic
- Measurement is a phase-register readout with a zero-vs-nonzero threshold, and the 0/1 convention is assumed

## Missing information

- Graph weights from span program
- Gate-specific span programs
- Complexity bounds
- Exact graph construction and weights
- Success threshold and precision are not specified in the abstract
- Exact initial state and Hamiltonian simulation implementation are not stated in the abstract
- Paper's actual measurement and postprocessing are not given in the abstract
