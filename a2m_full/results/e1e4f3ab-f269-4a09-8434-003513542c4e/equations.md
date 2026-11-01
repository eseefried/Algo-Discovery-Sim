# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Identify an unknown multilinear polynomial f of degree <=d in n variables over F_q exactly, using O(n^{d-1}) quantum queries for constant d. Scoped instance: q=2, n=3, d=2, with a phase oracle U_f|x>=(-1)^{f(x)}|x> and degree-1 Bernstein-Vazirani as the base subroutine.

Scope: Smallest useful construction: q=2, n=3, d=2. Recursion on degree through discrete derivatives D_{e_i}f, with BV used on each derivative. Out of scope: general q (QFT over F_q), the paper's actual exact algorithm and optimality proof, the lower bound, and the Reed-Muller decoding details beyond the identification f <-> codeword. The recursion here is an assumed reconstruction, and the paper's algorithm may be more refined.

## Symbols

- $q$: field size (prime power); domain: q=2 in the scoped instance
- $n$: number of variables; domain: positive integer, n=3 in the scoped instance
- $d$: degree bound; domain: positive integer, d=2 in the scoped instance
- $f$: multilinear polynomial \sum_{S\subseteq[n],|S|\le d} c_S \prod_{i\in S}x_i; domain: F_q^n \to F_q
- $c_S$: coefficient of monomial S; domain: F_q
- $D_y f$: discrete derivative f(x+y)-f(x); domain: function F_q^n \to F_q
- $e_i$: i-th basis vector; domain: F_q^n
- $T(n,d)$: query count of the recursion; domain: nonnegative integers
- $\omega$: primitive p-th root of unity, e^{2\pi i/p}, with p the characteristic of F_q; equals -1 for q=2; domain: complex

## eq_1: Phase oracle

$$
U_f|x\rangle=\omega^{\mathrm{Tr}(f(x))}|x\rangle
$$

Phase oracle form. For q=2 it is (-1)^{f(x)}. It is obtained from an XOR oracle by kickback with an ancilla in the Fourier state.

Provenance: `assumption`. The sketch assumes the oracle model. The abstract only says 'queries to the polynomial'.

Equation assumptions:

- Oracle convertible to a phase oracle by kickback

## eq_2: BV base case

$$
H^{\otimes n}U_{f}H^{\otimes n}|0^n\rangle=(-1)^{b}|a\rangle,\quad f(x)=a\cdot x+b
$$

For a degree-1 function over F_2, a single query returns a exactly. b is only a global phase, so it needs a separate evaluation, for example a query on |0> or a controlled version.

Provenance: `standard_background`. Standard Bernstein-Vazirani. The affine offset b is not recovered from this circuit alone.

Equation assumptions:

- q=2

## eq_3: Derivative of a multilinear polynomial

$$
D_{e_i}f(x)=f(x+e_i)-f(x)=\partial_i f(x)=\sum_{S\ni i}c_S\prod_{j\in S\setminus\{i\}}x_j
$$

The derivative along e_i has degree <=d-1 and does not depend on x_i. It is implemented by U_f(shift by e_i)U_f^{-1}, which costs 2 queries. For q=2 the phase is (-1)^{f(x+e_i)+f(x)}.

Provenance: `abstract_inferred`. This is a derivative reduction, inferred from the family sketch. It is not stated in the abstract.

Abstract evidence: identify an unknown multilinear polynomial of degree d in n variables over a finite field Fq

Equation assumptions:

- Multilinear: each variable has degree at most 1
- Phase oracle with its inverse available

## eq_4: Query recursion

$$
T(n,d)=n\,T(n-1,d-1)+O(1),\quad T(n,1)=O(1)\Rightarrow T(n,d)=O(n^{d-1})
$$

Recursion giving the claimed query count for constant d. This is an assumed reconstruction that matches the abstract's O(n^{d-1}) claim.

Provenance: `abstract_inferred`. The recursion is consistent with the claimed bound. The paper's actual recursion may differ.

Abstract evidence: uses O(nd-1 ) queries for constant d

Equation assumptions:

- Each derivative query costs O(1) oracle calls

## eq_5: Classical reassembly

$$
c_S=\big[\partial_i f\big]_{S\setminus\{i\}}\ \text{for any } i\in S,\qquad c_\emptyset=f(0)
$$

The coefficient of S is read from the coefficient of S\{i} in the learned derivative. The constant term comes from a direct evaluation of f(0), via a query with a Fourier ancilla.

Provenance: `assumption`. This follows from eq_3 and is a proposed combination step.

Equation assumptions:

- Derivatives learned exactly

## Registers

- x: n*ceil(log2 q) = 3 qubits in the scoped instance qubits; input register, one qudit per variable; reused sequentially in the recursion
- anc: ceil(log2 q) = 1 qubit qubits; phase-kickback ancilla in the Fourier state, only for the XOR oracle

## Initial state

|0>^{n} on x. For an XOR oracle, anc is in |-> (q=2).

## Measurement

Measure the n-1 data qubits in the computational basis after the final Hadamards in each BV run. In Qiskit the counts string is little-endian, so qubit j is bits[::-1][j]. Do not measure in unitary tasks.

## Classical postprocessing

Map the measured bitstrings from each BV run to the coefficients c_{ij}. Reconcile the redundant estimates of c_{ij} obtained from i and from j, which should agree. Combine with c_i and c_empty into the full coefficient list, or the truth table for Reed-Muller decoding.

## Algorithm steps

1. For d=2, n=3, and each i in {1,2,3}, build the derivative phase oracle on the other n-1 variables by fixing x_i=0: x -> shift e_i -> query U_f -> shift back -> query U_f^{-1}. Apply this to the remaining 2 qubits. The result is a phase oracle for the degree-1 function ∂_i f. (eq_3)
2. Run BV on each ∂_i f: Hadamards, derivative oracle, Hadamards, then measure the 2 qubits. This gives the linear coefficients c_{ij}. The offset of ∂_i f, which is c_{i}, needs one extra evaluation of ∂_i f(0)=f(e_i)-f(0), for example via a Fourier-ancilla query or a bit-test. (eq_2, eq_3)
3. Evaluate f(0) by one query, to get c_empty. Reassemble all c_S classically. (eq_5)
4. Count total queries against the recursion bound. (eq_4)

## Assumptions

- Scoped to q=2, n=3, d=2 as one small choice, not given by the abstract
- The recursion and the use of the e_i directions come from the sketch, not the abstract
- Derivative oracles with fixed x_i=0 may need a query to f at shifted inputs, which a placeholder oracle gate acting on all n qubits permits
- Constant terms are read by evaluations, not by BV phase

## Missing information

- The paper's actual exact algorithm and its optimality argument
- The exact query counts and constants in the recursion
- The handling of general q, including the QFT over F_q
- How it achieves exactness for non-binary fields
- The Reed-Muller decoding details
