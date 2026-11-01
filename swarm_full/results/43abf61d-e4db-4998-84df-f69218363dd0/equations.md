# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Construct a single-shot Toffoli (CCNOT) gate on three nearest-neighbor-coupled superconducting transmon systems via quantum optimal control using an enhanced Differential Evolution algorithm, targeting 99.9% fidelity and a gate time comparable to an entangling two-qubit gate under the same realistic conditions.

Scope: Gate-synthesis/control-optimization problem, not an algorithmic circuit. The abstract gives only the target gate, platform, fidelity and speed claims; Hamiltonian, pulse parameterization, and optimizer details are not given. Reconstruction limited to target unitary and fidelity objective as background.

## Symbols

- $U_{\mathrm{T}}$: Target Toffoli (CCNOT) unitary on three qubits; domain: 8x8 unitary matrix
- $U(T)$: Implemented unitary at gate time T from the control pulses; domain: unitary on the computational subspace
- $F$: Gate fidelity; domain: [0,1]

## eq_1: Toffoli action

$$
U_{\mathrm{T}}|a,b,c\rangle=|a,b,c\oplus ab\rangle
$$

Toffoli flips the target bit c iff both controls a and b equal 1.

Provenance: `standard_background`. Standard definition of the controlled-controlled-NOT gate named in the abstract.

Equation assumptions:

- a,b,c in {0,1}

## eq_2: Fidelity objective

$$
F=\frac{|\mathrm{Tr}(U_{\mathrm{T}}^\dagger U(T))|^2}{64}
$$

Illustrative unitary-overlap fidelity to be maximized, with target F of at least 0.999.

Provenance: `assumption`. Common choice for an 8-dimensional gate fidelity; the paper's exact definition is not stated in the abstract.

Equation assumptions:

- Leakage outside the computational subspace ignored
- Exact fidelity definition unknown

## Registers

- q0: 1 transmon (qubit) qubits; Control qubit a, at one end of the nearest-neighbor chain
- q1: 1 transmon (qubit) qubits; Middle control qubit b, coupled to both neighbors
- q2: 1 transmon (qubit) qubits; Target qubit c

## Initial state

Any three-qubit computational basis state |a,b,c> (or superposition for process characterization); assumed, not stated in the abstract.

## Measurement

Assumed: measure all three transmons in the computational basis after the pulse; for each input |a,b,c> estimate the output distribution and compare with |a,b,c XOR ab>. The abstract describes numerical optimization only and gives no measurement protocol.

## Classical postprocessing

Offline: the Differential Evolution loop evaluates F (eq_2) from simulated U(T) and updates pulse parameters until F >= 0.999. Optionally, truth-table success probabilities from measured counts are used as an experimental proxy. Details are not given in the abstract.

## Algorithm steps

1. Prepare the three transmons in a chosen computational basis state |a,b,c>. (eq_1)
2. Apply a single optimized, simultaneous control pulse sequence over gate time T to the coupled transmons, found by the enhanced Differential Evolution search, so that U(T) approximates the Toffoli unitary. (eq_1, eq_2)
3. Evaluate the fidelity of U(T) against the target and iterate the optimizer until F reaches about 0.999. (eq_2)

## Assumptions

- Fidelity measure is a standard unitary-overlap measure.
- Three qubits are arranged in a linear chain with nearest-neighbor coupling; the middle qubit's role as control is assumed.
- The differential evolution loop is treated as classical offline optimization.
- Linear chain of three transmons with the target at one end; the abstract does not specify which qubit is the target.
- Computational-basis readout of all three transmons is assumed.

## Missing information

- Transmon Hamiltonian and coupling strengths
- Control pulse parameterization
- Enhanced Differential Evolution details
- Gate time value
- Noise model and fidelity definition
- Actual measurement or characterization protocol (not in abstract)
- Which transmon is the target and how the chain is ordered
