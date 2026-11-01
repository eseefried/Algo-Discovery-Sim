# Equation to Qiskit

Circuit-model Simon's algorithm operation for n input qubits (2<=n<=6) and a nonzero hidden period s: H on the input register, a reversible oracle U_f built from CNOTs, then H on the input register. For n=2, s=11 the oracle reproduces the assumed f(00)=f(11)=00, f(01)=f(10)=01. There is no measurement, input preparation or classical postprocessing, and the one-way cluster-state implementation is not reconstructed.

Source equation run: `ffb230cc-f141-4254-882f-286789c5883c`

Generation: **generated**; validation: **failed**.

Isolated build failed: ValueError: Only unitary gate operations are supported in this block.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: input register x (qubit i = bit i of x, qubit 0 least significant); Hadamard-transformed before and after the oracle
- qubits n..2n-1: output register y (qubit n+k = bit k of y); only the first n-1 output qubits receive f(x), the last stays idle
- example n=2: q0,q1 = x; q2,q3 = y

## Assumptions

- Circuit-model Simon algorithm is a proxy for the one-way implementation.
- s is given as a bitstring whose first character is the most significant bit.
- The initial Hadamard layer is part of the algorithm operation; the runner supplies |0...0>.
- The linear oracle is one representative 2-to-1 function, not necessarily those tested in the experiment.

## Unresolved issues

- Cluster-state graph, measurement angles and the set of functions tested in the experiment are not recoverable from the abstract.
- The oracle is restricted to linear 2-to-1 functions.

## Equation mapping

- `eq_1`: background; no code location. Promise on the black box. The oracle in build_circuit is constructed to satisfy it, but the promise itself is not a circuit operation.
- `eq_2`: implemented; build_circuit: oracle section (CX gates between the x and y registers). Reversible oracle |x>|y> -> |x>|y xor f(x)> implemented with CNOTs, with f linear over GF(2).
- `eq_3`: background; no code location. Output distribution is a property of the circuit's result, to be checked by the runner. It is not coded directly.
- `eq_4`: implemented; build_circuit with instance {"n":2,"s":"11"}: oracle section. For n=2, s=11 the oracle gives j=0 and y bit 0 = x1 XOR x0, so f(00)=f(11)=00 and f(01)=f(10)=01, matching the assumed instance.
- `eq_5`: background; no code location. Expected outcomes z in {00,11} with probability 1/2 each are a consequence for the instance. They are not hardcoded.

## Specification changes

- eq_1, eq_2, eq_4: Generalized from the single fixed n=2, s=11 instance to a parametrized (n, s) family with 2<=n<=6, using an explicit linear oracle f(x)_k = x_i XOR s_i*x_j. Reason: The operation should vary over valid instance parameters. For n=2, s=11 the oracle reduces exactly to the assumed eq_4 function.
- eq_2: The output register has n qubits but only n-1 carry f(x); the remaining qubit is idle. Reason: A 2-to-1 linear function needs only n-1 output bits. The register size is kept at n to match the specification.
- eq_3, eq_5: Measurement, repetition and classical postprocessing are excluded from the circuit. Reason: The task requires a measurement-free unitary operation.
- eq_1, eq_2, eq_3, eq_4, eq_5: The five-qubit cluster-state one-way implementation, measurement bases and the n-qubit resource analysis are out of scope. Only the circuit-model proxy is built. Reason: The abstract gives no cluster graph, angles or resource formulas.
