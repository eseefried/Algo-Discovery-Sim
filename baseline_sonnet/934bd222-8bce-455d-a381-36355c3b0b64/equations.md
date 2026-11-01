# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Identify a Boolean function f:{0,1}^n->{0,1} that is linear, f(x)=a.x, or affine, f(x)=a.x xor b, using one oracle query (BV) or two queries, with certainty for fully specified functions; the incompletely defined case is only noted.

Scope: Tiny instance n=2 with standard phase-oracle BV (one query) for linear f, plus an assumed two-query affine identification that runs BV and then a second query on the all-zero input to read off b. Incompletely defined functions, the 2/3 bounded-error analysis, the specific classes of partial functions, and the paper's actual two-query construction are outside the scope.

## Symbols

- $n$: number of input bits; domain: positive integer; n=2 in the tiny instance
- $a$: hidden linear coefficient string; domain: {0,1}^n
- $b$: hidden affine offset bit; domain: {0,1}
- $f$: Boolean function f(x)=a.x xor b; domain: {0,1}^n -> {0,1}
- $U_f$: phase oracle |x> -> (-1)^{f(x)}|x>; domain: unitary on n qubits
- $H^{\otimes n}$: Hadamard transform on n qubits; domain: unitary

## eq_1: Affine function form

$$
f(x)=a\cdot x\oplus b,\quad a\in\{0,1\}^n,\ b\in\{0,1\}
$$

Linear functions correspond to b=0; affine functions allow arbitrary b.

Provenance: `abstract_inferred`. The abstract refers to linear and affine Boolean functions; the standard definition of these is used for the explicit form.

Abstract evidence: if the provided Boolean function is affine

Equation assumptions:

- Standard definition of affine Boolean function over GF(2)

## eq_2: Phase oracle

$$
U_f|x\rangle=(-1)^{f(x)}|x\rangle
$$

Oracle convention used in the construction.

Provenance: `assumption`. The abstract does not specify the oracle form; the phase oracle is the common choice.

Equation assumptions:

- Phase-oracle form rather than a bit-flip oracle with ancilla

## eq_3: BV output state

$$
H^{\otimes n}U_fH^{\otimes n}|0^n\rangle=(-1)^{b}|a\rangle
$$

One query yields a with certainty, up to a global phase (-1)^b that is unobservable, so b is not recovered.

Provenance: `standard_background`. Standard BV derivation using the identity sum_x (-1)^{a.x xor y.x} = 2^n delta_{a,y}.

Equation assumptions:

- f fully specified
- f affine as in eq_1

## eq_4: Offset from f(0)

$$
f(0^n)=b
$$

Given a, the offset is the value of f at the zero input. A second query, e.g. a phase kickback or interference measurement, can determine it.

Provenance: `assumption`. A simple construction consistent with the abstract's claim that one more query is needed for affinity, but it is not the paper's stated method.

Equation assumptions:

- The second query is used to extract b; the exact circuit is not given in the abstract

## eq_5: Success threshold for incomplete functions

$$
\Pr[\text{success}]\ge \tfrac{2}{3}
$$

The bounded-error success criterion for the incompletely defined case.

Provenance: `abstract_explicit`. Stated directly in the abstract; the classes of functions for which it holds are not specified.

Abstract evidence: with probability of success at least $2/3$

## Registers

- x: n (=2 in the instance) qubits; input register carrying the query, initial |0^n>
- anc: 1 (optional) qubits; possible ancilla or control qubit for the second query

## Initial state

|0^n> on the input register, in the n=2 instance |00>

## Measurement

Computational-basis measurement of the input register after the BV circuit gives a; the second measurement gives b under the assumed construction.

## Classical postprocessing

Output f(x)=a.x xor b; the affine versus linear decision is b=1 versus b=0 (that is, f is linear iff b=0).

## Algorithm steps

1. Query 1 (BV): apply H^{\otimes n}, then U_f, then H^{\otimes n}, and measure in the computational basis to obtain a. (eq_2, eq_3)
2. Query 2 (assumed): determine b=f(0^n) by a second query using an interference or control construction. The details are not specified in the abstract. (eq_4, eq_1)

## Assumptions

- Phase oracle model
- n=2 tiny instance
- Second-query circuit is a placeholder, not the paper's method

## Missing information

- Actual two-query algorithm circuit
- Definition of the incompletely defined function classes
- Analysis proving the 2/3 success probability
- Oracle model used in the paper
