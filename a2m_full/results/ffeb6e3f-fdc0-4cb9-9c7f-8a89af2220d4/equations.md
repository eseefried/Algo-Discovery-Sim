# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a standard XOR oracle U_f|x>|y>=|x>|y xor f(x)> for f(x)=a.x xor b on n bits, recover a with one BV query and decide linear (b=0) versus affine non-linear (b=1) with a second query. Incompletely defined variant: f is known only on a subset D of {0,1}^n, and the BV output distribution is used as a bounded-error test.

Scope: Smallest construction: n=2 (3 qubits for query 1; the second-query circuit uses n+1 qubits or fewer), fully defined affine f, two queries, deterministic. The incompletely-defined-domain case is given only as the output-distribution formula under an assumed promise class. The precise classes of incompletely defined functions in the paper, and the proof of the 2/3 bound, are outside scope.

## Symbols

- $n$: number of input bits; domain: positive integer, e.g. 2
- $a$: linear coefficient string; domain: {0,1}^n
- $b$: affine offset bit; domain: {0,1}
- $f$: Boolean function f(x)=a.x xor b; domain: {0,1}^n -> {0,1}
- $D$: defined subset of inputs for an incompletely defined f; domain: subset of {0,1}^n
- $s$: measured n-bit string from the BV query; domain: {0,1}^n
- $x_0$: known defined input used in the second query (0^n if defined); domain: element of D

## eq_1: XOR oracle

$$
U_f|x\rangle|y\rangle=|x\rangle|y\oplus f(x)\rangle
$$

Standard oracle acting on n input qubits and one target qubit.

Provenance: `standard_background`. Standard oracle model; the sketch assumes it, and the abstract only mentions queries to the oracle.

Equation assumptions:

- Standard XOR oracle with an ancilla target

## eq_2: BV output state, fully defined affine f

$$
H^{\otimes n}\,\Big(2^{-n/2}\sum_x(-1)^{a\cdot x\oplus b}|x\rangle\Big)=(-1)^b|a\rangle
$$

With the target in |->, the oracle gives phase (-1)^{f(x)}. After the final H^n the input register is |a> up to a global phase (-1)^b, so s=a with certainty and b is unobservable from query 1.

Provenance: `standard_background`. Standard BV analysis extended to the affine case. The abstract implies one query is not enough to identify affinity, consistent with b being a global phase.

Equation assumptions:

- Target ancilla prepared in |->=(|0>-|1>)/sqrt2

## eq_3: Second query reads offset

$$
U_f|0^n\rangle|0\rangle=|0^n\rangle|f(0^n)\rangle=|0^n\rangle|b\rangle
$$

Measuring the target gives b=f(0). The function is linear iff b=0 and affine non-linear iff b=1.

Provenance: `assumption`. The abstract says one more query is needed. Evaluating f(0) is one proposed way to use it, and the paper's actual second query may differ.

Equation assumptions:

- 0^n is in the defined domain
- Computational-basis evaluation counts as a query

## eq_4: Offset from any defined point

$$
b=f(x_0)\oplus (s\cdot x_0)
$$

If 0^n is undefined, use the measured s=a and a defined point x_0 to compute b classically.

Provenance: `assumption`. Follows from f(x)=a.x xor b once a is known. Requires f(x_0) from a query.

Equation assumptions:

- s=a was obtained
- x_0 in D

## eq_5: BV output distribution on partial domain

$$
P(s)=\Big|2^{-n}\sum_{x\in D}(-1)^{f(x)\oplus s\cdot x}\Big|^2
$$

Undefined inputs contribute zero amplitude. The method succeeds if P(a) is at least 2/3 and a is the most probable string.

Provenance: `abstract_inferred`. The abstract claims bounded-error success on certain classes of incompletely defined functions. The formula is the natural BV distribution with undefined terms dropped, and the sketch states it.

Abstract evidence: with probability of success at least $2/3$

Equation assumptions:

- Undefined terms contribute 0
- Promise class guarantees P(a)>=2/3

## Registers

- x: n qubits; input register, measured to give s; Qiskit classical bit i holds s_i, so read counts keys reversed
- t: 1 qubits; oracle target; |-> in query 1, |0> in query 2 where f(0) is read directly

## Initial state

Query 1: |0^n>|1> with H on all qubits, giving |+^n>|->. Query 2: |0^n>|0>.

## Measurement

Query 1: measure the n input qubits in the computational basis. Query 2: measure the target qubit. Use little-endian reversal when reading s.

## Classical postprocessing

a=s (most frequent string for partial domains). b=f(0), or f(x_0) xor s.x_0. Output linear if b=0, otherwise affine non-linear.

## Algorithm steps

1. Query 1: prepare target in |->, apply H^n to the input register, apply the oracle once, apply H^n, measure the input register to get s=a. Reverse the counts key to index bits. (eq_1, eq_2)
2. Query 2: on |0^n>|0> apply the oracle once and measure the target to get b=f(0). Decide linear if b=0, affine non-linear if b=1. (eq_3)
3. If 0^n is undefined, query a defined x_0 and compute b classically from s. (eq_4)
4. Partial-domain case: run the same BV circuit and take the most frequent s from the histogram. (eq_5)

## Assumptions

- Smallest instance n=2
- Second query is a computational-basis evaluation at a known defined point
- Promise class for partial domains is not specified, only assumed to give P(a)>=2/3
- Qiskit little-endian ordering

## Missing information

- Exact classes of incompletely defined linear and affine functions
- The paper's actual second-query circuit, which may differ from evaluating f(0)
- Proof or threshold for the 2/3 bound
- How undefined inputs are implemented in the oracle
