# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Design quantum simulation algorithms on solid-state qubit systems with nearest-neighbor interactions to prepare target states of pairing Hamiltonians, study fidelity, compare complexity across Hamiltonian types, and extract energy spectra by a measurement scheme.

Scope: Abstract-level reconstruction only: a tiny finite pairing-Hamiltonian instance with background equations. The paper's specific algorithms, gate sequences, measurement protocol details, and numerical results are not available.

## Symbols

- $H_P$: Pairing Hamiltonian to be simulated (generic BCS-type form, background); domain: Operator on n-qubit Hilbert space
- $F$: Fidelity between prepared state and target state; domain: [0,1]
- $|\psi_t\rangle$: Target state of the pairing Hamiltonian; domain: Normalized n-qubit state
- $\rho$: State prepared by the simulation algorithm; domain: Density matrix on n qubits

## eq_1: Pairing Hamiltonian (background)

$$
H_P=\sum_{j}\epsilon_j\,n_j-G\sum_{j,k}c^\dagger_{j\uparrow}c^\dagger_{j\downarrow}c_{k\downarrow}c_{k\uparrow}
$$

Standard reduced BCS pairing Hamiltonian, mapped to qubits via pair occupation (spin-1/2 operators).

Provenance: `standard_background`. The abstract names pairing Hamiltonians but gives no explicit form; this is the common textbook form and may differ from the paper's.

Equation assumptions:

- Reduced BCS form assumed
- Qubit mapping unspecified in abstract

## eq_2: Fidelity of target state

$$
F=\langle\psi_t|\rho|\psi_t\rangle
$$

Fidelity metric for the target states of each algorithm.

Provenance: `abstract_inferred`. The abstract states that fidelity is studied; this standard definition is assumed.

Abstract evidence: Fidelity of the target states corresponding to each algorithm is numerically studied.

Equation assumptions:

- Pure target state

## Registers

- q: n (one qubit per pair level, assumed) qubits; System register encoding pair occupation of the pairing Hamiltonian

## Initial state

Assumed product state |0>^{\otimes n} (or a simple reference state such as a filled-pair configuration), prepared on the solid-state qubits.

## Measurement

The abstract only states a measurement scheme extracts energy spectra from the simulator. Assumed generic approach: an ancilla-assisted phase-estimation-like or Ramsey-type interferometric readout of the evolution under H_P, measuring ancilla/qubit observables in the computational basis over many repetitions. The paper's actual scheme is not specified. Fidelity is evaluated numerically, not by measurement.

## Classical postprocessing

Assumed: Fourier-transform the measured time-series signal; peak positions give energy eigenvalues of H_P and peak weights give overlaps with the prepared state. Not confirmed by the abstract.

## Algorithm steps

1. Map the pairing Hamiltonian H_P to spin-1/2 operators on n qubits (assumed pair-occupation mapping). (eq_1)
2. Decompose the evolution or state preparation into gate sequences using the native nearest-neighbor interactions of the platform (e.g. Ising/XY/Heisenberg; the specific sequences are not in the abstract). (eq_1)
3. Apply the algorithm to prepare the target state, then numerically compute the fidelity with the target state to assess each algorithm. (eq_1, eq_2)

## Assumptions

- Reduced BCS pairing form used as the generic pairing Hamiltonian
- One qubit per pair level and a generic nearest-neighbor decomposition assumed for the circuit plan
- Spectrum measurement assumed to be Ramsey/phase-estimation-type with Fourier postprocessing

## Missing information

- Specific qubit platform interactions (Ising, XY, Heisenberg, etc.)
- Explicit algorithms and gate sequences
- Energy spectrum measurement scheme details (actual protocol)
- Complexity results
- Actual register size and encoding used in the paper
- Actual measurement protocol and readout observables for spectrum extraction
