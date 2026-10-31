# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Depth of quantum circuits restricted to nearest-neighbour interactions on a k-dimensional grid (k >= 2), both in an adaptive model with a classical controller (claimed to match the arbitrary-interaction model up to a constant factor) and in the non-adaptive model, where fanout and controlled operations on n qubits are claimed to have optimal depth Theta(n^{1/k}), size Theta(n) and width Theta(n).

Scope: Chosen scope (no experiment_scope supplied): one non-adaptive nearest-neighbour CNOT-fanout circuit on a 2D grid (k = 2), with the tiny explicit instance of an m x m = 3 x 3 grid (n = 9 qubits: one control plus 8 targets), achieving depth 2(m-1) = 4 and size n-1 = 8 CNOTs, together with the light-cone lower bound that shows depth Omega(n^{1/k}) is unavoidable. Outside scope: the paper's main adaptive-model theorem (constant-factor depth equivalence with the arbitrary-interaction model, which presumably uses measurements and classically controlled corrections), the constant-depth implementations of Shor's algorithm, general controlled operations and fanouts in that model, the general non-adaptive circuits for controlled-U operations on a kD grid, and the lower bound for the 'more general class of operations'. The specific construction below is my own proposal consistent with the stated bounds, not a reconstruction of the paper's circuit.

## Symbols

- $k$: dimension of the grid architecture; domain: integer, k \geq 2 (instance: k = 2)
- $n$: total number of qubits in the fanout (1 control + n-1 targets); also width of the circuit; domain: positive integer (instance: n = 9)
- $m$: side length of the square grid, n = m^2 for k = 2; domain: positive integer (instance: m = 3)
- $(r,c)$: grid coordinates of a qubit; linear index i = r m + c; domain: r, c \in \{0,\dots,m-1\}
- $x$: value of the control qubit; domain: \{0,1\}
- $y_i$: initial value of target qubit i; domain: \{0,1\}, i = 1,\dots,n-1
- $F_n$: n-qubit fanout (one control, n-1 targets); domain: unitary on (\mathbb{C}^2)^{\otimes n}
- $\mathrm{CNOT}_{u \to v}$: controlled-NOT with control at grid site u and target at adjacent grid site v; domain: two-qubit unitary, \|u-v\|_1 = 1
- $d$: circuit depth (number of layers of disjoint nearest-neighbour gates); domain: non-negative integer
- $D_{\mathrm{grid}}(U), D_{\mathrm{arb}}(U)$: minimum depth of U in the adaptive kD-grid model and in the arbitrary-interaction model, respectively; domain: non-negative integers

## eq_1: Fanout operation

$$
F_n \,|x\rangle |y_1, \dots, y_{n-1}\rangle = |x\rangle |y_1 \oplus x, \dots, y_{n-1} \oplus x\rangle
$$

Definition of the n-qubit fanout gate on computational basis states; it extends linearly. \oplus is addition mod 2.

Provenance: `standard_background`. Standard definition of the fanout gate named in the abstract; the abstract names it but does not define it.

Equation assumptions:

- Fanout is taken to mean the standard CNOT-fanout (classical copy of a control bit onto many targets).

## eq_2: Nearest-neighbour grid constraint

$$
\text{a two-qubit gate on sites } u, v \in \{0,\dots,m-1\}^k \text{ is allowed only if } \|u - v\|_1 = 1
$$

Only adjacent grid sites may interact; a layer consists of such gates acting on disjoint pairs. Qubit (r,c) carries linear index i = r m + c for k = 2.

Provenance: `abstract_inferred`. The abstract refers to local interactions on the kD grid and to the nearest-neighbour architecture; the L1-adjacency rule is the standard formalisation of this.

Abstract evidence: the nearest-neighbor architecture

Equation assumptions:

- Finite m^k sub-grid of the infinite lattice; single-qubit gates are unconstrained and not counted separately.

## eq_3: Stated optimal non-adaptive resource bounds

$$
\mathrm{depth} = \Theta(n^{1/k}), \quad \mathrm{size} = \Theta(n), \quad \mathrm{width} = \Theta(n)
$$

Asymptotic resources of the paper's non-adaptive fanout / controlled-operation circuits on a kD grid.

Provenance: `abstract_explicit`. Directly stated; the k-th root is read as n^{1/k}.

Abstract evidence: These circuits have depth Θ( k√n), size Θ(n) and width Θ(n)

## eq_4: Light-cone lower bound

$$
(2d+1)^k \geq n \;\Rightarrow\; d \geq \tfrac{1}{2}\left(n^{1/k} - 1\right) = \Omega(n^{1/k})
$$

In depth d, information from one site can reach at most the (2d+1)^k sites within L1 distance d; a fanout whose control must influence all n qubits therefore needs d = Omega(n^{1/k}). Exact inequality, not just asymptotic.

Provenance: `abstract_inferred`. The abstract asserts a matching lower bound; the light-cone argument is the standard way to obtain Omega(n^{1/k}) for non-adaptive nearest-neighbour circuits and is consistent with the stated Theta bound. The paper's actual proof and its generalisation are not available.

Abstract evidence: Our lower bound also applies to a more general class of operations

Equation assumptions:

- Non-adaptive model (no mid-circuit measurement/classical feed-forward), since adaptive circuits are claimed to achieve constant depth.

## eq_5: Proposed row-then-column CNOT fanout on an m x m grid

$$
F_n = \left[\prod_{t=1}^{m-1} \bigotimes_{c=0}^{m-1} \mathrm{CNOT}_{(t-1,c)\to(t,c)}\right] \left[\prod_{t=1}^{m-1} \mathrm{CNOT}_{(0,t-1)\to(0,t)}\right], \quad \mathrm{depth} = 2(m-1) = 2(\sqrt{n}-1), \; \mathrm{size} = n-1
$$

Control at (0,0) with all targets initially |0>. First a chain of m-1 CNOTs broadcasts x along row 0 (sequential, depth m-1); then m-1 layers of m parallel CNOTs broadcast down every column simultaneously. Products are time-ordered right to left. Equality with F_n holds exactly on inputs with all y_i = 0; for arbitrary y_i the same circuit computes a different Boolean map, so the general fanout of eq_1 would need the standard conversion via a clean ancilla copy or a tree of CNOTs that also propagates correctly, which is left outside scope.

Provenance: `assumption`. My own simple construction meeting eq_2 with depth O(sqrt n) and size n-1, i.e. matching eq_3 for k = 2 up to constants; the paper's actual circuit is not given in the abstract.

Equation assumptions:

- k = 2, n = m^2, control qubit placed at corner (0,0).
- All target qubits start in |0> (clean-ancilla fanout / GHZ-type copy).

## eq_6: Adaptive-model depth equivalence (out of scope, stated for context)

$$
D_{\mathrm{grid}}(U) = \Theta\big(D_{\mathrm{arb}}(U)\big) \quad \text{for every } U, \; k \geq 2
$$

The paper's main claim: with a classical controller choosing local interactions on the kD grid, minimum depth matches the arbitrary-interaction model up to a constant factor (with polynomial size and width).

Provenance: `abstract_explicit`. Directly stated as the main result; the construction achieving it is not described in the abstract and is not reconstructed here.

Abstract evidence: is the same (up to a constant factor) as in the standard model where arbitrary interactions are allowed

Equation assumptions:

- Adaptive model: measurements and classically controlled gates are allowed within a layer at unit depth cost, as implied by 'a classical controller determines which local interactions to apply'.

## Registers

- ctrl: 1 qubits; Control qubit at grid site (0,0), linear index 0, holding |x>
- tgt: 8 qubits; Target qubits at the remaining sites (r,c) of the 3 x 3 grid, linear index i = 3r + c in {1,...,8}, each initialised to |0>

## Initial state

|x\rangle_{(0,0)} \otimes |0\rangle^{\otimes 8} on the 3 x 3 grid (n = 9, m = 3); x in {0,1} or a superposition such as (|0>+|1>)/sqrt2 to produce a 9-qubit GHZ state.

## Measurement

Not required for the (unitary, non-adaptive) construction. For verification only: measure all 9 qubits in the computational basis; for basis input x every outcome bit should equal x, and for input (|0>+|1>)/sqrt2 the outcomes should be all-0 or all-1 with probability 1/2 each.

## Classical postprocessing

Verification only: check that all measured bits are equal (and equal to x for a basis-state control); estimate the failure fraction over repeated runs.

## Algorithm steps

1. Row broadcast: apply CNOT_{(0,0)->(0,1)} then CNOT_{(0,1)->(0,2)} sequentially (2 layers), so row 0 holds |x,x,x>. (eq_2, eq_5)
2. Column broadcast layer 1: apply in parallel CNOT_{(0,c)->(1,c)} for c = 0,1,2 (1 layer). (eq_2, eq_5)
3. Column broadcast layer 2: apply in parallel CNOT_{(1,c)->(2,c)} for c = 0,1,2 (1 layer). Total depth 4 = 2(m-1), size 8 = n-1, output |x>^{\otimes 9}, realising eq_1 on the all-zero target input. (eq_1, eq_5)
4. Check against bounds: depth 4 satisfies the light-cone inequality (2d+1)^2 = 81 >= 9 and the lower bound d >= (3-1)/2 = 1; asymptotically depth is Theta(sqrt n), matching eq_3 for k = 2. (eq_3, eq_4)

## Assumptions

- No experiment_scope was provided, so the non-adaptive 2D-grid fanout with a 3 x 3 instance was chosen as the single smallest useful construction.
- The k-th root notation 'k√n' in the abstract is interpreted as n^{1/k}.
- Fanout means CNOT-fanout (eq_1); targets are assumed clean (|0>) for the proposed circuit.
- The proposed row-then-column circuit (eq_5) is my construction consistent with the stated Theta bounds, not the paper's circuit.
- Depth counts layers of disjoint nearest-neighbour two-qubit gates; single-qubit gates are not counted.

## Missing information

- The paper's construction proving constant-factor depth equivalence between the adaptive kD-grid model and the arbitrary-interaction model (eq_6), including how the classical controller, measurements and corrections are used.
- The constant-depth adaptive implementations of fanout, controlled operations and Shor's algorithm, and their polynomial size/width.
- The paper's actual optimal non-adaptive circuits for general controlled operations (not just fanout) on a kD grid and the precise constants in Theta(n^{1/k}).
- The exact statement and proof of the lower bound and the 'more general class of operations' it covers.
- How arbitrary (non-zero) target inputs are handled in the paper's fanout circuits.
