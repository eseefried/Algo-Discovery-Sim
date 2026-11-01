# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Characterize which decompositions of a two-outcome generalized quantum measurement into a continuous stochastic feedback process are possible when each iteration is a weak measurement from interaction with a qubit probe under a constant interaction Hamiltonian, with arbitrary unitary pulses allowed between iterations.

Scope: Abstract-level reconstruction of a qubit-system, qubit-probe weak-measurement feedback loop. Only the abstract's qualitative result is used: achievable generalized measurements have two distinct singular values. The specific Hamiltonian, probe state, and pulse protocol are not given.

## Symbols

- $M_0,M_1$: Kraus operators of a two-outcome generalized measurement; domain: Linear operators on the system Hilbert space
- $H_{int}$: Constant system-probe interaction Hamiltonian; domain: Hermitian operator on system tensor probe

## eq_1: Two-outcome completeness

$$
M_0^\dagger M_0+M_1^\dagger M_1=I
$$

Completeness relation for a two-outcome generalized measurement.

Provenance: `standard_background`. Standard definition of a generalized measurement; the abstract mentions two-outcome measurements.

## eq_2: Weak measurement step

$$
M_k=(I\otimes\langle k|)\,e^{-iH_{int}\,\delta t}\,(I\otimes|\phi\rangle)
$$

One weak-measurement iteration from a short interaction with a qubit probe, followed by probe readout.

Provenance: `assumption`. An assumed standard model of probe-induced weak measurement; the abstract does not give the exact form.

Equation assumptions:

- Probe initial state |phi>
- Readout in a fixed basis
- Short interaction time delta t

## Registers

- S: 1 qubit qubits; System qubit being measured
- P: 1 qubit qubits; Probe qubit, freshly prepared each iteration and read out

## Initial state

System in an arbitrary state rho; probe in assumed fixed state |phi> each iteration.

## Measurement

Each iteration measures the probe qubit in a fixed (assumed computational) basis, giving a binary outcome k that updates the system via M_k. The overall two-outcome result is inferred from the accumulated outcome record.

## Classical postprocessing

Record the probe outcomes and use them to choose feedback unitary pulses and decide when to stop. Map the final record to the overall binary outcome of the target generalized measurement. The abstract does not give the explicit rule.

## Algorithm steps

1. Prepare a fresh probe qubit in |phi>. (no equation reference)
2. Apply the constant interaction e^{-iH_int dt} for short time dt between system and probe. (eq_2)
3. Measure the probe in a fixed basis, giving outcome k and applying the Kraus operator M_k to the system. (eq_2, eq_1)
4. Apply an arbitrary system unitary pulse chosen by feedback from the record so far; repeat until the accumulated product of Kraus operators realizes the target two-outcome measurement. (eq_1)

## Assumptions

- Standard Kraus model of a probe-induced weak measurement
- Fresh probe per iteration with feedback pulses depending on prior outcomes
- Fixed probe readout basis assumed
- Probe readout in a fixed computational basis

## Missing information

- Explicit Hamiltonian
- Probe initial state and readout basis
- Feedback and pulse rule
- Stopping criterion for the continuous decomposition
- Explicit rule mapping the outcome record to the final binary outcome
