# Equation to Qiskit

Qiskit circuit for the first-order Lie-Trotter product (eq_3) of U(t)=exp(-i(|w><w|+|s><s|)t) on n<=12 qubits with m steps. Each factor exp(-i phi |w><w|) is X-conjugated multi-controlled phase, and exp(-i phi |s><s|) is H^n-conjugated phase on |0...0>. No state preparation or measurement is included.

Source equation run: `5d0473fe-89ef-47b2-b452-00a97463ef1a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 form the search register q; qubit 0 is the least significant bit of the basis index x; marked integer w is encoded in this little-endian convention.
- No ancillas; total qubits = n <= 12.

## Assumptions

- Hamiltonian H=|w><w|+|s><s| with hbar=1, as in eq_1.
- Each projector exponential is implemented exactly, including global phase, using multi-controlled phase gates.
- Little-endian encoding of marked state w.

## Unresolved issues

- The paper's actual Hamiltonian and time convention are unknown.
- The reflection scheme with logarithmic error scaling is not reconstructed.
- Error bounds and complexity claims are not verified by this circuit.

## Equation mapping

- `eq_1`: background; build_circuit (the two projector factors). Assumed Hamiltonian H=|w><w|+|s><s|; it is not built as a matrix, only its two projector exponentials appear as Trotter factors.
- `eq_2`: background; no code location. Exact evolution U(t)=exp(-iHt) is the target being approximated; it is not constructed as a dense operator.
- `eq_3`: implemented; build_circuit loop over m steps with _phase_on_basis. Implements (exp(-i|w><w|t/m) exp(-i|s><s|t/m))^m, with the s-factor applied first as the right-hand operator.
- `eq_4`: out_of_scope; no code location. Reflection-operator construction is the alternative discretisation and is not implemented here.
- `eq_5`: out_of_scope; no code location. Grover iteration and success probability formula belong to the reflection option; not implemented.

## Specification changes

- eq_3: Scope narrowed to the Lie-Trotter option only, generalised to n qubits (1..12), arbitrary marked index, real t, and m steps. Reason: The task requires one explicit construction; the reflection scheme is not fully specified.
- eq_4, eq_5: Reflection-based Grover iteration not implemented. Reason: The paper's logarithmic-error scheme is unspecified, and this is a separate construction.
- eq_1: The projector |s><s| exponential is realised as H^n exp(-i phi|0..0><0..0|) H^n, using |s>=H^n|0>. Reason: Gives an exact gate-level decomposition of each Trotter factor.
