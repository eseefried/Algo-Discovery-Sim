# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Exactly identify an unknown multilinear polynomial f over F_2 in n=3 variables with degree at most 2 (7 coefficients: c_0, c_1..c_3, c_12, c_13, c_23) using a naive derivative-based Bernstein-Vazirani scheme. The coefficients are hard-coded into the oracle for functional simulation only, and no query-complexity claim is made.

Scope: Only the tiny instance n=3, d=2, q=2, with a naive full-identification circuit that recovers all 7 coefficients exactly. It runs three controlled-derivative BV blocks, one per direction e_i, plus one f(0) block. Each block uses its own register. This costs 7 controlled-oracle calls, versus 7 classical monomials, so it is NOT the paper's O(n^(d-1)) exact algorithm. Out of scope: general q and d, the optimal query construction and orthogonality argument, the lower bound, and any black-box query-count certification.

## Symbols

- $n$: number of variables; domain: positive integer, n=3
- $d$: degree bound; domain: positive integer, d=2
- $c_S$: coefficient of monomial prod_{i in S} x_i; domain: F_2, S subset of {1,2,3}, |S|<=2
- $f$: multilinear polynomial over F_2; domain: F_2^3 -> F_2
- $D_i f$: discrete derivative f(x+e_i)+f(x); domain: F_2-valued affine function for d=2
- $l^{(i)}$: linear part of D_i f as a bit vector, with l^{(i)}_j=c_{ij} for j!=i and l^{(i)}_i=0; domain: F_2^3

## eq_1: Multilinear polynomial

$$
f(x)=\sum_{S\subseteq[3],|S|\le 2}c_S\prod_{i\in S}x_i \pmod 2
$$

Parametrization of the unknown polynomial, with 7 coefficients for n=3, d=2.

Provenance: `abstract_inferred`. The abstract names multilinear polynomials of degree d. The explicit sum form is a standard definition, specialized to q=2.

Abstract evidence: identify an unknown multilinear polynomial of degree d in n variables over a finite field Fq

Equation assumptions:

- q=2
- n=3
- d=2

## eq_2: Phase oracle and its controlled version

$$
O_f|x\rangle=(-1)^{f(x)}|x\rangle,\qquad C\text{-}O_f|b\rangle|x\rangle=(-1)^{b f(x)}|b\rangle|x\rangle
$$

The oracle is diagonal. Each monomial is compiled into Z, CZ or CCZ on x, and the controlled version adds one control qubit b (CZ, CCZ, CCCZ).

Provenance: `assumption`. Explicit classical coefficients are compiled into gates for functional simulation. This is not an opaque oracle.

Equation assumptions:

- Coefficients are classical build parameters
- No query counting is certified

## eq_3: Derivative of a multilinear polynomial

$$
D_if(x)=f(x+e_i)+f(x)=c_i+\sum_{j\ne i}c_{ij}x_j \pmod 2
$$

For multilinear f with deg<=2 the derivative in direction e_i is affine and independent of x_i. Its constant term is c_i and its linear part is l^{(i)}.

Provenance: `standard_background`. Direct expansion over F_2 with x_i^2=x_i. It is used as a candidate degree-reduction step and is not claimed to be the paper's method.

Equation assumptions:

- multilinear, so each variable appears with exponent at most 1

## eq_4: Controlled-derivative BV block

$$
(H\otimes H^{\otimes 3})\,\mathrm{C\text{-}}(O_fX_iO_fX_i)\,(H\otimes H^{\otimes 3})|0\rangle|000\rangle=|c_i\rangle|l^{(i)}\rangle
$$

The ancilla a_i is in |+> and the x^{(i)} register is uniform. The controlled phase is (-1)^{b D_if(x)}, with X_i acting on qubit i of x^{(i)}, and it uses two controlled-O_f calls. The H layers then give the affine function's constant c_i on a_i and its linear part on x^{(i)}. Phase kickback onto b makes the constant exactly recoverable, with no global-phase loss.

Provenance: `assumption`. Exact identity from eq_2 and eq_3. The phase is (-1)^{b(c_i+l.x)}. H on x gives |l> with sign (-1)^{b c_i}, and H on b gives |c_i>.

Equation assumptions:

- Derivative oracle built from two controlled-O_f calls
- Not query-optimal

## eq_5: Constant term block

$$
H\,\mathrm{C\text{-}}O_f\,H\,|0\rangle_{a_0}|000\rangle_{z}=|c_0\rangle_{a_0}|000\rangle_{z}
$$

The z register stays in |000>, so the controlled phase is (-1)^{b f(0)}=(-1)^{b c_0}. H on a_0 then reads out c_0.

Provenance: `assumption`. f(0)=c_0 by eq_1. The controlled oracle turns the global sign into a relative phase.

Equation assumptions:

- The z register is not Hadamarded

## Registers

- x1: 3 qubits; BV register for the e_1 derivative block. Qubit j is x_j, with qubit 0 least significant. Output is l^{(1)}=(0,c_12,c_13).
- x2: 3 qubits; BV register for the e_2 derivative block. Output is l^{(2)}=(c_12,0,c_23).
- x3: 3 qubits; BV register for the e_3 derivative block. Output is l^{(3)}=(c_13,c_23,0).
- a1: 1 qubits; Control/kickback ancilla for block 1. Output is c_1.
- a2: 1 qubits; Control/kickback ancilla for block 2. Output is c_2.
- a3: 1 qubits; Control/kickback ancilla for block 3. Output is c_3.
- a0: 1 qubits; Ancilla for the constant block. Output is c_0 (the oracle acts on a fixed |000> register, so 3 extra qubits are needed unless one reuses the x registers).
- z: 3 qubits; Fixed |000> register on which the controlled oracle is evaluated for the c_0 block

## Initial state

All qubits in |0>; total 16 qubits (x1,x2,x3: 9; a1,a2,a3,a0: 4; z: 3).

## Measurement

Output decoding: the circuit is measurement-free, so read the computational-basis state of the final simulated state. Read c_0 from a0, c_i from a_i, and c_ij from x_i qubit j (j!=i). The c_ij are redundantly available from x_i and x_j and should agree.

## Classical postprocessing

Fixed classical map: c_0=a0, c_i=a_i, c_12=x1[2] (equal to x2[1]), c_13=x1[3], c_23=x2[3], with 1-indexed qubit positions inside each x register. Check redundancy consistency x_i[j]=x_j[i].

## Algorithm steps

1. Input preparation: apply H to every qubit of x1,x2,x3 and to a0,a1,a2,a3. Leave z in |000>. The coefficients c_S are classical build parameters compiled into the oracle. (eq_2)
2. For each i in {1,2,3}: apply C-O_f (control a_i, target x_i), then X on qubit i of x_i, then C-O_f again, then X on qubit i of x_i. This implements the controlled derivative phase. (eq_2, eq_3, eq_4)
3. Constant block: apply C-O_f with control a0 and target z (in |000>). (eq_2, eq_5)
4. Apply H to all qubits of x1,x2,x3 and to a0,a1,a2,a3. The final state is a computational basis state encoding all coefficients. (eq_4, eq_5)

## Assumptions

- Tiny instance n=3, d=2, q=2 chosen by me
- Coefficients hard-coded into the oracle
- Naive derivative-BV scheme using 7 controlled-oracle calls, no query-efficiency claim
- The oracle only accepts monomials with |S|<=2
- Qubit j of each x register holds x_j, with qubit 0 as x_1

## Missing information

- The paper's actual exact O(n^(d-1)) query algorithm and its state-orthogonality construction
- General q and d
- Optimality proof
