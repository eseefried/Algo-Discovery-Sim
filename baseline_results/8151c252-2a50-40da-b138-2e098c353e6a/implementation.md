# Equation to Qiskit

Gate-model Simon operation for an n-bit black box (n input qubits + n output qubits, n<=6): H on the input register, the standard reversible oracle U_f|x>|y>=|x>|y xor f(x)> for the 'pivot' family f(x)=x xor (x_j * s) (which reproduces the specification's explicit n=2 instance s=11, f(x1,x2)=(0,x1 xor x2) = CNOT_{x2,y2} CNOT_{x1,y2}), then H on the input register again. No state preparation or measurement is included; the runner measures the input register to obtain z with z.s=0 mod 2.

Source equation run: `ac0666bb-03a8-4a20-a164-7e383c117317`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: input x_2 (least significant input bit), register 'x'
- qubit 1: input x_1 (most significant input bit), register 'x'
- qubit 2: output y_2 (least significant output bit), register 'y'; receives CNOTs from x_2 and x_1 in the example
- qubit 3: output y_1 (most significant output bit), register 'y'; untouched (stays |0>) in the example s=11
- Runner measures qubits 0..1 as z = z_1 z_2 (z_1 on qubit 1); for the example Pr(z=00)=Pr(z=11)=1/2, Pr(01)=Pr(10)=0
- Expected input state: |0000> on all qubits (prepared by the runner)

## Assumptions

- Hidden string s is given as a bit string 's_1...s_n' with s_1 the most significant bit, matching the specification's |x_1 x_2> ordering.
- The pivot-oracle family is the agent's choice; the paper's 'key representative functions' are unknown and are not claimed to be reproduced beyond the eq_5 instance.
- The one-way (cluster-state) implementation of the paper is assumed logically equivalent to this circuit-model unitary; the cluster graph and measurement pattern are not reconstructed.
- Optional key include_hadamards=false returns only the oracle U_f, for runners that want to test eq_2 in isolation.

## Unresolved issues

- The paper's actual five-qubit cluster-state graph, measurement bases, and the list of queried black-box functions are not available; only the logical circuit is implemented.
- No simulation or verification has been performed by the agent; the stated outcome probabilities (eq_4, eq_5) are analytic expectations for the runner to check.

## Equation mapping

- `eq_1`: background; no code location. Simon's promise is a property of the chosen oracle family (argued in the module docstring), not an operation to implement.
- `eq_2`: implemented; _apply_oracle. U_f|x>|y>=|x>|y xor f(x)> realized with CNOTs for f(x)=x xor (x_j*s).
- `eq_3`: implemented; build_circuit (Hadamard layers around _apply_oracle). The returned circuit is (H^n x I) U_f (H^n x I); applied to |0^n>|0^n> by the runner it produces the state of eq_3.
- `eq_4`: out_of_scope; no code location. Outcome distribution of the input-register measurement; measurement and sampling are performed by the runner, not in the module.
- `eq_5`: implemented; _apply_oracle with the example instance n=2, s="11" (pivot j=1 gives CNOT x_2->y_2, CNOT x_1->y_2). The explicit n=2 instance is exactly reproduced by the general pivot construction.
- `eq_6`: out_of_scope; no code location. Classical GF(2) postprocessing of measured outcomes is not part of the unitary operation.

## Specification changes

- eq_3, eq_4: The module returns only the unitary (H^n x I) U_f (H^n x I); state preparation |0^n>|0^n> and the computational-basis measurement of the input register are left to the runner. Reason: Task requires a measurement-free operation without input-state preparation.
- eq_2, eq_5: Scope generalized from the single n=2, s=11 instance to the oracle family f(x)=x xor (x_j*s) for any 1<=n<=6 and any s (including s=0^n, giving f(x)=x); the n=2, s=11 member coincides with eq_5. Reason: The task asks for an operation that works for varying valid instance parameters; this family is the simplest CNOT-only realization satisfying eq_1 for every s.
- eq_2: The two cancelling CNOTs x_j->y_j (from the copy step and the mask step) are omitted rather than appended. Reason: They multiply to the identity; omitting them yields the same unitary with fewer gates and matches the two-CNOT form of eq_5.
- eq_2, eq_3: Bit/qubit order made explicit: x_i (x_1 most significant) sits on qubit n-i, y_i on qubit 2n-i. Reason: Qiskit qubit 0 is the least significant bit while the specification writes x_1 as the leftmost (most significant) bit.
