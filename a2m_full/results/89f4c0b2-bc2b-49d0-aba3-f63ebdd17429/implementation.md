# Equation to Qiskit

Builds an n-qubit diagonal Hermitian gate D=diag((-1)^f(x)) from a truth table f. The circuit computes the GF(2) algebraic normal form of f with the fast binary Moebius transform. It then applies one multi-controlled Z gate (Z, CZ, or H-MCX-H) per nonempty subset S with c_S=1, on data qubits only. A constant ANF term becomes a global phase of pi. There are no ancillas, measurements, or state preparation.

Source equation run: `2c5148d1-0c1d-4363-889f-2d50e7ab149d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubit i (Qiskit index i, i=0..n-1) holds bit x_i of the computational basis index x; index 0 is least significant.
- Single register q of n data qubits, no ancillas.
- truth_table[x] = f(x) with x = sum_i x_i 2^i; D|x> = (-1)^f(x)|x>.

## Assumptions

- Instance keys are n and truth_table; truth_table[x]=f(x) with x little-endian.
- Order of MCZ gates is irrelevant because they are all diagonal and commute.
- Gate decomposition of MCX is left to Qiskit's standard mcx.

## Unresolved issues

- The paper's exact binary representation convention and its gate ordering/sharing optimization are not reconstructed.
- How the paper decomposes MCZ gates with |S|>=3 into CZ gates is unknown.

## Equation mapping

- `eq_1`: implemented; build_circuit: truth_table validation (bits 0/1 define signs (-1)^f(x)). The gate is specified directly by its sign function f as a 0/1 truth table; non-binary entries are rejected with ValueError.
- `eq_2`: implemented; build_circuit: final loop applying z/cz/h-mcx-h on qubits of S. MCZ_S applies the phase (-1)^(prod x_i over S) via Z, CZ, or H-MCX-H on the last qubit of S.
- `eq_3`: implemented; build_circuit: Moebius transform result b[S] used as c_S; global_phase for b[0]. The ANF coefficients c_S are the expansion of the binary representation in the MCZ basis. The constant term is mapped to global_phase=pi when it is 1.
- `eq_4`: implemented; build_circuit: nested loops over i and x (Moebius butterfly). For each bit i and each x with bit i set, b[x] ^= b[x without bit i], giving c_S = xor of f(x) over x subset of S.
- `eq_5`: implemented; build_circuit: loop over s in 1..2^n-1 with b[s]==1. The circuit is the product of the commuting MCZ_S gates over the support of c, with global phase (-1)^c_empty.

## Specification changes

- eq_3, eq_5: The constant ANF term c_empty is kept as an exact circuit global_phase of pi instead of being dropped. Reason: This makes the circuit equal to D exactly, not only up to global phase; it costs no gates.
- eq_1, eq_3, eq_4, eq_5: The instance is generalized from the tiny n=3 case to any n in 1..12, with the truth table supplied in the instance. Reason: Required to support varying valid instance parameters, under the 12-qubit cap.
- eq_5: Gray-code ordering, gate sharing, CZ-based decomposition of large MCZ gates, and cost comparison are not implemented. MCZ with |S|>=3 uses H-MCX-H. Reason: These are outside the stated reconstruction scope.
