# Equation to Qiskit

Qiskit module implementing the scoped construction: a Grover oracle for an unstructured classical database realised as compute-lookup / compare-with-target / uncompute-lookup, where the quantumly accessible classical memory U_D is a product of multi-controlled-X gates (one per stored 1-bit), followed by the standard Grover diffusion on the address register. build_circuit returns k Grover iterates (oracle then diffusion) or k bare oracle calls; it does not prepare the uniform superposition or measure (the runner supplies inputs). Database, record width, target and iteration count are instance parameters; total qubits n+m are capped at 12.

Source equation run: `f5a049e7-f011-4ec5-bf44-726f80f40de4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: addr[0] = a_0 (least significant address bit of x = 2 a_1 + a_0)
- qubit 1: addr[1] = a_1 (most significant address bit)
- qubit 2: data[0] = bit 0 of D[x]; expected |0> on input and returned to |0> after each oracle call
- Total 3 qubits for the example; general layout is addr = qubits 0..n-1 (bit i of x on qubit i), data = qubits n..n+m-1 (bit j of D[x] on qubit n+j); n+m <= 12
- Expected runner input for the example: H on qubits 0 and 1 (uniform |s>), qubit 2 in |0>; output after the circuit is |x=1> = addr bits (a_1,a_0)=(0,1), data |0>

## Assumptions

- The paper's concrete memory architecture is unknown; the memory is modelled as the reversible XOR lookup U_D realised by one multi-controlled-X per stored 1-bit (this is a simple correct realisation, not necessarily the paper's circuit).
- The search predicate is exact equality D[x] = t; the data register is assumed to enter in |0...0> and is uncomputed to |0...0> after each oracle call.
- Multi-controlled X gates (qc.mcx) are treated as available primitives; no ancilla-based decomposition is specified.
- The example instance uses n=2, m=1, D=(0,1,0,0), t=1, k=1, for which a single Grover iterate maps |s>|0> to |x=1>|0> exactly.

## Unresolved issues

- The actual oracle circuit, gate counts and memory layout proposed in the paper cannot be reconstructed from the abstract.
- Whether the paper uses additional ancilla or garbage qubits, or handles unknown numbers of matches M, is unknown; the module requires the iteration count to be supplied.

## Equation mapping

- `eq_1`: implemented; _lookup (docstring 'eq_1 / eq_2'). XOR semantics of the quantumly accessible classical memory: data bit j is flipped exactly when bit j of D[x] is 1, implemented as mcx gates controlled on the address register being |x>.
- `eq_2`: implemented; _lookup. Product over addresses with stored 1-bits of C^{(x)}X: X gates on address lines where the bit of x is 0, mcx onto the data bit, X gates undone. Generalised to m > 1 by one such gate per set bit j of D[x].
- `eq_3`: implemented; _oracle and _phase_flip_on_value. Compute lookup, apply I - 2|t><t| on the data register (Z for m=1 and t=1; X-conjugated multi-controlled Z in general), then uncompute with the same lookup sequence since U_D is self-inverse.
- `eq_4`: implemented; _diffusion. Inversion about the mean H^n (2|0><0| - I) H^n on the address register, implemented up to a global phase as H, X-conjugated multi-controlled Z, H. The uniform state |s> preparation part of eq_4 is deliberately NOT included: the runner prepares inputs.
- `eq_5`: background; no code location. The iteration count k and success probability are analysis results; k is taken as the instance parameter 'iterations' (k=1 for the example N=4, M=1) rather than computed inside the circuit module.

## Specification changes

- eq_4: The circuit omits the H^{\otimes n} preparation of |s> and omits measurement; it returns only the operation (O_t followed by diffusion)^k. Reason: Task requires an operation without input-state preparation or measurement; the runner supplies the uniform superposition input.
- eq_1, eq_2: Address bit ordering is mapped to Qiskit little-endian: bit a_i of x is stored on qubit i (qubit 0 = a_0), whereas the specification listed a_{n-1} as the 'first' qubit. Reason: Qiskit qubit index 0 is the least significant computational-basis bit; mapping bit i to qubit i makes the integer value of the address register equal to x.
- eq_4: Diffusion is implemented as H^n (I - 2|0><0|) H^n, i.e. -(2|s><s| - I), differing by a global phase of -1. Reason: Multi-controlled Z realises I - 2|0><0| directly; the global phase has no observable effect.
- eq_5: Iteration count k is an explicit instance parameter ('iterations' >= 1) and is not derived from N and M in code; an 'oracle_only' flag allows returning O_t^k without diffusion. Reason: Keeps the module a pure operation builder and allows validation of the oracle in isolation.
- eq_2, eq_3: Generalised from the scoped m=1, t=1 instance to arbitrary m-bit records and target t (multi-controlled Z on the data register conjugated by X on zero bits of t), with n+m capped at 12. Reason: Requirement that build_circuit handle varying valid instance parameters.
