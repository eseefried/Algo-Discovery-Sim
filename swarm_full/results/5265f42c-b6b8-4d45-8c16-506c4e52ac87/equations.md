# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Show that quantum circuit depth in the adaptive nearest-neighbor architecture, where a classical controller chooses which local interactions to apply on the kD grid Z^k with k>=2, matches (up to a constant factor) the depth in the standard model with arbitrary pairwise interactions. Also give optimal non-adaptive circuits for controlled operations and fanout on a kD grid.

Scope: Abstract-level problem statement and depth/size/width scaling relations only. No explicit circuit construction, simulation protocol, or measurement scheme is reconstructed from the abstract.

## Symbols

- $n$: number of qubits or fanout targets; domain: positive integers
- $k$: dimension of the grid Z^k; domain: integers, k>=2
- $D_{grid}$: minimum depth in the adaptive nearest-neighbor grid architecture; domain: positive integers
- $D_{std}$: minimum depth in the standard model with arbitrary interactions; domain: positive integers

## eq_1: Depth equivalence

$$
D_{grid}=\Theta(D_{std})
$$

Adaptive kD nearest-neighbor depth equals standard-model depth up to a constant factor.

Provenance: `abstract_inferred`. Formalizes the stated 'same up to a constant factor' claim.

Abstract evidence: is the same (up to a constant factor) as in the standard model where arbitrary interactions are allowed

Equation assumptions:

- Constant factor may depend on k

## eq_2: Non-adaptive depth

$$
\mathrm{depth}=\Theta(\sqrt[k]{n})
$$

Optimal non-adaptive depth for controlled operations and fanout on the kD grid.

Provenance: `abstract_explicit`. Stated in the abstract, with k√n read as the k-th root of n.

Abstract evidence: These circuits have depth Θ( k√n)

## eq_3: Size and width

$$
\mathrm{size}=\Theta(n),\ \mathrm{width}=\Theta(n)
$$

Size and width of the non-adaptive circuits.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: size Θ(n) and width Θ(n)

## Registers

- control: 1 qubits; control qubit for fanout or controlled operation
- targets: n qubits; target qubits laid out on a kD grid of side about n^{1/k}

## Initial state

Assumed: control in arbitrary state, targets in arbitrary state; any ancillas (within Θ(n) width) start in |0>.

## Measurement

The abstract specifies no measurement for the controlled-operation/fanout circuits. Assumed: computational-basis measurement of the output qubits, or of the Shor period-register qubits when simulating Shor's algorithm. In the adaptive model, mid-circuit measurement outcomes may be used by the classical controller to choose later local interactions; the details are not given.

## Classical postprocessing

Not specified in the abstract. For Shor's algorithm, the standard continued-fractions and gcd postprocessing would apply (background assumption). The classical controller computes the interaction schedule.

## Algorithm steps

1. Embed the control and n targets in a kD grid of side Θ(n^{1/k}), using Θ(n) total qubits including ancillas. (eq_3)
2. Assumed: spread the control value across the grid by nearest-neighbor copying (CNOT) steps, covering distance Θ(n^{1/k}). (eq_2)
3. Apply the local controlled operations on each target using the copies, then uncompute the copies by reversing the spreading, giving non-adaptive depth Θ(n^{1/k}) and size Θ(n). (eq_2, eq_3)
4. For the adaptive result: a standard-model circuit is simulated on the grid with classical control, at constant-factor depth overhead. The mechanism is not given in the abstract. (eq_1)

## Assumptions

- k-th root reading of 'k√n'
- The fanout spreading/uncompute scheme is a plausible assumed plan, not taken from the abstract
- The adaptive simulation mechanism is not reconstructed
- Measurement is assumed computational-basis, since the abstract gives no details
- Shor postprocessing is the standard textbook procedure, not taken from the abstract
- Measurement is assumed computational-basis; Shor postprocessing is standard background

## Missing information

- Explicit adaptive simulation construction
- Exact gate sequence and ancilla layout
- Lower-bound proof
- Measurement and classical control details
- Whether mid-circuit measurement is used in the simulation
