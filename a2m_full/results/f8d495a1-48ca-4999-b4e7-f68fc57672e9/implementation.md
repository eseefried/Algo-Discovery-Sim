# Equation to Qiskit

Gate-level Naimark dilation of the 3-outcome trine POVM on 3 qubits. The input polarisation qubit is moved into the position register by a swap. A controlled-RY and a controlled-Hadamard conjugated by CNOTs map the input to the outcome amplitudes sqrt(2/3)<t_k|psi> on position k. An optional controlled-RY set then rotates the polarisation qubit into |t_k>, so that K_k = sqrt(2/3)|t_k><t_k|. The circuit is unitary, measurement-free and prepares no input state.

Source equation run: `e7c334d9-9c51-4139-be57-5aaea17626d0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: pol (polarisation/coin qubit, input |psi>, little-endian LSB of the full register)
- qubit 1: pos bit 0 (LSB of outcome label k)
- qubit 2: pos bit 1 (MSB of outcome label k)
- Outcome k = q1 + 2*q2 in {0,1,2}; k=3 has zero amplitude. Input convention: pos=|00>, pol=|psi>. Output: sum_k |k>_pos (x) K_k|psi>_pol.

## Assumptions

- Trine states are real, in the x-z Bloch plane, with t_0=|0>.
- Outcome label k is encoded as pos value q1+2*q2, with the |00> start state on pos.
- Outcomes are identified with position labels. The pol output state is |t_k> (default) or |0>.
- Global phases per outcome follow the real amplitude signs of the Kraus operators.

## Unresolved issues

- The paper's actual coin angles, shift schedule, and (x,p)-to-outcome mapping are not reproduced.
- SIC and USD constructions are not implemented.
- The circuit's validity as an exact Naimark dilation has not been simulated here and is left to downstream verification.

## Equation mapping

- `eq_1`: background; no code location. Defines the POVM and Born rule. Completeness is guaranteed by the isometry construction, and probabilities are left to downstream analysis.
- `eq_2`: implemented; build_circuit: ry(-phi), swap, cry, cx/ch/cx (amplitudes sqrt(2/3)<t_k|psi>) and the final controlled RYGate loop (post-state |t_k>). Trine elements E_k = (2/3)|t_k><t_k| with t_k = ry(2k*pi/3)|0>, optionally rotated by frame_angle.
- `eq_3`: out_of_scope; no code location. The literal two-step coined walk S2(I(x)C2)S(I(x)C1) is not reproduced because the coin angles are unspecified. An equivalent gate-level Naimark dilation is used instead.
- `eq_4`: implemented; build_circuit (whole circuit is a unitary whose action on |00>_pos|psi> is the isometry V). V^dag V = I holds because the circuit is unitary. The amplitude-producing part acts as a unitary on the 3-state span and was checked analytically to give columns (sqrt(2/3),1/sqrt6,-1/sqrt6) and (0,1/sqrt2,1/sqrt2).
- `eq_5`: out_of_scope; no code location. SIC and USD targets are not implemented. Only the trine is scoped.

## Specification changes

- eq_3: Replaced the coined-walk form with an equivalent gate-level dilation: swap, controlled-RY, a CX-conjugated controlled-H, and controlled-RY post-rotations. The shifts are not literal beam-displacer analogues. Reason: The paper's coin angles and shift schedule are not given. The explicit analytic decomposition avoids opaque unitaries and numerical offline solving.
- eq_2, eq_4: Added optional frame_angle (rotation of the trine frame about the Bloch y axis) and restore_polarisation (if false the pol qubit ends in |0>, so K_k = sqrt(2/3)|0><t_k|). Reason: Orientation of the trine frame is unresolved in the specification. The same E_k = K_k^dag K_k is preserved in both modes.
- eq_5, eq_3: Narrowed scope to trine only. SIC and USD are not implemented. Reason: The task requires ONE explicitly scoped construction. The USD state pair and SIC orientation are unspecified.
