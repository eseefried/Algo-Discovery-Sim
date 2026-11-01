# Equation to Qiskit

Measurement-free unitary for n iterations of a qubit-probe weak measurement on one system qubit. Each iteration applies a system pulse U_k, then exp(-i*eps_k*H_SP) with an assumed constant H_SP = |1><1|_S (x) X_P, implemented as a controlled-RX(2*eps_k) onto a fresh probe qubit. Probes start in |0> (prepared by the runner) and are read out in the computational basis by the runner. Projecting probe k onto <j| gives K_0 = diag(1, cos eps), K_1 = diag(0, -i sin eps), which have distinct singular values.

Source equation run: `902d05b5-350d-49c8-a6a7-228bd7a1d59a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system S (computational basis, qubit 0 is least significant bit)
- qubit 1: probe P_0 (iteration 1), expected input |0>
- qubit 2: probe P_1 (iteration 2), expected input |0>
- qubit k+1: probe P_k (iteration k+1), expected input |0>; up to 11 probes

## Assumptions

- The system is a single qubit.
- The probe starts in |0> and is prepared by the runner.
- Probe readout is in the computational basis and is done by the runner.
- H_SP = |1><1|_S (x) X_P, so exp(-i eps H_SP) is a controlled-RX with angle 2*eps.
- Fixed pulse angles and a fixed number of iterations are supplied in the instance.
- If pulses are omitted, identity pulses are used.

## Unresolved issues

- The paper's actual interaction Hamiltonian is unknown.
- The feedback rule, stopping criterion and outcome coarse-graining to M_0 and M_1 are not implemented.
- The continuous-time limit and the characterization theorem are not reconstructed.
- The number of iterations is capped at 11 by the 12-qubit limit, which is far from a continuous decomposition.

## Equation mapping

- `eq_1`: background; no code location. Completeness of the Kraus operators follows from the global unitarity of the circuit (a probe-outcome partition) and is not coded separately.
- `eq_2`: implemented; build_circuit: qc.crx(2*eps[k], S[0], P[k]). Unitary exp(-i eps H_SP) with the assumed H_SP = |1><1|_S (x) X_P, acting on a fresh probe. The projection onto <j|_P (probe measurement) is left to the runner.
- `eq_3`: implemented; build_circuit: loop over k with qc.u(...) then qc.crx(...). Interleaves system pulses U_k with weak-interaction iterations, using one fresh probe per iteration so that the Kraus product K_{j_n}U_n...K_{j_1}U_1 arises after probe outcomes are read. Coarse-graining is not implemented.
- `eq_4`: background; no code location. The SVD and distinct-singular-value condition is a characterization of achievable measurements, not an operation. The chosen H_SP gives K_0 = diag(1, cos eps), which has distinct singular values, but nothing checks that.

## Specification changes

- eq_2: Chose the specific constant Hamiltonian H_SP = |1><1|_S (x) X_P, with initial probe |0> and computational-basis readout. Reason: The abstract and spec leave H_SP unspecified, and a concrete choice is needed. A Z(x)X-type coupling would give two Kraus operators with equal singular values, so it was avoided.
- eq_3: Scope narrowed to a fixed, user-given list of iteration strengths and pulse angles, with no feedback, stopping rule or coarse-graining. Pulses are U3 gates (U(2), differing from SU(2) by a global phase). Probe measurements are deferred, and fresh probe qubits are used instead of reset. Reason: The feedback rule is unspecified and dynamic circuits, reset and measurement are disallowed. Fresh probes make the circuit a unitary on the system plus the probes.
- eq_1, eq_4: Not implemented as circuit operations. Reason: They are a background constraint and a characterization result, respectively.
