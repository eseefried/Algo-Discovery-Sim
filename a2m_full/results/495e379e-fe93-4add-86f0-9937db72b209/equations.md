# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

For a diagonal unitary U=sum_{jk} exp(i phi_jk)|jk><jk| on two n-qubit registers (N=2^n), prepare |psi>=U(H^{\otimes 2n}|0>) and obtain the von Neumann entropy S(rho) of rho=AA^dagger/N^2, where A is the N x N unimodular matrix of phases. This entropy is the entanglement of |psi> and is related to the entangling power and operator Schmidt strength of U. Then average over random phase draws.

Scope: Tiny instance n=2 (4 qubits, no ancillas) with i.i.d. uniform phases, statevector simulation, no measurements. Entropy is computed classically from the reshaped amplitude matrix. The swap-test purity estimate (4n+1 qubits) is an optional extension. Analytic moment derivations, the Borel triangle conjecture, and the exact mean entropy formula are outside the scope; they appear only as classical comparison targets that are not specified here.

## Symbols

- $N$: Dimension of each register, N=2^n; domain: power of two, N=4 for the tiny instance
- $\phi_{jk}$: Random phase of diagonal entry (j,k); domain: i.i.d. uniform on [0,2\pi)
- $A$: N x N matrix with A_{jk}=e^{i\phi_{jk}}, reshaped diagonal of U; domain: complex unimodular matrices
- $\rho$: Auxiliary state AA^\dagger/N^2, equal to the reduced state of A in |\psi>; domain: density matrices of dimension N, trace 1
- $\lambda_i$: Eigenvalues of rho, i.e. squared singular values of A/N; domain: [0,1], sum to 1
- $S$: Von Neumann entropy of rho; domain: [0, log N]

## eq_1: Diagonal gate

$$
U=\sum_{j,k=0}^{N-1} e^{i\phi_{jk}}|j\rangle\langle j|\otimes|k\rangle\langle k|
$$

Random-phase diagonal gate on registers A and B. The N^2 diagonal entries reshape into the matrix A.

Provenance: `abstract_inferred`. The abstract describes diagonal random unitaries of order N^2 with random phases, so the diagonal entries are unit-modulus phases.

Abstract evidence: reshaping the vector of diagonal elements of $U$ of length $N^{2}$ into a square matrix of order $N$

Equation assumptions:

- phases i.i.d. uniform

## eq_2: Prepared state

$$
|\psi\rangle=U(H^{\otimes 2n}|0\rangle)=\frac1N\sum_{j,k}e^{i\phi_{jk}}|j\rangle|k\rangle
$$

Applying U to |+>^{2n} gives a pure bipartite state whose coefficient matrix is A/N.

Provenance: `assumption`. Proposed construction from the sketch. It is a direct calculation, not a statement in the abstract.

Equation assumptions:

- register A holds j, register B holds k
- Qiskit little-endian: A qubits are the low n qubits unless reordered
- reshape index = j*N+k with j the A index

## eq_3: Reduced state

$$
\rho=\frac{AA^{\dagger}}{N^{2}},\quad \rho_{jj}=\frac1N
$$

The reduced state on A has all diagonal entries equal to 1/N. This is the contradiagonal property.

Provenance: `abstract_explicit`. The abstract states the form of rho and that its diagonal entries are all 1/N. The diagonal value follows from unimodularity: (AA^\dagger)_{jj}=N.

Abstract evidence: auxiliary quantum state $\rho=AA^{\dagger}/N^{2}$

## eq_4: Entropy readout

$$
S(\rho)=-\sum_i\lambda_i\ln\lambda_i,\quad \{\lambda_i\}=\mathrm{sv}(A/N)^2
$$

The entanglement of |psi> and the entropy relevant to the entangling power of U are read from the singular values of the reshaped statevector matrix.

Provenance: `abstract_inferred`. The abstract relates entangling power to S(rho). The exact proportionality constant is not given, so only S is computed.

Abstract evidence: Entangling power of a diagonal gate $U$ is related to the von Neumann entropy of an auxiliary quantum state

Equation assumptions:

- natural logarithm

## eq_5: Purity and moment

$$
\mathrm{Tr}\rho^2=\sum_i\lambda_i^2
$$

The purity is the second moment of the squared singular values. It can be estimated with a swap test on two copies, and is a classical check from the statevector.

Provenance: `standard_background`. Standard definition. The abstract mentions moments but does not give formulas for them.

## eq_6: Ensemble mean

$$
\bar S=\frac1M\sum_{m=1}^{M}S(\rho^{(m)})
$$

Monte Carlo mean entropy over M independent phase draws. It is compared with the analytic prediction, which is not specified here.

Provenance: `assumption`. A numerical estimator, not given in the abstract.

Equation assumptions:

- M chosen by the runner

## Registers

- A: n qubits (2 for the tiny instance) qubits; first subsystem, index j
- B: n qubits (2 for the tiny instance) qubits; second subsystem, index k
- anc: 0 (optional n for a copy of B; 4n+1 total for a two-copy swap test) qubits; optional, only for the swap-test extension

## Initial state

|0>^{2n}

## Measurement

None for the statevector route. The swap-test extension would measure one ancilla.

## Classical postprocessing

Reshape the statevector into a matrix M with M[j,k]=amplitude of index k*N+j under Qiskit's little-endian ordering with A on the low qubits. Use the SVD, set lambda_i to the squared singular values, and compute S, Tr rho^2, and the average over draws.

## Algorithm steps

1. Sample N^2 phases uniformly from [0,2pi). (eq_1)
2. Apply H to every qubit of A and B. (eq_2)
3. Apply the diagonal gate with the sampled phases, built from standard gates (e.g. Qiskit Diagonal or phase and controlled-phase gates), with no black box and no measurements. (eq_1, eq_2)
4. Read the statevector and reshape it into an N x N matrix, then compute the singular values and S. Optionally check purity. (eq_3, eq_4, eq_5)
5. Repeat over many draws and average. (eq_6)

## Assumptions

- Smallest construction: n=2, 4 qubits.
- Phases i.i.d. uniform.
- The statevector is read directly.
- Natural log is used for entropy.
- Moment and Borel triangle predictions are for classical comparison only.

## Missing information

- Exact formulas for the first four moments and the Borel triangle connection are not in the abstract.
- The exact mean entropy formula is not in the abstract.
- The proportionality between entangling power and S is not given.
- Schmidt strength scaling constants are not given.
