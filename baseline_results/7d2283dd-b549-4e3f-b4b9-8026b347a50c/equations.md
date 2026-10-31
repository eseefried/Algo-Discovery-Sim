# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Approximate synthesis of single-qubit rotations e^{-i f(\phi_1,\ldots,\phi_k) X}, where the angle is a smooth computable function f of input rotation angles, using Repeat-Until-Success (RUS) circuits built from a small number of ancilla qubits, with multiplication and reciprocal as the target arithmetic functions.

Scope: No experiment_scope was supplied, so one smallest useful construction is chosen (labelled as an assumption): a one-ancilla RUS 'squaring' primitive that, on measuring the ancilla in 0, applies e^{-i\theta X} to the target with \tan\theta = \tan^2\phi \approx \phi^2, and its two-angle generalisation \tan\theta = \tan\phi_1\tan\phi_2 \approx \phi_1\phi_2 (approximate multiplication). Tiny explicit instance: \phi = \pi/8, giving success probability exactly 3/4 and \theta = \arctan(3-2\sqrt{2}) \approx 0.1699 rad versus \phi^2 \approx 0.1542. Outside scope: the paper's exact primitive definitions and their names, the 3-ancilla multiplication and reciprocal circuits, composition of primitives to synthesize general smooth f, error/precision analysis, and the resource comparison with conventional quantum arithmetic.

## Symbols

- $X$: Pauli-X operator on a single qubit; domain: 2x2 Hermitian unitary
- $\phi, \phi_j$: Input rotation angles (classically known or carried by ancilla rotations); domain: \mathbb{R}, typically |\phi_j| \ll 1 for arithmetic approximations
- $f$: Smooth computable function of the input angles defining the target rotation angle; domain: \mathbb{R}^k \to \mathbb{R}
- $\theta$: Rotation angle actually implemented on the target qubit on RUS success; domain: (-\pi/2,\pi/2)
- $|\psi\rangle$: Arbitrary input state of the target qubit; domain: \mathbb{C}^2, unit norm
- $p_s$: Probability that one RUS attempt succeeds (ancilla outcome 0); domain: [0,1]
- $K_0, K_1$: Kraus operators on the target qubit conditioned on ancilla measurement outcome 0 or 1; domain: 2x2 complex matrices with K_0^\dagger K_0 + K_1^\dagger K_1 = I
- $R_x(\phi)$: Single-qubit X rotation e^{-i\phi X}; domain: SU(2)

## eq_1: Target rotation family

$$
U_f = e^{-i f(\phi_1,\ldots,\phi_k) X}
$$

The class of single-qubit rotations the method synthesizes: an X-rotation whose angle is a smooth computable function of k input angles.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: single–qubit rotations of the form $e^{-if(\phi_{1},\ldots,\phi_{k})X}$

## eq_2: One-ancilla RUS squaring primitive (success branch)

$$
K_0 = \left(\langle 0| e^{+i\phi X}\right)_a\, C_a\!\left[e^{-i\frac{\pi}{2}X_t}\right] \left(e^{-i\phi X}|0\rangle\right)_a = \cos^2\phi\, I - i\sin^2\phi\, X = \sqrt{\cos^4\phi+\sin^4\phi}\; e^{-i\theta X},\quad \tan\theta = \tan^2\phi
$$

Ancilla a prepared in |0>, rotated by e^{-i\phi X}, used as control of a controlled e^{-i\pi X/2} = -iX on the target t, rotated back by e^{+i\phi X}, and measured in the Z basis. Outcome 0 implements an exact X-rotation by \theta = \arctan(\tan^2\phi) on the target.

Provenance: `assumption`. Derived here by direct matrix computation as the smallest construction consistent with the abstract's claim that smooth functions of input angles are produced by RUS primitives; the abstract does not state this circuit, and it may differ from the paper's actual primitives.

Equation assumptions:

- Target register t is one qubit, ancilla a is one qubit; tensor order (a,t).
- Controlled gate acts when ancilla is |1>.
- Angle \phi is known classically so the rotations e^{\mp i\phi X} can be applied directly.

## eq_3: Success probability and failure branch

$$
p_s = \cos^4\phi + \sin^4\phi = 1 - \tfrac{1}{2}\sin^2(2\phi),\qquad K_1 = i\sin\phi\cos\phi\,(I + iX) = \sqrt{1-p_s}\; e^{+i\frac{\pi}{4}X}
$$

On outcome 1 the target receives a fixed, angle-independent Clifford rotation e^{+i\pi X/4}, which is undone by applying e^{-i\pi X/4} before repeating the attempt. Expected number of attempts is 1/p_s. For the instance \phi=\pi/8, p_s = 3/4.

Provenance: `assumption`. Follows from the Kraus decomposition of eq_2 and completeness K_0^\dagger K_0 + K_1^\dagger K_1 = I; the repeat-on-failure structure is what makes the circuit Repeat-Until-Success.

Equation assumptions:

- Same circuit and conventions as eq_2.
- Ideal gates and measurement.

## eq_4: Two-angle generalisation (approximate multiplication)

$$
K_0^{(\phi_1,\phi_2)} = \cos\phi_1\cos\phi_2\, I - i\sin\phi_1\sin\phi_2\, X \;\Rightarrow\; \tan\theta = \tan\phi_1\tan\phi_2,\quad p_s = \cos^2\phi_1\cos^2\phi_2 + \sin^2\phi_1\sin^2\phi_2
$$

Replacing the pre-rotation by e^{-i\phi_1 X} and the post-rotation by e^{+i\phi_2 X} in eq_2 yields on success a rotation whose tangent is the product of the input tangents, i.e. approximate multiplication of small angles. In this derived circuit the failure branch is e^{+i\theta' X} with \tan\theta' = \tan\phi_1/\tan\phi_2, which is not a fixed correction unless \phi_1=\phi_2; the paper's 3-ancilla multiplication circuit presumably resolves this differently.

Provenance: `abstract_inferred`. The abstract asserts RUS circuits for approximate multiplication exist; the product-of-tangents form is the natural inference from the squaring primitive, but the specific circuit is reconstructed here, not taken from the abstract.

Abstract evidence: one can obtain RUS circuits for approximate multiplication and reciprocals

Equation assumptions:

- Angles \phi_1,\phi_2 are classically known.
- Failure-branch handling for \phi_1 \neq \phi_2 is left unspecified.

## eq_5: Small-angle arithmetic approximation

$$
\arctan(\tan\phi_1\tan\phi_2) = \phi_1\phi_2 + O\!\left((|\phi_1|+|\phi_2|)^4\right),\qquad \arctan(\tan^2\phi) = \phi^2 + \tfrac{2}{3}\phi^4 + O(\phi^6)
$$

The implemented angle approximates the product (resp. square) of the input angles; the relation is an approximation, not an exact equality, with error of fourth order in the angles.

Provenance: `standard_background`. Taylor expansion of tan and arctan; explains the sense in which eq_2/eq_4 constitute 'approximate' multiplication.

Equation assumptions:

- |\phi_j| small enough that fourth-order terms are negligible for the intended precision.

## eq_6: RUS attempt count

$$
\mathbb{E}[\text{attempts}] = \frac{1}{p_s},\qquad \Pr[\text{not succeeded after } m \text{ attempts}] = (1-p_s)^m
$$

Standard geometric-distribution statistics for an RUS protocol whose failure branch is exactly correctable so that each attempt is independent and identical.

Provenance: `standard_background`. Elementary property of Repeat-Until-Success circuits.

Equation assumptions:

- Failure is corrected to restore the pre-attempt target state (true for eq_2/eq_3; not guaranteed for eq_4 with \phi_1\neq\phi_2).

## Registers

- t (target): 1 qubits; Qubit receiving the synthesized rotation e^{-i\theta X}; initial state arbitrary |\psi\rangle.
- a (ancilla): 1 qubits; RUS ancilla prepared in |0\rangle, rotated, used as control, measured in Z basis each attempt. (The abstract's 3-ancilla multiplication/reciprocal circuits are outside this scope.)

## Initial state

|0\rangle_a \otimes |\psi\rangle_t with |\psi\rangle arbitrary (for the tiny instance one may take |\psi\rangle = |0\rangle and \phi = \pi/8).

## Measurement

Single Z-basis measurement of the ancilla qubit per attempt; outcome 0 signals success, outcome 1 signals a correctable failure (squaring case). The target qubit is not measured by the primitive itself.

## Classical postprocessing

Classical control loop: on outcome 1 apply the fixed correction e^{-i\pi X/4} and repeat; on outcome 0 halt. Optionally record the number of attempts to compare with 1/p_s. Verification of the implemented angle (e.g. by state tomography of the target) is outside the primitive.

## Algorithm steps

1. Prepare ancilla in |0\rangle and apply e^{-i\phi X} (for the two-angle variant, e^{-i\phi_1 X}). (eq_2, eq_4)
2. Apply controlled-(e^{-i\pi X/2}) = controlled-(-iX) with ancilla as control and target as target (realisable as CNOT followed by S^\dagger on the control). (eq_2)
3. Apply e^{+i\phi X} to the ancilla (for the two-angle variant, e^{+i\phi_2 X}). (eq_2, eq_4)
4. Measure the ancilla in the computational basis. Outcome 0: target has received e^{-i\theta X} with \tan\theta=\tan^2\phi (or \tan\phi_1\tan\phi_2); stop. Outcome 1 (squaring case): apply e^{-i\pi X/4} to the target to undo the failure rotation, reset the ancilla, and repeat from step 1. (eq_3, eq_6)

## Assumptions

- Scope choice: a one-ancilla RUS squaring primitive and its two-angle multiplication variant were chosen as the smallest useful construction because no experiment_scope was provided.
- The explicit circuit (eqs. 2-4) was derived here and is not taken from the paper; the paper's actual primitives (and their failure handling, especially for distinct angles) may differ.
- Tensor-product ordering is (ancilla, target); controlled gates trigger on ancilla |1\rangle.
- Input angles are classically known so that e^{\mp i\phi_j X} can be applied directly; the abstract's notion of 'quantum arithmetic' may instead carry angles in quantum ancilla states.
- Ideal, noiseless gates and measurements.

## Missing information

- Exact definitions of the paper's two basic RUS primitives and their success/failure maps.
- The 3-ancilla circuits for approximate multiplication and for reciprocals, including how the reciprocal is obtained (e.g. iterative scheme) and how failures are corrected.
- How primitives are composed to synthesize general smooth computable f and the associated approximation-error bounds.
- Precision/resource (qubit and gate count) analysis and the comparison with conventional quantum arithmetic claimed in the abstract.
