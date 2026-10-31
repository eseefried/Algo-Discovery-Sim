# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Universal quantum computation using spinless interacting bosonic quantum walkers on a piecewise-constant 2D graph governed by the Bose-Hubbard model, with qubits encoded in walker positions, single-qubit X and Z rotations, a two-qubit cphase gate, a swap gate, localized single-qubit measurements, and a vertex count linear in the number of qubits.

Scope: Scoped (by assumption, no experiment_scope supplied) to the smallest useful instance: two logical qubits, each a single boson on a two-vertex (dual-rail) pair, i.e. four graph vertices in total, with Fock space truncated to at most two bosons per vertex. We reconstruct the position encoding, the Bose-Hubbard generator, an X rotation from intra-pair tunneling, a Z rotation from an on-site energy bias, and a collisional controlled-phase from the on-site interaction U, followed by localized occupation measurement. Outside scope: the explicit piecewise-constant graph layout, the swap gate construction, the proof of linear vertex scaling, the Steane-code logical encoding, the 3D lattice extension for error correction, and the ultracold-atom optical-lattice implementation parameters.

## Symbols

- $a_v^{\dagger}, a_v$: Bosonic creation/annihilation operators on graph vertex v; domain: Operators on bosonic Fock space; [a_v, a_w^{\dagger}] = \delta_{vw}
- $n_v$: Number operator a_v^{\dagger} a_v on vertex v; domain: Non-negative integer spectrum, truncated to {0,1,2} in scope
- $J$: Nearest-neighbour tunneling (hopping) amplitude, piecewise constant in time; domain: Real, J \geq 0
- $U$: On-site two-boson interaction energy; domain: Real
- $\epsilon_v$: On-site potential (energy offset) at vertex v; domain: Real
- $t, \tau$: Durations of piecewise-constant evolution segments; domain: Real, t, \tau \geq 0 (units with \hbar = 1)
- $v_0^{(k)}, v_1^{(k)}$: The two vertices (rail 0 and rail 1) assigned to logical qubit k; domain: Vertices of the graph; k \in \{1,2\} in scope
- $|0_L\rangle_k, |1_L\rangle_k$: Logical basis states of qubit k, walker localized on rail 0 or rail 1; domain: Single-boson Fock states
- $\theta, \phi$: Rotation angle of a single-qubit gate; conditional phase of the cphase gate; domain: Real, taken modulo 2\pi
- $X, Z$: Pauli operators acting on the logical dual-rail subspace; domain: 2x2 Hermitian unitaries

## eq_1: Bose-Hubbard Hamiltonian on the graph

$$
H = -J \sum_{\langle v,w \rangle} \left( a_v^{\dagger} a_w + a_w^{\dagger} a_v \right) + \frac{U}{2} \sum_v n_v (n_v - 1) + \sum_v \epsilon_v n_v
$$

Generator of the walker dynamics; the sum over edges, J, and \epsilon_v are piecewise constant in time so that evolution is a product of exponentials of constant Hamiltonians.

Provenance: `standard_background`. The abstract names the two-dimensional Bose-Hubbard model; this is the standard form of that Hamiltonian recalled from background knowledge, not extracted from the paper.

Equation assumptions:

- Nearest-neighbour hopping only; \hbar = 1
- Edge set and parameters are piecewise constant in time (interpretation of 'piecewise-constant graph')

## eq_2: Dual-rail position encoding of a logical qubit

$$
|0_L\rangle_k = a_{v_0^{(k)}}^{\dagger} |\mathrm{vac}\rangle, \qquad |1_L\rangle_k = a_{v_1^{(k)}}^{\dagger} |\mathrm{vac}\rangle
$$

Each logical qubit is one boson whose position on one of two assigned vertices stores the bit; the two-qubit computational basis is a_{v_{i}^{(1)}}^{\dagger} a_{v_{j}^{(2)}}^{\dagger}|\mathrm{vac}\rangle for i,j \in \{0,1\}.

Provenance: `abstract_inferred`. The abstract states position encoding and linear vertex count; a two-vertex-per-qubit (dual-rail) encoding with one walker per qubit is the minimal such encoding consistent with both claims. The exact vertex assignment used in the paper is not given.

Abstract evidence: Quantum information is encoded in the positions of the walkers on the graph

Equation assumptions:

- Exactly one boson per logical qubit
- Two vertices per qubit (minimal linear scaling)

## eq_3: X rotation from intra-pair tunneling

$$
H_X^{(k)} = -J \left( a_{v_0^{(k)}}^{\dagger} a_{v_1^{(k)}} + a_{v_1^{(k)}}^{\dagger} a_{v_0^{(k)}} \right), \qquad e^{-i H_X^{(k)} t} \big|_{\mathrm{span}\{|0_L\rangle_k,|1_L\rangle_k\}} = e^{i J t X} = R_X(\theta),\ \theta = -2 J t \ (\mathrm{mod}\ 4\pi)
$$

Switching on only the edge between a qubit's two rails for duration t realizes an exact X rotation within the single-boson subspace, with R_X(\theta) = e^{-i \theta X / 2}.

Provenance: `assumption`. The abstract claims arbitrary X rotations are constructed; on the dual-rail subspace the hopping term acts exactly as -J X, so a tunneling pulse is the natural realization. The paper's actual control sequence is unknown.

Equation assumptions:

- Only the intra-pair edge is active during the pulse
- \epsilon_{v_0^{(k)}} = \epsilon_{v_1^{(k)}} during the pulse

## eq_4: Z rotation from on-site energy bias

$$
H_Z^{(k)} = \frac{\epsilon}{2} \left( n_{v_0^{(k)}} - n_{v_1^{(k)}} \right), \qquad e^{-i H_Z^{(k)} t} \big|_{\mathrm{span}\{|0_L\rangle_k,|1_L\rangle_k\}} = e^{-i \epsilon t Z / 2} = R_Z(\theta),\ \theta = \epsilon t \ (\mathrm{mod}\ 4\pi)
$$

With all edges of the pair switched off, a potential difference \epsilon between the two rails for duration t gives an exact Z rotation (global phases dropped).

Provenance: `assumption`. The abstract claims arbitrary Z rotations are constructed; a relative on-site energy between the two rails is the minimal Bose-Hubbard mechanism producing a relative phase. Not sourced from the paper.

Equation assumptions:

- Tunneling between the rails is off (J = 0 on that edge) during the pulse
- Uniform offset of \epsilon_v contributes only a global phase

## eq_5: Collisional controlled-phase from on-site interaction

$$
H_{\mathrm{int}} = \frac{U}{2} \, n_{v}(n_{v} - 1), \qquad e^{-i H_{\mathrm{int}} \tau} \, a_{v}^{\dagger} a_{v}^{\dagger} |\mathrm{vac}\rangle = e^{-i U \tau} \, a_{v}^{\dagger} a_{v}^{\dagger} |\mathrm{vac}\rangle, \qquad \mathrm{CPHASE}(\phi) = \mathrm{diag}(1,1,1,e^{i\phi}),\ \phi = -U\tau \ (\mathrm{mod}\ 2\pi)
$$

If, and only if, both walkers are on their rail-1 vertices, a transfer step T brings them onto a common vertex v, where a wait of duration \tau accumulates the phase -U\tau; the inverse transfer T^{\dagger} restores the encoding, yielding a controlled phase on |1_L 1_L\rangle.

Provenance: `assumption`. The abstract claims an entangling cphase gate using interacting walkers; the on-site U term in eq_1 is the only interaction in the Bose-Hubbard model, so a collisional phase is the natural mechanism. The specific transfer sequence T (tunneling pulses, including the bosonic sqrt(2) enhancement when two bosons share a site) is a construction detail not supplied by the abstract.

Equation assumptions:

- A transfer T mapping the rail-1 walker of qubit 1 onto the rail-1 vertex of qubit 2 (and acting trivially on rail-0 states) exists and is reversible
- Single-occupancy phases acquired during T are compensated by Z rotations (eq_4)

## eq_6: Localized single-qubit measurement by occupation readout

$$
P_0^{(k)} = n_{v_0^{(k)}}, \quad P_1^{(k)} = n_{v_1^{(k)}}, \quad \Pr(\text{outcome } b) = \langle \psi | P_b^{(k)} | \psi \rangle \ \text{on the one-boson-per-qubit subspace}
$$

Measuring the occupation number of each rail vertex of qubit k projects onto the logical basis; n_{v_0^{(k)}} + n_{v_1^{(k)}} = 1 on the code subspace so the two operators act as orthogonal projectors.

Provenance: `abstract_inferred`. Given position encoding, a localized operator distinguishing the logical states must detect which vertex is occupied; the number operator on a rail is the minimal such operator.

Abstract evidence: single-qubit measurements to be performed in a straightforward manner with localized operators

Equation assumptions:

- State remains in the one-boson-per-qubit subspace (no loss or double occupancy at readout)

## Registers

- qubit_1_rails: 2 graph vertices (v_0^{(1)}, v_1^{(1)}), each a bosonic mode truncated to occupation \leq 2 qubits; Dual-rail position encoding of logical qubit 1 (one boson)
- qubit_2_rails: 2 graph vertices (v_0^{(2)}, v_1^{(2)}), each a bosonic mode truncated to occupation \leq 2 qubits; Dual-rail position encoding of logical qubit 2 (one boson)

## Initial state

|0_L\rangle_1 \otimes |0_L\rangle_2 = a_{v_0^{(1)}}^{\dagger} a_{v_0^{(2)}}^{\dagger} |\mathrm{vac}\rangle, i.e. one boson on the rail-0 vertex of each qubit, all other vertices empty (ordering: qubit 1 is the left factor, qubit 2 the right factor; computational basis |ij\rangle has walker 1 on v_i^{(1)} and walker 2 on v_j^{(2)}).

## Measurement

Measure the number operators n_{v_0^{(k)}} and n_{v_1^{(k)}} on each qubit's two vertices; outcome b \in \{0,1\} is the rail found occupied (eq_6). Any outcome with total occupation of a pair not equal to 1 is flagged as a leakage/loss error.

## Classical postprocessing

Map each pair readout to a classical bit (occupied rail index); discard or flag shots with pair occupation \neq 1. For the example sequence R_X(\pi/2) on qubit 1 followed by CPHASE(\pi), the ideal two-qubit outcome distribution is 1/2 on |00\rangle and 1/2 on |10\rangle (cphase acts trivially when qubit 2 is in |0_L\rangle); compare empirical frequencies to this target.

## Algorithm steps

1. Prepare one boson on v_0^{(1)} and one on v_0^{(2)} with all edges switched off. (eq_2)
2. Apply R_X(\theta_1) to qubit 1 by activating only the edge (v_0^{(1)}, v_1^{(1)}) with amplitude J for time t_1 = -\theta_1/(2J); e.g. \theta_1 = \pi/2 gives J t_1 = \pi/4 (mod 2\pi). (eq_1, eq_3)
3. Apply R_Z(\theta_2) to qubit 1 by biasing the on-site energies of its two rails by \epsilon for time t_2 = \theta_2/\epsilon with all edges off. (eq_1, eq_4)
4. Apply CPHASE(\phi) between qubits 1 and 2: transfer the rail-1 walker of qubit 1 onto v_1^{(2)}, wait \tau = -\phi/U (e.g. \phi = \pi gives U\tau = \pi), then apply the inverse transfer; compensate single-particle phases with eq_4. (eq_1, eq_5, eq_4)
5. Read out each qubit by localized occupation measurement of its two rail vertices. (eq_6)

## Assumptions

- No experiment_scope was supplied; the two-qubit, four-vertex dual-rail instance was chosen as the smallest useful construction.
- One boson per logical qubit, two vertices per qubit; Fock space truncated to occupation \leq 2 per vertex (needed only transiently during the cphase).
- Piecewise-constant graph interpreted as time-piecewise-constant edge set, hopping J, and on-site energies \epsilon_v, so evolution is a product of exponentials of constant Bose-Hubbard Hamiltonians.
- \hbar = 1; global phases are ignored.
- The transfer step in the cphase construction is assumed to exist and be exactly reversible; its pulse schedule is not derived here.

## Missing information

- Explicit piecewise-constant graph geometry and how it achieves vertex count linear in the number of qubits for arbitrary connectivity.
- The paper's actual control sequences (pulse durations, which edges are activated) for X, Z, cphase, and especially the swap gate, which is not reconstructed.
- How the transfer step handles bosonic enhancement (\sqrt{2} tunneling factor) and single-particle phases during the collisional cphase.
- Logical encoding for the seven-qubit Steane code and the third-dimension lattice extension for error correction.
- Ultracold-atom optical-lattice parameters (J, U, \epsilon_v ranges, timescales, loss and heating rates).
- Any numerical fidelity or error-threshold results from the paper.
