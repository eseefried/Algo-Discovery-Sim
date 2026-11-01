# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Additive approximation of the Ising partition function Z = sum_s exp(sum J_ij s_i s_j + sum h_i s_i) on a square lattice, via the overlap mapping (Van den Nest, Dür, Briegel) and its MBQC interpretation.

Scope: Smallest useful construction: the standard overlap-mapping identity expressing Z as an inner product between a product state and a graph (cluster) state on a tiny 2x2 square lattice, plus the Hadamard-test style estimation of that overlap. Out of scope: the specific algorithmic domain, the approximation scale, the BQP-completeness proof, the extension to real parameters and the explicit scale calculation, the exponential improvement over constant-depth algorithms, and the hardness of multiplicative approximation.

## Symbols

- $G=(V,E)$: square lattice graph; domain: 2x2 lattice, |V|=4 (assumed instance)
- $s_i$: Ising spin; domain: {+1,-1}
- $J_{ij}$: coupling strength; domain: complex in general (abstract); real in the physical region
- $h_i$: magnetic field; domain: complex in general; real in the physical region
- $Z$: partition function; domain: complex number
- $|G\rangle$: graph state on G; domain: n-qubit state
- $|\alpha\rangle$: product state encoding J and h; domain: n-qubit (possibly unnormalized) product state
- $n$: number of spins/qubits; domain: positive integer

## eq_1: Ising partition function

$$
Z=\sum_{s\in\{\pm1\}^n}\exp\Big(\sum_{(i,j)\in E}J_{ij}s_is_j+\sum_{i}h_is_i\Big)
$$

Partition function with the inverse temperature absorbed into J and h.

Provenance: `standard_background`. Standard definition of the Ising partition function; the abstract states only that Z is the quantity to be approximated.

Equation assumptions:

- Inverse temperature absorbed into J and h
- Sign convention chosen here

## eq_2: Graph state

$$
|G\rangle=\prod_{(i,j)\in E}CZ_{ij}\,|+\rangle^{\otimes n}
$$

Graph state on the lattice used in the overlap mapping.

Provenance: `standard_background`. Standard definition of graph states; the abstract mentions the overlap mapping and MBQC but gives no formulas.

Equation assumptions:

- The graph state is built on the lattice or a related graph

## eq_3: Overlap form of Z

$$
Z=c\,\langle\alpha|G\rangle,\quad |\alpha\rangle=\bigotimes_i|\alpha_i(J,h)\rangle
$$

Z is proportional to the overlap of a product state with a graph state. The exact single-qubit states and the constant c are not reconstructed here.

Provenance: `abstract_inferred`. The overlap mapping is named in the abstract, which implies that Z is an overlap between states. The detailed form is from background knowledge of that work and is not verified; the lattice used for the graph state may differ from the Ising lattice.

Abstract evidence: we utilize the overlap mapping developed by Van den Nest, Dür, and Briegel

Equation assumptions:

- Details of |\alpha_i\rangle and c are left unspecified

## eq_4: Hadamard-test estimate

$$
\Pr[0]=\tfrac12\big(1+\mathrm{Re}\,\langle\psi|U|\psi\rangle\big),\quad \Pr[0]=\tfrac12\big(1+\mathrm{Im}\,\langle\psi|U|\psi\rangle\big)\ \text{with an extra }S^\dagger\text{ on the ancilla}
$$

Generic way to estimate the real and imaginary parts of an overlap with additive error. This is not claimed to be the paper's MBQC-based procedure.

Provenance: `standard_background`. Generic overlap-estimation primitive, used as a placeholder because the abstract does not give the actual algorithm.

Equation assumptions:

- The overlap is expressed as an amplitude of a unitary circuit

## Registers

- spin/qubit register: n=4 (assumed 2x2 instance) qubits; One qubit per lattice site, holding the graph state or MBQC resource state
- ancilla: 1 qubits; Hadamard-test control qubit (assumed)

## Initial state

|0\rangle_{anc}|+\rangle^{\otimes n}, assumed for the graph-state preparation

## Measurement

Ancilla measured in the Z basis for the Hadamard test, a generic assumption; the paper's MBQC measurement pattern is not specified in the abstract.

## Classical postprocessing

Rescale the estimated overlap by the constant c to give an additive approximation of Z. The error scale is not specified.

## Algorithm steps

1. Define the instance (2x2 lattice with chosen J_ij, h_i) and write Z as in eq_1. (eq_1)
2. Map Z to the overlap of a product state with a graph state. (eq_2, eq_3)
3. Estimate the overlap with additive error, either through the MBQC interpretation or, as a stand-in, a Hadamard test. (eq_4)

## Assumptions

- No scope was given, so a tiny 2x2 lattice instance was chosen.
- The overlap mapping details are recalled from background and not verified.
- The Hadamard test replaces the paper's MBQC-based procedure as a placeholder.

## Missing information

- Exact algorithmic domain
- Explicit approximation scale for complex and real parameters
- Concrete product-state definitions and the constant c
- MBQC measurement pattern and its depth
- BQP-completeness construction
- Comparison with the constant-depth algorithm
