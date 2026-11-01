# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximate a single-qubit z-rotation by a single-qubit circuit over the Pauli+V gate set, using a deterministic-search technique adapted from the Ross-Selinger analysis for Clifford+T. The abstract gives no explicit formulas, so only background definitions can be supplied.

Scope: Define the approximation problem for one z-rotation Rz(theta) and precision epsilon, with an assumed tiny instance (theta = pi/8, epsilon = 0.1). Include the standard V-gate definition and the operator-norm error criterion. The deterministic-search algorithm, its geometric construction, and the depth and optimality results are outside this scope.

## Symbols

- $\theta$: target z-rotation angle; domain: real number in [0, 2\pi)
- $R_z(\theta)$: target z-rotation unitary; domain: SU(2)
- $\varepsilon$: approximation precision; domain: positive real number
- $U$: candidate single-qubit circuit over Pauli+V; domain: U(2)
- $V$: V gate; the standard definition is assumed here; domain: 2x2 unitary
- $\|\cdot\|$: operator norm; domain: norm on 2x2 matrices

## eq_1: z-rotation

$$
R_z(\theta)=\begin{pmatrix}e^{-i\theta/2}&0\\0&e^{i\theta/2}\end{pmatrix}
$$

Standard definition of the target z-rotation.

Provenance: `standard_background`. Standard convention; the abstract names z-rotations but gives no formula.

Equation assumptions:

- The phase convention is the standard SU(2) one.

## eq_2: V gate

$$
V=\frac{1}{\sqrt5}\begin{pmatrix}1+2i&0\\0&1-2i\end{pmatrix}\ \text{(not assumed)}
$$

Placeholder removed; see eq_3 for the actual standard V definition.

Provenance: `assumption`. Superseded; kept only to flag that the exact V convention is not given in the abstract.

Equation assumptions:

- Do not use this equation; it is not the V-gate definition.

## eq_3: V gate (standard)

$$
V_1=\frac{1}{\sqrt5}\begin{pmatrix}1&2i\\2i&1\end{pmatrix},\quad V_3=\frac{1}{\sqrt5}\begin{pmatrix}1&2\\-2&1\end{pmatrix}\ \text{(with analogues for other axes)}
$$

Recalled V-type gates from the literature, with the normalization 1/sqrt(5) and the specific matrices recalled from memory. Their exact form is an assumption.

Provenance: `standard_background`. The gate set is recalled from memory of the Pauli+V literature and the abstract does not define it.

Equation assumptions:

- The exact V matrices and their normalization must be checked against the source.

## eq_4: Approximation criterion

$$
\|U-R_z(\theta)\|\le\varepsilon
$$

U is an epsilon-approximation of the target in operator norm; equality is not required.

Provenance: `assumption`. A natural error measure for the stated approximation problem, not stated in the abstract.

Equation assumptions:

- The error is measured in operator norm, possibly up to global phase.

## eq_5: Circuit form

$$
U=g_k g_{k-1}\cdots g_1,\quad g_j\in\{X,Y,Z,V_1,V_2,V_3,V_1^{\dagger},V_2^{\dagger},V_3^{\dagger}\}
$$

A candidate circuit is a finite product of Pauli and V gates; depth is the length k.

Provenance: `abstract_inferred`. The abstract says the technique is adapted to Pauli+V circuits, which implies finite words over that gate set; the specific generator list is background.

Abstract evidence: single-qubit Clifford+T circuits

Equation assumptions:

- The generator list is assumed.

## Registers

- q: 1 qubits; single data qubit acted on by the approximating circuit

## Algorithm steps

1. Fix theta and epsilon, with the assumed tiny instance theta = pi/8 and epsilon = 0.1, and form the target R_z(theta). (eq_1)
2. Fix the Pauli+V gate set and its V-gate convention. (eq_3, eq_5)
3. Seek a short word U over the gate set satisfying the error criterion. The deterministic-search method for finding such a word is not specified in the abstract and must be supplied from the source. (eq_4, eq_5)

## Assumptions

- The instance theta = pi/8, epsilon = 0.1 is an illustrative assumption.
- The V-gate definitions are recalled background and must be verified.
- The operator-norm error criterion is assumed.
- eq_2 is a flagged placeholder and should be discarded.

## Missing information

- The deterministic-search algorithm itself.
- The geometric methods and the constructions used for the proofs.
- The precise Pauli+V gate set and V definition.
- The depth bounds and optimality results.
- The Ross-Selinger Clifford+T details and how they are adapted.
