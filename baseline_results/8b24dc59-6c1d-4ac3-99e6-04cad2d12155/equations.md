# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Compute the ground-state electronic energy E_0(R) of the helium hydride cation HeH+ in a minimal (assumed STO-3G) basis as a function of internuclear distance R (the bond dissociation curve), using a small quantum register (NV-center spins) and a phase-estimation-type eigenvalue algorithm whose energy uncertainty for the model Hamiltonian is of order 1e-14 Hartree.

Scope: Smallest useful construction (assumption, no experiment_scope supplied): iterative phase estimation (IPEA) with one ancilla qubit and a 2-qubit system register encoding the four N=2, S_z=0 Slater determinants of minimal-basis HeH+, for a single internuclear distance R (e.g. R = 0.9 Angstrom) and a small number of phase bits (e.g. m = 4) as a tiny illustrative instance. The full dissociation curve is obtained by repeating the same procedure over a grid of R values. Out of scope: the specific NV-center physical encoding (electron/nuclear spin levels), pulse-level control, how the paper reaches ~47-bit (1e-14 Ha) precision, decoherence/error analysis, and any claims about classical intractability.

## Symbols

- $R$: Internuclear He–H distance; domain: R > 0 (Angstrom or Bohr)
- $h_{pq}(R), h_{pqrs}(R)$: One- and two-electron integrals of HeH+ in the minimal orthonormal (molecular-orbital) basis, computed classically; domain: real numbers, p,q,r,s \in \{1,2\} spatial orbitals (spin-orbitals 1\alpha,1\beta,2\alpha,2\beta)
- $E_{nuc}(R)$: Nuclear repulsion energy Z_{He} Z_{H}/R = 2/R (atomic units); domain: real, positive
- $a_p^\dagger, a_p$: Fermionic creation/annihilation operators for spin-orbital p; domain: operators on 16-dim Fock space of 4 spin-orbitals
- $|\Phi_i\rangle, i=1..4$: Slater determinants in the N=2, S_z=0 sector: |1\alpha1\beta\rangle, |1\alpha2\beta\rangle, |2\alpha1\beta\rangle, |2\alpha2\beta\rangle; domain: orthonormal basis of a 4-dim subspace
- $H(R)$: 4x4 Hermitian (real symmetric) matrix of the electronic Hamiltonian in the basis \{|\Phi_i\rangle\}; domain: real symmetric 4x4 matrix, entries in Hartree
- $E_n(R), |\psi_n\rangle$: Eigenvalues and eigenvectors of H(R); E_0 is the ground-state energy; domain: E_n real (Hartree), n = 0..3
- $t$: Evolution-time parameter chosen so that all relevant phases lie in [0,1); domain: t > 0 (inverse Hartree, atomic units)
- $U(R)$: Unitary e^{-iH(R)t} acting on the 2-qubit system register; domain: 4x4 unitary matrix
- $\phi_n$: Eigenphase of U associated with E_n, defined modulo 1; domain: [0,1)
- $m$: Number of phase bits extracted by IPEA; domain: positive integer
- $x_k$: k-th measured phase bit (k=1 most significant); domain: \{0,1\}
- $\omega_k$: Classical feedback rotation angle at IPEA iteration k; domain: real, radians
- $\delta E$: Energy uncertainty (resolution) of the estimate; domain: positive real (Hartree)

## eq_1: Second-quantized molecular Hamiltonian

$$
H_{el}(R) = \sum_{p,q=1}^{4} h_{pq}(R)\, a_p^\dagger a_q + \frac{1}{2}\sum_{p,q,r,s=1}^{4} h_{pqrs}(R)\, a_p^\dagger a_q^\dagger a_r a_s + E_{nuc}(R)
$$

Electronic-structure Hamiltonian in a fixed basis of 4 spin-orbitals (minimal basis for HeH+); the integrals h_{pq}, h_{pqrs} are classical inputs depending on R.

Provenance: `standard_background`. Standard starting point of ab initio quantum chemistry simulation; the abstract names the problem (minimal-basis HeH+) but not this formula.

Equation assumptions:

- Born–Oppenheimer approximation
- Minimal basis with one spatial orbital per atom (2 spatial / 4 spin-orbitals), e.g. STO-3G
- Spin-orbitals orthonormalized (e.g. canonical Hartree–Fock orbitals)

## eq_2: Symmetry-reduced 4x4 Hamiltonian and 2-qubit compact encoding

$$
H(R)_{ij} = \langle \Phi_i | H_{el}(R) | \Phi_j \rangle,\quad i,j \in \{1,2,3,4\},\qquad |\Phi_i\rangle \mapsto |q_1 q_2\rangle \text{ with } i-1 = 2 q_1 + q_2
$$

Restriction of H_el to the N=2, S_z=0 subspace containing the ground state; the four determinants are mapped to the four 2-qubit computational basis states (register order q_1 q_2, q_1 most significant). H(R) = sum_{ij} H_ij |i-1><j-1| is the system Hamiltonian.

Provenance: `assumption`. A smallest register that still contains the exact minimal-basis ground state; the abstract only says a 'solid-state quantum register' was used, so this encoding is a proposed construction, not sourced.

Equation assumptions:

- Ground state lies in the N=2, S_z=0 sector (true for closed-shell singlet HeH+)
- Matrix elements H_ij evaluated classically via Slater–Condon rules from h_pq, h_pqrs
- Compact (configuration) encoding rather than Jordan–Wigner on 4 qubits

## eq_3: Time-evolution unitary and eigenphase relation

$$
U(R) = e^{-iH(R)t},\qquad U(R)|\psi_n\rangle = e^{-iE_n(R)t}|\psi_n\rangle = e^{2\pi i \phi_n}|\psi_n\rangle,\qquad \phi_n = \left(-\frac{E_n(R)\,t}{2\pi}\right) \bmod 1
$$

Eigenvalues of H are encoded as phases of U; the relation between phi_n and E_n is only defined modulo 1, so t (and an optional energy shift) must be chosen so the target phase is unambiguous.

Provenance: `standard_background`. Standard phase-estimation mapping between Hamiltonian eigenvalues and unitary eigenphases; the abstract does not state which eigenvalue algorithm was used.

Equation assumptions:

- Since H(R) is a 4x4 matrix, U(R) and its powers U^{2^{k-1}} can be compiled exactly (classically) as 2-qubit unitaries, no Trotterization needed
- t chosen so that |E_n t| < 2π for the eigenvalue of interest

## eq_4: Iterative phase estimation (IPEA) iteration k

$$
P(x_k = 0) = \cos^2\!\left(\pi\, 2^{k-1}\phi_n + \frac{\omega_k}{2}\right),\qquad \omega_k = -2\pi \sum_{l=k+1}^{m} x_l\, 2^{k-l-1},\qquad k = m, m-1, \dots, 1
$$

For iteration k (processed from least to most significant bit): ancilla prepared in (|0>+|1>)/sqrt2, controlled-U^{2^{k-1}} applied to the system in eigenstate |psi_n>, ancilla phase gate diag(1, e^{i omega_k}) applied, Hadamard, then ancilla measured giving bit x_k. With exact eigenstate input the outcome is deterministic when 2^{k-1}phi_n plus the feedback is an exact binary fraction; otherwise the last bit is probabilistic.

Provenance: `standard_background`. Standard single-ancilla iterative phase estimation with classical feedback; it is the natural candidate for a few-qubit register reaching very high phase precision, but its use in the paper is not stated in the abstract.

Equation assumptions:

- System register prepared in (or with large overlap on) the target eigenstate |psi_0>
- Bits x_{k+1..m} from previous iterations are used classically in omega_k

## eq_5: Energy reconstruction and resolution

$$
\tilde{\phi} = \sum_{k=1}^{m} x_k 2^{-k},\qquad \tilde{E}_0(R) = -\frac{2\pi\tilde{\phi}}{t},\qquad \delta E \approx \frac{2\pi\, 2^{-m}}{t}
$$

The m measured bits form a binary fraction approximating phi_0 (truncation, not exact), converted back to an energy estimate; the resolution is set by 2^{-m}/t. The 1e-14 Hartree uncertainty quoted in the abstract corresponds, for t of order 1 a.u., to m on the order of 45–50 bits (inference, not a sourced number).

Provenance: `abstract_inferred`. The abstract reports an energy uncertainty; relating it to phase-bit resolution assumes a phase-estimation-type readout. The exact algorithmic source of the uncertainty is not given in the abstract.

Abstract evidence: we report an energy uncertainty (given our model basis) of the order of $10^{-14}$ Hartree

Equation assumptions:

- Phase bits are extracted sequentially with negligible readout error
- The uncertainty refers to algorithmic/statistical precision for the model Hamiltonian, not basis-set error

## eq_6: Bond dissociation curve

$$
E_0(R) = \min_n E_n(R) \text{ for } R \in \{R_1,\dots,R_N\},\qquad D_e = \lim_{R\to\infty} E_0(R) - \min_R E_0(R)
$$

The ground-state energy is estimated at each grid point R (requiring recompilation of U(R) and re-preparation of the input state), giving the dissociation curve; D_e is the resulting dissociation energy.

Provenance: `abstract_inferred`. The abstract explicitly states the dissociation curve is computed; the equation formalizes 'curve' as E_0 sampled over R and the derived dissociation energy.

Abstract evidence: we compute the bond dissociation curve of the minimal basis helium hydride cation, HeH+

Equation assumptions:

- A finite grid of R values is used
- The large-R limit is approximated by the largest R on the grid

## Registers

- ancilla: 1 qubits; Phase-estimation probe qubit: prepared in |+>, controls U^{2^{k-1}}, receives feedback phase, measured to yield bit x_k (written leftmost in |a> ⊗ |q_1 q_2>)
- system: 2 qubits; Encodes the four N=2, S_z=0 Slater determinants of minimal-basis HeH+ via i-1 = 2 q_1 + q_2; holds the (approximate) eigenstate on which U(R) acts

## Initial state

|0\rangle_a \otimes |\psi_{in}\rangle, with |\psi_{in}\rangle = |00\rangle = |1\alpha 1\beta\rangle (Hartree–Fock determinant, assumed to have large overlap with |\psi_0\rangle), or, since H(R) is 4x4, the exact |\psi_0(R)\rangle prepared by a classically compiled 2-qubit unitary (assumption).

## Measurement

Projective measurement of the single ancilla qubit in the computational basis at each IPEA iteration, yielding one phase bit x_k; m iterations per energy value. Repetition per bit (majority vote) is used if the input state is not an exact eigenstate.

## Classical postprocessing

Compute omega_k from previously obtained bits (eq_4); form phi = sum_k x_k 2^{-k}; convert to E_0(R) = -2π phi / t (eq_5), undoing any energy shift used to place the phase in [0,1); tabulate E_0 versus R and extract the dissociation energy (eq_6).

## Algorithm steps

1. Classical pre-processing at fixed R: compute minimal-basis integrals h_pq(R), h_pqrs(R) and E_nuc(R); build the 4x4 matrix H(R) in the S_z=0 determinant basis; choose t; compile U(R)^{2^{k-1}} for k=1..m as exact 2-qubit unitaries. (eq_1, eq_2, eq_3)
2. Prepare the system register in the input state (Hartree–Fock |00> or the exact ground state) and the ancilla in |0>; set k = m and the bit record to empty. (eq_2)
3. IPEA iteration k: apply Hadamard to the ancilla, controlled-U(R)^{2^{k-1}} on the system, the feedback phase gate diag(1, e^{i omega_k}) on the ancilla, a second Hadamard, and measure the ancilla to obtain x_k; reset the ancilla; decrement k and repeat until k = 1. (eq_3, eq_4)
4. Assemble the binary fraction from x_1..x_m and convert to the energy estimate E_0(R); repeat the whole procedure for each R on the grid to trace out the dissociation curve. (eq_5, eq_6)

## Assumptions

- No experiment_scope was supplied; the chosen scope (IPEA, 1 ancilla + 2 system qubits, single R, small m) is the author's smallest-useful-construction choice, not derived from the abstract.
- Minimal basis taken to be STO-3G (the abstract says only 'minimal basis').
- Compact encoding of the S_z=0 two-electron sector on 2 qubits with ordering i-1 = 2 q_1 + q_2.
- Because the Hamiltonian is a tiny matrix, U(R) and its powers are compiled exactly from the classically diagonalizable H(R); no Trotter error.
- The reported ~1e-14 Hartree uncertainty is interpreted as the resolution of a many-bit phase estimate, which is an inference.
- The NV-center specifics (which spin levels play ancilla/system roles) are not reconstructed.

## Missing information

- Numerical values of the integrals / matrix elements H_ij(R) and the R grid used in the paper
- The actual eigenvalue algorithm used (IPEA or otherwise), number of phase bits, and choice of t
- How the molecular Hamiltonian was mapped onto the NV electron spin / nuclear spin levels and the size of the physical register
- The gate/pulse sequence implementing controlled-U^{2^{k-1}} and state preparation
- Whether the Hamiltonian was further symmetry-reduced (e.g., to the singlet subspace) before encoding
- Error model, decoherence times, readout fidelity, and how the 1e-14 Hartree uncertainty was estimated
- Comparison values (e.g., full-CI energies, equilibrium distance, dissociation energy) are not provided in the abstract
