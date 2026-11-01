# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Approximately synthesize single-qubit rotations e^{-i f(phi_1,...,phi_k) X}, for smooth computable f, using the Repeat-Until-Success (RUS) framework built from two basic primitives. Examples are approximate multiplication and reciprocals with as few as 3 ancilla qubits. The approach is compared on qubit cost with conventional quantum arithmetic.

Scope: Abstract-level problem statement and a small set of defining equations only. The two primitives, the RUS circuits and the success probabilities are not specified in the abstract and are not reconstructed.

## Symbols

- $f(\phi_1,\ldots,\phi_k)$: Smooth computable function giving the target rotation angle; domain: real-valued function of real angles
- $\phi_j$: Input rotation angles encoded in the input rotations; domain: real
- $X$: Pauli X operator; domain: single-qubit operator

## eq_1: Target rotation

$$
R_f=e^{-if(\phi_{1},\ldots,\phi_{k})X}
$$

Single-qubit rotation about X by angle f to be approximated.

Provenance: `abstract_explicit`. Stated in the abstract as the synthesis target.

Abstract evidence: e^{-if(\phi_{1},\ldots,\phi_{k})X}

## eq_2: Multiplication instance

$$
f(\phi_1,\phi_2)=\phi_1\phi_2
$$

Assumed form of the multiplication example for k=2.

Provenance: `assumption`. The abstract mentions approximate multiplication; the exact form of f is assumed.

Equation assumptions:

- Product of the two angles

## eq_3: Reciprocal instance

$$
f(\phi)=1/\phi
$$

Assumed form of the reciprocal example for k=1.

Provenance: `assumption`. The abstract mentions reciprocals; the exact form is assumed.

Equation assumptions:

- Reciprocal of the single angle, with the domain restricted away from 0

## Registers

- target: 1 qubits; Qubit that ends up holding the output rotation R_f
- ancilla: 3 (for multiplication and reciprocal per abstract) qubits; Ancilla qubits used in each RUS attempt and measured to flag success or failure

## Initial state

All qubits in |0>; the input angles phi_j enter as rotation gates, so no separate input register is used (assumed).

## Measurement

Ancilla qubits are measured each RUS attempt; one outcome pattern (unspecified in the abstract) signals success, the others failure (assumed).

## Classical postprocessing

Classical control repeats the attempt on failure, with any correction as needed, until success (assumed generic RUS logic).

## Algorithm steps

1. Prepare the target and ancilla qubits in |0> or |+> (assumed). (no equation reference)
2. Apply the two basic primitives (unspecified in the abstract), interleaved with the input rotations by phi_j, to compose the function f on the target. (eq_1, eq_2, eq_3)
3. Measure the ancillas. On the success outcome the target holds the approximation of R_f. On failure, correct or reset and repeat the attempt. (eq_1)

## Assumptions

- Multiplication and reciprocal are taken to be f=phi1*phi2 and f=1/phi
- The RUS skeleton (prepare, apply primitives, measure ancillas, repeat on failure) is generic and not taken from the abstract
- The primitives and exact gate sequences are not from the abstract
- Measurement and classical postprocessing are generic RUS placeholders, not from the abstract

## Missing information

- The two basic primitives are not specified
- RUS circuit structure, success and failure conditions and recovery are not specified
- Approximation error and success-probability analysis are not given
- Conventional-approach qubit cost figures are not given
- The ancilla measurement basis and which outcome counts as success are not specified
