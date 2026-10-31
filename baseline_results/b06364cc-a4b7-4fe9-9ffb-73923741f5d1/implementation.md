# Equation to Qiskit

Implements the first-order Trotterized time-evolution operator of the N-level pairing Hamiltonian in its Anderson pseudospin (qubit) form: single-qubit Z rotations for the level energies and nearest-neighbor XY (flip-flop) gates for the pair-scattering couplings (eq_2-eq_4). Optionally the whole evolution is made controlled on one ancilla qubit, which is the unitary core of the ancilla-based energy-spectrum extraction scheme (eq_5). State preparation, ancilla measurements, Fourier post-processing and fidelity evaluation are left to the runner/classical side.

Source equation run: `702fa4f1-994b-4dcc-8221-a63337bdc81e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system qubit for pair mode m=1 (|1> = Cooper pair occupies level 1), energy eps_1 = -1.0
- qubit 1: system qubit for pair mode m=2 (|1> = pair occupies level 2), energy eps_2 = 1.0; coupled to qubit 0 by XY gate with V_12 = 0.5
- qubit 2: ancilla control qubit for the spectrum-extraction scheme (runner prepares |+>, measures X and Y); present only because controlled=true
- Little-endian: qubit 0 is the least significant bit of the computational basis label

## Assumptions

- hbar = 1; RZ(phi) = exp(-i phi Z/2), so exp(-i eps_m/2 Z dt) = RZ(eps_m*dt) and the XY factor has theta = V_{m,m+1} dt.
- Anderson pseudospin encoding: qubit m-1 in |1> means pair mode m is occupied; no Jordan-Wigner strings are needed.
- Within each Trotter step the single-qubit Z rotations are applied before the two-qubit XY gates (first-order formula; order affects only O(dt^2) error).
- Ideal noiseless gates; device-specific native interaction types are not modeled.
- Initial states (|10> system, |+> ancilla) are prepared by the runner, not inside build_circuit.

## Unresolved issues

- The paper's actual Hamiltonian conventions, interaction types (Heisenberg/Ising/XXZ), Trotter order and measurement scheme are unknown; the XY/ancilla construction is a plausible stand-in.
- Long-range pairing couplings V_{ml} with |m-l|>1 are rejected rather than routed via SWAP networks.
- Controlled Trotter evolution extracts eigenvalues up to the dropped constant offset; absolute energies require adding it classically.

## Equation mapping

- `eq_1`: background; no code location. Fermionic pairing Hamiltonian; only its qubit image (eq_2) is used to define gates.
- `eq_2`: implemented; build_circuit: 'eq_2/eq_3 single-qubit terms' loop (rz/crz) and _xy_gate for the XY couplings. Pseudospin form defines the Z and XY generators exponentiated in each Trotter step; the constant term is dropped (global phase in the uncontrolled case).
- `eq_3`: implemented; build_circuit: dt = t/n_steps and the outer 'for _ in range(n_steps)' loop. First-order Trotter product with uniform step; Z rotations then nearest-neighbor XY gates, repeated n_T times.
- `eq_4`: implemented; _xy_gate and _zz_core. exp(-i theta/2 (XX+YY)) built exactly as RXX(theta)RYY(theta) via basis-changed CX-RZ-CX cores; controlled variant replaces RZ by CRZ.
- `eq_5`: implemented; build_circuit: controlled=True branch (ancilla register, crz in Z terms and _zz_core). Only the unitary controlled-U_Trotter(t) is implemented; ancilla |+> preparation, X/Y measurement, time sweep and Fourier transform are excluded (runner/classical post-processing).
- `eq_6`: out_of_scope; no code location. Fidelity is a classical numerical benchmark comparing with exact evolution; not part of the circuit operation.

## Specification changes

- eq_2, eq_3: Constant term of H_P dropped. In the ancilla-controlled circuit this is not a global phase but a uniform shift of all extracted energies E_k by the dropped constant. Reason: The abstract/specification does not fix the constant; a uniform spectral offset is irrelevant for level spacings and can be added classically.
- eq_2, eq_3, eq_4: Generalized from the N=2 instance to any N>=2 (N+ancilla<=12) but restricted the coupling matrix to nearest-neighbor pairs V_{m,m+1} only; non-adjacent V_{ml} are not accepted (no SWAP routing). Reason: Matches the 'nearest-neighbor interaction' device model of the abstract while keeping the construction parameterizable; routing strategy is listed as missing information.
- eq_4: XY gate realized as RXX(theta)*RYY(theta) decomposed into H/S/CX/RZ(CRZ) gates rather than a native device coupling. Reason: Qiskit has no native tunable XY interaction primitive; XX and YY commute so the decomposition is exact.
- eq_5: Scope narrowed to the controlled-evolution unitary; ancilla preparation, measurements, time sampling and Fourier analysis omitted. Reason: Task requires a measurement-free unitary operation; these parts belong to the runner and classical post-processing.
- eq_6: Not implemented. Reason: Fidelity is a classical figure of merit, not a circuit operation.
