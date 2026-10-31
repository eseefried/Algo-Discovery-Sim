# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Show that in measurement-based quantum computation (MBQC) any quantum oracle implementing a classical function can be written in constant depth, via equivalence between MBQC and a circuit model with arbitrary Z-axis rotations and unbounded fan-outs as elementary operations; as a corollary, disjunction (OR) is implementable exactly in constant depth.

Scope: Abstract-level problem statement and a small finite-instance sketch of the oracle and constant-depth claim; the actual construction, depth constants and MBQC pattern are not in the abstract and are not reconstructed.

## Symbols

- $f:\{0,1\}^n\to\{0,1\}$: classical function implemented by the oracle; domain: Boolean functions on n bits
- $O_f$: quantum oracle for f; domain: unitary on n+1 qubits
- $R_Z(\theta)$: arbitrary Z-axis rotation, elementary gate; domain: \theta\in[0,2\pi)

## eq_1: Classical function oracle

$$
O_f|x\rangle|b\rangle=|x\rangle|b\oplus f(x)\rangle
$$

Standard action of a quantum oracle for a classical function f.

Provenance: `standard_background`. Standard definition of the oracle; the abstract only mentions 'quantum oracle implementing a classical function'.

Equation assumptions:

- Bit-flip (XOR) oracle form assumed

## eq_2: Z rotation

$$
R_Z(\theta)=e^{-i\theta Z/2}
$$

Arbitrary Z-axis rotation gate, an elementary operation in the equivalent circuit model.

Provenance: `standard_background`. Standard gate definition; abstract names arbitrary Z rotations as elementary.

## eq_3: Disjunction

$$
\mathrm{OR}(x)=x_1\lor\cdots\lor x_n
$$

Disjunction whose oracle is implementable exactly in constant depth.

Provenance: `abstract_inferred`. Corollary stated in the abstract; the formula is the standard OR definition.

Abstract evidence: disjunction can be implemented exactly in constant-depth

## Registers

- x: n qubits; input register holding the bit string x
- b: 1 qubits; target qubit receiving b XOR f(x)
- anc: unknown (assumed poly(n) fan-out copies/ancillas) qubits; ancilla qubits for fan-out copies and phase gadgets

## Initial state

Assumed: |x>|b>|0...0> for a computational-basis input; general superposition inputs follow by linearity.

## Measurement

Assumed: in the circuit picture, measure the x and b registers in the computational basis to read x and b XOR f(x); ancillas are uncomputed or measured and discarded. In the MBQC realization, the single-qubit measurement angles and adaptive corrections come from the equivalence and are not given in the abstract.

## Classical postprocessing

Assumed: none beyond reading the output bit b XOR f(x) (XOR with known b). Any MBQC Pauli-frame byproduct corrections are computed classically as parities of earlier outcomes; details unspecified.

## Algorithm steps

1. Use the circuit-model equivalent of MBQC with elementary gates being arbitrary Z rotations R_Z(theta) and unbounded fan-out (plus standard Hadamard/Clifford basis changes, assumed). (eq_2)
2. Assumed sketch: write f as a phase/parity-based expansion, fan out the x bits in one layer, apply parallel Z rotations to parity registers in one layer, then uncompute fan-out so total depth is independent of n. Exact construction is not in the abstract. (eq_1, eq_2)
3. Conjugate the target qubit with Hadamards to turn the phase oracle into the bit-flip oracle O_f. For f=OR, this gives the exact constant-depth disjunction oracle stated as a corollary. (eq_1, eq_3)

## Assumptions

- O_f assumed to be the XOR-type oracle
- Circuit plan is a hedged sketch, not the paper's construction
- Parity/phase-polynomial decomposition assumed as the mechanism
- Circuit plan uses an assumed phase-polynomial/fan-out sketch
- Measurement is assumed to be computational-basis readout; MBQC angles are not specified

## Missing information

- Explicit constant-depth construction
- MBQC pattern and measurement angles
- Depth constants
- Ancilla count
- Exact decomposition of f into Z rotations and fan-outs
- Explicit byproduct-correction rules
