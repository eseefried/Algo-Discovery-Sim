# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Relate the depth of quantum circuits on a kD nearest-neighbor grid with classical control (adaptive circuits) to depth in the abstract all-to-all interaction model, and the depth of non-adaptive fanout/controlled-operation circuits on a kD grid. Only the stated asymptotic relations are available; no construction is given in the abstract.

Scope: Smallest useful scope: a formal statement of the depth-equivalence claim and the non-adaptive depth/size/width bounds for n-target fanout on a k-dimensional grid, plus a tiny explicit fanout instance (n=3) as an assumed illustration. The actual adaptive simulation construction, constant-depth Shor, and lower-bound proof remain outside scope.

## Symbols

- $k$: grid dimension; domain: integer, k >= 2
- $n$: number of target qubits (problem size); domain: positive integer
- $D_{\mathrm{grid}}(C)$: minimum depth on kD grid with classical control for implementing operation C; domain: positive integers
- $D_{\mathrm{abs}}(C)$: minimum depth in the standard model with arbitrary pairwise interactions; domain: positive integers
- $\mathrm{FANOUT}_n$: fanout: copies control bit onto n targets in the computational basis; domain: unitary on n+1 qubits

## eq_1: Depth equivalence (up to constant)

$$
D_{\mathrm{grid}}(C)=\Theta\left(D_{\mathrm{abs}}(C)\right)
$$

Adaptive nearest-neighbor depth on the kD grid equals abstract-model depth up to a constant factor.

Provenance: `abstract_inferred`. Stated in words; the Theta form is a formalization of 'same up to constant factor'. The constant may depend on k (assumption).

Abstract evidence: is the same (up to a constant factor) as in the standard model where arbitrary interactions are allowed

Equation assumptions:

- Constant factor may depend on k
- Applies to the adaptive classical-controller model

## eq_2: Non-adaptive depth bound

$$
\mathrm{depth}=\Theta\left(n^{1/k}\right)
$$

Optimal non-adaptive depth for controlled operations and fanout on the kD grid.

Provenance: `abstract_inferred`. The abstract's 'k√n' is read as the k-th root of n, as the garbled rendering suggests.

Abstract evidence: These circuits have depth Θ( k√n), size Θ(n) and width Θ(n).

Equation assumptions:

- k√n means n^{1/k}

## eq_3: Non-adaptive size and width

$$
\mathrm{size}=\Theta(n),\quad \mathrm{width}=\Theta(n)
$$

Gate count and qubit count of the optimal non-adaptive circuits.

Provenance: `abstract_explicit`. Directly stated.

Abstract evidence: These circuits have depth Θ( k√n), size Θ(n) and width Θ(n).

## eq_4: Fanout action

$$
\mathrm{FANOUT}_n\,|x\rangle|y_1\ldots y_n\rangle=|x\rangle|y_1\oplus x,\ldots,y_n\oplus x\rangle
$$

Definition of fanout on a control bit x and targets y_i.

Provenance: `standard_background`. Standard definition of the fanout operation named in the abstract.

Equation assumptions:

- Fanout as CNOT from one control onto n targets

## eq_5: Tiny instance

$$
n=3,\ \mathrm{FANOUT}_3|1\rangle|000\rangle=|1\rangle|111\rangle
$$

Illustrative instance for later circuit generation.

Provenance: `assumption`. Chosen as the smallest illustration; not from the abstract.

Equation assumptions:

- n=3 chosen for illustration

## Registers

- control: 1 qubits; fanout control qubit x
- targets: n qubits; fanout target qubits y_1..y_n
- ancilla: Theta(n) total width (unspecified) qubits; possible workspace in the grid layout; details not given

## Algorithm steps

1. Embed the n+1 qubits (plus ancillas) on a kD grid with side about n^{1/k}. (eq_2, eq_3)
2. Apply the non-adaptive nearest-neighbor fanout circuit (construction not specified in the abstract) achieving depth Theta(n^{1/k}). (eq_2, eq_3, eq_4)
3. For general circuits, a classical controller adaptively simulates arbitrary-pair interactions, preserving depth up to a constant. (eq_1)

## Assumptions

- Scope limited to the asymptotic statements and a tiny fanout instance
- k√n interpreted as n^{1/k}
- Constants may depend on k

## Missing information

- Explicit adaptive simulation construction
- Gate set and ancilla layout
- Constant-depth Shor construction
- Lower-bound proof and the 'more general class of operations'
- Explicit circuit for non-adaptive fanout
