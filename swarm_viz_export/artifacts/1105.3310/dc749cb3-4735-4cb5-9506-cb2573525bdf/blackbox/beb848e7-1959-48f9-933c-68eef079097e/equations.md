# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Identify an unknown multilinear polynomial f over F_2 of degree at most d in n variables (coefficients c_S) using phase-oracle queries. Tiny instance: n=3, d=2, 7 unknown coefficients (constant, 3 linear, 3 quadratic) with coefficients hard-coded into the oracle for functional simulation only.

Scope: Only the tiny instance n=3, d=2, q=2. The circuit is a Walsh-spectrum / Bernstein-Vazirani-style construction applied to (-1)^f, including the derivative-degree-reduction identity. The paper's O(n^(d-1)) query-efficient exact algorithm, general q and d, the lower bound and the query-complexity proof are out of scope. No black-box query count is certified.

## Symbols

- $n$: number of variables; domain: positive integer, n=3 in the instance
- $d$: degree bound; domain: positive integer, d=2
- $c_S$: coefficient of monomial x_S; domain: F_2, S subset of {1..n}, |S|<=d
- $f$: multilinear polynomial f(x)=sum_S c_S prod_{i in S} x_i; domain: F_2^n -> F_2
- $D_a f$: discrete derivative f(x+a)+f(x); domain: F_2-valued, degree <= d-1
- $\hat F(s)$: normalized Walsh coefficient of (-1)^f; domain: real, in [-1,1]

## eq_1: Multilinear polynomial

$$
f(x)=\sum_{S\subseteq[n],\,|S|\le d} c_S\prod_{i\in S}x_i \pmod 2
$$

Parametrization of the unknown polynomial over F_2; the monomial count is sum_{i<=d} C(n,i), which is 7 for n=3, d=2.

Provenance: `abstract_inferred`. The abstract names multilinear polynomials of degree d; the explicit sum form is a standard definition. The native predictions (2) to (8) use exponents up to d and a prime p, which would not be multilinear over F_2, so I reject them.

Abstract evidence: identify an unknown multilinear polynomial of degree d in n variables over a finite field Fq

Equation assumptions:

- q=2

## eq_2: Phase oracle

$$
O_f|x\rangle=(-1)^{f(x)}|x\rangle
$$

Diagonal unitary with the coefficients c_S compiled into gates: one Z-type phase for each monomial, built with Z, CZ and CCZ for |S|=1,2,3.

Provenance: `assumption`. The sketch fixes a functional-simulation oracle with hard-coded coefficients. This is not an opaque oracle.

Equation assumptions:

- The coefficients are explicit classical parameters
- No query counting

## eq_3: Walsh transform circuit

$$
H^{\otimes n}O_fH^{\otimes n}|0^n\rangle=\sum_{s}\hat F(s)|s\rangle,\quad \hat F(s)=2^{-n}\sum_x(-1)^{f(x)+s\cdot x}
$$

One query gives the Walsh spectrum of (-1)^f. For affine f it is a single basis state |s=linear part> (the Bernstein-Vazirani case). The constant term appears only as a global sign.

Provenance: `standard_background`. Standard Fourier sampling identity. For degree 2 it does not determine f by itself.

## eq_4: Derivative degree reduction

$$
\deg(D_af)\le d-1,\qquad D_af(x)=f(x+a)+f(x)
$$

Derivatives in directions a=e_i reduce the degree. For d=2 each D_{e_i}f is affine, with linear part given by c_{ij} for j!=i and constant c_i + c_{ii}-type terms. For multilinear f, D_{e_i}f(x)=c_i+sum_{j!=i}c_{ij}x_j.

Provenance: `standard_background`. Standard property of discrete derivatives. It motivates recursion on degree but is not shown to be the paper's method.

Equation assumptions:

- multilinear, so x_i^2=x_i

## eq_5: Derivative phase oracle via two phase queries

$$
O_{D_af}=O_{f}\,(X^{a}O_{f}X^{a})\quad\text{since}\;(-1)^{f(x)}(-1)^{f(x+a)}=(-1)^{D_af(x)}
$$

A derivative phase oracle is built from two oracle calls. For a=e_i, one Bernstein-Vazirani run on this oracle returns the linear part of D_{e_i}f, i.e. c_{ij} for j!=i. A constant-term kickback ancilla is not needed because the constant is a global sign.

Provenance: `assumption`. Exact identity, but 3 derivative runs cost 6 queries, so this is not the paper's query-efficient scheme.

Equation assumptions:

- Query cost not optimized

## Registers

- x: 3 qubits; input register, with Walsh outcome s read from it after final H

## Initial state

|000> on x

## Measurement

Computational-basis measurement of the x register after the final H in each run. The runner's circuit is measurement-free, so outcomes would be read from the simulated state.

## Classical postprocessing

Read c_{ij} from the derivative-run bitstrings, with c_{ij}=c_{ji}. The linear coefficients c_i and constant c_0 need extra runs, and c_0 is not recoverable.

## Algorithm steps

1. Reference run (BV on f): H on all qubits, apply O_f, H on all qubits. This gives the Walsh spectrum of (-1)^f. (eq_2, eq_3)
2. For each i in {1,2,3}, build O_{D_{e_i}f} from O_f and X_i, then run H, O_{D_{e_i}f}, H on a fresh x register. For multilinear f the derivative is affine, so the outcome is the basis state |c_{ij} for j!=i>, which gives the quadratic coefficients. (eq_4, eq_5)
3. Classical decoding: the quadratic c_{ij} are read directly from the derivative runs. Linear coefficients c_i come from the signs or constants of the derivative runs, or from f(e_i) values. These need a sign or constant extraction that this sketch does not provide with phase-only outputs, so they are only partially determined. c_0 is a global phase and is not recoverable from a phase oracle. (eq_1, eq_4)

## Assumptions

- Tiny instance n=3, d=2, q=2 chosen by me
- Coefficients hard-coded into the oracle
- Simple derivative-based scheme rather than the paper's O(n^(d-1)) algorithm
- Qubit ordering x1 is least significant

## Missing information

- The paper's actual exact query-efficient algorithm and state-orthogonality construction
- How linear and constant coefficients are recovered exactly
- General q and d
- Optimality proof
