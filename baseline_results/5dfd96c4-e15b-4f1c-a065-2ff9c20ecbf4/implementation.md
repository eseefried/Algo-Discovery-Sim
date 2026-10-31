# Equation to Qiskit

Implements the scoped dual-rail Bose-Hubbard quantum-walk gate set as a Qiskit operation. Each graph vertex is one qubit (hard-core truncation, occupation <= 1); logical qubit k occupies physical qubits 2k (rail 0) and 2k+1 (rail 1). Three piecewise-constant Hamiltonian segments are exponentiated exactly: intra-pair tunneling -J(a0^dag a1 + h.c.) -> RXX(-Jt) RYY(-Jt) (eq_3, logical R_X(-2Jt)); on-site bias (eps/2)(n0 - n1) -> P(-eps t/2) on rail 0 and P(+eps t/2) on rail 1 (eq_4, logical R_Z(eps t)); and the collisional controlled phase, realized as its net effect cp(-U tau) between the two rail-1 vertices (eq_5). The number of logical qubits is 1..6 (<= 12 physical qubits); measurement (eq_6) is excluded because the module returns an operation only.

Source equation run: `6184036e-aac4-45e3-83c1-6f6dfc334b83`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- v[0] (qubit index 0, least significant): graph vertex v_0^(1), rail 0 of logical qubit 1; occupied (|1>) encodes |0_L>_1
- v[1] (qubit index 1): graph vertex v_1^(1), rail 1 of logical qubit 1; occupied (|1>) encodes |1_L>_1
- v[2] (qubit index 2): graph vertex v_0^(2), rail 0 of logical qubit 2; occupied (|1>) encodes |0_L>_2
- v[3] (qubit index 3): graph vertex v_1^(2), rail 1 of logical qubit 2; occupied (|1>) encodes |1_L>_2
- General rule: logical qubit k (0-indexed) uses physical qubits 2k (rail 0) and 2k+1 (rail 1); the code subspace has exactly one of each pair set to |1>
- Specification initial state |0_L>_1 |0_L>_2 corresponds to physical basis state with v[0]=1, v[1]=0, v[2]=1, v[3]=0 (bitstring '0101' in Qiskit little-endian order); the runner prepares inputs

## Assumptions

- hbar = 1; gate parameters are the physical quantities J, epsilon, U and durations t, tau; angles are theta_X = -2 J t, theta_Z = epsilon t, phi = -U tau as in the specification.
- Qubit index 2k is rail 0 and 2k+1 is rail 1 of logical qubit k; the input state supplied by the runner has exactly one of each pair in |1> (code subspace). Outside the code subspace the tunneling gate acts as identity on |00> and |11> and the bias gate contributes only phases.
- Hard-core bosonic mapping a_v^dag a_w + h.c. -> (X_v X_w + Y_v Y_w)/2 is used for the single active edge; no Jordan-Wigner string is needed because bosons commute and only one edge is active per segment.
- Durations t and tau are required to be non-negative; J, epsilon, U may have either sign.
- Global phases are ignored, consistent with the specification.

## Unresolved issues

- The paper's actual pulse sequences (including the swap gate and the transfer step with bosonic sqrt(2) enhancement) are unknown; only the effective gates on the code subspace are reproduced.
- The explicit piecewise-constant 2D graph layout achieving linear vertex count is not represented; the circuit only encodes per-qubit vertex pairs and the pairwise interaction edge.
- Leakage out of the one-boson-per-pair subspace (loss, double occupancy) is not modelled; the hard-core truncation forbids double occupancy by construction.

## Equation mapping

- `eq_1`: implemented; _apply_tunnel, _apply_bias, _apply_collide (module docstring): each gate is exp(-i H t) of a piecewise-constant Bose-Hubbard segment restricted to the hard-core (occupation <= 1) subspace. The hopping term is mapped to (XX+YY)/2 per active edge, on-site energies to phase gates, and the interaction term to its effective conditional phase; only the segments needed for the gate set are instantiated, not the full 2D lattice.
- `eq_2`: implemented; _rails and module docstring. Dual-rail position encoding: vertex v_0^(k) -> physical qubit 2k, vertex v_1^(k) -> physical qubit 2k+1; a boson on a vertex is the qubit value |1>.
- `eq_3`: implemented; _apply_tunnel. exp(-i H_X t) with H_X = -J(a0^dag a1 + h.c.) = -J(XX+YY)/2 realized as RXX(-Jt) RYY(-Jt); equals R_X(theta), theta = -2Jt on the single-boson subspace and identity on |00>,|11>.
- `eq_4`: implemented; _apply_bias. exp(-i H_Z t) with H_Z = (eps/2)(n_v0 - n_v1) realized as P(-eps t/2) on rail 0 and P(+eps t/2) on rail 1, equal to R_Z(eps t) on the logical subspace.
- `eq_5`: implemented; _apply_collide. The net CPHASE(phi), phi = -U tau, on |1_L 1_L> is implemented as cp(-U tau) between the two rail-1 vertex qubits; the transfer T / double-occupancy intermediate is not modelled (see specification_changes).
- `eq_6`: out_of_scope; no code location. Occupation-number readout is a measurement; the module must return a measurement-free operation, so readout is left to the runner (measure each rail qubit; occupied rail index is the logical bit).

## Specification changes

- eq_1, eq_2: Fock space truncated to occupation <= 1 per vertex (hard-core bosons, one qubit per vertex) instead of the specification's occupation <= 2. Reason: Double occupancy appears only transiently in the unspecified transfer step of the cphase; the hard-core truncation makes the hopping term an exact (XX+YY)/2 qubit Hamiltonian and keeps the circuit within 12 qubits for up to 6 logical qubits.
- eq_5: The collisional controlled phase is implemented by its net effect, a direct cp(-U tau) between the rail-1 vertices of the two logical qubits, rather than by an explicit transfer T, on-site wait, and inverse transfer with sqrt(2) bosonic enhancement. Reason: The transfer pulse schedule is listed as missing information in the specification and double occupancy is excluded by the hard-core truncation; the implemented unitary equals the specified CPHASE(phi = -U tau) on the code subspace (it corresponds physically to an interaction U n_{v1^(1)} n_{v1^(2)} for duration tau). Compensating single-particle Z rotations are therefore not needed.
- eq_1: Only intra-pair tunneling edges, per-pair on-site biases, and the pairwise rail-1 conditional phase are instantiated; the general 2D piecewise-constant graph, swap gate, and the full Bose-Hubbard lattice evolution are not built. Reason: Scope narrowing to the gate set reconstructed in the math stage; the explicit graph geometry is missing information.
- eq_2, eq_3, eq_4, eq_5: Generalized from exactly two logical qubits to 1..6 logical qubits (2..12 physical qubits) with an arbitrary user-supplied sequence of tunnel/bias/collide segments. Reason: Required to implement the operation for varying valid instance parameters; the two-qubit example instance matches the specification's steps.
- eq_6: Measurement and the classical post-processing (leakage flagging for pairs with occupation != 1) are omitted from the module. Reason: The module must return a measurement-free unitary operation; readout belongs to the runner.
