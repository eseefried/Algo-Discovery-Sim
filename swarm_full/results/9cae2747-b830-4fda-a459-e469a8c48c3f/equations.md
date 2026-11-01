# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Construct Toffoli (control-control-phase) and Fredkin (control-swap) gates, and a conditional four-qubit phase gate, from a small number of global two-qubit entangling gates without ancilla qubits or ancilla internal states, for platforms such as ion qubits and circuit QED. Targets: three global two-qubit gates for Toffoli, four for Fredkin, seven for the four-qubit phase gate, and five nearest-neighbour interactions for Toffoli and Fredkin.

Scope: Abstract-level reconstruction of the gate definitions and gate-count claims only. The explicit global-gate sequences, single-qubit rotations, and Hamiltonians are not given in the abstract. A small finite instance (3-qubit CCZ and Fredkin) is used for illustration.

## Symbols

- $|a b c\rangle$: computational basis state of three qubits; domain: a,b,c in {0,1}
- $U_{CCZ}$: control-control-phase (Toffoli-equivalent) gate; domain: unitary on 3 qubits
- $U_{F}$: control-swap (Fredkin) gate; domain: unitary on 3 qubits

## eq_1: CCZ action

$$
U_{CCZ}|a b c\rangle=(-1)^{abc}|a b c\rangle
$$

The control-control-phase gate flips the sign only on |111>.

Provenance: `standard_background`. Standard definition of the control-control-phase gate named in the abstract.

## eq_2: Fredkin action

$$
U_{F}|a b c\rangle=|a\rangle\otimes\begin{cases}|b c\rangle & a=0\\|c b\rangle & a=1\end{cases}
$$

The control-swap gate swaps the two target qubits when the control is 1.

Provenance: `standard_background`. Standard definition of the control-swap gate named in the abstract.

## Registers

- q1: 1 qubits; first control qubit (Toffoli/Fredkin); first qubit of the phase gate
- q2: 1 qubits; second control qubit (Toffoli) or first target (Fredkin)
- q3: 1 qubits; target qubit (Toffoli) or second target (Fredkin)

## Initial state

Arbitrary three-qubit input state, e.g. computational basis |a b c>; no ancilla qubits or ancilla internal states.

## Measurement

Illustrative verification only: measure all three qubits in the computational basis after the gate on basis-state inputs (for CCZ, first apply Hadamard on the target so Toffoli's bit flip is visible; for Fredkin, read the swapped targets). Phase action of CCZ requires interference or state tomography/process tomography. The abstract specifies no measurement protocol.

## Classical postprocessing

Estimate output distributions or truth-table fidelity from repeated shots; for phase information, reconstruct from tomography. Not specified in the abstract.

## Algorithm steps

1. Toffoli/CCZ: apply a sequence of three global two-qubit entangling gates interleaved with single-qubit rotations (exact sequence not given in the abstract) to realize U_CCZ; a Hadamard on the target converts it to Toffoli. (eq_1)
2. Fredkin: apply a sequence of four global two-qubit gates with single-qubit rotations (exact sequence not given in the abstract) to realize U_F. (eq_2)
3. Nearest-neighbour variant: realize Toffoli and Fredkin with five nearest-neighbour interactions (details not given in the abstract). The four-qubit phase gate uses seven global gates (not detailed). (eq_1, eq_2)

## Assumptions

- Gate definitions use the standard textbook forms.
- Circuit steps are schematic placeholders that follow only the gate counts stated in the abstract.
- Register roles are an illustrative 3-qubit instance.
- Measurement and postprocessing are generic verification choices, not from the abstract.

## Missing information

- Explicit global two-qubit gate sequences and single-qubit rotations
- Hamiltonians and pulse details for global addressing
- Circuits for the four-qubit phase gate and the nearest-neighbour constructions
- Which qubit pairs the global gates act on in each step
- Measurement and verification protocol used by the authors
