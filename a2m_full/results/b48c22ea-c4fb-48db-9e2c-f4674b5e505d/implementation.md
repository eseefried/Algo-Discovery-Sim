# Equation to Qiskit

Implements the label-independent Bell-like basis-generating operation for the n-qubit scope: H on m control qubits, then a type A CNOT fan from controls to targets realizing the GF(2)-linear map f, then optional type B sign gates (Z on controls) for g(c)=w.c. The runner prepares |b>_ctrl|a>_tgt with X gates, and the circuit maps it to |Psi_{a,b}> of eq_1. No measurements or state preparation are included.

Source equation run: `18c8056f-187d-4ec7-bf3a-5e2800d6b504`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: ctrl[0] (control, H applied; input X sets phase label b_0)
- qubits 1..n-m... generally: qubits 0..m-1 = ctrl[0..m-1], least significant first
- qubits m..n-1 = tgt[0..n-m-1] (input X sets bit-flip label a)
- example n=3,m=1: q0=ctrl[0], q1=tgt[0], q2=tgt[1]; input basis state |a_1 a_0 b_0> in Qiskit order, fan flips both targets (GHZ-like for a=0,b=0)

## Assumptions

- The paper's two multiple-qubit controlled unitaries are interpreted as a CNOT-fan type A and a linear phase type B (my interpretation, not the paper's definitions).
- Gate order is H on controls, then CNOT fan, then sign gates.
- Qiskit little-endian order: controls at qubits 0..m-1, targets at m..n-1.

## Unresolved issues

- The paper's exact controlled-unitary definitions and basis-generation orderings are not recoverable from the abstract.
- Type B as Z on controls only relabels b, so it does not produce a genuinely different basis; paper's different-entanglement bases may require other constructions.
- Monogamy-score measure used by the paper is unspecified.

## Equation mapping

- `eq_1`: implemented; build_circuit: H loop on controls and CNOT fan loop. H on controls plus CNOT fan maps runner-prepared |b>|a> to (1/sqrt(2^m)) sum_c (-1)^{b.c}|c>|f(c) xor a>.
- `eq_2`: background; no code location. Amplitude magnitude is a property of the output states (H then CNOTs and Z only); it is checked externally, not coded.
- `eq_3`: background; no code location. Orthonormality follows because the circuit is unitary and maps computational basis labels bijectively; Gram matrix check is a classical postprocessing step outside the operation.
- `eq_4`: implemented; build_circuit: Z loop over controls with w_i = 1. Type B sign (-1)^{w.c} is implemented as Z gates on the control qubits selected by w.
- `eq_5`: out_of_scope; no code location. Monogamy score is classical statevector postprocessing, not part of the circuit operation.

## Specification changes

- eq_1: Labels a and b are not applied inside the circuit; the runner prepares |b>_ctrl|a>_tgt with X gates and the circuit is only the H+fan(+sign) operation. Reason: The task requires an operation without input-state preparation.
- eq_1, eq_3: Injectivity of f is enforced as GF(2) rank m of the fan matrix, which requires m <= n-m; invalid fans raise ValueError. A default fan is provided: control i flips target i, and the last control flips targets m-1..n-m-1. Reason: The specification assumes f injective and linear, but did not fix a pattern.
- eq_4: Type B is implemented as Z gates on controls (g depends only on c). Since this equals a relabeling b -> b xor w, it permutes basis states and yields the same set of states, differing only in label assignment. Reason: Matches the stated linear g(c) literally; the paper's actual CZ-type gate is not specified.
- eq_1: Instance size range widened from n in 3..5 to n in 3..12 (the platform qubit cap). Reason: The 12-qubit cap is the actual constraint; the circuit is cheap and valid for any n.
- eq_5: Entanglement and monogamy measures excluded. Reason: Classical postprocessing on statevectors, not a circuit operation.
