# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Construct, in the circuit model augmented with unbounded fan-out gates and arbitrary Z-axis rotations (equivalent to MBQC depth), a constant-depth (depth independent of the input size n) unitary oracle U_f for a classical Boolean function f:{0,1}^n -> {0,1}, with the disjunction OR_n as the key corollary instance (exact, constant depth).

Scope: Scoped to defining the target object (a standard bit-flip oracle U_f), the elementary gate set named in the abstract (R_Z(theta) for arbitrary theta, unbounded fan-out F_n, plus standard single-qubit gates), the OR_n target function, and one tiny explicit instance: OR_3 on 3 input qubits, 1 target qubit, and an unspecified ancilla register. The abstract's actual constant-depth construction for general f and for exact OR_n is NOT reconstructible from the abstract; only the specification of what must be realized and standard primitives (Hamming-weight phase via parallel Z-rotations) are supplied. The MBQC-to-circuit equivalence proof, the general-f compilation, and ancilla/depth constants remain outside scope.

## Symbols

- $n$: number of classical input bits / input qubits; domain: positive integer; tiny instance n=3
- $f$: classical Boolean function to be implemented as an oracle; domain: f:\{0,1\}^n \to \{0,1\}
- $x$: input bit string x = x_1 x_2 \cdots x_n, qubit j holds x_j (qubit 1 leftmost); domain: \{0,1\}^n
- $y$: target (output) bit of the oracle; domain: \{0,1\}
- $|x|$: Hamming weight of x, \sum_j x_j; domain: \{0,\dots,n\}
- $U_f$: bit-flip quantum oracle for f; domain: unitary on (\mathbb{C}^2)^{\otimes (n+1)} (plus ancillas returned to |0\rangle)
- $F_m$: unbounded fan-out gate with one control and m targets; domain: unitary on m+1 qubits, m arbitrary
- $R_Z(\theta)$: rotation about the Z axis by arbitrary angle theta; domain: \theta \in [0,2\pi)
- $\mathrm{OR}_n$: disjunction of n bits; domain: \{0,1\}^n \to \{0,1\}
- $d(U)$: circuit depth of U over the gate set {single-qubit gates, R_Z(theta), F_m}; domain: positive integer

## eq_1: Oracle semantics

$$
U_f\,|x\rangle|y\rangle = |x\rangle|y \oplus f(x)\rangle,\quad x\in\{0,1\}^n,\ y\in\{0,1\}
$$

Standard bit-flip oracle implementing the classical function f; register order is input x (n qubits) then target y (1 qubit); any ancillas are assumed returned to |0...0>. The XOR is exact (mod 2).

Provenance: `abstract_inferred`. The abstract speaks of an oracle implementing a classical function; the bit-flip oracle is the standard meaning. The abstract does not state the formula or whether a phase-oracle variant is intended.

Abstract evidence: any quantum oracle implementing a classical function

Equation assumptions:

- Bit-flip (XOR) oracle convention rather than phase oracle
- Ancilla qubits, if used, are returned to |0> so U_f acts as stated on the x,y registers

## eq_2: Unbounded fan-out gate

$$
F_m\,|b\rangle|t_1\rangle\cdots|t_m\rangle = |b\rangle|t_1\oplus b\rangle\cdots|t_m\oplus b\rangle,\quad b,t_j\in\{0,1\}
$$

Fan-out with one control b and m targets, counted as a single depth-1 elementary operation for arbitrary m. Equivalent (up to Hadamards) to the parity gate.

Provenance: `standard_background`. Standard definition of the fan-out gate used by Høyer and Špalek; the abstract names 'unbounded fan-outs' as elementary but does not define them.

Equation assumptions:

- Fan-out counts as depth 1 regardless of m

## eq_3: Arbitrary Z-rotation

$$
R_Z(\theta) = \begin{pmatrix} 1 & 0 \\ 0 & e^{i\theta} \end{pmatrix},\quad \theta\in[0,2\pi)
$$

Single-qubit diagonal rotation about the Z axis by an arbitrary real angle, treated as an elementary depth-1 gate (global-phase convention chosen so that |0> is fixed).

Provenance: `standard_background`. Standard matrix for Z-rotations; the abstract names 'arbitrary rotations along Z axis' as elementary operations without giving the matrix.

Equation assumptions:

- Phase convention diag(1, e^{i theta}) rather than diag(e^{-i theta/2}, e^{i theta/2}); the two differ only by a global phase

## eq_4: Disjunction target function

$$
\mathrm{OR}_n(x) = x_1 \vee x_2 \vee \cdots \vee x_n = 1 - [\,|x| = 0\,]
$$

The OR function equals 1 unless the Hamming weight of x is exactly 0. For the tiny instance n=3, U_{OR_3} |x_1x_2x_3\rangle|y\rangle = |x_1x_2x_3\rangle|y\oplus(x_1\vee x_2\vee x_3)\rangle.

Provenance: `abstract_inferred`. Disjunction is OR; the Iverson-bracket form makes explicit that OR reduces to exactly detecting zero Hamming weight, which is the standard route in fan-out-based constructions.

Abstract evidence: disjunction can be implemented exactly in constant-depth

Equation assumptions:

- n=3 chosen as the tiny explicit instance (an assumption, not from the abstract)

## eq_5: Hamming-weight phase primitive (depth 1)

$$
\Big(\bigotimes_{j=1}^{n} R_Z(\theta)\Big)|x\rangle = e^{i\theta |x|}\,|x\rangle
$$

Parallel Z-rotations imprint a phase linear in the Hamming weight in a single layer; combined with fan-out (to make it controlled by one ancilla and to parallelize), this is the standard primitive by which fan-out circuits access |x| in constant depth. It is supplied as a plausible building block only; the abstract's actual exact-OR construction is not given.

Provenance: `standard_background`. Direct consequence of eq_3 applied to each qubit; this is the well-known primitive underlying Høyer–Špalek-style constant-depth threshold/OR circuits with fan-out.

Equation assumptions:

- This primitive is not claimed to be the paper's method; how to turn weight-dependent phases into an exact OR bit in constant depth is the missing paper-specific content

## eq_6: Constant-depth claim

$$
d\big(U_f\big) = O(1)\ \text{(independent of } n\text{) for every } f:\{0,1\}^n\to\{0,1\},\ \text{over gates } \{\text{1-qubit}, R_Z(\theta), F_m\};\quad d\big(U_{\mathrm{OR}_n}\big)=O(1)\ \text{exactly}
$$

The paper's stated main result and corollary: depth bounded by a constant independent of n, with the OR corollary being exact (no approximation error). The number of ancillas and the constant are not given in the abstract.

Provenance: `abstract_explicit`. Directly restates the abstract's main claim and corollary in the gate model the abstract says is equivalent to MBQC.

Abstract evidence: it is possible to write any quantum oracle implementing a classical function in constant depth

Equation assumptions:

- Constant depth is measured in the circuit model with fan-out and arbitrary R_Z as depth-1 gates, which the abstract states is equivalent to MBQC depth
- Ancilla count may grow with n (not constrained by the abstract)

## Registers

- x (input): n (tiny instance: 3) qubits; holds the classical input string x_1...x_n in the computational basis; qubit 1 is leftmost / most significant in the string notation
- y (target): 1 qubits; receives y XOR f(x)
- a (ancilla): unknown (poly(n) expected, not stated in abstract) qubits; workspace for fan-out copies and phase/Fourier-style intermediate values; must be returned to |0...0> for eq_1 to hold

## Initial state

|x\rangle_x \otimes |y\rangle_y \otimes |0\cdots0\rangle_a for a computational-basis test input (x,y); for the OR_3 instance x \in \{0,1\}^3, y \in \{0,1\}.

## Measurement

None intrinsic to the oracle (it is a unitary). For validation of the tiny instance: for each of the 16 basis inputs (x,y) with x in {0,1}^3, y in {0,1}, measure the y register (and ancillas) in the computational basis after applying C_f.

## Classical postprocessing

Check that the measured target bit equals y XOR OR_3(x) with probability 1 for every basis input and that all ancilla outcomes are 0; any nonzero failure probability would contradict the exactness claim of eq_6. Also record the circuit depth over the stated gate set and check it does not increase when the construction is instantiated at larger n.

## Algorithm steps

1. Fix the target function f (instance: f = OR_3, eq_4) and the elementary gate set: single-qubit gates, R_Z(theta) for arbitrary theta (eq_3), and unbounded fan-out F_m (eq_2), each counted as depth 1. (eq_2, eq_3, eq_4)
2. Apply the constant-depth circuit C_f realizing U_f (eq_1) with depth bound eq_6. The abstract asserts existence; the specific gate sequence is not available. A plausible (background, not sourced) skeleton is: fan-out copies of input/ancilla bits in O(1) layers, a layer of Z-rotations producing Hamming-weight-dependent phases (eq_5), interference via Hadamards to convert the phase information into the bit f(x), and fan-out-based uncomputation of ancillas. (eq_1, eq_5, eq_6)
3. Verify ancillas are returned to |0...0> and the target register holds y XOR f(x), so the overall action on (x,y) matches eq_1 exactly (no approximation). (eq_1, eq_6)

## Assumptions

- No experiment_scope was supplied; the tiny instance OR_3 (3 input qubits, 1 target) was chosen as the smallest useful illustration of the corollary
- Oracle means bit-flip oracle (eq_1), ancillas returned to |0>
- Depth model: single-qubit gates, arbitrary R_Z, and unbounded fan-out each have depth 1; the abstract's MBQC equivalence is taken as given, not reconstructed
- eq_5 is a standard primitive offered as a building block, not the paper's construction

## Missing information

- The explicit constant-depth circuit (gate sequence, rotation angles, ancilla count) for a general classical function f
- The explicit exact constant-depth OR_n construction and how it avoids the approximation inherent in earlier fan-out-based OR circuits
- The precise statement and proof of the MBQC <-> (R_Z + fan-out) circuit-model depth equivalence, including the MBQC resource state and measurement patterns
- Whether the result allows ancilla counts polynomial in n and what the depth constant is
- Whether the oracle convention is bit-flip or phase, and whether f is required to be efficiently computable classically (e.g., any f, or f given by a classical circuit)
