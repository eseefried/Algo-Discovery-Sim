# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Evaluate a Boolean formula built from binary NAND gates over N input variables using a discrete-query quantum algorithm; the abstract claims O(sqrt(N)) queries for balanced formulas and N^{1/2+O(1/sqrt(log N))} queries for arbitrary formulas.

Scope: Define the NAND formula evaluation problem and the stated query complexities, plus a tiny explicit instance (depth-2 balanced formula on N=4 inputs). The actual discrete-query algorithm (walk/span-program construction, unitaries, phase estimation or any subroutine) is outside scope and not reconstructed.

## Symbols

- $N$: number of input variables (leaves) of the formula; domain: positive integer
- $x_i$: i-th input bit; domain: {0,1}
- $\phi$: binary NAND formula over x_1..x_N; domain: Boolean function {0,1}^N -> {0,1}
- $Q(\phi)$: number of discrete oracle queries used by the algorithm; domain: nonnegative integer
- $O_x$: standard discrete query oracle; domain: unitary on index and target registers

## eq_1: NAND gate

$$
\mathrm{NAND}(a,b)=1\oplus(a\wedge b)=\neg(a\wedge b)
$$

Definition of the binary gate from which formulas are built.

Provenance: `standard_background`. Standard definition of NAND; the abstract only names NAND formulas.

Equation assumptions:

- a,b in {0,1}

## eq_2: Balanced-formula query bound

$$
Q(\phi_{\mathrm{balanced}})=O(\sqrt{N})
$$

Claimed query complexity for balanced binary NAND formulas.

Provenance: `abstract_explicit`. Directly stated complexity claim.

Abstract evidence: We present an O(√N) discrete query quantum algorithm for evaluating balanced binary NAND formulas

Equation assumptions:

- Discrete query model as in the abstract

## eq_3: Arbitrary-formula query bound

$$
Q(\phi)=O\!\left(N^{\frac12+O\left(\frac{1}{\sqrt{\log N}}\right)}\right)
$$

Claimed query complexity for arbitrary binary NAND formulas.

Provenance: `abstract_explicit`. The abstract text is garbled; I read the exponent as 1/2 + O(1/sqrt(log N)).

Abstract evidence: O(N 12 +O( 1 √logN ) ) discrete query quantum algorithm for evaluating arbitrary binary NAND formulas

Equation assumptions:

- Exponent reading 1/2+O(1/sqrt(log N)) from garbled extraction

## eq_4: Toy balanced instance

$$
\phi(x_1,x_2,x_3,x_4)=\mathrm{NAND}\big(\mathrm{NAND}(x_1,x_2),\mathrm{NAND}(x_3,x_4)\big)=(x_1\wedge x_2)\vee(x_3\wedge x_4)
$$

Smallest balanced depth-2 instance, N=4, equivalent to an OR of ANDs.

Provenance: `assumption`. Chosen as a tiny explicit instance; the equality follows from De Morgan's laws.

Equation assumptions:

- Instance chosen by me, not from the abstract

## eq_5: Discrete query oracle

$$
O_x\,|i\rangle|b\rangle=|i\rangle|b\oplus x_i\rangle
$$

Standard bit-flip oracle commonly meant by discrete queries.

Provenance: `standard_background`. The abstract does not define the query form; this is the usual convention.

Equation assumptions:

- Index register encodes i in binary
- The paper may use a different but equivalent oracle form

## Registers

- index: ceil(log2 N) qubits; binary-encoded input position i for oracle queries
- target: 1 qubits; oracle output qubit receiving x_i

## Algorithm steps

1. Fix the formula phi and the input access model via the bit-flip oracle. (eq_1, eq_5)
2. Specify the toy instance for later circuit generation (N=4). (eq_4)
3. Record the claimed query complexity targets that a full algorithm must meet. (eq_2, eq_3)

## Assumptions

- No scope given; chose the problem definition, complexity claims, and an N=4 balanced instance as the smallest useful construction.
- The oracle form is assumed standard.
- The garbled exponent in the abstract is interpreted as 1/2+O(1/sqrt(log N)).

## Missing information

- The algorithm construction itself (e.g. Hamiltonian, quantum walk, or span program, and any phase or time schedule)
- State preparation, working registers and gate decomposition
- Success probability and error handling
- Measurement and decision rule
- How arbitrary formulas are rebalanced or handled
- The precise discrete-query model
