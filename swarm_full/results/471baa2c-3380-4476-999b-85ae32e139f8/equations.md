# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Construct the 35 f-controlled phase gates of a three-qubit refined Deutsch-Jozsa algorithm using single-qubit sigma_z gates, two-qubit controlled phase gates, and two-target-qubit controlled phase gates, and implement the algorithm with superconducting transmon qutrits resonantly coupled to a single cavity (circuit QED).

Scope: Abstract-level reconstruction of the gate-decomposition protocol and the circuit-QED implementation goal; detailed pulse sequences, Hamiltonian parameters, refined-DJ definition and numerical results are not given in the abstract.

## Symbols

- $f$: Oracle function of the DJ problem on 3-bit inputs; domain: f:{0,1}^3 -> {0,1}
- $U_f$: f-controlled phase gate (phase oracle); domain: diagonal unitary on 3 qubits
- $\sigma_z$: Pauli Z gate; domain: single-qubit operator
- $x$: Computational basis input string; domain: x in {0,1}^3

## eq_1: f-controlled phase gate

$$
U_f|x\rangle=(-1)^{f(x)}|x\rangle
$$

Diagonal phase oracle applying a phase determined by f(x) on three qubits.

Provenance: `standard_background`. Standard phase-oracle form; the abstract only names f-controlled phase gates.

Equation assumptions:

- Phase-oracle convention for the refined DJ algorithm

## eq_2: Gate count

$$
N_f=35
$$

Number of f-controlled phase gates to be constructed for the three-qubit refined DJ algorithm.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: 35 $f$-controlled phase gates

## eq_3: DJ promise

$$
f\ \text{constant or balanced:}\ \sum_x (-1)^{f(x)}\in\{\pm 8,0\}
$$

Standard DJ promise for three bits.

Provenance: `standard_background`. Background for the DJ problem; refined version details are not in the abstract.

Equation assumptions:

- Refined DJ uses the same promise structure

## Registers

- q: 3 qubits; Three algorithm qubits encoded in transmon levels
- cavity: 1 mode qubits; Shared bus mediating resonant interactions among transmon qutrits

## Initial state

Assumed: all three qubits in |0>, then Hadamard-type preparation into uniform superposition (refined DJ details not given).

## Measurement

Assumed: projective measurement of all three qubits in the computational basis; the all-zero outcome indicates constant f and any other outcome balanced f (standard DJ; refined variant details not in abstract).

## Classical postprocessing

Classify f as constant if the outcome is 000, else balanced; compare outcome statistics with ideal to assess fidelity.

## Algorithm steps

1. Prepare the three qubits in an equal superposition (assumed standard DJ preparation). (eq_1)
2. Apply one of the 35 f-controlled phase gates U_f, each built from single-qubit sigma_z, two-qubit controlled-phase, and two-target controlled-phase gates. (eq_1, eq_2)
3. Apply final Hadamard-type rotations (assumed) to map the constant/balanced distinction onto measurable outcomes. (eq_3)

## Assumptions

- Phase-oracle convention for U_f
- Standard DJ preparation and readout used in place of unspecified refined DJ details
- The refined DJ algorithm is assumed to share the standard DJ promise and all-zero readout rule

## Missing information

- Explicit decomposition of each of the 35 gates
- Definition of the refined DJ algorithm
- Cavity-transmon Hamiltonian and pulse parameters
- Numerical fidelity results
- Actual readout scheme
- Exact qutrit-to-qubit encoding and readout method
- Why 35 gates arise (the refined DJ function set) is not stated in the abstract
