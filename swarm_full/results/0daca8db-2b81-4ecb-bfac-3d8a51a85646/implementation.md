# Equation to Qiskit

Coherent (deferred-measurement) unrolling of n weak-measurement iterations on a system qubit with n fresh probe qubits. Each iteration applies exp(-i*phi*|0><0|_S (x) Y_P), a controlled-RY(2*phi) from system to probe, followed by a fixed system unitary pulse. Probe preparation and readout are left to the runner. The Hamiltonian, probe state and pulses are assumed, since the abstract does not give them.

Source equation run: `4ed49d48-77fd-4f3b-8beb-e653f671d1d4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system S (qubit being weakly measured; input prepared by runner)
- qubits 1..n_steps: probe qubits P_k, one fresh probe per iteration k, assumed prepared in |0> by runner; computational-basis readout is done by runner (deferred measurement)
- Qiskit little-endian: qubit 0 is least significant bit

## Assumptions

- Probe qubits start in |0>, prepared by the runner.
- H_int = |0><0|_S (x) Y_P, with phi = g*dt supplied in the instance.
- Pulses are arbitrary fixed single-qubit U(theta, phi, lambda) gates on the system, applied after each step.
- Up to 11 iterations, each with its own probe, so the total is at most 12 qubits.

## Unresolved issues

- The paper's actual Hamiltonian, probe state and readout basis are unknown.
- The feedback pulse rule and stopping criterion are unknown, and outcome-conditioned feedback is not implemented.
- The rule mapping the outcome record to the final binary outcome is unknown.
- The circuit does not itself demonstrate the abstract's claim about two distinct singular values.

## Equation mapping

- `eq_1`: background; no code location. Completeness of the Kraus operators is a standard property. It holds automatically here because each step is a unitary dilation, so the code does not implement it directly.
- `eq_2`: implemented; build_circuit: loop body, X-CRY-X on (S, P_k). With assumed H_int = |0><0|_S (x) Y_P, probe |0> and readout in the computational basis, M_0 = diag(cos(phi), 1) and M_1 = diag(sin(phi), 0). The unitary exp(-i*phi*H) is implemented as a controlled-RY(2*phi) with the control active on system |0>.

## Specification changes

- eq_2: Chose a concrete H_int = |0><0|_S (x) Y_P with phi = g*dt, probe initial state |0>, and computational-basis readout. Reason: The abstract gives no explicit Hamiltonian, probe state or readout basis, so a concrete simple choice was needed to build a circuit.
- eq_1, eq_2: Narrowed scope to a fixed-length unrolled sequence of n_steps coherent weak-measurement steps. Pulses are fixed U gates given in the instance and are not conditioned on outcomes. Measurement is deferred and left to the runner. Reason: The required output is a measurement-free unitary circuit with no dynamic circuits, reset or classical feedback. The abstract's feedback rule and stopping criterion are not specified.
- eq_1, eq_2: The circuit does not realize or verify a specific target two-outcome measurement or the two-distinct-singular-values result. Reason: The mapping from the outcome record to the final binary outcome is not given.
