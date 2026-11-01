# Equation to Qiskit

build_circuit(instance) synthesizes a diagonal Hermitian gate D=diag((-1)^f(x)) as a product of multiple-controlled Z gates. It solves the GF(2) system for the coefficients c_S with an in-place Moebius (algebraic normal form) transform, then emits Z, CZ, or H-MCX-H for each S with c_S=1. It covers n=1..12 and includes the specified n=2 case.

Source equation run: `9f5358cb-6d33-42e4-8bfe-5b7ff5ebd3c3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register q has n qubits (n<=12); Qiskit qubit i is bit i of the basis-state integer x (qubit 0 = LSB).
- For n=2, the spec's qubit 1 (MSB) is Qiskit q[1] and spec's qubit 2 (LSB) is Qiskit q[0].
- The f/signs list index x = sum_i x_i 2^i is the computational-basis integer.
- No ancillas; no input preparation or measurement.

## Assumptions

- The binary representation is the f-vector (the paper's encoding may differ).
- The GF(2) monomial (algebraic normal form) basis is used for the MCZ gates.
- Input is either 'f' bits or 'signs' as a list of length 2^n.
- Global phase is handled via circuit global_phase.

## Unresolved issues

- The paper's exact binary representation, basis ordering, and construction are not known, so the decomposition may differ from the paper's gate ordering and counts.
- No cost optimization or CZ versus CNOT cost comparison is implemented.
- MCX with many controls is left to Qiskit's transpiler and is not decomposed explicitly into CZ.

## Equation mapping

- `eq_1`: implemented; build_circuit: validation of 'signs' entries (+1/-1) and conversion to f. Diagonal entries restricted to +-1 for a Hermitian unitary diagonal gate.
- `eq_2`: implemented; build_circuit: construction of list f from signs or f input. The binary representation is taken to be the f-vector, indexed by basis integer x.
- `eq_3`: implemented; build_circuit: emission loop using z, cz, and h+mcx+h. MCZ_S is a phase -1 iff all qubits in S are 1. For |S|>=3 it is realized as H on the last qubit, multi-controlled X, then H.
- `eq_4`: implemented; build_circuit: Moebius transform loop producing a[mask]=c_S, then the emission loop. The GF(2) coefficients c_S are computed and D is emitted as the product of MCZ_S gates with c_S=1.
- `eq_5`: implemented; build_circuit: Moebius transform loop (general n includes n=2). For n=2 the transform yields c_2=f(01), c_1=f(10), c_12=f(11)^f(01)^f(10), matching the triangular solution.

## Specification changes

- eq_4, eq_5: Generalized from the n=2 instance to arbitrary n in 1..12, with the coefficients computed by the in-place Moebius transform (the inverse of the triangular monomial basis matrix). Reason: The same GF(2) monomial-basis construction applies for any n and contains the n=2 case. The paper's own basis and algorithm remain unknown.
- eq_4, eq_5: If f(0)=1, the circuit sets global_phase=pi instead of requiring f(0)=0. Reason: The MCZ products cannot produce a -1 on |0...0>, so a global phase restores the exact operator, which stays unitary and measurement-free.
- eq_2, eq_5: Index order is made explicit: x is the Qiskit basis integer (qubit 0 = LSB). The spec's 'qubit 1 most significant' maps to Qiskit q[n-1]. Reason: Qiskit's little-endian convention; MCZ is symmetric so only the labeling is affected.
- eq_3: MCZ with three or more qubits is built from H, MCX, and H, which is exactly equivalent. CZ-library cost optimization is not attempted. Reason: This uses standard gates, and cost comparison is out of scope.
