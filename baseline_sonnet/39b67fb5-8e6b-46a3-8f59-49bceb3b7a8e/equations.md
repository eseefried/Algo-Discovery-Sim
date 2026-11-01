# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximate synthesis of an n-qubit diagonal unitary with k distinct phases over Clifford+T, minimizing phase-rotation (T) count; the abstract gives only the T-count bound, not the construction.

Scope: Smallest useful construction: the diagonal operator definition, the abstract's T-count bound, and a tiny assumed instance (n=2, k=2) with a background phase-polynomial/parity view. The paper's actual decomposition algorithm, entanglement cost E(n,k) formula, and decision boundary in (n,k,epsilon)-space remain outside scope.

## Symbols

- $n$: number of qubits; domain: positive integer
- $k$: number of distinct phases in the diagonal unitary; domain: integer, 1<=k<=2^n
- $\theta_x$: phase on computational basis state |x>; domain: [0,2\pi)
- $D$: diagonal n-qubit unitary; domain: 2^n x 2^n unitary
- $\varepsilon$: target approximation precision; domain: (0,1)
- $C_0$: quality factor of the single-phase-rotation synthesis method; domain: 1<C_0<4
- $E(n,k)$: total entanglement cost in T gates; domain: nonnegative integer
- $T_{eq}$: equivalent T-count of the synthesized circuit; domain: nonnegative real
- $\phi_j$: j-th distinct phase value; domain: [0,2\pi), j=1..k

## eq_1: Diagonal unitary

$$
D=\sum_{x\in\{0,1\}^n} e^{i\theta_x}|x\rangle\langle x|,\quad |\{\theta_x\}|=k
$$

Diagonal operator with k distinct phase values.

Provenance: `abstract_inferred`. Definition of a diagonal n-qubit unitary with k distinct phases follows from the abstract's description.

Abstract evidence: k$ is the number of distinct phases in the diagonal $n$-qubit unitary

Equation assumptions:

- Phases taken modulo 2\pi

## eq_2: T-count bound

$$
T_{eq}\le kC_0\log_2(1/\varepsilon)+E(n,k)
$$

Upper bound on equivalent T-count: k rotations each costing about C_0 log2(1/eps) plus entanglement cost.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: The equivalent $T$-count of the synthesized circuit is bounded by $kC_{0}\log_{2}(1/\varepsilon)+E(n,k)$

Equation assumptions:

- E(n,k) form unknown

## eq_3: Phase-class grouping

$$
D=\sum_{j=1}^{k}e^{i\phi_j}P_j,\quad P_j=\sum_{x:\theta_x=\phi_j}|x\rangle\langle x|,\quad \sum_j P_j=I
$$

Decomposition into projectors on phase classes, motivating k rotations rather than 2^n.

Provenance: `assumption`. Plausible reading of why cost scales with k; the actual algorithm is not given in the abstract.

Equation assumptions:

- Paper's method uses such grouping

## eq_4: Rotation synthesis precision

$$
\|R_z(\phi)-U_{C+T}\|\le\varepsilon,\quad T(U_{C+T})\approx C_0\log_2(1/\varepsilon)
$$

Single-rotation Clifford+T approximation with T-count scaling logarithmically in 1/eps.

Provenance: `standard_background`. Known Clifford+T synthesis scaling; the C_0 identification with this per-rotation cost is inferred from the bound.

Equation assumptions:

- Operator norm up to global phase

## eq_5: Tiny instance

$$
n=2,\ k=2,\ D=\mathrm{diag}(1,1,1,e^{i\phi})
$$

CZ-like controlled phase instance with 2 distinct phases for illustration.

Provenance: `assumption`. Chosen as the smallest explicit instance since no scope was given.

Equation assumptions:

- Chosen for illustration only

## Registers

- q: n qubits; qubits on which the diagonal unitary acts; computational basis index x=sum_i x_i 2^i (assumed little-endian)
- anc: unknown qubits; possible ancillas for entanglement/parity computation; not specified in abstract

## Classical postprocessing

Classical computation of the distinct phases and the synthesis of each rotation; the decision rule comparing against prior methods in (n,k,epsilon) space is not specified.

## Algorithm steps

1. Identify the k distinct phases and their basis-state classes for D. (eq_1, eq_3)
2. Synthesize each distinct phase rotation over Clifford+T to precision epsilon (per-rotation cost C_0 log2(1/eps)). (eq_4)
3. Combine with a Clifford/entangling structure whose T cost is E(n,k) (construction unspecified) and check the total against the bound. (eq_2)

## Assumptions

- Scope chosen as the T-count bound plus tiny n=2,k=2 instance
- Grouping by phase class is an assumed interpretation
- Little-endian basis encoding

## Missing information

- Actual decomposition algorithm
- Formula for E(n,k)
- Optimal decision boundary in (n,k,epsilon)
- Definition and value of C_0 for the method
- Baseline state-of-the-art costs
- Ancilla requirements
