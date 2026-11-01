# Equation to Qiskit

Builds a palindromic NCT circuit G = g1...gk [c] gk...g1 on n data lines (plus an optional ancilla line). The caller supplies the half-sequence of NOT/CNOT/Toffoli gates and an optional central self-inverse gate. The builder appends the half-sequence, the center, and the mirrored half-sequence, so the gate list equals its reverse by construction and the circuit is an involution. It does not synthesize a circuit from an involution table.

Source equation run: `b81bdbc2-7ac1-41a0-bab8-3efd7b175cf7`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n-1: data register, little-endian (x = sum x_i 2^i), qubit i holds bit x_i
- qubit n (only if ancilla=1): ancilla line, expected |0> in and |0> out (not enforced)
- example: n=3, no ancilla -> qubits 0,1,2 are data bits x0,x1,x2

## Assumptions

- Gates are NOT (0 controls), CNOT (1 control) or Toffoli (2 controls), all self-inverse.
- Qubit indices in instance gates are global, with data on 0..n-1 and the ancilla on n.
- The central gate, if present, is a single self-inverse NCT gate.
- The runner prepares inputs and reads outputs with little-endian ordering.

## Unresolved issues

- No synthesis of a palindromic circuit from an arbitrary involution table is implemented.
- The necessary-and-sufficient condition for palindromic realizability is not encoded.
- The ancilla construction and the controlled-V/V-dagger palindrome are not implemented.
- The parity obstruction and the ancilla-returns-to-0 condition are not checked in code.

## Equation mapping

- `eq_1`: background; no code location. Involution/cycle structure of f is the mathematical framing. The module takes a gate list rather than a permutation table and does not decompose f or verify f(f(x))=x.
- `eq_2`: implemented; build_circuit: half gates, then optional center, then reversed(half). The gate list is a palindrome of self-inverse NOT/CNOT/Toffoli gates, so G equals its reverse circuit and G^2 = id.
- `eq_3`: implemented; build_circuit: h = half gates, c = center gate, h^-1 = reversed half. Conjugation form G = h c h^-1 with c a single self-inverse gate (or absent, giving the identity). The mirrored half-sequence is exactly h^-1.
- `eq_4`: background; no code location. The parity obstruction on n>=4 lines is a known result used to motivate the ancilla. It is not checked or enforced in code.
- `eq_5`: implemented; build_circuit: ancilla option (qubit n) usable in half/center gates. Only the container is implemented: a palindromic circuit on n+1 lines whose gates may act on the extra line. The code does not construct an ancilla realization of a given f and does not verify that the ancilla is restored to 0.

## Specification changes

- eq_1, eq_3, eq_5: Scope narrowed to a palindrome builder. The caller supplies the half gate list and center gate, and the module does not search for or synthesize a circuit realizing a given involution table. Reason: The abstract does not give the characterization or construction, and the task forbids simulation and searching with unverified claims. The synthesis rule is not resolvable from the available information.
- eq_5: Ancilla restoration to |0> is the caller's responsibility and is not validated. Reason: Checking it would require simulating the circuit.
- eq_2, eq_3: The controlled-V/V-dagger palindrome variant is omitted. The gate library is NCT only (up to 2 controls). Reason: The V/V-dagger placement rule is unspecified, since the reverse of V is V-dagger.
- eq_4: The data-line range is restricted to 2<=n<=4, with an optional single ancilla (at most 5 qubits). Reason: This matches the declared domain of n in the specification.
