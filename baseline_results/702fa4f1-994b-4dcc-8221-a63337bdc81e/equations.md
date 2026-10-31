# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Digital quantum simulation of a pairing (BCS-type) Hamiltonian on a register of solid-state qubits that natively provide nearest-neighbor two-qubit interactions, including (i) preparation/evolution of target states with a quantified fidelity and (ii) a measurement scheme that extracts the energy spectrum of the simulated pairing Hamiltonian.

Scope: Smallest useful instance chosen here (not fixed by the abstract): a two-level pairing model (N=2 single-particle levels, one Cooper pair) mapped to 2 system qubits via the Anderson pseudospin mapping, evolved by a first-order Trotter decomposition built from single-qubit Z rotations and a nearest-neighbor XY-type interaction, plus 1 ancilla qubit used for an ancilla-controlled-evolution scheme that extracts the energy spectrum by Fourier analysis of the ancilla signal. Outside scope: the paper's 'complete set' of algorithms for several interaction types (e.g. Heisenberg, Ising/ZZ, XXZ), their comparison and complexity analysis, numerical fidelity results, and the paper's specific measurement scheme, none of which are specified in the abstract.

## Symbols

- $N$: Number of single-particle levels (pair modes) in the pairing model; equals the number of system qubits; domain: positive integer; N=2 in the chosen instance
- $\epsilon_m$: Single-particle energy of level m (pair energy 2\epsilon_m in some conventions); domain: real
- $V_{ml}$: Pairing interaction matrix element between pair modes m and l; domain: real, symmetric
- $c_{\pm m}^{\dagger}, c_{\pm m}$: Fermionic creation/annihilation operators for the time-reversed pair of states (m,-m); domain: fermionic operators
- $\sigma^{m}_{x,y,z}$: Pauli operators on qubit m (qubit m encodes occupation of pair m: |1\rangle occupied, |0\rangle empty); domain: 2x2 Hermitian operators
- $H_P$: Pairing Hamiltonian (fermionic or qubit form); domain: Hermitian operator on 2^N-dimensional space
- $t$: Simulated evolution time; domain: real, nonnegative
- $n_T$: Number of Trotter steps; domain: positive integer
- $\Delta t$: Trotter time step, \Delta t = t/n_T; domain: positive real
- $E_k, |E_k\rangle$: Eigenvalues and eigenstates of H_P (\hbar = 1); domain: real / normalized vectors
- $c_k$: Overlap amplitude of the prepared system state with eigenstate |E_k\rangle; domain: complex
- $F$: Fidelity between simulated state and ideal target state; domain: real in [0,1]

## eq_1: Pairing Hamiltonian (fermionic form)

$$
H_P = \sum_{m=1}^{N} \frac{\epsilon_m}{2}\left(c_m^{\dagger}c_m + c_{-m}^{\dagger}c_{-m}\right) + \sum_{m,l=1}^{N} V_{ml}\, c_m^{\dagger}c_{-m}^{\dagger}c_{-l}c_l
$$

Standard BCS-type pairing model: level energies plus scattering of time-reversed fermion pairs between levels.

Provenance: `standard_background`. The abstract names 'pairing Hamiltonians' but gives no formula; this is the conventional definition recalled from background knowledge (conventions for the factor 1/2 vary).

Equation assumptions:

- Pair-scattering form with real symmetric V_{ml}; no unpaired (blocked) levels

## eq_2: Qubit (pseudospin) representation of the pairing Hamiltonian

$$
H_P = \sum_{m=1}^{N} \frac{\epsilon_m}{2}\,\sigma_z^{m} + \sum_{m<l} \frac{V_{ml}}{2}\left(\sigma_x^{m}\sigma_x^{l} + \sigma_y^{m}\sigma_y^{l}\right) + \text{const}
$$

Each pair mode is one qubit (occupied pair ↔ |1\rangle). Pair operators c_m^{\dagger}c_{-m}^{\dagger} map to \sigma_+^{m}, giving an XY-type (flip-flop) interaction; the total number of occupied pairs is conserved.

Provenance: `standard_background`. Standard Anderson pseudospin mapping used in known pairing-model simulation proposals; the abstract's reference to nearest-neighbor interacting qubits motivates expressing H_P in qubit form, but the paper's exact mapping is not stated.

Equation assumptions:

- Hard-core-boson/pseudospin mapping (no Jordan-Wigner strings needed because pair operators on different levels commute)
- Sign/constant conventions may differ from the paper

## eq_3: First-order Trotter decomposition of the time evolution

$$
e^{-iH_P t} \approx \left[\prod_{m=1}^{N} e^{-i\frac{\epsilon_m}{2}\sigma_z^{m}\Delta t}\;\prod_{m<l} e^{-i\frac{V_{ml}}{2}(\sigma_x^{m}\sigma_x^{l}+\sigma_y^{m}\sigma_y^{l})\Delta t}\right]^{n_T},\quad \Delta t = t/n_T
$$

Approximate (not exact) product formula; error is O(t^2/n_T) in operator norm for fixed couplings. For N=2 only one two-qubit factor appears and the nearest-neighbor interaction is used directly.

Provenance: `standard_background`. Digital simulation of a many-body Hamiltonian with native two-body gates conventionally uses Trotterization; the abstract mentions algorithms and complexity but does not specify the decomposition order.

Equation assumptions:

- First-order Trotter–Suzuki formula; the paper may use higher-order or interaction-specific decompositions

## eq_4: Native nearest-neighbor XY interaction gate (chosen device model)

$$
U_{XY}^{(m,m+1)}(\theta) = \exp\!\left[-i\frac{\theta}{2}\left(\sigma_x^{m}\sigma_x^{m+1}+\sigma_y^{m}\sigma_y^{m+1}\right)\right],\qquad \theta = V_{m,m+1}\Delta t
$$

Two-qubit gate generated by an XY (flip-flop) nearest-neighbor coupling, acting as the Trotter factor for adjacent pair modes. Non-adjacent couplings V_{ml} (|m-l|>1) would require SWAP networks and are outside the N=2 instance.

Provenance: `assumption`. The abstract says the qubits have 'various types of nearest-neighbor interactions' without naming them; XY coupling is chosen because it matches eq_2 directly and gives the smallest construction.

Equation assumptions:

- Device provides a tunable XY-type nearest-neighbor coupling and arbitrary single-qubit Z rotations
- Only N=2 (one coupling, no routing) is reconstructed

## eq_5: Ancilla-based energy-spectrum extraction (controlled evolution and Fourier analysis)

$$
|\psi_0\rangle = \sum_k c_k |E_k\rangle,\quad g(t) = \langle \sigma_x^{a}\rangle - i\langle \sigma_y^{a}\rangle = \sum_k |c_k|^2 e^{-iE_k t},\quad \tilde g(\omega) = \int dt\, e^{i\omega t} g(t) \propto \sum_k |c_k|^2\,\delta(\omega - E_k)
$$

Ancilla a prepared in |+\rangle controls e^{-iH_P t} on the system; measuring ancilla \sigma_x and \sigma_y as a function of t gives g(t), whose Fourier transform peaks at eigenvalues E_k with weights |c_k|^2 (up to an irrelevant global phase convention). With finitely many sampled t the peaks are broadened; sampling resolution limits spectral resolution.

Provenance: `standard_background`. The abstract states a measurement scheme to extract energy spectra is designed but gives no details; this is the established ancilla/phase-estimation-type procedure from the quantum-simulation literature, offered as a placeholder for the paper's unspecified scheme.

Equation assumptions:

- Controlled evolution is realizable (e.g., via controlled versions of the Trotter gates)
- The paper's actual scheme may differ (e.g., direct spectroscopy without an ancilla)

## eq_6: Target-state fidelity

$$
F = \left|\langle \psi_{\mathrm{target}} | \psi_{\mathrm{sim}} \rangle\right|^2,\qquad |\psi_{\mathrm{target}}\rangle = e^{-iH_P t}|\psi_0\rangle,\; |\psi_{\mathrm{sim}}\rangle = U_{\mathrm{Trotter}}(t)|\psi_0\rangle
$$

Figure of merit comparing the Trotterized (and possibly noisy) output state with the exact evolved target state.

Provenance: `abstract_inferred`. The abstract says fidelities of target states are studied numerically; the standard state-overlap fidelity is inferred as the quantity meant, though the abstract does not define it.

Abstract evidence: Fidelity of the target states corresponding to each algorithm is numerically studied.

Equation assumptions:

- Pure-state fidelity; target defined as the exact pairing-Hamiltonian evolution of the initial state

## Registers

- system: N (=2 in chosen instance) qubits; One qubit per single-particle level / pair mode; encodes pair occupation (|1\rangle = pair present). Qubit m is adjacent to qubit m+1 on the device chain.
- ancilla: 1 qubits; Control qubit for controlled time evolution in the spectrum-extraction scheme; measured in X and Y bases.

## Initial state

Assumption for the N=2 instance: system in the one-pair product state |1\rangle_1|0\rangle_2 (overlapping both one-pair eigenstates of H_P), ancilla in |+\rangle = (|0\rangle+|1\rangle)/\sqrt{2}; overall |+\rangle_a \otimes |10\rangle.

## Measurement

Ancilla qubit measured in the \sigma_x and \sigma_y bases at each sampled time t to obtain \langle\sigma_x^a\rangle and \langle\sigma_y^a\rangle (eq_5). For fidelity benchmarking of the system state, either full-state simulation (numerical) or state tomography on the system register is required; the abstract indicates numerical study.

## Classical postprocessing

Form g(t) from the ancilla expectation values, compute the discrete Fourier transform over the sampled times, and read off peak positions as energy eigenvalues E_k (resolution limited by total time span and Trotter error). Fidelity F is computed numerically from eq_6.

## Algorithm steps

1. Map the N-level pairing Hamiltonian to N qubits using the pseudospin representation, identifying single-qubit Z terms and XY-type pair couplings. (eq_1, eq_2)
2. Prepare the system register in the chosen initial state |10\rangle and the ancilla in |+\rangle. (no equation reference)
3. For a chosen time t and n_T Trotter steps, apply n_T repetitions of: single-qubit Z rotations by angles \epsilon_m \Delta t/2 on each system qubit, then the nearest-neighbor XY gate with \theta = V_{12}\Delta t. For spectrum extraction, make each repetition controlled on the ancilla. (eq_3, eq_4)
4. Measure the ancilla in the X and Y bases (repeat shots) to estimate g(t); repeat the whole procedure for a grid of times t. (eq_5)
5. (Classical/numerical benchmarking, not on-device) compare the Trotterized system state with the exact evolution to evaluate fidelity F. (eq_6)

## Assumptions

- No experiment scope was supplied; the N=2 (one Cooper pair, two levels) instance with XY nearest-neighbor coupling was chosen as the smallest useful construction.
- Natural units \hbar = 1.
- First-order Trotterization with uniform \Delta t.
- Spectrum extraction uses a generic ancilla-controlled-evolution/Fourier scheme standing in for the paper's unspecified measurement scheme.
- Ideal (noiseless) gates; the paper's numerical fidelity study likely includes effects not modeled here.

## Missing information

- Exact form and conventions of the pairing Hamiltonian used in the paper (energies, coupling matrix, presence of blocked levels).
- Which nearest-neighbor interaction types (e.g., Heisenberg, Ising, XY, XXZ) the paper's algorithms target and how each is compiled into the pairing evolution.
- Trotter order, step count, and complexity (gate-count) results of the paper.
- The paper's specific measurement scheme for energy spectra and whether it uses an ancilla.
- Definition of the target states whose fidelity is studied and the numerical fidelity values.
- Routing/SWAP strategy for non-nearest-neighbor pairing couplings V_{ml} with |m-l|>1.
