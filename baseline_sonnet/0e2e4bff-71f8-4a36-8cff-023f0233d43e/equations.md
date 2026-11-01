# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Trotterized quantum simulation of a molecular electronic-structure Hamiltonian in second quantization, with gate-count scaling in the number of spin orbitals N determined by the Trotter step size needed for a target error. The abstract gives scaling claims but no Hamiltonian, error bound, or algorithm details.

Scope: One minimal construction: a first-order Trotter-Suzuki product formula for a generic second-quantized molecular Hamiltonian, with the gate-count scaling relations quoted in the abstract. A tiny explicit instance is not fixed. The paper's alternative simulation scheme, the coalescing scheme with term-dependent Trotter steps, and the efficient classical complexity-bounding method are outside scope.

## Symbols

- $N$: number of spin orbitals (= qubits under Jordan-Wigner); domain: positive integer
- $h_{pq}, h_{pqrs}$: one- and two-electron integrals; domain: real (or complex) coefficients
- $a_p^\dagger, a_p$: fermionic creation/annihilation operators; domain: operators on N-mode Fock space
- $H=\sum_j H_j$: Hamiltonian decomposed into terms; domain: Hermitian operators
- $t$: total evolution time; domain: real, positive
- $r$: number of Trotter steps; domain: positive integer
- $\epsilon$: target simulation error; domain: positive real
- $G$: total gate count; domain: positive integer

## eq_1: Molecular Hamiltonian

$$
H=\sum_{p,q}h_{pq}a_p^\dagger a_q+\tfrac12\sum_{p,q,r,s}h_{pqrs}a_p^\dagger a_q^\dagger a_r a_s
$$

Generic second-quantized electronic Hamiltonian in a basis of N spin orbitals, with O(N^4) terms.

Provenance: `standard_background`. Standard form for molecular simulation; the abstract does not state the Hamiltonian.

Equation assumptions:

- Born-Oppenheimer, fixed nuclei, finite basis

## eq_2: First-order Trotter formula

$$
e^{-iHt}\approx\left(\prod_{j}e^{-iH_jt/r}\right)^{r}
$$

Product formula approximating time evolution with r steps; error depends on commutators of the H_j.

Provenance: `standard_background`. Abstract refers to Trotter steps, but not the specific order or ordering used.

Equation assumptions:

- First-order formula chosen as the smallest construction
- Term ordering unspecified

## eq_3: Gate count from Trotter steps

$$
G\approx r\,G_{\text{step}}(N),\qquad r=r(N,\epsilon,t)
$$

Total gates equal the number of Trotter steps times the per-step cost; the required r grows with N for fixed accuracy.

Provenance: `abstract_inferred`. Inferred from the abstract linking gate count to the Trotter step analysis; the decomposition into r and G_step is a standard assumption.

Abstract evidence: the complexity in gate count of such simulations increases with the number of spin orbitals $N$

Equation assumptions:

- G_step is the cost of one product-formula step

## eq_4: Previously reported worst-case scaling

$$
G=O(N^{8})
$$

Gate-count scaling reported by the earlier studies on random artificial molecules.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: increases with the number of spin orbitals $N$ as $N^{8}$

Equation assumptions:

- Applies to the cited random-ensemble analysis

## eq_5: Revised worst-case scaling for model molecules

$$
G=O(N^{6})\ \text{(worst case, model molecules)}
$$

Empirical scaling found for the real model molecules studied; the actual scaling may be better.

Provenance: `abstract_explicit`. Stated in the abstract as an approximate empirical scaling, not an exact law.

Abstract evidence: the scaling is closer to $N^{6}$ in worst case for real model molecules we have studied

Equation assumptions:

- Approximate exponent; specific molecules not given

## Registers

- system: N qubits; one qubit per spin orbital, occupation encoding (e.g. Jordan-Wigner, assumed)

## Initial state

Unspecified; a reference state such as the Hartree-Fock determinant would be an assumption.

## Algorithm steps

1. Build H from the integrals h_pq and h_pqrs and split it into terms H_j. (eq_1)
2. Map fermionic terms to qubit gates (encoding assumed) and apply r Trotter steps. (eq_2, eq_3)
3. Choose r so that the Trotter error is at most epsilon and compare the resulting gate count to the reported scalings. (eq_3, eq_4, eq_5)

## Assumptions

- Jordan-Wigner encoding and first-order Trotter formula chosen as the smallest generic construction
- No specific molecule or basis chosen

## Missing information

- Explicit error bound and Trotter step-size criterion
- The alternative simulation scheme
- The coalescing scheme and its term-dependent step sizes
- The efficient complexity-bounding method
- Specific molecules, basis sets and fitted numerical exponents
