# Equation to Qiskit

Builds a Grover oracle for a classical database as compute-mark-uncompute. A QROM-style memory (multi-controlled X gates) loads D_x into a data register conditioned on the index register. A multi-controlled X then marks the flag qubit when D_x equals a target value. The memory is then uncomputed. With the flag in |-> (prepared by the runner) this gives the phase (-1)^{f(x)}.

Source equation run: `f6f41210-36c9-4056-b1dc-0046983a1f6c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: index register (qubit 0 least significant address bit)
- qubits n..n+m-1: data register (qubit n least significant data bit), must start in |0>
- qubit n+m: flag ancilla; the runner should prepare |-> for phase kickback
- Example (n=3, m=2): index=q0-q2, data=q3-q4, flag=q5

## Assumptions

- Data register starts in |0> and is restored to |0> by uncomputation.
- Entries are fixed-width m-bit integers.
- Memory contents are classical parameters of the instance and are compiled into gates.

## Unresolved issues

- The abstract does not give the paper's actual memory circuit; this QROM construction is an assumed realization.
- The number of marked items and the Grover iteration count are not addressed.

## Equation mapping

- `eq_1`: implemented; build_circuit (memory, mark, memory sequence). The net action is |x>|0>|b> -> |x>|0>|b XOR f(x)>. With the flag in |-> this equals the phase (-1)^{f(x)}. The |-> preparation is left to the runner.
- `eq_2`: implemented; _memory. The classical memory is a QROM made of multi-controlled X gates that load D_x into the data register for each address x. It is applied once to compute and once to uncompute.
- `eq_3`: implemented; _mark. The predicate g is fixed as equality with a target value, f(x) = [D_x == target], computed by a multi-controlled X onto the flag.

## Specification changes

- eq_3: The predicate g is narrowed to equality with an integer target. Reason: The specification leaves g unspecified; equality is a simple concrete choice.
- eq_1, eq_2: The circuit implements only the oracle. It excludes Hadamard initialization, diffusion, iteration and measurement. The flag |-> is prepared externally, so the oracle is a phase oracle only for that input. Reason: The task requires an operation without state preparation or measurement.
- eq_2: The database size is restricted to N = 2^n entries. Reason: The index register is made of qubits and needs a full address space.
