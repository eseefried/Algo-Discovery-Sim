# Equation to Qiskit

Ideal Grover search (D O_w)^k on n qubits (default n=4, k=3), with the marked-state phase oracle O_w = I - 2|w><w| built explicitly from the integer w using X, H and mcx gates, and the diffusion operator D = 2|s><s| - I built as H^n X^n MCZ X^n H^n with a global phase of pi. No measurements or state preparation by default; an optional flag prepends H^n. The nuclear spin chain physics (Rabi pulses, Ising couplings, 2*pi*k condition) is not implemented.

Source equation run: `b5568342-6324-4e56-827e-e3f510756634`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 (n=4 in the example): data qubits, qubit i is bit i of the marked integer w (qubit 0 least significant).
- No ancilla qubits; no classical bits; no measurements.
- Multi-controlled Z acts on target qubit n-1 with controls 0..n-2.

## Assumptions

- Single marked basis state w, provided in the instance.
- Qiskit little-endian: qubit i holds bit i of w.
- Ideal gates only; no noise and no Ising coupling.
- Standard gates h, x, mcx are used. Qiskit decomposes the multi-controlled X without any dense unitary.
- Default iteration count follows eq_2 for the chosen n.

## Unresolved issues

- The paper's marked state and pulse-level implementation are not specified.
- The nuclear-spin-chain Hamiltonian, coupling strengths, Rabi frequencies and the 2*pi*k condition are not modeled.
- Fidelity versus iteration (eq_4) is left to the downstream verifier.

## Equation mapping

- `eq_1`: implemented; _oracle, _diffusion, _mcz. O_w is built from X gates on the zero bits of w plus MCZ. D is H^n X^n MCZ X^n H^n with a global phase of pi added so it equals 2|s><s|-I exactly.
- `eq_2`: implemented; build_circuit: k_star. Default iteration count floor(pi/4*sqrt(N)), which is 3 for n=4. It can be overridden by the iterations parameter.
- `eq_3`: implemented; build_circuit: loop over k iterations and optional include_uniform_layer H^n. Applies (D O_w)^k. The initial H^n is applied only if include_uniform_layer is true, because input state preparation is normally done by the runner.
- `eq_4`: background; no code location. The closed form F_k = sin^2((2k+1)theta) is an analytic prediction, not a circuit operation. It is not encoded in the module.
- `eq_5`: out_of_scope; no code location. Readout and bit-order post-processing involve measurement, which the module must not contain. The qubit i = bit i of w convention is respected in the oracle.

## Specification changes

- eq_1: The oracle is an explicit, parameterized phase flip on a marked integer w, not an opaque placeholder gate. Reason: The runner needs a concrete unitary for varying w. An opaque or dense-unitary oracle is not allowed.
- eq_1: A global phase of pi is added per diffusion so the circuit equals D = 2|s><s|-I exactly rather than only up to a global phase. Reason: The gate sequence H X MCZ X H equals -D, so the phase is corrected to match the stated equation.
- eq_3: Initial H^n is optional and off by default. Reason: The operation must not include input-state preparation. The flag lets the full algorithm be reproduced if wanted.
- eq_1, eq_2, eq_3: Generalized from fixed n=4 to n in 2..12 and a configurable iteration count, with defaults reproducing n=4, k=3. Reason: The task requires the operation to work for varying valid parameters. The default behaviour matches the specification.
- eq_4, eq_5: Fidelity analysis and measurement/readout are excluded from the circuit. Reason: The module must be measurement-free. The fidelity formula is analysis only.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope narrowed to ideal, coupling-free Grover search. Spin-chain pulses, Ising couplings and the 2*pi*k condition are not modeled. Reason: The specification gives no Hamiltonian, coupling strengths, Rabi frequencies or pulse decomposition.
