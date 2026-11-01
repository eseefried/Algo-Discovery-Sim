# Equation to Qiskit

Builds a baseline amplitude-estimation circuit for the mean of f:{0..2^n-1}->[0,1]. It uses a uniform superposition on x and controlled-RY oracle rotations on a flag qubit to form A. Controlled powers of Q=-A S_0 A^dagger S_chi act on an m-qubit phase register, followed by an inverse QFT. This is only the generic textbook baseline, not the paper's novel optimal or Aharonov-variant algorithms or the median algorithm.

Source equation run: `46119d5d-77da-4fbe-ac0f-3fd293ca839d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1: phase register (little-endian; qubit j controls Q^(2^j)); after inverse QFT, integer y read little-endian gives estimate sin^2(pi*y/2^m)
- qubits m..m+n-1: x index register (qubit m is least significant bit of x)
- qubit m+n: flag qubit holding sqrt(f(x)) amplitude on |1>
- example: n=2, m=3 -> phase=[0,1,2], x=[3,4], flag=[5]

## Assumptions

- f values lie in [0,1] and the domain is uniform over 2^n points.
- Total qubits n+m+1 are at most 12.
- The runner prepares the input state (all zeros) and handles measurement and postprocessing.

## Unresolved issues

- The paper's actual algorithms (novel optimal mean estimation, Aharonov variant, median) are not reconstructed.
- The paper's oracle and error models are unknown.
- The circuit uses repeated controlled Q applications, so depth grows as 2^m.

## Equation mapping

- `eq_1`: background; no code location. Classical definition of the target mean; the circuit encodes it as the flag-1 probability, and no classical sum is computed in the module.
- `eq_2`: implemented; _prep_A. Hadamards on x then multi-controlled RY(2 arcsin sqrt(f(x))) on the flag for each x give A|0>.
- `eq_3`: background; no code location. Follows from eq_2 by direct computation, so it is not a separate circuit element; the angles in _prep_A rely on it.
- `eq_4`: implemented; _grover_gate and build_circuit. Q = -A S_0 A^dagger S_chi is built from Z on the flag, A^dagger, a sign flip of |0..0>, and A, with the -1 supplied as a Z on the control qubit; controlled powers act on the phase register and an inverse QFTGate follows.
- `eq_5`: out_of_scope; no code location. Error bound on the classical estimate after measurement; no measurement or postprocessing is in the operation.

## Specification changes

- eq_2: The oracle is realized as explicit multi-controlled RY rotations from a user-supplied table f_values, with f restricted to [0,1] and N=2^n with n>=1. Reason: A concrete bound circuit is needed instead of an abstract black box.
- eq_4: The global -1 of Q is implemented as a Z gate on the phase qubit 0, since controlled Q^(2^j) carries the -1 only for j=0, and Q' = A S_0 A^dagger S_chi is controlled without it. Reason: The sign becomes a relative phase under control and must be included to get eigenphases e^{±2i theta}.
- eq_4, eq_5: The inverse QFT is QFTGate(m).inverse() on the phase qubits in little-endian order, with qubit j controlling Q^(2^j). Reason: This matches the specified Qiskit qubit ordering and its bit-reversal convention.
- eq_1, eq_3, eq_5: Scope is narrowed to the generic amplitude-estimation baseline circuit, with no measurement, sampling or classical postprocessing; the paper's novel optimal algorithm, the Aharonov variant and the median algorithm are not implemented. Reason: The abstract gives no details of those algorithms, and the task requires an operation without measurement.
