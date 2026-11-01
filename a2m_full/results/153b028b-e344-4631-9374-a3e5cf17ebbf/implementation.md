# Equation to Qiskit

Builds the 2-qubit Clifford+T block W on (data q0, ancilla q1) from an instance-supplied gate list over {h,s,sdg,t,tdg,x,y,z,cx}. The ancilla is assumed to start in |0>, and W block-encodes A=(I x <0|)W(I x |0>) on the data qubit. Measurement, the retry loop, correction and synthesis of the gates are excluded. The abstract gives no actual RUS gate sequence, so the circuit is a generic, validated block builder and the example sequence is a placeholder.

Source equation run: `e578db56-4806-4760-aed6-699639dcfab1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: data qubit q0 (QuantumRegister 'data'), least significant bit
- qubit 1: ancilla q1 (QuantumRegister 'anc'), expected to be prepared in |0> by the runner; success = measured 0
- no classical bits; the circuit has no measurement

## Assumptions

- The runner prepares the ancilla in |0> and the data qubit in the input state, then postselects or measures the ancilla.
- Gate names are limited to h, s, sdg, t, tdg, x, y, z and cx, which keeps the block in the Clifford+T set.
- The total qubit count is fixed at 2, within the cap of 12, and the gate list is capped at 200 entries.

## Unresolved issues

- The actual RUS circuit family, failure-branch correction and exact T-count structure are not given in the abstract.
- No guarantee is made that the example W has a success branch A proportional to a unitary, or that it approximates a particular U.
- The randomized polynomial-time synthesis algorithm and the 2.5x T-count benchmark are not reconstructed.

## Equation mapping

- `eq_1`: implemented; build_circuit: constructs the unitary block W on (data=qubit 0, ancilla=qubit 1); A is the <0|_anc W |0>_anc sub-block, which is defined by the runner's input and postselection. The circuit is W. The block-encoding relation holds by construction when the ancilla is prepared in |0> and projected onto 0. The runner does the preparation and projection.
- `eq_2`: background; no code location. The success probability and the identity A†A+B†B=I follow from unitarity of W and are analysis quantities. Nothing is computed in the circuit.
- `eq_3`: out_of_scope; no code location. The approximation criterion and the (u,v) form of A require the paper's synthesis algorithm, which is not given in the abstract. The module does not synthesize W for a target U and eps.
- `eq_4`: background; no code location. The expected T-count T_W/p_s is classical post-processing of the retry loop. It needs measurement and feedback, which are excluded from this operation.
- `eq_5`: background; no code location. The ancilla-free bound 3 log2(1/eps) is a reference value for comparison only.

## Specification changes

- eq_1, eq_2, eq_4: Scope narrowed to the single unitary block W. Ancilla measurement, the failure-branch correction and the retry loop are not implemented. Reason: The task requires a measurement-free, non-dynamic unitary circuit. The runner handles input preparation and postselection.
- eq_1, eq_3: W is taken as an instance-supplied Clifford+T gate list rather than a synthesized circuit approximating a given U. The example sequence is a placeholder and not the paper's RUS circuit. Reason: The abstract does not give the RUS gate sequence or the synthesis algorithm, so no specific construction can be reproduced faithfully.
- eq_3: The trailing '$$' in the eq_3 LaTeX is treated as a typographical artifact, and the equation is not implemented. Reason: The (u,v) matrix form is only an assumption in the specification and its derivation is unknown.
- eq_1: Register order is fixed as the data qubit at index 0 and the ancilla at index 1. The block-encoding notation (I x <0|_1) is read with Qiskit little-endian ordering. Reason: This matches the stated assumption that q0 is data and q1 is the ancilla.
