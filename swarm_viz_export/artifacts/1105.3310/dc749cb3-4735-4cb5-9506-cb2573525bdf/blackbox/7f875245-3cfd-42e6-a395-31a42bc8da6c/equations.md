# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Exactly identify an unknown multilinear polynomial f over F_2 in n=3 variables, degree at most 2 (7 coefficients c_0, c_1, c_2, c_3, c_12, c_13, c_23), using a naive derivative-based Bernstein-Vazirani scheme. Coefficients are hard-coded into compiled gates for functional simulation only. No query-complexity claim is made.

Scope: Only the tiny instance n=3, d=2, q=2 with a naive 10-qubit identification circuit that recovers all 7 coefficients. It is NOT the paper's O(n^(d-1)) exact quantum algorithm and does not demonstrate any query advantage. Because the coefficients are compiled into the gates, it shows only that the coefficients can be read back from classical build parameters. Out of scope: general q and d, the optimal query construction and orthogonality argument, the lower bound, and any black-box query-count certification.

## Symbols

- $c_S$: coefficient of the monomial prod_{i in S} x_i; domain: F_2, S subset of {1,2,3}, |S|<=2
- $f$: multilinear polynomial; domain: F_2^3 -> F_2
- $D_i f$: discrete derivative f(x+e_i)+f(x); domain: affine function of x_j, j!=i
- $l^{(i)}$: linear part of D_i f restricted to variables j!=i, with l^{(i)}_j=c_{ij}; domain: F_2^2

## eq_1: Multilinear polynomial

$$
f(x)=\sum_{S\subseteq[3],|S|\le 2}c_S\prod_{i\in S}x_i \pmod 2
$$

Parametrization of the unknown polynomial with 7 coefficients.

Provenance: `abstract_inferred`. The abstract names multilinear polynomials of degree d. The explicit sum form is standard, specialized to q=2, n=3, d=2.

Abstract evidence: identify an unknown multilinear polynomial of degree d in n variables over a finite field Fq

Equation assumptions:

- q=2
- n=3
- d=2

## eq_2: Derivative of a multilinear polynomial

$$
D_if(x)=f(x+e_i)+f(x)=c_i+\sum_{j\ne i}c_{ij}x_j \pmod 2
$$

For degree<=2 multilinear f, the derivative in direction e_i is affine and independent of x_i.

Provenance: `standard_background`. Direct expansion over F_2 using x_i^2=x_i. Used as a candidate degree-reduction step, not claimed to be the paper's method.

Equation assumptions:

- multilinear

## eq_3: Restricted phase gate for derivative block

$$
U_i|x'\rangle=(-1)^{D_if(x')}|x'\rangle,\quad x'\in F_2^2\ (\text{variables }j\ne i)
$$

Diagonal phase on the 2-qubit register of block i, compiled directly from the classical coefficients: Z on qubit j if c_ij=1, plus a global phase (-1)^{c_i} handled by the ancilla.

Provenance: `assumption`. Equals f(x'+e_i)+f(x') by eq_2. Compiled with classical coefficients, so no oracle calls are made.

Equation assumptions:

- Coefficients are classical build parameters

## eq_4: Controlled BV block

$$
(H\otimes H^{\otimes 2})\,C\text{-}U_i\,(H\otimes H^{\otimes 2})|0\rangle|00\rangle=|c_i\rangle|l^{(i)}\rangle
$$

Ancilla a_i in |+> controls the phase (-1)^{b(c_i+l.x')}. H on x' yields |l^{(i)}> and H on a_i yields |c_i>.

Provenance: `assumption`. Exact BV identity for affine phases with kickback on the ancilla.

Equation assumptions:

- Derivative phase compiled directly

## eq_5: Constant term

$$
H\,Z^{c_0}\,H|0\rangle_{a_0}=|c_0\rangle_{a_0}
$$

The constant f(0)=c_0 is read from a single ancilla by a Z gate if c_0=1. This is a classical shortcut since c_0 is compiled in.

Provenance: `assumption`. f(0)=c_0 by eq_1.

Equation assumptions:

- Shortcut, not an oracle query

## Registers

- a0: 1 qubits; Qubit 0. Output c_0.
- a1,a2,a3: 3 qubits; Qubits 1,2,3. Output c_1,c_2,c_3.
- x1: 2 qubits; Qubits 4,5 holding variables (x_2,x_3) for block 1. Output (c_12,c_13).
- x2: 2 qubits; Qubits 6,7 holding (x_1,x_3) for block 2. Output (c_12,c_23).
- x3: 2 qubits; Qubits 8,9 holding (x_1,x_2) for block 3. Output (c_13,c_23).

## Initial state

All 10 qubits in |0>.

## Measurement

Circuit is measurement-free. Read the computational basis state of the final state. Qubit 0 gives c_0, qubits 1-3 give c_1..c_3, qubits 4-9 give pairwise coefficients.

## Classical postprocessing

Fixed map with qubit indices 0..9, qubit 0 least significant: c_0=q0, c_1=q1, c_2=q2, c_3=q3, c_12=q4 (redundantly q6), c_13=q5 (redundantly q8), c_23=q7 (redundantly q9). Redundant copies must agree.

## Algorithm steps

1. Apply H to all 10 qubits. (eq_4)
2. For each i, apply the controlled restricted phase C-U_i with control a_i and target x_i register: CZ(a_i, x_i[j]) if c_ij=1, and Z on a_i if c_i=1. (eq_2, eq_3)
3. Apply Z on a0 if c_0=1. (eq_5)
4. Apply H to all 10 qubits. The final state is a computational basis state encoding all coefficients. (eq_4, eq_5)

## Assumptions

- Tiny instance n=3, d=2, q=2 chosen by me
- Coefficients hard-coded into gates
- Naive scheme, no query-efficiency claim
- Only monomials with |S|<=2 are accepted, keys outside this set must be rejected, and missing keys mean 0
- Only n=3, d=2 is covered

## Missing information

- The paper's actual exact O(n^(d-1)) query algorithm and its state-orthogonality construction
- General q and d
- Optimality proof
