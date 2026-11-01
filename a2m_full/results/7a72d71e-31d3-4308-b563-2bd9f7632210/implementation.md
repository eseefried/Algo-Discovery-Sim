# Equation to Qiskit

Implements one scoped PQF step as a measurement-free unitary W on 1 data qubit and 1 ancilla: H on the ancilla, controlled-G on the data qubit, then H on the ancilla. Here G = diag(e^{i a}, e^{-i a}) with a = j*pi/4, so each ancilla outcome m gives a data-qubit block A_m = (I + (-1)^m G)/2, which is proportional to a unitary. Block A_0 is proportional to Rz(-a), which is T^{-j} up to phase, and has probability cos^2(a/2). Block A_1 is proportional to Z*T^{-j}, with probability sin^2(a/2). An optional coherent (deferred-measurement) CZ correction implements the outcome-1 byproduct. Measurement, classical feedforward, the multi-step chain and the synthesis are not implemented.

Source equation run: `6ac1cbf5-bc96-4314-9f40-fcf2e0dcd0bc`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: data (single-qubit state acted on by the chain unitary; little-endian index 0)
- qubit 1: ancilla (input |0>, supplied by the runner; computational-basis value is the outcome m, which is not measured in the circuit)

## Assumptions

- The runner prepares the ancilla in |0> and the data qubit in an arbitrary state
- alpha = t_power*pi/4, so the data blocks are T-power gates up to phase
- Outcome m corresponds to the computational-basis value of qubit 1 after the final Hadamard
- t_power multiples of 4 are rejected because one outcome has zero probability
- The apply_correction option is a coherent stand-in for classical feedforward

## Unresolved issues

- The abstract does not specify the actual PQF W_k, fallback states, correction maps or the definition of b
- The multi-step chain, the absorbing target and the expected T-count cost are not realized in the circuit
- The Clifford+V and Clifford+pi/12 constructions are not implemented
- The asymptotic scaling claim is not addressed

## Equation mapping

- `eq_1`: implemented; build_circuit: h(1); crz(-2*alpha,1,0); h(1). A concrete instance of the ancilla-assisted step. W(|psi>|0>) = sum_m (I+(-1)^m G)/2 |psi> (x) |m>. Each block is proportional to a unitary, as eq_1 requires. The probabilities are p_0=cos^2(alpha/2) and p_1=sin^2(alpha/2).
- `eq_2`: out_of_scope; no code location. The full Markov-chain update needs mid-circuit measurement, classical feedforward and a multi-step chain, and the abstract gives no explicit chain. Only the optional coherent CZ correction (outcome-1 byproduct Z, via deferred measurement) touches this equation.
- `eq_3`: out_of_scope; no code location. Absorbing target states, approximation error and termination need a synthesized chain for a target unitary U, which is not constructed here.
- `eq_4`: background; no code location. The expected cost is a classical post-hoc computation over branch probabilities. It is not part of the unitary circuit.
- `eq_5`: out_of_scope; no code location. The asymptotic scaling claim cannot be realized or checked by a single-step circuit.

## Specification changes

- eq_1, eq_2, eq_3: Narrowed to a single measurement-free step with a hand-chosen W (H, controlled-Rz, H) instead of a chain of norm-equation-synthesized W_k with measurement and feedforward. Reason: The abstract gives no explicit W_k or chain, and the required output must be a unitary circuit with no measurement or dynamic circuits.
- eq_2: The classically controlled correction C_{k,m} is replaced by an optional coherent CZ from the ancilla to the data qubit (deferred measurement), and the next-state composition is not built. Reason: Classical feedforward is not allowed. Deferred measurement is the unitary equivalent for the single correction.
- eq_1: The block form is made concrete: A_0 is proportional to Rz(-alpha), i.e. T^{-j} up to phase, and A_1 is proportional to Z*Rz(-alpha). Reason: An explicit unitary-block example is needed. The instance is invented for illustration and is not claimed to come from the paper.
