# Equation to Qiskit

Exact compute-phase-uncompute implementation of a diagonal n-qubit unitary with k distinct phases. A multi-controlled-X oracle writes j(x) into an index register. The index diagonal is applied as parity Rz rotations from a Walsh-Hadamard decomposition. The oracle is then undone. No Clifford+T synthesis is performed; Rz stays exact.

Source equation run: `b6fe77a5-5c4c-408f-8c1e-0d679cbab80a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: data register (little-endian, data qubit i is bit i of x)
- Qubits n..n+m-1: index register, m = max(1, ceil(log2 k)), little-endian bits of j(x); starts and ends in |0>
- Example: n=3, k=3, m=2 gives data = qubits 0,1,2 and index = qubits 3,4 (5 qubits total)
- No extra work ancillas: multi-controlled X gates use Qiskit's ancilla-free decomposition

## Assumptions

- Level sets and phase values are known at compile time and passed in the instance
- Index and ancilla qubits start in |0>; the circuit returns them to |0>
- Data qubit i corresponds to bit i of x (little-endian)
- Phases on unused index values are 0
- Total qubits n+m <= 12, with n <= 10

## Unresolved issues

- The paper's actual oracle synthesis and E(n,k) formula are unknown
- Optimal handling of free phases on unused indices when k is not a power of 2 is not implemented
- Clifford+T approximation and T-count accounting are not included
- The decision boundary in (n,k,epsilon) space is not reproduced

## Equation mapping

- `eq_1`: implemented; build_circuit: parsing of 'phases' (phi_j) and 'index_map' (j(x)). The target diagonal is defined by the instance's level-set index map and the k distinct phase values.
- `eq_2`: implemented; _oracle and its two calls in build_circuit. The oracle |x>|y> -> |x>|y xor j(x)> is built from X-conjugated multi-controlled X gates. It is applied, then the parity-phase layer, then the oracle again, which is its own inverse.
- `eq_3`: implemented; _walsh and the parity-rotation loop in build_circuit. Walsh coefficients c_s of the padded phase vector give alpha_s = -2 c_s and global phase gamma = c_0. Each parity Z^s is applied as CX fan-in, Rz(alpha_s), CX fan-out.
- `eq_4`: background; no code location. The T-count bound is a resource statement. No Clifford+T synthesis is done, so the bound is not enforced or computed.
- `eq_5`: out_of_scope; no code location. Per-rotation precision epsilon/k applies only to approximate Clifford+T synthesis. This module keeps exact Rz rotations.

## Specification changes

- eq_3: Phases on unused index values j>=k are fixed to 0. The circuit uses up to 2^m-1 parity rotations, not k-1. Reason: The k-1 reduction needs optimized free phases on unused indices, which the specification did not resolve. A fixed choice keeps the construction deterministic.
- eq_4, eq_5: No Clifford+T approximation or T-count optimization is performed. Rz gates stay exact. Reason: Scope narrowing: the specification allows exact Rz for simulation, and no gridsynth-style synthesis is available.
- eq_1, eq_2: The oracle is a naive one-multi-controlled-X-per-(x, bit) construction. The instance supplies explicit phases and index_map, with the example fixed at n=3, k=3. Reason: The paper's oracle synthesis and E(n,k) are not available, and the tiny instance size was chosen in the specification, not taken from the abstract.
- eq_3: The global phase gamma is applied as the circuit's global_phase instead of being ignored. Reason: This makes the circuit equal D exactly on the ancilla-|0> subspace, including the global phase.
- eq_3: The index register uses m = max(1, ceil(log2 k)) qubits, so k=1 still has one index qubit. Reason: This avoids a zero-size register.
