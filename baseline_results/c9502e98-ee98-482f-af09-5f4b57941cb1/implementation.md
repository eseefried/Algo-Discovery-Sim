# Equation to Qiskit

Noiseless Bernstein–Vazirani-style parity-learning operation on n+1 qubits: the parity example oracle U_s (CNOTs from data qubits with s_i=1 into the label qubit, eq_1), optionally preceded by the data-register Hadamards that turn |0^n>|0> into the quantum example state |psi_s> (eq_2), and optionally followed by the learner's Hadamard layer H^(n+1) (eq_4) so that, on input |0^(n+1)>, the output is (|0^n>|0> + |s>|1>)/sqrt(2). The depolarizing noise channel, measurement, sampling and classical post-processing are non-unitary / experimental and are excluded from the generated operation.

Source equation run: `d06f258a-a260-42f8-a73c-c87e6aa66f7e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: data qubit d[0] (x_1 / s_1 = 1)
- qubit 1: data qubit d[1] (x_2 / s_2 = 0)
- qubit 2: data qubit d[2] (x_3 / s_3 = 1)
- qubit 3: label qubit l[0] (f_s(x) before learner Hadamards; branch bit b after)
- Encoding: computational basis, Qiskit little-endian (qubit 0 least significant). On input |0000> with stage 'full', the output is (|0000> + |1101>)/sqrt(2) in little-endian bitstring order q3 q2 q1 q0, i.e. label=1 with data = s = 101.

## Assumptions

- The quantum example oracle is the uniform-distribution Bshouty–Jackson oracle, implemented as H^{(x)n} on the data register followed by the parity CNOT oracle U_s.
- The learner's own gates are noiseless; any depolarizing noise (eq_3) is injected externally by the runner after the 'example' stage (e.g. by running stage 'example', applying noise, then the Hadamard layer) or via a noise model.
- Missing 'stage' key defaults to 'full' (example preparation followed by the learner's Hadamard layer).
- Instance size limited to n <= 11 so that n+1 <= 12 qubits.

## Unresolved issues

- The paper's exact noise model and algorithm are not available from the abstract; the implemented Bernstein–Vazirani learner is the reconstructor's inferred construction.
- Depolarizing noise cannot be represented inside a unitary circuit without ancilla-based dilation, which was not implemented; the noisy experiment must be assembled by the runner around this operation.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop 'eq_1: parity oracle U_s' (qc.cx(data[i], label[0]) for s_i = 1). The parity f_s(x) = XOR of x_i over s_i = 1 is computed into the label qubit by a chain of CNOTs, realizing U_s |x>|b> = |x>|b xor s.x>.
- `eq_2`: implemented; build_circuit: 'eq_2' Hadamard loop on data register (stages 'example' and 'full'). H^{(x)n} on D followed by U_s maps |0^n>|0> to the uniform superposition of labelled examples |psi_s>; the runner supplies the |0^(n+1)> input.
- `eq_3`: out_of_scope; no code location. The depolarizing channel is a non-unitary CPTP map and cannot appear in a measurement-free unitary QuantumCircuit; it is to be applied by the runner/noise model between the 'example' and learner stages if desired.
- `eq_4`: implemented; build_circuit: 'eq_4' Hadamard layer on all n+1 qubits (stage 'full'). The learner's H^{(x)(n+1)} is applied after the oracle, producing (|0^n>|0> + |s>|1>)/sqrt(2) from |psi_s>.
- `eq_5`: out_of_scope; no code location. Describes measurement statistics of the noisy state; measurements and noise are excluded from the generated operation.
- `eq_6`: out_of_scope; no code location. Classical per-bit correlation estimator; classical post-processing is not part of the circuit.
- `eq_7`: background; no code location. Asymptotic query-complexity bound motivating the construction; informs how many times the runner should repeat the circuit but has no circuit counterpart.

## Specification changes

- eq_3, eq_5, eq_6, eq_7: Scope narrowed to the noiseless unitary part of the learner: depolarizing noise, computational-basis measurement, repetition over m queries and the classical correlation estimate are removed from the generated module. Reason: The deliverable must be a measurement-free, unitary QuantumCircuit; noise channels, sampling and post-processing are non-unitary or experimental and are left to the runner.
- eq_2: The oracle output state |psi_s> is not taken as a given initial state; instead the circuit realizes the unitary (H^{(x)n} then U_s) that produces |psi_s> from the runner-supplied |0^(n+1)> input, with the oracle unitary U_s alone also available via stage 'oracle'. Reason: The construction must be an operation acting on runner-prepared inputs rather than a prepared state.
- eq_2, eq_4: Register ordering: the specification's data qubits 1..n and label qubit n+1 are mapped to Qiskit indices 0..n-1 and n respectively (little-endian), so the branch state reads |s>_D|1>_L with s_1 on qubit 0. Reason: Qiskit index 0 is the least significant bit; the mapping is disclosed to avoid misreading output bitstrings.
