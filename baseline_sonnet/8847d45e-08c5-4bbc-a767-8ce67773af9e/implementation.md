# Equation to Qiskit

Builds a measurement-free circuit for the noiseless quantum parity-learning round on n input qubits plus one label qubit: Hadamards on the input register, then the oracle CNOTs that write f_s(x)=s.x mod 2 into the label qubit (this gives |psi_s> from |0...0>), then Hadamards on all n+1 qubits (Fourier sampling). Depolarizing noise, measurement/post-selection, and LPN are not implemented.

Source equation run: `c467c185-16a6-4a65-b3c7-06e3167dff42`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: x_0 (least significant input bit; pairs with s_0 = last character of s)
- qubit 1: x_1
- qubit 2: x_2 (most significant input bit; pairs with first character of s)
- qubit 3: B, label qubit holding f_s(x) (for n=3)
- general n: qubits 0..n-1 are X, qubit n is B

## Assumptions

- The hidden string s is given as a bitstring with the most significant bit first, so s[n-1-i] multiplies x_i on qubit i.
- Parity has no affine offset.
- The input distribution is uniform.
- The runner supplies the all-zero input state.

## Unresolved issues

- The paper's noisy quantum learning algorithm and its depolarization handling are not specified in the abstract, so they are not implemented.
- The depolarizing noise model is not realized in the unitary circuit.
- Postprocessing (post-selecting on B=1 and reading s from X) is left to the runner.

## Equation mapping

- `eq_1`: implemented; build_circuit: CX loop from x_i to b for each s_i = 1. The parity s.x mod 2 is computed as an XOR of the selected x_i into the label qubit via CNOTs.
- `eq_2`: implemented; build_circuit: first H loop on x plus the oracle CX loop. Hadamards on X followed by the oracle CNOTs map |0>^n|0> to (1/sqrt(2^n)) sum_x |x>|f_s(x)>. This builds the example state from |0> inside the operation.
- `eq_3`: implemented; build_circuit: final H on x and on b. The final Hadamards on all n+1 qubits implement the Fourier-sampling transform. Measurement and post-selection on B=1 are left to the runner and not included.
- `eq_4`: out_of_scope; no code location. Depolarizing is a non-unitary channel, and the circuit must be unitary and measurement-free, so it is not included.
- `eq_5`: out_of_scope; no code location. Classical LPN example generation is a classical sampling model and not a quantum circuit operation.

## Specification changes

- eq_2, eq_3: The operation includes the example-state construction (H on X plus oracle CNOTs) from |0...0>, followed by the Fourier-sampling Hadamards, as one unitary. The runner supplies |0>^{n+1}. Reason: The oracle is implemented as a unitary query U_s, and a quantum example state requires a superposition over x. Doing it inside the operation keeps the circuit self-contained.
- eq_3: No measurement or post-selection on the label qubit is included. Fourier sampling with B=1 conditioning is left to the runner or analysis. Reason: The circuit must be measurement-free.
- eq_4: Depolarizing noise is omitted, so the scope is narrowed to the noiseless baseline. Reason: The channel is non-unitary and the eta parametrization was only an assumption.
- eq_5: The LPN classical model is not implemented. Reason: It is a classical sampling problem outside a quantum circuit operation.
