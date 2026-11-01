# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Specify a coinless (tessellation-based) discrete-time quantum walk on a 1D cycle and its relation to a coined walk; the abstract gives no explicit formulas, so only a minimal background construction is reconstructed.

Scope: One smallest construction: a coinless two-tessellation (staggered) walk on an N-site cycle with N=4 as a tiny instance, with evolution operator U=U1U0 and a probability distribution. Outside scope: the paper-specific transformation to an extended coined walk, the specific family of evolution operators, asymptotic features, mixing time and limiting distributions on cycles, and the search-algorithm efficiency claims.

## Symbols

- $N$: Number of sites on the cycle (N even); domain: even integer, N=4 in the tiny instance
- $|x\rangle$: Site basis state; domain: x in Z_N
- $\alpha_k$: Polygon (cell) state of tessellation k, uniform superposition of sites in the cell; domain: normalized vectors in C^N
- $U_0, U_1$: Reflection operators for the two tessellations; domain: unitary N x N
- $U$: One-step evolution operator; domain: unitary N x N
- $P_t(x)$: Probability of site x after t steps; domain: [0,1]

## eq_1: Tessellation reflection

$$
U_k = 2\sum_{j}|\alpha^{(k)}_j\rangle\langle\alpha^{(k)}_j| - I,\quad k\in\{0,1\}
$$

Each tessellation k has cells (edges on the cycle) j; U_k reflects about the span of cell states.

Provenance: `standard_background`. Standard form of staggered quantum walk operators from lattice tessellations; the abstract only mentions a graphical tessellation method.

Equation assumptions:

- Cells within a tessellation are disjoint and cover all sites

## eq_2: Cell states on cycle

$$
|\alpha^{(0)}_j\rangle=\tfrac{1}{\sqrt2}(|2j\rangle+|2j+1\rangle),\quad |\alpha^{(1)}_j\rangle=\tfrac{1}{\sqrt2}(|2j+1\rangle+|2j+2\rangle),\quad j\in Z_{N/2}
$$

Two edge tessellations of the cycle, with indices mod N.

Provenance: `assumption`. Chosen as a simple example tessellation; the paper's specific examples are not known.

Equation assumptions:

- Cell size 2 with uniform amplitudes
- Site indices taken mod N

## eq_3: Evolution

$$
|\psi_t\rangle = U^t|\psi_0\rangle,\quad U=U_1U_0
$$

Discrete-time coinless evolution on the site basis only.

Provenance: `standard_background`. Standard staggered walk evolution; the abstract states only that the walk is coinless and discrete-time.

Equation assumptions:

- Order U_1U_0 is a convention

## eq_4: Site distribution

$$
P_t(x)=|\langle x|\psi_t\rangle|^2,\quad \sum_{x\in Z_N}P_t(x)=1
$$

Measurement distribution in the site basis.

Provenance: `standard_background`. Born rule.

## eq_5: Hilbert space dimension comparison

$$
\dim\mathcal H_{\text{coinless}}=N,\quad \dim\mathcal H_{\text{coined}}=N\cdot d_c
$$

Coined walk uses site basis tensor coin space of dimension d_c; coinless uses only the site basis.

Provenance: `abstract_inferred`. Dimension counts follow from the tensor-product vs. site-only description; d_c is not specified in the abstract.

Abstract evidence: Coined walks require the direct product of the site basis with the coin space, coinless walks operate purely in the site basis

Equation assumptions:

- d_c is the coin space dimension, e.g. 2 in 1D

## Registers

- site: 2 qubits for N=4 (log2 N in general) qubits; Encodes site x in binary, |x> with x=0..N-1

## Initial state

Assumed |\psi_0\rangle=|0\rangle on the site register (localized at site 0).

## Measurement

Computational basis measurement of the site register, repeated to estimate P_t(x).

## Classical postprocessing

Histogram of outcomes to estimate P_t(x); mixing time analysis not specified in scope.

## Algorithm steps

1. Prepare the site register in |0>. (eq_2)
2. Apply U_0 (reflection about tessellation-0 cells). (eq_1, eq_2)
3. Apply U_1 (reflection about tessellation-1 cells); repeat the pair t times. (eq_1, eq_3)
4. Measure the site register to estimate P_t(x). (eq_4)

## Assumptions

- Chosen smallest construction: two-tessellation staggered walk on a cycle with N=4
- The tessellation is an assumed example, not taken from the paper
- Initial state localized at site 0

## Missing information

- The specific family of evolution operators for which the coinless-to-coined mapping holds
- The explicit transformation to the extended coined walk
- Definitions of mixing time and limiting distribution used in the paper
- Specific tessellation examples and asymptotic results
- Search algorithm details
