# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Reconstruct a universal quantum computation scheme using spinless interacting bosonic quantum walkers on a piecewise-constant graph governed by the 2D Bose-Hubbard model, with qubits encoded in walker positions, X/Z rotations, cphase and swap gates, with vertex count linear in qubit number.

Scope: Abstract-level reconstruction only: Bose-Hubbard Hamiltonian background, position encoding, and gate set (X/Z rotations, cphase, swap). Graph geometry, couplings, timings, Steane-code encoding and optical-lattice details are not given in the abstract. Steps and measurement are plausible placeholders, not the paper's protocol.

## Symbols

- $H$: Bose-Hubbard Hamiltonian on the graph; domain: operator on bosonic Fock space
- $J_{ij}$: hopping amplitude between sites i and j; domain: real, >= 0
- $U$: on-site interaction strength; domain: real
- $a_i$: bosonic annihilation operator at site i; domain: operator
- $\epsilon_i$: on-site potential; domain: real
- $n_i$: number operator a_i^\dagger a_i at site i; domain: non-negative integer eigenvalues

## eq_1: Bose-Hubbard Hamiltonian

$$
H=-\sum_{\langle i,j\rangle}J_{ij}(a_i^\dagger a_j+\mathrm{h.c.})+\frac{U}{2}\sum_i n_i(n_i-1)+\sum_i\epsilon_i n_i
$$

Standard Bose-Hubbard model on a graph with piecewise-constant parameters; the abstract only names the model.

Provenance: `standard_background`. The abstract names the two-dimensional Bose-Hubbard model; the explicit form is textbook background, not the paper's parameters.

Equation assumptions:

- Piecewise-constant J, U, epsilon
- Spinless bosons

## eq_2: Gate set

$$
R_X(\theta)=e^{-i\theta X/2},\; R_Z(\phi)=e^{-i\phi Z/2},\; \mathrm{CPHASE}=\mathrm{diag}(1,1,1,-1)
$$

Target gates: arbitrary X and Z rotations plus an entangling cphase (swap also provided).

Provenance: `abstract_inferred`. Gate families are stated in the abstract; matrix forms are standard. The cphase angle (pi) is assumed.

Abstract evidence: Arbitrary X and Z rotations are constructed, as well as an entangling two-qubit cphase gate and a swap gate.

Equation assumptions:

- CPHASE angle is pi

## Registers

- walker_position_qubits: n (one walker per encoded qubit, assumed; graph has O(n) vertices) qubits; Each qubit encoded in the position of a walker on the graph

## Initial state

Assumed: each walker localized at a designated vertex encoding logical |0>; the abstract gives no details.

## Measurement

Single-qubit measurement with localized operators: read out which vertex (site occupation n_i) the walker occupies, giving the computational-basis outcome. Exact detection mechanism not given; X-basis measurement would follow a rotation.

## Classical postprocessing

Assumed minimal: map occupation outcomes to logical bits; for the Steane code, compute syndromes classically and apply corrections. Details not in abstract.

## Algorithm steps

1. Place one walker per qubit on its assigned vertices of the piecewise-constant graph, encoding logical basis states by position. (eq_1)
2. Implement single-qubit R_X and R_Z rotations by evolving under H with tuned piecewise-constant hopping/potentials for suitable durations (parameters not given). (eq_1, eq_2)
3. Implement CPHASE between two walkers via on-site interaction U when they meet (assumed mechanism), and swap via routing; timings unspecified. (eq_1, eq_2)
4. Compose gates into circuits, optionally with error-correcting encodings such as the Steane code (details not in abstract). (eq_2)

## Assumptions

- Standard Bose-Hubbard form used as a placeholder
- One walker per encoded qubit (assumed)
- CPHASE arises from on-site interaction when walkers meet (assumed)
- Measurement is occupation readout of position
- Postprocessing is standard syndrome decoding

## Missing information

- Graph geometry and encoding of a qubit in walker positions
- Parameter values and gate pulse timings
- Exact vertex layout and gate-specific graph segments
- Exact measurement protocol and detection details
- Steane code logical encoding specifics
- Optical-lattice implementation details
