# Equation to Qiskit

Canonical amplitude-estimation unitary for the mean of a tabulated function f:{0..2^n-1}->[0,1]. It applies Hadamards to the index register and a multiplexed RY on the ancilla, so P(a=1)=mean(f). Counting qubit k then controls Q^(2^k), where Q is the Grover iterate, followed by an inverse QFT on the counting register. This is a generic placeholder, not the paper's algorithms. There is no input preparation or measurement, and the runner must supply |0...0>.

Source equation run: `f6ef9ddf-8e9a-4857-a0e7-96fcd22fcef1`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..m-1: counting register (qubit k controls Q^(2^k); qubit 0 is least significant bit of the phase integer y)
- qubits m..m+n-1: index register x (n=log2 N, qubit m is the least significant bit of x)
- qubit m+n: ancilla a whose |1> amplitude squared on branch x is f(x)
- example: m=4, n=2 -> counting 0-3, x 4-5, ancilla 6 (7 qubits)

## Assumptions

- f maps {0..N-1} to [0,1] with N=2^n, and the distribution is uniform
- The runner prepares |0...0> on all qubits. The state-preparation unitary A is part of the operation, since amplitude estimation includes it.
- Q = A(2|0><0|-I)A^dag S_chi with S_chi = Z on the ancilla, which has eigenphases e^{+-2i*theta_a} with sin^2(theta_a)=mu. Implemented as -A S0 A^dag S_chi, with the -1 applied as p(pi) on the control after each controlled-Q.
- The standard QPE bit order is used: counting qubit k controls Q^(2^k), and the inverse QFT is QFTGate(m).inverse() on qubits 0..m-1.

## Unresolved issues

- The paper's actual algorithms (novel optimal mean estimator, Aharonov variant, median algorithm) are not reconstructed.
- The oracle for f is modeled as a classical lookup table rather than a true black-box query.
- Non-power-of-two domain sizes are unsupported.

## Equation mapping

- `eq_1`: implemented; _state_prep (Hadamards plus multiplexed RY with theta_x=2*asin(sqrt(f(x))) so P(a=1)=mean f); used by _iterate and build_circuit. The mean mu=(1/N) sum f(x) is encoded as the probability of a=1 after A. Amplitude estimation then writes a phase encoding mu into the counting register.
- `eq_2`: background; no code location. The additive accuracy goal is not a circuit operation. It only informs the choice of counting_qubits (error about pi/2^m), and the circuit does not check it.

## Specification changes

- eq_1: The black-box oracle for f is replaced by an explicit table f_values of length N=2^n, compiled into a multiplexed RY rotation. The spec's ceil(log2 N) is restricted to N an exact power of two. Reason: No oracle model is specified, and a generic black box cannot be built without a defined interface. Padding non-power-of-two domains would change the mean.
- eq_1, eq_2: Scope is narrowed to the generic canonical amplitude-estimation unitary (state prep, controlled Grover powers, inverse QFT), with counting_qubits as the free accuracy parameter. It is not the paper's optimal algorithm, the Aharonov variant, or the median algorithm. Reason: The abstract gives no details of the paper's algorithms. The spec itself labels this generic sketch a placeholder.
- eq_2: Measurement, the sin^2(pi*y/M) postprocessing and median amplification are omitted. Reason: The task requires a measurement-free unitary operation, and the runner handles measurement.
- eq_1: Counting register size is capped at 6 qubits and total qubits at 12. Reason: Controlled Q^(2^k) is implemented by repetition, so gate count grows as 2^m. The caps keep the circuit compact and within the qubit limit.
