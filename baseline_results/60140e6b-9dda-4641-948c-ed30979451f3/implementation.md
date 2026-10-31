# Equation to Qiskit

Measurement-free unitary realisation of the two-query algorithm for a completely specified affine Boolean function f(x)=a.x xor b. Qubits 0..n-1 form the input register, qubit n is the phase-kickback ancilla for query 1 (runner prepares it in |1>), and optional qubit n+1 is a fresh |0> ancilla for query 2. Query 1 is the Bernstein-Vazirani circuit (H on all n+1 qubits, bit-flip oracle U_f, H on the input register) which leaves the input register in |a> up to a global phase (-1)^b. Because resets/measurements are disallowed, query 2 is applied coherently at the point x_0 = a now sitting in the input register, with the second ancilla as target, giving |f(a)> = |parity(a) xor b>; the runner recovers b = z xor parity(a) classically. The oracle is built from CX gates (one per nonzero a_i) and an X on the target if b = 1.

Source equation run: `89a7918c-7790-46c9-b738-18a571e43133`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1 (register x): input register, qubit i holds bit x_i, x_0 least significant; after query 1 holds the coefficient vector a (example: q1=1, q0=0, i.e. a=(a_1,a_0)=(1,0))
- qubit n (register y): first ancilla, runner prepares |1>; the circuit applies H so it is |-> during the kickback query and remains |-> at the output
- qubit n+1 (register z, only if two_query): second ancilla, runner prepares |0>; output is |f(a)> = |parity(a) xor b> (example: parity(a)=1, b=1 -> z=0, so b = z xor parity(a) = 1)
- example total qubits: 4 (n=2 input + 2 ancillas); the global phase (-1)^b is not observable

## Assumptions

- Affine Boolean function means f(x) = a.x xor b over GF(2); the instance key 'a' lists a_i for qubit i (a[0] = a_0 is the least significant bit).
- The runner prepares the input register in |0^n>, the first ancilla (qubit n) in |1>, and the optional second ancilla (qubit n+1) in |0>.
- The standard bit-flip oracle model is assumed; the oracle is built transparently from CX and X gates since a and b are instance parameters.
- Both the first and second oracle calls use the identical oracle U_f, so the construction uses exactly two queries.
- If two_query is false the circuit is the plain one-query Bernstein-Vazirani operation on n+1 qubits.
- Qubit cap: n <= 10 when two_query is true (n+2 <= 12), n <= 11 otherwise.

## Unresolved issues

- The paper's actual second-query circuit is unknown; the coherent evaluation at x_0 = a is a reconstruction.
- If the runner prepares the first ancilla in |0> instead of |1>, the phase kickback is lost and the input register returns to |0^n>; the expected input state must be honoured.
- The bounded-error algorithms for incompletely defined functions and the 2/3 bound (eq_5) are not reconstructable from the abstract.

## Equation mapping

- `eq_1`: implemented; _apply_oracle: CX from each input qubit i with a_i = 1 to the target computes a.x; X on target adds b. The affine function f(x) = a.x xor b is encoded reversibly into the oracle target via CX gates and a conditional X.
- `eq_2`: implemented; _apply_oracle (bit-flip oracle) and the H on anc1 in build_circuit producing the |-> ancilla for phase kickback. U_f|x>|y> = |x>|y xor f(x)> is realised by CX/X gates; with the ancilla in |-> this yields the phase (-1)^{f(x)}.
- `eq_3`: implemented; build_circuit, 'Query 1' block: H on inputs and ancilla, _apply_oracle to anc1, H on inputs. The Bernstein-Vazirani one-query unitary; on |0^n>|1> it outputs (-1)^b |a>|->.
- `eq_4`: implemented; build_circuit, 'Query 2' block: _apply_oracle to anc2 with the input register in |a>. Implemented in the general form b = f(x_0) xor a.x_0 with x_0 = a (the state already present after query 1) instead of x_0 = 0^n, because resets/measurements between queries are not permitted.
- `eq_5`: out_of_scope; no code location. The bounded-error analysis for incompletely defined functions requires the paper's function classes and algorithm modifications, which are not available.

## Specification changes

- eq_4: The second query point was changed from x_0 = 0^n (with the input register reset) to x_0 = a, the state the input register deterministically occupies after query 1, with a fresh second ancilla as the oracle target. Output z = f(a) = parity(a) xor b, so b is recovered classically as z xor parity(a) where parity(a) is computed from the measured input register. Reason: The deliverable must be a single measurement-free unitary circuit without reset or dynamic operations, so the mid-circuit measurement and re-preparation in the specification cannot be used; the specification itself allows any known query point x_0 with b = f(x_0) xor a.x_0.
- eq_3: The first ancilla is expected to be prepared by the runner in |1>; the circuit applies the Hadamard (not the X) as part of the algorithm. The global phase (-1)^b is left as is. Reason: Input-state preparation is reserved for the runner; the Hadamards are part of the Bernstein-Vazirani operation as described in the specification steps.
- eq_5: Scope narrowed to completely specified affine functions; the incompletely defined bounded-error setting is not implemented. Reason: Essential definitions (care sets, function classes, modified algorithms) are missing from the abstract.
