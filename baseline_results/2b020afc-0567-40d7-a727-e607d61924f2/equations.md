# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct, from the abstract alone, a mathematical specification of the proposed two-qutrit elementary gates (ternary controlled-X, TCX, and ternary controlled-Z, TCZ), their mutual relation, and a smallest useful synthesis example (the ternary SWAP gate) built from these elementary gates plus one-qutrit gates.

Scope: Scope chosen (no experiment_scope supplied): (i) define the qutrit shift/clock operators and the TCX/TCZ gates on two qutrits; (ii) state the Fourier-conjugation relation between TCX and TCZ; (iii) give the Cartan (KAK) structural form of a general one-qutrit gate as background; (iv) synthesize the ternary SWAP gate from three TCX gates and one one-qutrit gate, with the explicit tiny instance |1>|2> -> |2>|1>. Out of scope: the paper's specific one-qutrit elementary gate set derived from Cartan decomposition, synthesis of ternary Toffoli and Muthukrishnan-Stroud gates, physical-implementation analysis, and the qudit (d>3) generalization.

## Symbols

- $\omega$: primitive cube root of unity, \omega = e^{2\pi i/3}; domain: \mathbb{C}
- $|j\rangle, j\in\{0,1,2\}$: computational basis of a single qutrit; domain: \mathbb{C}^3
- $X_3$: qutrit cyclic shift (generalized Pauli X); domain: U(3)
- $Z_3$: qutrit clock operator (generalized Pauli Z); domain: U(3)
- $F_3$: single-qutrit discrete Fourier transform (ternary Hadamard-like gate); domain: U(3)
- $\mathrm{TCX}_{c\to t}$: ternary controlled-X with control qutrit c and target qutrit t; domain: U(9)
- $\mathrm{TCZ}$: ternary controlled-Z gate (symmetric in the two qutrits); domain: U(9)
- $\mathrm{SWAP}_3$: ternary SWAP gate exchanging two qutrits; domain: U(9)
- $|a\rangle|b\rangle$: two-qutrit computational basis state; left ket is qutrit 1 (control in TCX_{1\to2}), right ket is qutrit 2; domain: a,b\in\{0,1,2\}
- $K_1,K_2,A(\theta)$: factors of a Cartan KAK decomposition of a one-qutrit unitary; domain: U(3)

## eq_1: Qutrit shift and clock operators

$$
X_3|j\rangle=|j+1 \bmod 3\rangle,\qquad Z_3|j\rangle=\omega^{j}|j\rangle,\qquad \omega=e^{2\pi i/3},\qquad Z_3X_3=\omega X_3Z_3
$$

Generalized Pauli operators on a single qutrit; arithmetic in the ket label is modulo 3 (exact modular reduction, not integer addition).

Provenance: `standard_background`. Standard Weyl-Heisenberg (generalized Pauli) operators for d=3, needed to define controlled-X/Z gates.

Equation assumptions:

- Computational basis labelled by Z_3 = {0,1,2}.

## eq_2: Ternary controlled-X (TCX) gate

$$
\mathrm{TCX}_{1\to2}|a\rangle|b\rangle=|a\rangle|b+a \bmod 3\rangle=|a\rangle X_3^{a}|b\rangle,\qquad \mathrm{TCX}_{1\to2}^{-1}=\mathrm{TCX}_{1\to2}^{2}
$$

Control qutrit 1 applies the shift X_3 to target qutrit 2 a number of times equal to the control value. The gate has order 3, so its inverse is its square.

Provenance: `assumption`. The abstract names the TCX gate but does not define it; this is the standard generalized-CX (SUM) convention. The paper may instead use a convention where X (or a transposition X_{jk}) is applied only when the control is in a specific state such as |2>; that choice changes the synthesis equations below.

Equation assumptions:

- Generalized-CX (SUM gate) convention adopted for TCX.

## eq_3: Ternary controlled-Z (TCZ) gate

$$
\mathrm{TCZ}|a\rangle|b\rangle=\omega^{ab}|a\rangle|b\rangle
$$

Diagonal two-qutrit phase gate, symmetric under exchange of the two qutrits.

Provenance: `assumption`. The abstract names the TCZ gate but does not define it; this is the standard generalized-CZ convention consistent with eq_2.

Equation assumptions:

- Generalized-CZ convention adopted, consistent with eq_2.

## eq_4: Fourier relation between TCX and TCZ

$$
F_3|j\rangle=\frac{1}{\sqrt{3}}\sum_{k=0}^{2}\omega^{jk}|k\rangle,\qquad F_3X_3F_3^{\dagger}=Z_3,\qquad \mathrm{TCZ}=(I\otimes F_3)\,\mathrm{TCX}_{1\to2}\,(I\otimes F_3^{\dagger})
$$

TCX and TCZ are equivalent up to one-qutrit Fourier gates on the target; this is why either can serve as the two-qutrit elementary gate when arbitrary one-qutrit gates are available.

Provenance: `abstract_inferred`. The abstract treats TCX and TCZ as interchangeable elementary gates given free one-qutrit gates; under the conventions of eq_2 and eq_3 the explicit relation is the standard Fourier conjugation (exact equality).

Abstract evidence: we propose the ternary controlled X (TCX) gate or the ternary controlled Z (TCZ) gate as the two-qutrit elementary gate, which is universal when assisted by arbitrary one-qutrit gates

Equation assumptions:

- Conventions of eq_2 and eq_3.

## eq_5: Cartan (KAK) form of a one-qutrit gate

$$
U=e^{i\phi}\,K_1\,A(\theta)\,K_2,\qquad K_1,K_2\in S(U(2)\times U(1))\subset SU(3),\qquad A(\theta)=\exp\!\big(\theta\,(|0\rangle\langle 2|-|2\rangle\langle 0|)\big)
$$

Any U in U(3) factors as a global phase, two elements of a U(2)-type subgroup acting on a two-level subspace, and a one-parameter Cartan element mixing the remaining level pair (the symmetric space SU(3)/S(U(2)xU(1)) has rank 1).

Provenance: `standard_background`. The abstract states one-qutrit elementary gates are obtained from Cartan decomposition but gives no formulas; this is the generic KAK structure. The paper's actual choice of subgroup pair and resulting elementary gate list is not recoverable from the abstract.

Equation assumptions:

- Choice of the subgroup K and the Cartan subalgebra direction is one standard option among equivalent ones.

## eq_6: Ternary SWAP from three TCX gates and one one-qutrit gate

$$
\mathrm{SWAP}_3=(F_3^{2}\otimes I)\,\mathrm{TCX}_{1\to2}\,\mathrm{TCX}_{2\to1}^{-1}\,\mathrm{TCX}_{1\to2},\qquad F_3^{2}|j\rangle=|-j \bmod 3\rangle,\qquad \mathrm{SWAP}_3|a\rangle|b\rangle=|b\rangle|a\rangle
$$

Operators act right-to-left on |a>|b>: |a,b> -> |a,a+b> -> |-b,a+b> -> |-b,a> -> |b,a> (all arithmetic mod 3). The final one-qutrit negation gate F_3^2 is required because, unlike the qubit case, the three-CX circuit alone yields |-b>|a>.

Provenance: `assumption`. The abstract says the ternary SWAP gate is synthesized from the elementary gates but gives no circuit; this is a valid decomposition under the TCX convention of eq_2, offered as the smallest useful construction. The paper's actual circuit may differ.

Equation assumptions:

- TCX convention of eq_2.
- TCX_{2->1}^{-1} = TCX_{2->1}^2 is counted as elementary (or as two TCX gates).

## Registers

- q_1: 1 qutrit qubits; first qutrit (control of TCX_{1->2}); left ket in |a>|b>
- q_2: 1 qutrit qubits; second qutrit (target of TCX_{1->2}); right ket in |a>|b>

## Initial state

Two-qutrit computational basis state |a>|b> with a,b in {0,1,2}; explicit tiny instance |1>|2> (register order q_1 then q_2).

## Measurement

Optional verification only: measure both qutrits in the computational basis {|0>,|1>,|2>}; for input |1>|2> the outcome (2,1) should occur with probability 1 (exact, noiseless).

## Classical postprocessing

Compare measured ternary outcomes (a',b') with the expected (b,a); no further processing.

## Algorithm steps

1. Prepare |a>|b>; for the instance, |1>|2>. (eq_1)
2. Apply TCX_{1->2}: |a,b> -> |a, a+b mod 3>; instance |1,2> -> |1,0>. (eq_2)
3. Apply TCX_{2->1}^{-1} (= TCX_{2->1}^2): |a, a+b> -> |-b, a+b>; instance |1,0> -> |1,0>. (eq_2, eq_6)
4. Apply TCX_{1->2}: |-b, a+b> -> |-b, a>; instance |1,0> -> |1,1>. (eq_2, eq_6)
5. Apply the one-qutrit negation F_3^2 on q_1: |-b, a> -> |b, a>; instance |1,1> -> |2,1>, completing SWAP_3. Optionally, replace any TCX by TCZ conjugated with F_3 on the target (eq_4). (eq_4, eq_6)

## Assumptions

- No experiment_scope was supplied, so the ternary SWAP synthesis from TCX gates was chosen as the single smallest useful construction with instance |1>|2>.
- TCX and TCZ are taken in the generalized (SUM / omega^{ab}) convention; the paper may define them with a control condition on a specific state (e.g. |2>) or with transposition-type X gates.
- Arbitrary one-qutrit gates are assumed available, as stated in the abstract.

## Missing information

- Exact definition of the paper's TCX and TCZ gates (control condition and which X/Z operator is applied).
- The paper's explicit one-qutrit elementary gate set derived from Cartan decomposition and its parameterization.
- Circuits and gate counts for the ternary SWAP, ternary Toffoli, and Muthukrishnan-Stroud gates as given in the paper.
- Physical-implementation details and feasibility arguments.
- The qudit (d>3) generalization of the elementary gates.
- Any universality proof details for TCX/TCZ plus one-qutrit gates.
