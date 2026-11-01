# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Decompose an arbitrary isometry V from m to n qubits (n>=m) into single-qubit gates and C-not gates, minimizing the C-not count; the abstract gives a counting lower bound and decompositions within about a factor of two of it, plus Stinespring-based extension to quantum operations and POVMs.

Scope: Define the isometry, its real parameter count, and a generic parameter-counting argument for a C-not lower bound, plus the Stinespring dilation relation. Scope is a tiny instance m=1, n=2. The paper's three explicit decompositions, bespoke small-case optimizations, and exact bound constants are outside scope and not reconstructed.

## Symbols

- $m$: number of input qubits; domain: positive integer, m<=n
- $n$: number of output qubits; domain: positive integer
- $V$: isometry from m to n qubits; domain: 2^n x 2^m complex matrix with V^\dagger V = I_{2^m}
- $N_{\mathrm{CNOT}}$: number of C-not gates in a decomposition; domain: non-negative integer
- $d_{\mathrm{iso}}$: number of real parameters of the isometry manifold; domain: non-negative integer
- $\mathcal{E}$: quantum operation (CPTP map); domain: map on density matrices
- $K_j$: Kraus operators; domain: complex matrices with sum_j K_j^\dagger K_j = I
- $|0\rangle_E$: environment ancilla initial state; domain: computational basis state

## eq_1: Isometry condition

$$
V^\dagger V = I_{2^m},\quad V:(\mathbb{C}^2)^{\otimes m}\to(\mathbb{C}^2)^{\otimes n}
$$

Defines an isometry from m to n qubits.

Provenance: `standard_background`. Standard definition of an isometry; the abstract only names the object.

Equation assumptions:

- n>=m

## eq_2: Isometry real parameter count

$$
d_{\mathrm{iso}} = 2\cdot 2^{n}2^{m} - 2^{2m} = 2^{n+m+1}-2^{2m}
$$

Real dimension of the set of 2^n x 2^m isometries (Stiefel manifold).

Provenance: `standard_background`. Standard Stiefel manifold dimension: 2NM - M^2 with N=2^n, M=2^m.

## eq_3: Parameter-counting CNOT lower bound (schematic)

$$
N_{\mathrm{CNOT}} \gtrsim \frac{d_{\mathrm{iso}} - c_{1}(n)}{c_2}
$$

Generic counting-argument form: each CNOT plus its adjacent single-qubit gates contributes a bounded number of free parameters, so the count must cover d_iso. The constants are left unspecified.

Provenance: `abstract_inferred`. The abstract states a lower bound exists; the counting form is an inference, and the exact constants c_1, c_2 are not given.

Abstract evidence: We derive a theoretical lower bound on the number of C-not gates required to decompose an arbitrary isometry from $m$ to $n$ qubits

Equation assumptions:

- Bound derived by dimension counting, which is not confirmed by the abstract
- c_1(n) accounts for the n single-qubit rotation layers, c_2 is a constant

## eq_4: Near-optimality factor

$$
N_{\mathrm{CNOT}}^{\mathrm{decomp}} \le \approx 2\,N_{\mathrm{CNOT}}^{\mathrm{LB}}\ \text{(leading order)}
$$

Decompositions achieve the bound up to roughly a factor of two at leading order; this is an asymptotic approximation, not an exact equality.

Provenance: `abstract_inferred`. Direct paraphrase of the abstract's approximate factor claim.

Abstract evidence: give three explicit gate decompositions that achieve this bound up to a factor of about two in the leading order

Equation assumptions:

- LB denotes the derived lower bound

## eq_5: Stinespring dilation

$$
\mathcal{E}(\rho)=\mathrm{Tr}_E\!\left[V\rho V^\dagger\right],\quad V|\psi\rangle=\sum_j K_j|\psi\rangle\otimes|j\rangle_E
$$

Any quantum operation is an isometry V followed by a partial trace over the environment; this lets isometry decompositions yield decompositions of operations and POVMs.

Provenance: `standard_background`. Standard Stinespring and Kraus relation; the abstract only mentions Stinespring's theorem.

Equation assumptions:

- Environment dimension at least the Kraus rank

## Registers

- in: m qubits; input qubits, with the isometry's input state defined on them
- anc: n-m qubits; ancilla qubits initialized to |0>, which extend the input to n qubits

## Initial state

Input m-qubit state |psi> tensored with |0>^{n-m}, treated as a general instance with an ancilla register; the paper's concrete construction is unknown.

## Measurement

For POVMs via Stinespring: measure the environment register in the computational basis; the details are not given in the abstract.

## Classical postprocessing

Classical computation of the gate angles for a given V is needed, but the algorithm is not specified in the abstract.

## Algorithm steps

1. Specify the target isometry V and compute its real parameter count; take the tiny instance m=1, n=2, where d_iso = 16-4 = 12. (eq_1, eq_2)
2. Apply the counting argument to bound the number of C-nots from below; exact constants are missing. (eq_3)
3. Compare against a decomposition's C-not count, which is within about 2x of the bound at leading order. The explicit decompositions are not reconstructed. (eq_4)
4. For operations or POVMs, build the Stinespring isometry from Kraus operators and decompose it, then trace out or measure the environment. (eq_5)

## Assumptions

- Chosen tiny instance is m=1, n=2.
- The lower-bound form is a generic parameter-counting inference, not the paper's derived formula.
- Ancilla qubits start in |0>.

## Missing information

- Exact lower bound formula and constants
- The three explicit decomposition constructions and their C-not counts
- The bespoke optimizations for small m and n
- Gate-angle computation procedure
- Qubit ordering and encoding conventions used by the paper
