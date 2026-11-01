# Equation to Qiskit

Grover search iterations G^k on an n-qubit address register for a classical 1-bit database. The oracle is built from an XOR-type memory lookup U_M (one multi-controlled X per marked entry, writing d(x) into a data qubit). The oracle is U_M, Z on D, U_M, Z on D. This equals the phase oracle O on the address register and the identity on D for any input state of D. Each iteration is followed by diffusion 2|s><s|-1. No state preparation or measurement is included.

Source equation run: `e9fd34c2-bbf8-43a3-9b4b-4a669b423aa8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: address register A, little-endian (qubit 0 is the least significant bit of x)
- qubit n: data/ancilla qubit D, returned unchanged by the oracle; the operation acts as identity on D for any input state
- example (n=2): q0,q1 = A; q2 = D; marked address x=2 means q1=1,q0=0

## Assumptions

- The memory lookup is modelled as an XOR-type unitary built from multi-controlled X gates, which is not necessarily the paper's circuit.
- Database entries are single bits supplied in the instance.
- Standard Grover iterate with the diffusion operator 2|s><s|-1 including its global phase.
- The runner prepares the uniform superposition on A; D can be in any state.

## Unresolved issues

- The paper's actual simple oracle circuit and memory design are not reconstructed from the abstract.
- Gate counts and resource scaling are not those of the paper; the mcx-per-marked-entry construction is generic and costly.
- The optimal iteration count is not computed by the module; the caller chooses iterations.

## Equation mapping

- `eq_1`: implemented; _lookup. XOR memory lookup, implemented as one multi-controlled X per entry with d(x)=1, with X conjugation selecting the address pattern.
- `eq_2`: implemented; _phase_oracle. Phase oracle O via the lookup, but using compute-Z-uncompute instead of requiring the data qubit in |->. U_M Z_D U_M Z_D = O on A and identity on D.
- `eq_3`: implemented; _diffusion and build_circuit loop. Grover iterate G = (2|s><s|-1) O repeated k times. Diffusion is H X MCZ X H with a global phase of pi added to match 2|s><s|-1 exactly. Initial |s> preparation is left to the runner.
- `eq_4`: background; no code location. Success-probability formula. The circuit takes the iteration count k as an input and does not compute the optimal k.
- `eq_5`: background; no code location. Tiny instance n=2, d=(0,0,1,0), k=1; it is the example instance JSON, not code logic.

## Specification changes

- eq_2: The oracle uses lookup, Z on D, lookup, Z on D rather than the stated (1 (x) <-|) U_M (1 (x) |->) projection. D need not be in |->, and the data qubit is unchanged for any input. Reason: The operation must not prepare states. A bare U_M would be correct only if the runner puts D in |->. The compute-Z-uncompute form is exact for any D input.
- eq_1, eq_2, eq_3: Address encoding is little-endian (Qiskit qubit 0 is the LSB of x), not big-endian as in the register description. Reason: This matches the Qiskit convention. The database index x maps to the computational basis integer x.
- eq_3: The initial Hadamards on A and the X,H preparation of D are excluded from the circuit. The circuit contains only the k Grover iterations. Reason: The task requires an operation with no input-state preparation. The runner prepares |s> on A.
- eq_1, eq_2, eq_3, eq_4, eq_5: The scope is narrowed to 1-bit entries and generic XOR-lookup oracle synthesis, with n_address from 1 to 11. Instances must have at least one marked and one unmarked entry, and iterations are capped at 64. Reason: The abstract does not give the paper's memory circuit. The 12-qubit cap leaves at most 11 address qubits plus 1 data qubit.
