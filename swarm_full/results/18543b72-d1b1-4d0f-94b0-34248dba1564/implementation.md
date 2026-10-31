# Equation to Qiskit

Builds the Grover iterate G^k on an n-qubit index register (N=2^n) with a single marked address, using an ancilla-free phase oracle and the diffusion operator. k is given explicitly or derived from a guessed database size N' via k=floor(pi/4*sqrt(N')), which models the size-uncertainty setting. No state preparation or measurement is included; the runner supplies the uniform superposition. The phone-book encoding and the discrimination analysis are not implemented.

Source equation run: `69183d37-b2d9-4fd2-acb6-2bc4ad31d77f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: index register 'index', little-endian (qubit i holds bit i of the address; marked address m has bit i of m on qubit i)
- No ancilla qubits; total qubits = n <= 12
- Expected input prepared by runner: uniform superposition H^{⊗n}|0...0> for standard Grover

## Assumptions

- Single marked item, with N=2^n.
- The runner prepares the uniform superposition on the index register.
- The guessed size N' only affects the iteration count, and the physical register stays at n qubits.
- The iteration count is capped at 1000 and the guessed size at 2^24.

## Unresolved issues

- The quantum phone book encoding and programmable name or number queries are not specified in the abstract.
- The unambiguous discrimination scheme and its success rates are not implemented.
- The prior distribution over database size is unspecified.

## Equation mapping

- `eq_1`: implemented; build_circuit loop with _oracle and _diffusion. The circuit applies G^k (oracle then diffusion). On the uniform input state it yields sin((2k+1)theta)|w> + cos((2k+1)theta)|w_perp>.
- `eq_2`: implemented; build_circuit: k = floor(pi/4*sqrt(g)) branch. The iteration count is derived from the (possibly guessed) size g=N' using the approximate optimal formula. If guessed_size differs from 2^n, this models a mismatched-size run.
- `eq_3`: out_of_scope; no code location. The overlap and unambiguous-discrimination analysis is a classical or POVM analysis of states, not part of this unitary operation. The abstract also does not specify its setup.

## Specification changes

- eq_1: The initial Hadamard layer is omitted, and only the Grover iterate G^k is built as the operation. Reason: The task forbids input-state preparation in the circuit, so the runner must supply the uniform superposition.
- eq_1: The oracle is an ancilla-free phase oracle (multi-controlled phase) instead of the specified ancilla in |->. Reason: This is equivalent by phase kickback and uses fewer qubits. It also avoids ancilla preparation.
- eq_1: A global phase of pi per iteration is added so the circuit equals (2|s><s|-I)O exactly. Reason: Diffusion is built as I-2|s><s|, the negative of the standard form.
- eq_1, eq_2: The scope is narrowed to N=2^n and a single marked integer address. Number-versus-name phone-book queries are not modeled, and a guessed N' only sets k. Reason: The abstract gives no encoding of the phone book or the programmable query construction.
- eq_3: The distinguishability and discrimination analysis is not implemented. Reason: The discrimination setup, POVM and success rates are unspecified. The analysis is not a unitary circuit.
