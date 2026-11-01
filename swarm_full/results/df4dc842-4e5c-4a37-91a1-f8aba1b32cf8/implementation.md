# Equation to Qiskit

build_circuit(instance) implements a diagonal Hermitian gate D=diag((-1)^f(x)) on n<=12 qubits as a product of multiple-controlled Z gates. It takes the GF(2) algebraic normal form of the truth table f using a Moebius transform, then applies Z, CZ or a multi-controlled Z (H-MCX-H) for every subset S with c_S=1. A set empty-subset coefficient becomes a global phase of pi.

Source equation run: `b91b29a2-fe93-47d5-bdfe-48cd354d1e53`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubit i (0..n-1) is data qubit q[i]; qubit 0 is the least significant bit of the basis index x.
- Truth table f[x] with x = sum_i x_i 2^i gives D|x> = (-1)^f(x)|x>.
- No ancilla qubits; total qubits = n <= 12.

## Assumptions

- Qubit i corresponds to bit i of x in the truth-table index (little-endian, Qiskit convention).
- The binary representation is the truth table f over GF(2), and the MCZ basis is the monomial basis indexed by nonempty subsets.
- The instance supplies f directly as a list of 0/1 values.
- MCZ gates commute, so their order is arbitrary.

## Unresolved issues

- The paper's actual binary representation and basis-change algorithm are not available from the abstract.
- No cost metric (CZ count, depth) is optimized or reproduced.
- Larger MCZ gates are not decomposed into CZ plus single-qubit gates.

## Equation mapping

- `eq_1`: implemented; build_circuit: validation of n and truth-table f (entries 0/1 meaning diagonal +1/-1). The instance supplies the binary vector f that defines D=diag((-1)^f(x)). Its length and bit values are validated, and the circuit realizes this diagonal.
- `eq_2`: implemented; build_circuit: Moebius transform loop and the subset loop applying Z/CZ/H-MCX-H. The coefficients c_S are computed by the GF(2) ANF transform. A Z_S gate is applied for each nonempty S with c_S=1, and the empty-set term becomes a global phase.

## Specification changes

- eq_2: The empty-subset term c_empty=f(0) is implemented as a global phase of pi instead of a gate. Reason: The specification left this term unspecified. The identity-subset 'MCZ' is a scalar -1, and it is needed for the circuit to equal D exactly rather than up to phase.
- eq_1, eq_2: The scope is narrowed to the truth-table binary representation over GF(2) and the ANF/Moebius basis change. The paper's own binary encoding, cost optimization and ordering are not reproduced. Reason: The abstract does not give the paper's exact encoding or algorithm.
- eq_2: Multi-controlled Z on three or more qubits is built as H, MCX, H on the highest-index qubit of S, without further decomposition into CZ. Reason: The abstract gives no explicit CZ-level decomposition of larger MCZ gates, and they are valid unitary gates.
