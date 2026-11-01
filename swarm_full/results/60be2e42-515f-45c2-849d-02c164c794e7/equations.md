# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Show that coinless discrete-time quantum walks, whose evolution operators come from lattice tessellations and act only on the site basis, are equivalent to coined walks. In 1D, map the coinless walk to an extended coined walk for a specific family of evolution operators, then study its asymptotics and its mixing time and limiting distributions on cycles.

Scope: Conceptual and small finite-instance reconstruction of the 1D tessellation-based coinless walk. The abstract gives no explicit formulas, so all equations are standard background or assumed. The coined equivalence, the specific operator family and the cycle mixing results are not reconstructed.

## Symbols

- $\mathcal{H}_P$: Position (site) Hilbert space of the coinless walk; domain: span{|x>}, x in Z or Z_N
- $H_0, H_1$: Reflection operators for the two tessellations (assumed standard form); domain: Hermitian unitary operators on H_P
- $U$: One-step coinless evolution operator; domain: Unitary on H_P

## eq_1: Tessellation evolution operator

$$
U = H_1 H_0
$$

The coinless step is a product of two tessellation reflection operators, each built from the polygons of one tessellation.

Provenance: `standard_background`. The abstract says the evolution operators come from a graphical method based on lattice tessellations. The product form is the standard construction, not stated in the abstract.

Equation assumptions:

- Two tessellations in 1D, labelled 0 and 1

## eq_2: Tessellation reflection

$$
H_a = 2\sum_{k} |\alpha_k^{a}\rangle\langle\alpha_k^{a}| - I,\quad |\alpha_k^{a}\rangle = \tfrac{1}{\sqrt{2}}(|2k+a\rangle+|2k+a+1\rangle)
$$

Assumed 1D instance. Each polygon is a pair of adjacent sites and the reflection acts on the uniform superposition over its sites.

Provenance: `assumption`. Finite instance chosen for a small example. The abstract mentions only 'some examples of tessellations'.

Equation assumptions:

- Polygon size 2
- Shift between tessellations by one site

## eq_3: Walk state evolution

$$
|\psi_t\rangle = U^t|\psi_0\rangle,\quad p_t(x)=|\langle x|\psi_t\rangle|^2
$$

Evolution of the state and the position probability distribution.

Provenance: `standard_background`. Standard discrete-time walk dynamics.

## Registers

- pos: n = ceil(log2 N) qubits for an N-site cycle (assumed) qubits; Site register; the coinless walk acts only on this register, with no coin qubit

## Initial state

Localized site state |0> on the position register (assumed), i.e. |psi_0> = |x=0>

## Measurement

Measure the position register in the site basis after t steps, repeated over many runs to estimate p_t(x).

## Classical postprocessing

Build the empirical histogram of p_t(x). For cycles, compare it to the uniform distribution (for example by total variation distance) to estimate mixing behaviour, and average over t to approximate the limiting distribution.

## Algorithm steps

1. Prepare the position register in the localized state |psi_0>. (eq_3)
2. Apply the reflection H_0 for the first tessellation (pairs (2k,2k+1)). (eq_1, eq_2)
3. Apply the reflection H_1 for the shifted tessellation (pairs (2k+1,2k+2)); one step is U = H_1 H_0. (eq_1, eq_2)
4. Repeat the step t times to obtain |psi_t> = U^t |psi_0>. (eq_3)

## Assumptions

- The 1D tessellation operator is the product of two polygon reflections, as in eq_1 and eq_2.
- Polygon size 2 in 1D, with reflections as in eq_2.
- The cycle has even N, and a power-of-two N is assumed for the register layout; the circuit-level implementation of H_a is not specified.
- Localized initial state and an N-site cycle with a position-only register are assumed.
- All equations are background or assumed; none is quoted from the abstract.

## Missing information

- The specific family of evolution operators used for the coined mapping
- The explicit coin operator and extended coin space
- The mixing-time and limiting-distribution results on cycles
- Gate-level decomposition of the tessellation reflections
- The actual equivalence construction between coinless and coined walks
