# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Implement CCZ/Toffoli on 3 qubits with three global all-to-all Ising two-qubit gates G(theta)=exp(-i theta/2 sum_{i<j} Z_i Z_j) interleaved with single-qubit rotations, no ancillas. Fredkin and CCCZ (4 and 7 global gates) are outside the exact scope.

Scope: Smallest useful instance: 3-qubit CCZ (Toffoli = H_t CCZ H_t) built from three global ZZ/XX gates and single-qubit rotation layers. The exact angle schedule is not given in the abstract and must be found by solving phase equations or by numerical optimisation. Fredkin (4 global gates), CCCZ (7 global gates) and the 5-gate nearest-neighbour variants are not specified here.

## Symbols

- $n$: number of qubits; domain: integer, 3 for CCZ and Toffoli, 4 for CCCZ
- $w$: Hamming weight of basis state x; domain: integer 0..n
- $\theta_k$: angle of the k-th global gate; domain: real
- $G(\theta)$: global two-qubit gate (all pairs); domain: unitary on n qubits
- $U_k$: single-qubit layer product between global gates, e.g. Rx/Ry/Rz or Hadamard; domain: SU(2)^{\otimes n}
- $e_3$: third elementary symmetric polynomial of the bits, equal to x1 x2 x3 for n=3; domain: integer

## eq_1: Global gate depends on Hamming weight

$$
G(\theta)|x\rangle=\exp\!\left[-\tfrac{i\theta}{2}\cdot\tfrac{(n-2w)^2-n}{2}\right]|x\rangle
$$

The pair sum of Z_iZ_j equals ((sum Z_i)^2 - n)/2, and sum Z_i has eigenvalue n-2w. So the global ZZ gate is diagonal with a phase quadratic in w.

Provenance: `standard_background`. Algebraic identity: sum_{i<j} Z_iZ_j = ((sum Z_i)^2 - n)/2.

Equation assumptions:

- Global gate is symmetric all-to-all ZZ with a tunable angle

## eq_2: CCZ target

$$
\mathrm{CCZ}|x_1x_2x_3\rangle=(-1)^{x_1x_2x_3}|x_1x_2x_3\rangle=e^{i\pi e_3(x)}|x\rangle
$$

Target diagonal gate, a phase of pi on |111> only.

Provenance: `abstract_inferred`. The abstract names the control-control-phase gate; the formula is the standard definition.

Abstract evidence: control-control-phase (Toffoli) gate

Equation assumptions:

- Correctness up to global phase

## eq_3: Toffoli from CCZ

$$
\mathrm{Toffoli}=H_t\,\mathrm{CCZ}\,H_t
$$

Hadamard conjugation of the target qubit.

Provenance: `standard_background`. Standard identity.

## eq_4: Three-global-gate ansatz

$$
V=G(\theta_3)\,U_2\,G(\theta_2)\,U_1\,G(\theta_1)\,U_0,\quad V\simeq \mathrm{CCZ}\ \text{up to global phase}
$$

Circuit ansatz with three global gates and interleaved single-qubit layers. The angles and the layers U_k are free parameters to be solved for.

Provenance: `abstract_inferred`. The abstract gives the count of 3 global gates; the interleaved structure is the sketch's assumption and the parameters are unknown.

Abstract evidence: using three and four global two-qubit gates, respectively

Equation assumptions:

- Free individually addressable single-qubit rotations between global gates
- Angles found numerically or from phase equations at multiples of pi/4

## eq_5: Fredkin decomposition

$$
\mathrm{Fredkin}(c;a,b)=\mathrm{CNOT}(b\to a)\,\mathrm{Toffoli}(c,a;b)\,\mathrm{CNOT}(b\to a)
$$

Standard reduction of Fredkin to Toffoli. The 4-global-gate version absorbs the CNOTs into basis changes (not specified here).

Provenance: `standard_background`. Standard identity; the abstract only states the count of four global gates.

## Registers

- q: 3 (c1,c2,t) for CCZ/Toffoli; 3 (c,a,b) for Fredkin; 4 for CCCZ qubits; system qubits, no ancillas

## Initial state

Each computational basis state |x> for truth-table checks, or the unitary is read from the simulator with no measurement.

## Measurement

No measurements for a unitary check (compare to the target up to global phase). For a counts check, measure all qubits after preparing each basis input, remembering Qiskit little-endian ordering.

## Classical postprocessing

Compute the overlap |Tr(U_target^dagger V)|/2^n, which should equal 1. Alternatively compare the truth table.

## Algorithm steps

1. Build G(theta) in Qiskit as RZZ(theta) on every pair of qubits (or CX-RZ-CX, with H conjugation for the XX version). (eq_1)
2. Solve for or numerically optimise the angles theta_1..theta_3 and the single-qubit layers U_0..U_2 so that V equals CCZ up to global phase. (eq_2, eq_4)
3. For Toffoli, add H on the target before and after the CCZ circuit. (eq_3)
4. Optionally, for Fredkin, wrap the Toffoli with CNOTs as the baseline (more gates than the paper's 4-global-gate version). (eq_5)

## Assumptions

- Chosen scope: CCZ/Toffoli only
- Global gate is all-to-all ZZ with tunable angle, built from RZZ on every pair
- Free single-qubit rotations between global gates
- Exact synthesis, correct up to global phase
- Qubit 0 is the least significant bit

## Missing information

- Explicit angles and single-qubit rotation layers for the 3 and 4 global gate circuits
- Explicit 7-gate CCCZ construction
- Nearest-neighbour 5-gate circuits
- Whether the paper uses ZZ or XX with specific basis changes
