# Equation to Qiskit

Single-qubit Trine POVM as a Naimark-type isometric dilation: one polarisation qubit plus a 3-site walker position encoded in 2 qubits. The circuit applies Rx(pi/2) on the input, a SWAP, and a real orthogonal 4x4 operator built from Givens-rotation controlled-Ry gates. After the circuit, the polarisation qubit is |0> and the position register holds amplitudes a_k = sqrt(2/3)<psi_k|phi>, so p_k = Tr(E_k rho). The optical walk layout, SIC and USD POVMs are not implemented.

Source equation run: `5f0b0f1a-4a7a-489a-a280-965dbe45f0ac`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: pol (polarisation, |0>=|H>, |1>=|V>); input state qubit; ends in |0>
- qubit 1: pos bit 0 (least significant bit of position x), input |0>
- qubit 2: pos bit 1 (x = q1 + 2*q2); outcome k=x in {0,1,2}, x=3 has zero probability
- Input: |phi> on qubit 0, |00> on qubits 1,2. Output outcome read from qubits 1,2 (little-endian integer x).

## Assumptions

- Three equal-weight elements on the xy equator with theta_k = phase_offset + 2 pi k/3.
- Rx(phi) = exp(-i phi X/2) rotates the Bloch vector by phi about x, so psi_k = Rx(-pi/2) psi'_k and the circuit applies Rx(+pi/2) to the input.
- The input is |phi> on qubit 0 and |00> on qubits 1 and 2, prepared by the runner.
- Global phases are irrelevant.

## Unresolved issues

- The mapping to the experiment's actual wave-plate angles and displacer geometry is not reconstructed.
- SIC and USD POVMs are not covered.
- Numerical correctness of the Givens decomposition and the frame-change sign convention rely on downstream verification.

## Equation mapping

- `eq_1`: background; no code location. General POVM definition and Born rule. The circuit's position-register statistics are intended to reproduce p_k = Tr(E_k rho); completeness holds because sum E_k = I for equally spaced equatorial elements.
- `eq_2`: implemented; _isometry_columns (Trine elements through rows sqrt(2/3)<psi'_k|) and the Rx(pi/2) frame change in build_circuit. E_k = (2/3)|psi_k><psi_k| with theta_k = phase_offset + 2 pi k/3. The equatorial xy-plane trine is mapped to a real xz-plane trine by Rx(-pi/2) so the isometry can be built from real rotations.
- `eq_3`: implemented; build_circuit (rx, swap, controlled-Ry Givens network via _givens_sequence/_inverse_givens_gate). Dilation isometry realised with Kraus operators M_k = sqrt(2/3)|0><psi_k|, so M_k^dagger M_k = E_k and sum M_k^dagger M_k = I. The output polarisation is fixed to |0> rather than sqrt(E_k)|phi>; see specification_changes.
- `eq_4`: out_of_scope; no code location. The walk structure (wave-plate coins and displacer shifts) is not implemented. Coin angles and step counts are unspecified, so the dilation is built directly from Givens rotations instead.

## Specification changes

- eq_3: Used Kraus operators M_k = U_k sqrt(E_k) with U_k sending the polarisation output to the fixed state |0>, i.e. M_k = sqrt(2/3)|0><psi_k|, instead of M_k = sqrt(E_k) = sqrt(2/3)|psi_k><psi_k|. Reason: Both have M_k^dagger M_k = E_k, so the outcome statistics are identical. The chosen form lets the circuit be a 2-qubit real orthogonal operator on the position register after a SWAP, and the polarisation is not read out.
- eq_4: The alternating coin/shift walk is replaced by a direct gate decomposition (Rx, SWAP, controlled-Ry from Givens rotations); no walk steps appear. Reason: The coin angles and step count are not specified, and the walk is only one possible realisation of the dilation.
- eq_2, eq_3: The position register uses a binary encoding of 3 sites in 2 qubits (x = q1 + 2*q2); site 3 is unused. An optional phase_offset parameter rotates the trine about the Bloch z axis. Reason: Qubit encoding requirement; the offset is a convention-preserving generalisation and defaults to 0 (theta_k = 2 pi k/3).
- eq_2: Only the Trine POVM is implemented; SIC and USD are excluded. Reason: Scope narrowing: the specification gives no explicit SIC/USD elements or parameters.
