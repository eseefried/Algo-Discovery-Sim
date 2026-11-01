# Equation to Qiskit

One noiseless run of the parity-learning circuit as a unitary operation. The coherent example oracle for hidden parity s is built from H on the data qubits plus a CX from each data qubit i with s_i=1 onto the label qubit. This is followed by the Fourier-sampling Hadamard layer on all qubits. On |0^n>|0> the circuit ends in |s>|1>. Noise, measurement, repetition and majority voting are not in the circuit.

Source equation run: `a0eac547-8820-4b6f-9f4d-5ea1cb9fa193`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: data register, qubit i carries s_i (qubit 0 is least significant)
- qubit n: label qubit carrying f_s(x) = s.x mod 2; ends in |1> after the final H
- example n=4: qubits 0-3 data, qubit 4 label

## Assumptions

- Qubit i of the data register corresponds to s_i, with s given as a list or string indexed by i (s[0] is s_i for i=0).
- The runner supplies |0^n>|0> as input.
- Total qubits n+1 is at most 12, so n is at most 11.
- No constant offset in the parity function.

## Unresolved issues

- Noise model and the effective flip rate p'=2p/3 are not implemented, and the runner must add depolarizing noise if desired.
- Majority-vote post-processing and the choice of m are left to classical processing outside the circuit.

## Equation mapping

- `eq_1`: implemented; build_circuit: H layer on data followed by CX(i -> label) for s_i=1 (comment 'eq_1'). Builds the coherent quantum example oracle |psi_s> from |0^n>|0> using standard gates with no offset.
- `eq_2`: implemented; build_circuit: H on label then H on all data qubits (comment 'eq_2'). Applies the Fourier-sampling Hadamard layer H^{n} x H, taking |psi_s> to |s>|1>.
- `eq_3`: out_of_scope; no code location. Depolarizing noise and the effective bit-flip model are non-unitary and are not part of the measurement-free unitary circuit. The runner may add noise.
- `eq_4`: out_of_scope; no code location. Majority voting is classical post-processing over measured strings, so it is not part of the circuit.
- `eq_5`: out_of_scope; no code location. The repetition-count bound is a statistical statement about the number of runs and is not encoded in a single circuit.

## Specification changes

- eq_3, eq_4, eq_5: Scope narrowed to a single noiseless, measurement-free run. Noise, measurement, repetition and majority voting are excluded. Reason: The required output is a bound, unitary, measurement-free circuit, and noise sampling and classical post-processing cannot be expressed in it.
- eq_1, eq_2: The oracle is implemented explicitly as H on data plus CX gates controlled on the bits of s, and it is included in the returned circuit together with the Fourier-sampling layer. Reason: The spec treats the oracle as a black box, but a concrete hidden s is needed to build a circuit. The input is |0^n>|0>, so the oracle's own state preparation is part of the operation. The H on the data qubits before and after the CX layer do not cancel, because the CX layer sits between them.
