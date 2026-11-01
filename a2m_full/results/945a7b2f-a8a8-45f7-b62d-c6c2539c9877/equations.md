# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate the ternary controlled-X (TCX) gate and the ternary controlled-Z (TCZ) gate on qutrits encoded in qubit pairs. Check their action on the valid 3^n subspace, and use TCX to build a ternary SWAP.

Scope: Smallest instance: two qutrits (a,b) on 4 qubits, with a on qubits (a0,a1) and b on qubits (b0,b1). Build TCX(a->b) and TCX(b->a) (control on level 2, target shift +1 mod 3), and the TCZ variant. Verify the permutation or phase table on the 9 valid basis states, with |11> never populated. Out of scope: full Cartan decomposition of SU(3), the physical implementation analysis, universality proofs, ternary Toffoli and Muthukrishnan-Stroud synthesis, and the general qudit extension. These are only sketched in the notes.

## Symbols

- $|t\rangle$: qutrit basis state; domain: t in {0,1,2}
- $\omega$: primitive cube root of unity; domain: exp(2 pi i/3)
- $X_3$: ternary shift gate; domain: 3x3 permutation unitary
- $Z_3$: ternary clock gate; domain: diag(1,omega,omega^2)
- $(q_1 q_0)$: qubit-pair encoding of a trit, with q_1 the high bit; domain: {00,01,10}, 11 unused

## eq_1: Qutrit encoding

$$
|0\rangle\mapsto|00\rangle,\ |1\rangle\mapsto|01\rangle,\ |2\rangle\mapsto|10\rangle,\ t=2q_1+q_0
$$

Two-qubit encoding of a qutrit, with |11> unused.

Provenance: `assumption`. The encoding is the proposed construction from the sketch, not stated in the abstract.

Equation assumptions:

- |11> is never populated

## eq_2: TCX gate

$$
\mathrm{TCX}=\sum_{c\ne2}|c\rangle\langle c|\otimes I+|2\rangle\langle2|\otimes X_3,\quad X_3|t\rangle=|t+1\bmod3\rangle
$$

The target is shifted by +1 mod 3 when the control qutrit is |2>.

Provenance: `abstract_inferred`. The abstract names the gate. The control level 2 and the +1 shift are taken from the sketch convention.

Abstract evidence: we propose the ternary controlled X (TCX) gate

Equation assumptions:

- The control level is 2
- The shift is +1

## eq_3: TCZ gate

$$
\mathrm{TCZ}=\sum_{c\ne2}|c\rangle\langle c|\otimes I+|2\rangle\langle2|\otimes Z_3,\quad Z_3=\mathrm{diag}(1,\omega,\omega^2)
$$

The target gets a phase omega^t when the control qutrit is |2>.

Provenance: `abstract_inferred`. The abstract names the gate. The explicit form is the standard clock-gate definition.

Abstract evidence: ternary controlled Z (TCZ) gate

Equation assumptions:

- The control level is 2

## eq_4: Qubit-level shift on the valid subspace

$$
X_3:\ 00\to01\to10\to00,\ 11\to11;\quad \mathrm{TCX}=\text{shift on }(b_1b_0)\text{ controlled on }a_1=1
$$

On the valid subspace the control condition a=2 reduces to the single qubit a1=1. The shift is a controlled permutation of the target pair, leaving |11> fixed.

Provenance: `assumption`. Proposed decomposition from the sketch. Possible gate sequence: CCX(a1,b0,b1) first, which maps 01 to 11. Then CX(a1,b0) toggles b0, giving 11->10 and 00->01, but this also moves 10->11, so a further fix-up is needed. The exact sequence must be checked by simulation on the 9 valid states.

Equation assumptions:

- Behaviour on |11> is irrelevant
- Exact sequence to be verified by simulation

## eq_5: Ternary SWAP from TCX

$$
\mathrm{SWAP}_3|a,b\rangle=|b,a\rangle
$$

Target action of the ternary SWAP, to be built from TCX-type gates and shift conjugations. The exact count and arrangement are not given by the abstract and must be searched or verified by simulation.

Provenance: `assumption`. The abstract says the synthesis of the ternary SWAP is investigated. The construction is assumed from the sketch.

Equation assumptions:

- The construction is verified by simulation

## Registers

- a: 2 qubits qubits; Control qutrit (a0 low bit, a1 high bit)
- b: 2 qubits qubits; Target qutrit (b0 low bit, b1 high bit)

## Initial state

Each of the 9 valid basis states |a,b> with a,b in {0,1,2}, prepared with X gates, in turn. |11> is never populated.

## Measurement

If counts are required, measure all 4 qubits and decode with Qiskit little-endian order: for the key string s=bits[::-1], a0=s[0], a1=s[1], b0=s[2], b1=s[3]. For statevector or unitary tasks, apply no measurements.

## Classical postprocessing

Decode each qubit pair to a trit with t=2*q1+q0 and reject any outcome with pair 11. Compare the output trit pairs with the target table.

## Algorithm steps

1. Prepare a valid basis state by applying X to the appropriate qubits, following the encoding of eq_1. (eq_1)
2. Apply the TCX construction on the 4 qubits (or TCZ, built from controlled phases). (eq_2, eq_3, eq_4)
3. Optionally compose the TCX gates, with shift conjugations, to realize the ternary SWAP. (eq_5)
4. Read the statevector (no measurements) and compare with the expected permutation or phase table. (eq_2, eq_3)

## Assumptions

- The scope is a 2-qutrit instance on 4 qubits, chosen by the researcher
- TCX uses control level 2 and shift +1
- Qubit simulation stands in for qutrit hardware
- Gate counts are taken after unrolling to u and cx
- No black-box queries are used

## Missing information

- The paper's exact elementary one-qutrit gate set from the Cartan decomposition
- The exact TCX and SWAP gate sequences and counts
- Explicit ternary Toffoli and Muthukrishnan-Stroud constructions
- The specific qubit cap and gate budget
