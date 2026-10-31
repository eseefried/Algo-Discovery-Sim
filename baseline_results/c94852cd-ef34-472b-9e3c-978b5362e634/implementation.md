# Equation to Qiskit

Coinless (tessellation / staggered) discrete-time quantum walk on a cycle of N = 2^n sites, encoded on n site qubits with no coin register. One step is U = U_1 U_0 where U_0 = 2 sum_k |alpha_k><alpha_k| - I acts as the same single-qubit reflection R Z R^dagger (R = U(theta,phi,0)) on the least-significant site qubit (polygons {2k,2k+1}), and U_1 is the analogous reflection for the shifted tessellation {2k+1, 2k+2 mod N}, realised as S U_0(theta',phi') S^dagger with S the cyclic increment |x> -> |x+1 mod N> built from QFTGate and phase gates. The circuit applies U^t for t steps; input-state preparation and measurement are left to the runner.

Source equation run: `acb5370a-ec56-411a-aa35-5089b1d104ae`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- site[0] = qubit 0: least significant bit of the site index x (parity bit; equals the coin value c in the relabelling of eq_7)
- site[1] = qubit 1: most significant bit of x for the N = 4 example (general: site[j] = qubit j carries bit 2^j of x)
- Site x in Z_N, N = 2^num_qubits, is the integer with binary expansion x = sum_j x_j 2^j over the site qubits; there is no coin register

## Assumptions

- Two tessellations of nearest-neighbour two-site polygons with translation-invariant parameters (theta,phi) and (theta',phi').
- Each tessellation operator has the reflection form 2P - I (standard staggered form); more general operators from the paper are not covered.
- For num_qubits = 1 (N = 2) both tessellations consist of the same pair {0,1}; the construction remains well defined.
- Instance angles are arbitrary finite reals; steps capped at 1000 and qubits at 12 to bound circuit size.

## Unresolved issues

- The paper's specific family of evolution operators and its explicit 'extended coined' shift/coin factorisation of U_1 are unknown; only the reflection family of eq_3 with the parity relabelling of eq_7 is implemented.
- Mixing time and limiting-distribution analysis (eq_5, eq_6) require classical post-processing outside this module.

## Equation mapping

- `eq_1`: implemented; build_circuit: QuantumRegister(n, 'site') with comment 'eq_1: the whole Hilbert space is the site register, no coin factor'. The circuit uses only n = log2(N) site qubits, i.e. the N-dimensional site space, with no coin register.
- `eq_2`: implemented; _polygon_reflection (|alpha> = U(theta,phi,0)|0>) and _walk_step (tessellation-1 polygons obtained from tessellation-0 polygons by the cyclic shift S). Polygon states for both tessellations are parametrised by (theta,phi) and (theta',phi') exactly as in eq_2; the shifted pairs {2k+1, 2k+2 mod N} are handled by conjugating with S.
- `eq_3`: implemented; _walk_step (U = U_1 U_0), _polygon_reflection (2P-I as R Z R^dagger), _cyclic_shift (S for U_1 = S U_0' S^dagger). Each reflection 2 sum_k |.><.| - I is realised exactly as a single-qubit reflection on the LSB (optionally conjugated by the increment S); their product is one step.
- `eq_4`: implemented; build_circuit loop 'for _ in range(steps): _walk_step(...)' with comment 'eq_4'. Only the unitary part U^t is implemented; the initial state |0> and the measurement giving p_t(x) are the runner's responsibility per the operation-only contract.
- `eq_5`: out_of_scope; no code location. Time-averaged and limiting distributions are classical post-processing of measured p_t(x) (or classical diagonalisation of U); not part of the quantum operation.
- `eq_6`: out_of_scope; no code location. Mixing time is a classical quantity derived from eq_5 outputs; not part of the circuit.
- `eq_7`: implemented; _polygon_reflection docstring: LSB qubit plays the role of the coin so U_0 = I_{N/2} (x) C_0. The parity relabelling |2k+c> <-> |k>|c> is literally the binary encoding with qubit 0 = c; U_0 is implemented as the coin operation C_0 on that qubit. The shift/coin factorisation of U_1 from the paper is not reconstructed (U_1 is implemented as S C_0' S^dagger instead).

## Specification changes

- eq_1, eq_2, eq_3: Cycle size restricted to powers of two, N = 2^num_qubits (N even is automatically satisfied), with num_qubits in 1..12. Reason: Sites are encoded as binary integers on qubits; a non-power-of-two cycle would need a modular shift on a padded register, which is outside the minimal construction.
- eq_3: U_1 implemented as S U_0(theta',phi') S^dagger with S the cyclic increment realised as QFT^dagger . (phase gates) . QFT, instead of directly as parallel 2x2 blocks on pairs {2k+1, 2k+2 mod N}. Reason: The shifted tessellation pairs are not aligned with a single qubit, so a basis-shift conjugation is the natural exact gate-level realisation; the resulting operator equals eq_3's U_1 exactly.
- eq_4: Initial-state preparation |psi(0)> = |0> and computational-basis measurement removed from the circuit; only U^t is returned. Reason: Required operation-only contract (inputs prepared and measured by the runner).
- eq_5, eq_6: Time averaging, limiting distribution, and mixing time are not implemented. Reason: They are classical post-processing of measurement statistics, not quantum operations.
- eq_1, eq_7: Site index encoding fixed to Qiskit little-endian convention (qubit 0 = least significant bit) rather than the 'big-endian' wording of the specification. Reason: Qiskit's basis-state ordering; this makes the parity/coin bit of eq_7 coincide with qubit 0 and simplifies U_0 to a single-qubit gate.
- eq_3: Reflection 2|alpha><alpha| - I implemented as U(-theta,0,-phi) . Z . U(theta,phi,0) on the polygon qubit. Reason: Exact decomposition into standard gates; U(theta,phi,0)|0> = |alpha> so R Z R^dagger = 2|alpha><alpha| - I with no global-phase discrepancy.
