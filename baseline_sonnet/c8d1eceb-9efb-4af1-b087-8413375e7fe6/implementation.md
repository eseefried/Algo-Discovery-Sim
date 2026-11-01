# Equation to Qiskit

Implements the ancilla-controlled first-order Trotterized evolution C-U(t) = |0><0| (x) I + |1><1| (x) exp(-iHt) for the 2-level reduced pairing Hamiltonian mapped to 2 qubits. This is the core operation of the Hadamard-test spectroscopy in the spec. Input-state preparation, the final basis rotation, measurement and Fourier post-processing are not included.

Source equation run: `e2e8d93f-b31a-49c3-b2d6-46c90da8f937`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: system qubit q[0], pair occupation of level 0 (|0> empty, |1> occupied; LSB)
- qubit 1: system qubit q[1], pair occupation of level 1
- qubit 2: control ancilla a[0] (Hadamard-test ancilla; the runner prepares |+> and the reference state e.g. |01> meaning level 1 occupied, i.e. q1=1, q0=0)

## Assumptions

- Uniform pairing coupling G and two levels with energies epsilon_0 and epsilon_1
- The ancilla is the control qubit, with ancilla |1> selecting evolution
- Trotter ordering within each step: constant phase, CRZ on q0, CRZ on q1, then XX+YY exchange
- Valid inputs: finite real epsilon (length 2), G and time; integer trotter_steps in 1..100

## Unresolved issues

- The paper's actual Hamiltonians, hardware-native gate sequences, fidelity metrics and spectrum measurement scheme are not specified in the abstract
- The reference state |01> and the ancilla |+> must be prepared by the runner

## Equation mapping

- `eq_1`: implemented; build_circuit: coefficients a_j = eps_j - G/2 and exchange coupling G/2. The two-level reduced pairing Hamiltonian, including j=k terms, fixes the gate angles.
- `eq_2`: implemented; build_circuit: register layout, n_j=(1-Z_j)/2 with |1> occupied. One qubit per pair level; sigma+ sigma- exchange is realized as (XX+YY)/2.
- `eq_3`: implemented; build_circuit: const, a[], crz and RXX/RYY block. Implemented in simplified form H = sum_j (eps_j - G/2)(1-Z_j) - (G/2)(XX+YY). The zero-valued placeholder term is dropped.
- `eq_4`: implemented; build_circuit: for _ in range(n) loop. First-order Trotter product with n steps of dt=t/n. Each step applies the constant phase, the Z rotations and the XX+YY block, all controlled on the ancilla.
- `eq_5`: background; no code location. S(t) is obtained by a Hadamard test whose controlled evolution is provided here. The ancilla Hadamard or phase rotation, measurement and Fourier transform are outside the circuit operation.

## Specification changes

- eq_3: Removed the zero-valued placeholder term and merged the number terms: eps_j(1-Z_j) - G(1-Z_j)/2 = (eps_j - G/2)(1-Z_j). Reason: The placeholder carries no content. Merging gives the same operator with fewer terms.
- eq_4, eq_5: The Trotterized evolution is controlled on an ancilla, with the constant energy offset implemented as a phase gate on the ancilla. Reason: The Hadamard test needs a controlled-U, and the constant term of H is then a relative phase that affects S(t).
- eq_5: Scope narrowed to the controlled-evolution operation only. Initial-state preparation, ancilla basis changes, measurement and Fourier analysis are excluded. Reason: The circuit must be a measurement-free operation with inputs prepared by the runner.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope is a generic 2-level reduced pairing model, not the paper's specific Hamiltonians or nearest-neighbor decompositions. Reason: The abstract gives no explicit equations.
