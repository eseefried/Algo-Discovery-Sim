# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate synthesis of the single-qubit rotation exp(-i f(phi_1,...,phi_k) X) with a Repeat-Until-Success (RUS) framework, using two primitives (product and reciprocal/nonlinear), with few ancillas (about 3 for multiplication and reciprocal). Inputs are rotation angles, not binary registers.

Scope: Smallest useful instance: the product primitive for two small angles a,b, mapping to approximately exp(-i a b X) on one target qubit with up to 3 ancillas, read out by statevector on the success branch. Also give the ideal target formulas for the reciprocal primitive and the composition rules. The exact RUS gate sequences, failure corrections, and amplification are NOT in the abstract and remain outside scope. The paper's cost analysis of conventional reversible arithmetic is also out of scope.

## Symbols

- $f(\phi_1,\ldots,\phi_k)$: smooth computable function giving the target rotation angle; domain: real
- $a,b$: input rotation angles for the product gadget; domain: small reals, |a|,|b| << 1 (assumed)
- $X,Y,Z$: Pauli operators; domain: 2x2 matrices
- $c$: regularization constant of the reciprocal gadget; domain: positive real (assumed)
- $\theta$: input angle of the reciprocal gadget; domain: real, bounded away from 0 relative to c
- $K_0$: Kraus operator on the target for the all-zero (success) ancilla outcome; domain: 2x2 operator, up to normalization
- $p_s$: success probability per RUS round; domain: (0,1], assumed bounded below by a constant

## eq_1: Target rotation

$$
U_f=e^{-i f(\phi_1,\ldots,\phi_k)X}
$$

Desired output single-qubit rotation on target t.

Provenance: `abstract_explicit`. The abstract states the target form directly.

Abstract evidence: approximate synthesis of single–qubit rotations of the form $e^{-if(\phi_{1},\ldots,\phi_{k})X}$

## eq_2: Product primitive ideal action

$$
G_{\mathrm{prod}}(a,b)\approx e^{-i\,ab\,X}
$$

The multiplication gadget on the success branch approximates a rotation by the product of the angles, with error of higher order in a,b.

Provenance: `abstract_inferred`. Multiplication of angles implies the effective angle ab. The sketch notes a commutator-like second-order structure, but the exact gate sequence is not in the abstract.

Abstract evidence: RUS circuits for approximate multiplication and reciprocals

Equation assumptions:

- Small a,b
- Exact gadget sequence unknown

## eq_3: Reciprocal primitive ideal action

$$
G_{\mathrm{rec}}(\theta)\approx e^{-i\arctan(c/\theta)X},\quad \text{or}\quad e^{-i\,\theta/(\theta^2+c^2)X}
$$

Candidate success-branch rotations for the reciprocal gadget. Both are smooth reciprocal-like functions; for |theta| >> c, arctan(c/theta) is approximately c/theta.

Provenance: `assumption`. The sketch proposes these forms. The abstract only says reciprocals are obtained, and the exact function is a guess.

Equation assumptions:

- Which form the paper uses is unknown
- c is a rescaling parameter

## eq_4: Composition rules

$$
e^{-i\alpha X}e^{-i\beta X}=e^{-i(\alpha+\beta)X},\quad f=\text{nesting of }+,\ \times,\ (\cdot)^{-1}
$$

Addition is concatenation of commuting X-rotations. Multiplication and inversion use the two gadgets, with angles rescaled into the accurate region.

Provenance: `abstract_inferred`. X-rotations commute, so addition is exact. Nesting of the primitives follows from synthesizing smooth f from two primitives.

Abstract evidence: smooth computable functions $f$ can be synthesized from two basic primitives

Equation assumptions:

- Rescaling keeps all intermediate angles small

## eq_5: RUS success branch and readout

$$
\rho_t=\frac{K_0\rho K_0^\dagger}{\mathrm{tr}(K_0\rho K_0^\dagger)},\quad \langle Z\rangle=\cos(2f)
$$

Post-selected on the ancillas giving 00..0, the target is rotated by exp(-i f X) from |0>, giving <Z> = cos(2f). The effective angle is f = arccos(<Z>)/2 for f in [0,pi/2].

Provenance: `standard_background`. For |0> under exp(-ifX), <Z> = cos^2 f - sin^2 f = cos 2f. This is standard single-qubit algebra.

Equation assumptions:

- Target starts in |0>
- Ancillas post-selected on all-zero

## Registers

- t: 1 qubits; target qubit carrying exp(-i f X)
- anc: up to 3 qubits; RUS ancillas, measured mid-circuit and reset for reuse

## Initial state

Target |0>. Ancillas |0>, or |+> where the sketch's entangler construction uses them (assumption).

## Measurement

Ancillas are measured in the Z basis, with all-zero as success. The target is read by statevector or tomography on the success branch. If counts are required, measure only the target Z bit, keeping Qiskit's little-endian order in mind.

## Classical postprocessing

Post-select on the ancilla all-zero outcome, estimate f = (1/2) arccos<Z>, and compare with the ideal f. The expected number of repeats is 1/p_s.

## Algorithm steps

1. Initialize the target and ancillas. Choose small a,b so the second-order approximation is accurate. (eq_2)
2. Apply the product gadget: alternating rotations R_X(a), R_X(b) with CNOT/CZ entanglers (guessed from standard RUS constructions), then measure the ancillas. (eq_2, eq_5)
3. If the outcome is all-zero, accept. Otherwise apply the known Pauli correction or restart, and reset the ancillas. (eq_5)
4. Optionally compose with the reciprocal gadget or concatenated X-rotations for general f. (eq_3, eq_4)
5. Read the target statevector on the success branch and extract f from <Z>. (eq_1, eq_5)

## Assumptions

- Inputs are rotation angles given as gates, not binary registers
- Chosen scope is a single product gadget instance
- Success probability is bounded below by a constant for restricted angles
- Failure branches are fixable by Pauli corrections or a clean restart
- Gate sequences are guessed, not from the abstract
- Approximation error is controlled by small-angle scaling

## Missing information

- Exact RUS gate sequences and ancilla measurement bases
- Exact Kraus operators and the failure-correction rules
- The exact reciprocal function and its error bounds
- Success probabilities and the amplification scheme
- The conventional-arithmetic qubit cost formulas
