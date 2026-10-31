# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Estimate the ground-state energy of a molecular electronic-structure Hamiltonian on N spin orbitals using Trotter-Suzuki product formulas inside quantum phase estimation, and characterise how the Trotter step size (hence total gate count) required for a fixed energy error scales with N. The abstract claims N^8 scaling for random artificial molecules versus closer to N^6 worst-case for real model molecules, and mentions an alternative simulation scheme, a coalescing scheme with term-dependent Trotter steps, and an efficient classical method for bounding the simulation cost; none of these are specified mathematically in the abstract.

Scope: Scoped to ONE minimal construction: second-quantized electronic Hamiltonian mapped by Jordan-Wigner to qubits, second-order Trotter-Suzuki step, and iterative (single-ancilla) phase estimation of the Trotterized evolution operator, applied to a tiny explicit instance of N=4 spin orbitals (minimal-basis H2-like molecule, 2 electrons, Hartree-Fock reference |1100>). The scaling claims (N^8 vs N^6) are recorded as abstract-level statements, not derived. OUT OF SCOPE (not reconstructable from the abstract): the specific 'alternative simulation scheme', the detailed coalescing schedule (which terms get which step size), the efficient classical complexity-bounding method, the set of real model molecules, and all numerical results.

## Symbols

- $N$: number of spin orbitals (equals number of system qubits under Jordan-Wigner); domain: positive integer; N=4 in the chosen instance
- $h_{pq}, h_{pqrs}$: one- and two-electron molecular integrals in the chosen spin-orbital basis; domain: real numbers (assumed real orbitals)
- $a_p^{\dagger}, a_p$: fermionic creation/annihilation operators for spin orbital p; domain: operators on the 2^N-dimensional Fock space, p in {0,...,N-1}
- $X_j, Y_j, Z_j$: Pauli operators acting on qubit j; domain: 2x2 Hermitian unitaries, j in {0,...,N-1}
- $H_j$: j-th term of the qubit Hamiltonian after Jordan-Wigner transformation (a Pauli string with real coefficient); domain: Hermitian operators, j in {1,...,L}, L = O(N^4)
- $L$: number of Hamiltonian terms; domain: positive integer, L = O(N^4)
- $\Delta t$: Trotter step size (time per Trotter step); domain: positive real
- $U(\Delta t)$: one second-order Trotter-Suzuki step approximating e^{-iH\Delta t}; domain: unitary on 2^N dimensions
- $E_0$: exact ground-state energy of H; domain: real
- $\tilde E_0$: ground-state energy of the effective Hamiltonian defined by the Trotter step; domain: real
- $\epsilon$: target error in the estimated energy (e.g. chemical accuracy); domain: positive real
- $\phi$: phase of the eigenvalue of U(\Delta t) on the (approximate) ground state, estimated by phase estimation; domain: real modulo 2\pi
- $G(N)$: total gate count of the simulation as a function of N; domain: positive real/integer
- $\Delta t_j$: term-dependent Trotter step used for term H_j in a coalescing scheme; domain: positive real, integer multiple of a base step

## eq_1: Second-quantized electronic Hamiltonian

$$
H = \sum_{p,q=0}^{N-1} h_{pq}\, a_p^{\dagger} a_q + \frac{1}{2}\sum_{p,q,r,s=0}^{N-1} h_{pqrs}\, a_p^{\dagger} a_q^{\dagger} a_r a_s
$$

Molecular electronic Hamiltonian in a basis of N spin orbitals (Born-Oppenheimer, nuclear repulsion constant omitted). Number of terms L = O(N^4).

Provenance: `standard_background`. Standard starting point for quantum chemistry simulation; the abstract refers to 'spin orbitals N' and molecular simulation but does not write the Hamiltonian.

Equation assumptions:

- Real orbitals so h_{pq}, h_{pqrs} are real
- Nuclear repulsion constant omitted (added classically)

## eq_2: Jordan-Wigner transformation

$$
a_p = \Big(\prod_{j<p} Z_j\Big) \frac{X_p + i Y_p}{2}, \qquad a_p^{\dagger} = \Big(\prod_{j<p} Z_j\Big) \frac{X_p - i Y_p}{2}
$$

Maps fermionic operators to qubit operators; qubit j represents the occupation of spin orbital j (|1> occupied, |0> empty). Substituting into eq_1 gives H = \sum_{j=1}^{L} H_j with each H_j a real-weighted Pauli string.

Provenance: `standard_background`. Standard encoding; the abstract does not specify a fermion-to-qubit mapping.

Equation assumptions:

- Jordan-Wigner chosen for minimality; the paper's actual mapping is not stated in the abstract
- Qubit ordering: qubit 0 = spin orbital 0 is the leftmost tensor factor

## eq_3: Second-order Trotter-Suzuki step

$$
U(\Delta t) = \prod_{j=1}^{L} e^{-i H_j \Delta t/2} \prod_{j=L}^{1} e^{-i H_j \Delta t/2}, \qquad e^{-iH\Delta t} = U(\Delta t) + O(\Delta t^{3})
$$

Symmetric product formula; the second equality is an approximation with error cubic in the step for a single step. The effective Hamiltonian \tilde H defined by U(\Delta t) = e^{-i\tilde H \Delta t} has ground energy \tilde E_0 with |\tilde E_0 - E_0| = O(\Delta t^2).

Provenance: `standard_background`. The abstract discusses 'the Trotter step required' but does not state the order or form of the product formula; second-order is a common minimal choice.

Equation assumptions:

- Second-order formula assumed; the paper's actual order is not given in the abstract
- Term ordering j=1..L fixed but unspecified

## eq_4: Phase estimation energy readout (modular)

$$
U(\Delta t)\,|\tilde\psi_0\rangle = e^{-i\tilde E_0 \Delta t}|\tilde\psi_0\rangle, \qquad \tilde E_0 \Delta t \equiv -\phi \pmod{2\pi}
$$

Phase estimation on the Trotterized unitary returns the phase \phi only modulo 2\pi; the energy is recovered as \tilde E_0 = -\phi/\Delta t up to integer multiples of 2\pi/\Delta t, which must be resolved classically (e.g. by a prior energy bound or by choosing \Delta t < \pi/\|H\|). The readout approximates E_0 only up to the Trotter error |\tilde E_0 - E_0|.

Provenance: `standard_background`. Standard relation between phase estimation output and energy; the abstract does not describe the readout.

Equation assumptions:

- Initial state has non-negligible overlap with the ground state of \tilde H
- Aliasing resolved by prior knowledge of the energy range

## eq_5: Gate-count scaling claims

$$
G(N) \sim N^{8} \ \text{(random artificial molecules, Refs. [1,2])}, \qquad G(N) \lesssim N^{6} \ \text{(worst case, real model molecules, this work)}
$$

Empirical/asymptotic scaling of the total gate count with the number of spin orbitals, arising from the product of the number of Trotter terms per step (O(N^4)) and the number of Trotter steps required for fixed error \epsilon, which depends on how the required \Delta t shrinks with N. The abstract states these exponents but gives no derivation or constants.

Provenance: `abstract_explicit`. The abstract explicitly states the N^8 scaling of prior work and the N^6 worst-case scaling found for real molecules; the decomposition into terms-per-step times number-of-steps is standard but the exponents are taken from the abstract, not derived.

Abstract evidence: the scaling is closer to $N^{6}$ in worst case for real model molecules we have studied

Equation assumptions:

- The scaling is asymptotic/empirical, not a proven bound; the abstract adds that actual scaling may be better due to averaging

## eq_6: Coalescing scheme (term-dependent Trotter steps), structural form only

$$
U_{\mathrm{coal}}(\Delta t) \approx \prod_{j} e^{-i H_j \Delta t_j}, \qquad \Delta t_j = k_j\,\Delta t,\ k_j \in \mathbb{Z}_{\ge 1},\ \text{term } j \text{ applied once every } k_j \text{ base steps}
$$

Schematic form of a coalescing scheme in which terms with small norm are evolved with larger (less frequent) Trotter steps so that the total number of exponentials is reduced. The assignment rule for k_j, the ordering within a coalesced step and the resulting error bound are not given in the abstract.

Provenance: `abstract_inferred`. Inferred from the abstract's one-sentence description of the coalescing scheme of [1]; only the structural idea (different step per term) is supported, the concrete schedule is not.

Abstract evidence: this scheme is based on using different Trotter steps for different terms

Equation assumptions:

- Step ratios k_j are integers so that terms can be interleaved with a common base step
- Selection rule for k_j (e.g. based on |coefficient of H_j|) is unknown and not reconstructed

## Registers

- system: N (N=4 in the chosen instance) qubits; Holds the Jordan-Wigner encoded electronic state; qubit j is the occupation of spin orbital j, qubit 0 leftmost
- ancilla: 1 qubits; Control qubit for iterative phase estimation (phase kickback); one ancilla reused across iterations

## Initial state

|0\rangle_{\mathrm{anc}} \otimes |1100\rangle_{\mathrm{sys}} (Hartree-Fock reference: two electrons occupying spin orbitals 0 and 1 of N=4), assumed to have large overlap with the ground state of the minimal-basis H2-like Hamiltonian.

## Measurement

Computational-basis (Z) measurement of the single ancilla qubit after each iterative-phase-estimation round; each round yields one bit of the phase \phi. Repeat rounds to reach the desired precision in \phi (hence in energy, precision \epsilon requires roughly log2(\|H\|\Delta t/\epsilon)+O(1) bits).

## Classical postprocessing

Assemble the measured bits into \phi, compute \tilde E_0 = -\phi/\Delta t resolving the 2\pi/\Delta t aliasing using a prior energy bound (eq_4), add the nuclear repulsion constant, and estimate the Trotter error |\tilde E_0 - E_0| either by comparison with classical exact diagonalization (feasible only for the tiny N=4 instance) or by repeating at several \Delta t and fitting the O(\Delta t^2) dependence. The required \Delta t for target error \epsilon, multiplied by the gate count per step (O(L)=O(N^4)), gives the empirical gate-count scaling discussed in eq_5.

## Algorithm steps

1. Classically compute the integrals h_{pq}, h_{pqrs} for the N=4 instance, build H per eq_1, apply Jordan-Wigner (eq_2) to obtain the Pauli-string terms H_j, j=1..L, and fix a term ordering. (eq_1, eq_2)
2. Prepare the Hartree-Fock reference |1100> on the system register (X gates on qubits 0 and 1) and the ancilla in |0>. (no equation reference)
3. Choose a Trotter step \Delta t and construct the second-order Trotter step U(\Delta t) per eq_3 as a sequence of Pauli-string exponentials (each implemented with CNOT ladders and a single-qubit rotation). (eq_3)
4. Iterative phase estimation, iteration k: apply H to ancilla, apply controlled-U(\Delta t)^{2^k} (controlled on ancilla), apply a classically determined feedback Z-rotation on the ancilla, then apply H to ancilla. (eq_3, eq_4)
5. Measure the ancilla in the computational basis to obtain one bit of the binary expansion of \phi/(2\pi); reset ancilla and repeat for the next k, feeding previous bits into the feedback rotation. (eq_4)
6. Optional (within paper's theme, structure only): replace U(\Delta t) by a coalesced step U_coal in which small-norm terms are applied every k_j base steps (eq_6), then repeat the phase-estimation procedure to compare the Trotter step required for fixed error \epsilon. (eq_6)

## Assumptions

- No experiment_scope was supplied; the N=4 (minimal-basis H2-like, 2-electron) instance and the Jordan-Wigner + second-order Trotter + iterative phase estimation pipeline were chosen as the smallest useful construction
- Second-order Trotter-Suzuki formula and a fixed but unspecified term ordering
- Hartree-Fock state has large overlap with the ground state
- Register convention: qubit j = spin orbital j, qubit 0 leftmost in tensor products; |1> = occupied
- The N^8 and N^6 statements are taken as empirical scaling claims from the abstract, not derived or verified here

## Missing information

- Definition of the paper's 'alternative simulation scheme' and the conditions under which it outperforms standard Trotterization
- Concrete coalescing schedule: rule for assigning Trotter step multiples k_j to terms, ordering within coalesced steps, and its error analysis
- The efficient classical method used to bound the Trotter error / simulation complexity of a given molecule (the abstract only says it avoids exponentially costly exact simulation)
- Which real model molecules, basis sets and N values were studied, and the target accuracy \epsilon
- Trotter-Suzuki order and term ordering actually used in the paper
- Fermion-to-qubit mapping used in the paper
- All numerical results, fitted exponents, constants and comparisons with Refs. [1,2]
