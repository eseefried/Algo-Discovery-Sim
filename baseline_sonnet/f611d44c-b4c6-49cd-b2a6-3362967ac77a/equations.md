# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Implement a quantum oracle U_f|x>|y>=|x>|y xor f(x)> for an arbitrary classical Boolean function f in constant depth, via MBQC equivalence with a circuit model having arbitrary Z rotations and unbounded fan-out. The abstract gives no explicit construction.

Scope: Smallest useful instance: the n-bit OR (disjunction) oracle, with a background-style phase-polynomial form of a Boolean function as the Z-rotation ingredient. The actual constant-depth MBQC construction, its depth bound, and the exact OR implementation are outside scope and not reconstructed.

## Symbols

- $n$: number of input bits; domain: positive integer (tiny instance n=2 or 3 assumed)
- $f$: classical Boolean function; domain: f:{0,1}^n -> {0,1}
- $x$: input bit string; domain: {0,1}^n
- $y$: target bit; domain: {0,1}
- $U_f$: oracle unitary; domain: unitary on n+1 qubits
- $S$: subset of input indices; domain: subset of {1,...,n}
- $\hat f(S)$: Fourier (Walsh) coefficient of (-1)^{f}; domain: real
- $\theta_S$: Z-rotation angle for parity of subset S; domain: real, mod 2\pi
- $x_S$: parity of x over S; domain: {0,1}

## eq_1: Oracle action

$$
U_f|x\rangle|y\rangle=|x\rangle|y\oplus f(x)\rangle
$$

Standard definition of a quantum oracle implementing a classical function, with computational basis encoding of x and y.

Provenance: `abstract_inferred`. The abstract refers to oracles implementing classical functions; the bit-flip form is the standard meaning, not stated explicitly.

Abstract evidence: any quantum oracle implementing a classical function

Equation assumptions:

- Standard XOR-into-target oracle convention

## eq_2: Phase oracle from bit oracle

$$
U_f=(I\otimes H)\,\left(\sum_x (-1)^{f(x)}|x\rangle\langle x|\otimes I\right)(I\otimes H)
$$

The bit oracle equals a Hadamard-conjugated diagonal phase oracle on the target qubit.

Provenance: `standard_background`. Standard identity: H Z H = X controlled on f(x).

Equation assumptions:

- Z-type phase on target qubit controlled by f(x)

## eq_3: Walsh expansion of phase

$$
(-1)^{f(x)}=\sum_{S\subseteq[n]}\hat f(S)(-1)^{x_S},\quad x_S=\bigoplus_{i\in S}x_i
$$

Boolean function phase as a combination of parity characters, which relates to Z-rotations on parities computed with fan-out.

Provenance: `standard_background`. Standard Fourier analysis on the Boolean cube; not stated in the abstract.

## eq_4: Z rotation on parity

$$
R_Z(\theta_S)=\exp(-i\theta_S Z/2),\quad Z|b\rangle=(-1)^b|b\rangle
$$

Arbitrary Z-axis rotation as the elementary gate, to be applied to qubits holding parities x_S.

Provenance: `abstract_inferred`. The abstract names arbitrary Z rotations as elementary; the explicit form is standard. The angle schedule is not given and is not invented.

Abstract evidence: arbitrary rotations along $Z$ axis and unbounded fan-outs are elementary operations

Equation assumptions:

- Angles theta_S are left unspecified

## eq_5: Disjunction function

$$
\mathrm{OR}(x)=1\oplus\prod_{i=1}^{n}(1\oplus x_i)
$$

Boolean definition of the n-bit OR whose exact constant-depth oracle is the corollary.

Provenance: `abstract_inferred`. The OR function is the target of the corollary; the algebraic form is standard background.

Abstract evidence: disjunction can be implemented exactly in constant-depth

Equation assumptions:

- Construction of the constant-depth circuit is not given

## Registers

- x: n qubits; input register in computational basis, qubit i holds x_i
- y: 1 qubits; target qubit receiving f(x)
- anc: unknown qubits; ancillas for fan-out/parity computation and MBQC resource; count not given

## Initial state

|x>|y>|0...0> on computational basis input (or a superposition over x), with ancillas in |0>; assumed.

## Algorithm steps

1. Prepare input and target; the oracle is to be defined by the bit-flip action. (eq_1)
2. Conjugate the target with Hadamards to reduce to a phase oracle. (eq_2)
3. Express the phase (-1)^{f(x)} via parities; compute needed parities with unbounded fan-out/CNOT-type operations (specific scheme not given). (eq_3)
4. Apply Z rotations on parity qubits, uncompute parities; the angle schedule is missing from the abstract. Then the circuit is translated to MBQC through the stated equivalence. (eq_4)
5. For the OR instance, the target function is eq_5; the exact constant-depth circuit is not reconstructed. (eq_5)

## Assumptions

- Scope chosen by me: OR/phase-polynomial oracle as a tiny instance (n=2 or 3).
- Walsh-parity approach is a generic background route and not claimed to be the paper's method.
- Constant-depth property, MBQC pattern, and equivalence mapping are not derived.

## Missing information

- Actual constant-depth construction for arbitrary f
- Angle schedule and ancilla count
- MBQC measurement pattern and feed-forward correction rules
- Depth bound and exact OR construction
- Details of the circuit-MBQC equivalence
