# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate time evolution exp(-iHt) of a second-quantized molecular Hamiltonian on N spin-orbital qubits (Jordan-Wigner) with a second-order Trotter formula, bound the Trotter error classically via nested commutator norms, and reduce gate count with a coalesced multi-rate product formula that gives different groups different step sizes.

Scope: One tiny instance: N=4 qubits (minimal-basis H2-like or generic small molecule with classically supplied integrals h_pq, h_pqrs), no ancillas, no black box. Build the second-order Trotter circuit from Pauli rotations and compare the statevector to exact exp(-iHt). Compute the commutator-based error bound classically. Out of scope: the N^8 vs N^6 scaling fits over molecule families, the paper's specific alternative scheme (the sketch's low-rank/Givens form is only a guess), the optimization of coalescing counts, and phase estimation readout.

## Symbols

- $N$: number of spin orbitals = number of qubits; domain: integer, 4 in the tiny instance
- $h_{pq},h_{pqrs}$: one- and two-body molecular integrals, computed classically; domain: real numbers
- $c_j,P_j$: real coefficient and Pauli string of term j after Jordan-Wigner; domain: c_j real, P_j in {I,X,Y,Z}^{\otimes N}
- $t,r,\Delta t$: total time, number of Trotter steps, step size t/r; domain: t>0, r positive integer
- $\epsilon$: target total error; domain: positive real
- $H_k,\Delta t_k,r_k$: coalescing group k, its step size and its repetition count; domain: groups partition the terms; r_k positive integer

## eq_1: Second-quantized Hamiltonian

$$
H=\sum_{pq}h_{pq}a_p^\dagger a_q+\tfrac12\sum_{pqrs}h_{pqrs}a_p^\dagger a_q^\dagger a_r a_s=\sum_j c_jP_j
$$

Molecular Hamiltonian written as a sum of Pauli strings after Jordan-Wigner mapping.

Provenance: `standard_background`. Standard electronic-structure form; the abstract only mentions molecule simulation with N spin orbitals.

Equation assumptions:

- Jordan-Wigner mapping
- Pauli grouping done classically

## eq_2: Second-order Trotter step

$$
S_2(\Delta t)=\prod_{j=1}^{L}e^{-ic_jP_j\Delta t/2}\prod_{j=L}^{1}e^{-ic_jP_j\Delta t/2},\quad U(t)\approx S_2(t/r)^r
$$

Symmetric product formula; each Pauli rotation is built as basis change, CX parity ladder, Rz(2 c_j Delta t/2), and uncompute.

Provenance: `standard_background`. Second-order Trotter-Suzuki is the assumed scheme; the abstract names Trotter steps but not the order.

Equation assumptions:

- Second-order formula
- fixed term order

## eq_3: Commutator error bound

$$
\left\|U(t)-S_2(t/r)^r\right\|\lesssim \frac{t^3}{r^2}\sum_{\gamma}\|[A_{\gamma_1},[A_{\gamma_2},A_{\gamma_3}]]\|
$$

Error bound from nested commutators of the terms, evaluated term by term through Pauli commutation and the triangle inequality, polynomial in N. It gives r(\epsilon)\propto \sqrt{\text{bound}/\epsilon}.

Provenance: `abstract_inferred`. The abstract implies an efficient classical bound; the nested-commutator form is the standard one, and its constants are not given.

Abstract evidence: The method we use to bound the complexity of simulating a given molecule is efficient, in contrast to the approach of [1, 2] which relied on exponentially costly classical exact simulation.

Equation assumptions:

- Constants omitted
- the bound is not tight

## eq_4: Coalesced multi-rate formula

$$
U(t)\approx\Big[\prod_k e^{-iH_k\Delta t_k}\Big]^{r},\quad H=\sum_kH_k
$$

Different groups get different effective Trotter steps, with group splitting by coefficient magnitude. Counts r_k are chosen to minimize total gates subject to the error bound being below epsilon.

Provenance: `abstract_inferred`. The abstract says different Trotter steps are used for different terms. The exact interleaving is a guess.

Abstract evidence: this scheme is based on using different Trotter steps for different terms

Equation assumptions:

- Grouping by magnitude
- interleaving pattern unspecified

## eq_5: Scaling fit

$$
G(N)\propto N^{\alpha},\quad \alpha\approx 6\ \text{(worst case, real models)},\ 8\ \text{(random ensemble)}
$$

Gate-count exponent fit to bounds across a molecule family.

Provenance: `abstract_explicit`. The exponents are stated in the abstract. The fit procedure is out of scope for the tiny instance.

Abstract evidence: the scaling is closer to $N^{6}$ in worst case for real model molecules we have studied

## Registers

- q: N (4 in the tiny instance) qubits; system qubits, one per spin orbital, Jordan-Wigner; qubit index i is orbital i, little-endian

## Initial state

A computational-basis state, e.g. Hartree-Fock |1100> on 4 qubits, or a random product state for validation. This is an assumption.

## Measurement

Validation reads the statevector with no measurements. Optional readout is observable expectation values; phase estimation is out of scope.

## Classical postprocessing

Compute the commutator bound from the integrals, the fidelity or norm error against exact exponentiation, and optionally a log-log fit of gate count against N.

## Algorithm steps

1. Classically build the Pauli terms (c_j,P_j) from the integrals, group them, and group by magnitude for coalescing. (eq_1)
2. Build the second-order Trotter circuit with r steps. Each rotation uses basis change gates, a CX ladder onto the last qubit of the support, Rz, and uncompute. (eq_2)
3. Compute the commutator bound classically and choose r, or r_k per group, to meet epsilon. (eq_3, eq_4)
4. Build the coalesced circuit and compare the statevectors of both circuits with exact exp(-iHt), checking that the observed error is at most the bound. (eq_2, eq_4)

## Assumptions

- The tiny instance is N=4 with arbitrary classically supplied integrals
- Jordan-Wigner and second-order Trotter
- The alternative scheme (number-number terms in one layer, Givens/low-rank) is a guess, not from the abstract
- Coalescing is by coefficient magnitude with per-group steps

## Missing information

- Paper's alternative simulation scheme
- Exact coalescing rule and optimization
- Exact bound constants and term ordering
- Molecule family and integrals
- Readout method
