# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Implement the CCZ (control-control-phase/Toffoli-equivalent) and Fredkin (controlled-SWAP) gates on qubits using few global two-qubit gates, without ancillas. The abstract gives only gate counts, not the explicit gate sequences.

Scope: Define the target unitaries (CCZ, Toffoli via Hadamard conjugation, Fredkin) and the conventional conditional-two-qubit-gate decomposition of CCZ as background, plus the abstract's gate-count claims. The paper's global-gate circuits, the four-qubit phase gate with seven gates, and the nearest-neighbour constructions are outside scope and not reconstructed.

## Symbols

- $|a,b,c\rangle$: Computational basis state of three qubits (a,b,c); domain: a,b,c in {0,1}
- $\mathrm{CCZ}$: Control-control-phase gate; domain: 8x8 diagonal unitary
- $\mathrm{CSWAP}$: Fredkin gate; qubit 1 controls a swap of qubits 2 and 3; domain: 8x8 permutation unitary
- $H_t$: Hadamard on target qubit; domain: 2x2 unitary
- $CP(\phi)$: Conditional two-qubit phase gate diag(1,1,1,e^{i\phi}); domain: \phi real
- $N_{conv}$: Number of conditional two-qubit gates in conventional circuits; domain: 5 for Toffoli, 7 for Fredkin (abstract)

## eq_1: CCZ action

$$
\mathrm{CCZ}|a,b,c\rangle=(-1)^{abc}|a,b,c\rangle
$$

Definition of the control-control-phase gate on the computational basis.

Provenance: `standard_background`. Standard definition of CCZ; the abstract names the gate but states no formula.

Equation assumptions:

- Qubit order (a,b,c); phase -1 for |111>

## eq_2: Toffoli from CCZ

$$
\mathrm{Toffoli}=(I\otimes I\otimes H_t)\,\mathrm{CCZ}\,(I\otimes I\otimes H_t)
$$

Toffoli equals CCZ conjugated by Hadamards on the target.

Provenance: `standard_background`. Standard identity relating the two gates.

Equation assumptions:

- Target is the third qubit

## eq_3: Fredkin action

$$
\mathrm{CSWAP}|a,b,c\rangle=|a,\,b\oplus a(b\oplus c),\,c\oplus a(b\oplus c)\rangle
$$

Controlled swap of qubits 2 and 3 when qubit 1 is 1.

Provenance: `standard_background`. Standard definition of Fredkin gate.

Equation assumptions:

- Qubit 1 is control

## eq_4: Conventional CCZ decomposition

$$
\mathrm{CCZ}=CP_{bc}(\pi/2)\,CP_{ab}(\pi/2)\,\mathrm{CNOT}_{ab}\,CP_{bc}(-\pi/2)\,\mathrm{CNOT}_{ab}\,CP_{ac}(\pi/2)
$$

Textbook-style five conditional two-qubit-gate decomposition (three CP-type plus two CNOT-type entanglers), shown as a representative of the conventional count; not the paper's circuit.

Provenance: `standard_background`. Matches the abstract's conventional count of five conditional two-qubit gates (Toffoli); exact phases/ordering not verified here.

Equation assumptions:

- Exact form of the conventional circuit is a recalled variant, unverified
- CP(\phi) conditional-phase convention

## eq_5: Gate-count claims

$$
N_{global}(\mathrm{CCZ})=3,\; N_{global}(\mathrm{Fredkin})=4,\; N_{global}(C^3Z)=7,\; N_{conv}(\mathrm{Toffoli})=5,\; N_{conv}(\mathrm{Fredkin})=7
$$

Numbers of global two-qubit gates versus conventional conditional two-qubit gates.

Provenance: `abstract_explicit`. The abstract states these counts; the full sequences are not given.

Abstract evidence: using three and four global two-qubit gates, respectively

Equation assumptions:

- C^3Z denotes the conditional four-qubit phase gate

## Registers

- q: 3 qubits; Qubits (a,b,c) for CCZ/Fredkin; no ancillas per abstract

## Algorithm steps

1. Fix target unitaries CCZ and Fredkin on three qubits in the computational basis. (eq_1, eq_2, eq_3)
2. Recall the conventional decomposition as baseline for the five-gate count. (eq_4)
3. Record the paper's claimed global-gate counts; the actual global-gate sequences are missing. (eq_5)

## Assumptions

- No experiment_scope given: chose the smallest useful construction, the three-qubit CCZ target and its conventional baseline.
- Equation eq_4 is a recalled background variant, not from the paper.

## Missing information

- Explicit global two-qubit gate definitions (Hamiltonian, phases, and addressing)
- Exact sequences and single-qubit gates for the 3- and 4-gate constructions
- The seven-gate conditional four-qubit phase construction
- The five nearest-neighbour Toffoli/Fredkin constructions
- Fidelity or error analysis
