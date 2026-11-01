# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate an abstract-model circuit (arbitrary pairwise interactions) on a nearest-neighbor kD grid (k>=2) with a classical controller, using Bell-pair routing, entanglement swapping, gate teleportation and Pauli-frame feed-forward, so depth stays O(d). Scoped target: a tiny measurement-free unitary instance of the core primitive, long-range CNOT between two logical qubits at distance 2 on a 1D line segment of a grid, via a Bell pair created by local gates and entanglement swapping, with the measurement corrections deferred as coherent controlled Paulis.

Scope: Only the long-range CNOT on 5 qubits (control c, target t, with an intermediate chain) is specified, as a deferred-measurement unitary with nearest-neighbor gates only. Not covered: general routing on Z^k, congestion handling, Shor's algorithm, fanout and controlled-operation constant-depth constructions, non-adaptive Theta(k-th root of n) circuits, lower bounds.

## Symbols

- $c,t$: logical control and target qubits at the two ends of the line; domain: qubits
- $a_1,a_2,a_3$: ancilla qubits on the path between c and t; domain: qubits
- $X,Z$: Pauli operators; domain: single-qubit operators
- $m_1,m_2$: Bell-measurement outcomes (here coherent control qubits); domain: {0,1}
- $d$: depth of the abstract circuit; domain: positive integer

## eq_1: Depth equivalence

$$
\mathrm{depth}_{\text{grid}}(C)=\Theta(\mathrm{depth}_{\text{abstract}}(C))
$$

Grid circuits with classical control match abstract-model depth up to a constant factor.

Provenance: `abstract_inferred`. Directly states the claimed depth equivalence; the form of the equation is my rewriting.

Abstract evidence: is the same (up to a constant factor) as in the standard model where arbitrary interactions are allowed

Equation assumptions:

- Classical controller is free

## eq_2: Bell pair

$$
|\Phi^+\rangle_{ab}=\frac{1}{\sqrt2}(|00\rangle+|11\rangle)=\mathrm{CNOT}_{a\to b}(H_a\otimes I_b)|00\rangle
$$

Local EPR pair preparation used for routing.

Provenance: `standard_background`. Standard identity.

## eq_3: Entanglement swapping with Pauli byproduct

$$
(\text{Bell meas. on }a_2a_3\text{ of }|\Phi^+\rangle_{a_1a_2}|\Phi^+\rangle_{a_3a_4})\Rightarrow |\Phi^+\rangle_{a_1a_4}\text{ up to }X^{m_1}Z^{m_2}\text{ on }a_4
$$

Fusing local Bell pairs into a long-range pair; byproduct is a Pauli determined by XOR of outcomes along path.

Provenance: `standard_background`. Standard teleportation/swapping identity; the parity combination across a path is from the method plan.

Equation assumptions:

- Byproducts commute through to a Pauli frame

## eq_4: Gate teleportation of CNOT via EPR pair (deferred measurement)

$$
\mathrm{CNOT}_{c\to t}=\big(Z_t^{m_2}X_c^{m_1}\text{-type corrections}\big)\cdot\text{(local CNOTs and Bell-basis rotations on }c,a_1,a_4,t\text{)}
$$

Remote CNOT consuming a long-range EPR pair, with measurements replaced by coherent controlled Paulis so the circuit is a unitary.

Provenance: `assumption`. Proposed concrete realization of the plan's step 4; correction details for the instance must be derived by the builder and verified against CNOT on the data qubits.

Equation assumptions:

- Ancillas begin in |0>
- Deferred measurement principle

## Registers

- data: 2 qubits; logical control c and target t at line ends
- anc: 3 qubits; path ancillas for Bell pair routing and swapping, and corrections

## Initial state

data in arbitrary input state; ancillas in |0>

## Classical postprocessing

In the full method, the controller computes Pauli corrections as XOR of outcomes and plans routes; in the scoped build these are coherent controls.

## Algorithm steps

1. Create local Bell pairs on adjacent ancilla pairs along the path. (eq_2)
2. Fuse them by Bell-basis rotations (CNOT, H) and coherent controlled Pauli corrections to get a long-range EPR pair. (eq_3)
3. Teleport CNOT from c to t using the EPR pair, with deferred controlled Pauli corrections; ancillas end disentangled up to measurement-equivalent state. (eq_4)
4. Scale: parallelize across all disjoint pairs per layer (out of scoped build). (eq_1)

## Assumptions

- Instance chosen by me: long-range CNOT on a 1D segment
- Measurements deferred into controlled gates to produce a measurement-free unitary
- Exact ancilla count and layout left to builder

## Missing information

- Routing/congestion construction on Z^k
- Exact constant-depth constructions for fanout, controlled operations, Shor
- Full details of adaptive corrections for non-Clifford gates
- Non-adaptive Theta(n^{1/k}) circuit construction
