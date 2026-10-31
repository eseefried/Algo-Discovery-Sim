# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Characterize nonlocal properties (Schmidt strength, entangling power) of random diagonal unitary gates of order N^2, by relating entangling power to the von Neumann entropy of the auxiliary state rho = A A^dagger / N^2, where A is the N x N reshaping of the diagonal vector of U. Study the ensemble of unimodular random-phase matrices A and the resulting random-phase density matrices, including moments of squared singular values and mean entropy.

Scope: Theoretical random-matrix and entanglement analysis from the abstract only; no explicit circuit or measurement protocol is given. A small finite instance (e.g. N=2) may be used for illustration. The numerical pipeline below is an assumed illustration, not the paper's method.

## Symbols

- $N$: Dimension of each subsystem; gate acts on N^2-dimensional space; domain: positive integer
- $U$: Diagonal unitary gate with random phases; domain: N^2 x N^2 unitary
- $A$: Unimodular matrix obtained by reshaping the diagonal of U into an N x N matrix; domain: complex N x N, |A_ij|=1
- $\rho$: Auxiliary density matrix A A^\dagger / N^2; domain: N x N positive semidefinite, trace 1

## eq_1: Auxiliary state

$$
\rho = \frac{A A^{\dagger}}{N^{2}}
$$

Auxiliary quantum state built from the reshaped diagonal of U

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: \rho=AA^{\dagger}/N^{2}

## eq_2: Unimodular entries and diagonal of rho

$$
|A_{ij}|=1,\quad \rho_{ii}=\frac{1}{N}
$$

All entries of A have modulus 1 with random phases, so rho has diagonal entries 1/N and trace 1

Provenance: `abstract_inferred`. Diagonal equal to 1/N is stated; unimodularity follows from the abstract's description of A.

Abstract evidence: all their diagonal entries are equal to $1/N$

## eq_3: Entropy of rho

$$
S(\rho)=-\mathrm{Tr}\,\rho\ln\rho
$$

Von Neumann entropy, which is related to the entangling power of U and gives the entanglement of the associated bipartite pure state

Provenance: `standard_background`. Standard definition; abstract only names the von Neumann entropy.

## Registers

- classical_phases: N^2 real phases qubits; Random phases phi_k defining diagonal entries exp(i phi_k) of U (classical sampling)
- A_matrix: N x N classical complex array qubits; Reshaped diagonal vector of U, used to form rho
- sys_AB: 2 log2 N qubits (illustrative; N a power of 2) qubits; Optional two-subsystem register on which diagonal U acts; state with coefficient matrix A/N would be the associated bipartite pure state

## Initial state

Classical: sample N^2 independent uniform phases. Optional quantum illustration: bipartite pure state with coefficient matrix A/N (an assumed reading of 'corresponding bipartite pure states').

## Measurement

Numerical (classical) readout, no physical quantum measurement protocol is given in the abstract. For each sampled instance, record the eigenvalues of rho and its diagonal entries as a consistency check. Hardware entropy estimation of the associated pure state would need tomography, which is an assumption.

## Classical postprocessing

Compute eigenvalues of rho (squared singular values of A/N), check they sum to 1, evaluate S(rho) per sample, and average over samples for several N. Estimate the first four empirical moments (averages of Tr rho^k, k=1..4) to compare with the conjectured Borel-triangle connection once its formula is available. Relating mean S to entangling power and Schmidt strength (log N vs log N^2) requires formulas not given in the abstract.

## Algorithm steps

1. Sample N^2 independent uniform phases and form the diagonal of U with entries exp(i phi_k). (eq_2)
2. Reshape the diagonal vector into the N x N unimodular matrix A. (eq_2)
3. Form rho = A A^dagger / N^2; its diagonal should equal 1/N (consistency check). (eq_1, eq_2)
4. Compute eigenvalues of rho and its von Neumann entropy; average over the ensemble. (eq_3)

## Assumptions

- Exact formula relating entangling power to S(rho) is not given in the abstract.
- The circuit plan is an assumed classical/numerical pipeline, not a protocol from the paper.
- N is a power of 2 for the illustrative qubit encoding.
- Measurement is a classical numerical readout, not a protocol from the paper.
- Hardware entropy estimation of the associated pure state would need tomography; this is an assumption.
- Unimodularity in eq_2 is inferred from the abstract's description of A.

## Missing information

- Exact entangling power formula
- Explicit moment values and the Borel triangle formula
- Paper's own circuit and measurement protocol (none given in abstract)
- Exact normalization of the moments of squared singular values used for comparison
- Exact closed-form mean entropy result
- Definition/formula for the average Schmidt strength
