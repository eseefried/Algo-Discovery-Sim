# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Relate the entangling power/operator entanglement of a diagonal bipartite unitary U on C^N x C^N to the von Neumann entropy of the auxiliary state rho = A A^dagger / N^2, where A is the N x N reshaping of the diagonal of U, and set up the random-phase (unimodular) ensemble.

Scope: Smallest useful construction: the diagonal gate U = diag(exp(i phi_{jk})) with i.i.d. uniform phases, its reshaped matrix A, and the auxiliary state rho with its entropy, for a tiny instance N=2. The exact moment formulas, the Borel-triangle conjecture, the mean-entropy result, and the Schmidt-strength scaling proofs are outside this scope.

## Symbols

- $N$: local dimension of each subsystem; U has order N^2; domain: integer >= 2
- $U$: diagonal random unitary gate on C^N tensor C^N; domain: N^2 x N^2 unitary
- $\phi_{jk}$: random phase of the diagonal element of U for basis state |j,k>; domain: [0,2\pi)
- $A$: N x N unimodular matrix with A_{jk}=exp(i phi_{jk}), the reshaped diagonal of U; domain: complex N x N matrix
- $\rho$: auxiliary density matrix A A^dagger / N^2; domain: N x N positive semidefinite, trace 1
- $\lambda_i$: eigenvalues of rho, i.e. squared singular values of A divided by N^2; domain: [0,1], sum equals 1
- $S(\rho)$: von Neumann entropy of rho; domain: [0, \ln N]

## eq_1: Diagonal gate and reshaping

$$
U=\sum_{j,k=1}^{N} e^{i\phi_{jk}}\,|j\rangle\langle j|\otimes|k\rangle\langle k|,\quad A_{jk}=e^{i\phi_{jk}}
$$

Diagonal gate with the vector of its N^2 diagonal entries reshaped row-wise into the square matrix A (index (j,k) maps to row j, column k).

Provenance: `abstract_inferred`. The abstract states the reshaping; the explicit index convention is a choice, and unit modulus follows from U being unitary.

Abstract evidence: reshaping the vector of diagonal elements of $U$ of length $N^{2}$ into a square matrix of order $N$

Equation assumptions:

- Row-major reshaping
- Phases i.i.d. uniform for the random ensemble

## eq_2: Auxiliary state

$$
\rho=\frac{A A^{\dagger}}{N^{2}},\quad \mathrm{tr}\,\rho=1
$$

Normalized auxiliary state. Trace is 1 because the sum of |A_{jk}|^2 equals N^2.

Provenance: `abstract_explicit`. Given in the abstract; the trace follows from unimodular entries.

Abstract evidence: $\rho=AA^{\dagger}/N^{2}$

## eq_3: Equal diagonal entries

$$
\rho_{jj}=\frac{1}{N^{2}}\sum_{k}|A_{jk}|^{2}=\frac{1}{N}
$$

Unimodular entries force every diagonal entry of rho to equal 1/N (the 'contradiagonal' property).

Provenance: `abstract_inferred`. Direct computation from |A_{jk}|=1.

Abstract evidence: all their diagonal entries are equal to $1/N$

## eq_4: Von Neumann entropy

$$
S(\rho)=-\mathrm{tr}\,\rho\ln\rho=-\sum_i\lambda_i\ln\lambda_i
$$

Entropy of the auxiliary state, to which the entangling power of U is related.

Provenance: `standard_background`. Standard definition. The exact functional relation between entangling power and S(rho) is not given in the abstract.

## eq_5: Tiny instance N=2

$$
A=\begin{pmatrix}1&e^{i\alpha}\\ e^{i\beta}&e^{i\gamma}\end{pmatrix},\quad \rho=\frac{AA^{\dagger}}{4},\quad \rho_{12}=\frac{1+e^{i(\alpha-\gamma)}\cdot e^{i(\gamma-\beta)}\cdot e^{-i(\alpha-\beta)}\cdot 0+e^{i(\alpha-\beta)}}{4}
$$

N=2 example with a global phase fixed to 1. The off-diagonal element rho_12 = (e^{-i\beta}+e^{i(\alpha-\gamma)})/4 is the correct expression; the printed form is superseded by it.

Provenance: `assumption`. Illustrative instance chosen for a later circuit stage, not from the abstract. The rho_12 expression in the latex is garbled and should be replaced by (e^{-i\beta}+e^{i(\alpha-\gamma)})/4.

Equation assumptions:

- N=2
- Global phase fixed

## Registers

- A_reg: log2 N qubits (1 for N=2) qubits; first subsystem index j
- B_reg: log2 N qubits (1 for N=2) qubits; second subsystem index k

## Classical postprocessing

Compute eigenvalues of rho and S(rho); average over phase samples for ensemble mean.

## Algorithm steps

1. Sample N^2 i.i.d. uniform phases and define the diagonal gate U. (eq_1)
2. Reshape the diagonal into the unimodular matrix A and form rho. (eq_1, eq_2, eq_3)
3. Compute the entropy S(rho) classically as the entanglement-related quantity. (eq_4, eq_5)

## Assumptions

- N=2 tiny instance chosen by me since no scope was given
- Row-major reshaping and i.i.d. uniform phases
- Input state for entangling power not specified in the abstract

## Missing information

- Exact relation between entangling power and S(rho)
- Formulas for the first four moments of squared singular values
- The Borel-triangle conjecture details
- The mean entropy formula
- Schmidt strength definition and proof of log N scaling
- Circuit implementation of the diagonal gate
