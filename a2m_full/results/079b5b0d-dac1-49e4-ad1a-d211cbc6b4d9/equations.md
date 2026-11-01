# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Decide f(x) for a read-once formula over an extended gate set by building a weighted bipartite graph G_P(x) from a span program P for f, then running phase estimation of the walk U=R_B R_A started at the output vertex |r>, and accepting if the phase register reads 0.

Scope: Smallest useful instance (assumed): a single 2-input NAND/AND span program with fixed small explicit edge weights on a few vertices. Build the oracle-dependent walk, run a small phase estimation, and read the all-zero acceptance probability. Out of scope: composition for nested formulas, the balance-condition analysis, optimality proofs, the paper's exact span-program-to-graph weight formulas, the 3-majority and general 2- and 3-bit gate span programs, and the N^0.753 and 2.5^d scaling claims.

## Symbols

- $x\in\{0,1\}^n$: input bits accessed through the oracle; domain: binary strings
- $G_P(x)$: weighted bipartite graph built from span program P and input x; domain: left/right vertex sets A,B
- $W$: witness size (span-program complexity); domain: positive real
- $\mathcal{A}$: normalized weighted adjacency matrix of G_P(x); domain: real symmetric matrix
- $U$: walk unitary R_B R_A; domain: unitary on the vertex/edge register
- $|r\rangle$: output vertex start state; domain: computational basis state
- $\theta$: eigenphase of U; domain: [0,2\pi)
- $\lambda$: eigenvalue of \mathcal{A}; domain: [-1,1]
- $\epsilon$: phase estimation precision; domain: positive real, O(1/\sqrt W)

## eq_1: Oracle

$$
O_x|i,b\rangle=|i,b\oplus x_i\rangle
$$

Coherent query access to the input bits, one query per placement.

Provenance: `standard_background`. Standard query oracle, taken from the sketch rather than the abstract.

Equation assumptions:

- Oracle gives coherent access to x

## eq_2: Zero-eigenvector criterion

$$
f(x)=1\Rightarrow \exists\,|\psi\rangle:\ \mathcal{A}|\psi\rangle=0,\ \langle r|\psi\rangle\neq0;\quad f(x)=0\Rightarrow \operatorname{spec}(\mathcal{A})\cap(-\Delta,\Delta)=\emptyset,\ \Delta\sim1/\sqrt W
$$

A true formula gives a zero-eigenvalue eigenvector of the graph. A false formula gives a spectral gap of order 1/sqrt(W).

Provenance: `abstract_inferred`. The abstract states the zero-eigenvector correspondence. The gap scale and false-case behaviour come from the sketch.

Abstract evidence: A span program's evaluation corresponds to an eigenvalue-zero eigenvector of the associated graph.

Equation assumptions:

- Gap scale 1/sqrt(W) is from the sketch, not the abstract

## eq_3: Walk as two reflections

$$
U=R_B R_A,\quad R_S=2\Pi_S-I
$$

Each reflection is about the span of the stars of the left or right vertices. The x-dependent reflection uses oracle calls to keep or remove input edges.

Provenance: `abstract_inferred`. Spectral estimation of a graph suggests a walk built from two reflections, as in the AND-OR algorithm. The details are recalled, not stated.

Abstract evidence: A quantum computer can therefore evaluate the span program by applying spectral estimation to the graph.

Equation assumptions:

- Star states are normalized using span-program weights
- Szegedy-style walk

## eq_4: Eigenphase relation

$$
U\ \text{has eigenvalues}\ e^{\pm i\theta},\quad \cos\theta=\lambda
$$

Eigenphases of U are the arccos of the eigenvalues of the normalized adjacency matrix. So lambda=0 maps to theta=pi/2 on the plain walk, and the sketch's 'phase 0' needs a convention such as a shifted walk. The sketch states that the zero eigenspace corresponds to phase 0.

Provenance: `standard_background`. Standard spectral relation for a product of two reflections. The mapping of lambda=0 to phase 0 is unresolved.

Equation assumptions:

- Spectrum normalized into [-1,1]
- Convention for lambda=0 versus phase 0 fixed by a shift

## eq_5: Phase estimation acceptance

$$
p_{acc}=\|\Pi^{\epsilon}_{\theta=\theta_0}|r\rangle\|^2,\quad \epsilon=O(1/\sqrt W),\ \text{queries}=O(\sqrt W)
$$

Accept on the all-zero phase outcome, which is the theta_0 outcome under the convention in eq_4. The overlap is large if f=1 and small if f=0.

Provenance: `assumption`. Sketch-level design with precision tied to the gap. The constants are not given.

Equation assumptions:

- Precision set by the known gap
- Constant repetition with majority vote

## Registers

- vertex: ceil(log2|V|) qubits qubits; vertices of G_P(x); starts in |r>
- query: ceil(log2 n)+1 qubits qubits; index and answer bit for O_x; uncomputed after each use
- phase: m qubits, m=O(log W) qubits; phase estimation counter
- ancilla: 1-2 qubits qubits; oracle-controlled edge choice

## Initial state

vertex register in |r>, phase register Hadamards on |0^m>, ancillas |0>

## Measurement

Measure only the phase register. Qiskit is little-endian, so bit i of the counts string is bits[::-1][i]. Accept on the all-zero outcome.

## Classical postprocessing

Majority vote over a constant number of repetitions of the accept/reject outcome.

## Algorithm steps

1. Choose a tiny gate (NAND or AND) and write its span program with explicit vectors and witness size W. This is an assumed instance, and the oracle O_x supplies the input bits for it. (eq_1)
2. Build G_P(x) with weights from the span program vectors. Input edges are kept or removed according to x_i via O_x. A true formula gives a zero-eigenvector and a false one gives a gap. (eq_1, eq_2)
3. Implement U=R_B R_A, with the x-dependent reflection using oracle calls, then uncompute the query register. Fix the phase convention so that the zero eigenspace maps to the accepted phase. (eq_3, eq_4)
4. Run phase estimation with controlled powers of U from |r>, using about sqrt(W) applications of U. (eq_3, eq_5)
5. Measure the phase register and accept on all zeros. Repeat a constant number of times and take a majority vote. (eq_5)

## Assumptions

- Smallest instance chosen: a single gate span program with explicit weights
- Read-once, balanced formula
- Witness sizes known
- Constant-factor error reduction by repetition is allowed
- Phase 0 versus eigenvalue 0 is handled by a convention

## Missing information

- Exact span-program-to-graph weight construction
- Exact composition and balance rule for nested gates
- Precise reflections and the mapping of lambda=0 to phase 0
- Constants for phase estimation precision and acceptance thresholds
- The paper's explicit span programs for 3-majority and general 2- and 3-bit gates
