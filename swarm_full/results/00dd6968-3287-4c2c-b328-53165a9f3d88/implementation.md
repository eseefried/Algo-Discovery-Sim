# Equation to Qiskit

Scoped construction: a 2m-qubit generalized Bell-like basis generator. Hadamards on m control qubits, then a multi-qubit controlled-X layer (variant 'copy' or 'cascade') onto m target qubits. On the label basis state |i>_c|j>_t it produces 2^(-m/2) sum_k (-1)^(i.k) |k>_c |A k xor j>_t, where A is an invertible GF(2) matrix. This gives 2^m terms with amplitudes +-1/sqrt(2^m). The 4^m outputs are orthonormal because the circuit is unitary. This is one concrete instance of the abstract's idea, not the paper's two gates.

Source equation run: `a468317f-b692-4501-b6ea-b290199cbe79`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..m-1: control register c (qubit 0 is the least significant bit of k and of the control label i)
- qubit m..2m-1: target register t (qubit m is the least significant bit of the target label j)
- Example m=2: q0,q1 = controls; q2,q3 = targets
- Input |i>_c|j>_t is computational basis, prepared by the runner; output is 2^(-m/2) sum_k (-1)^(i.k)|k>_c|A k xor j>_t

## Assumptions

- The generalized Bell basis (Hadamards plus CNOT layer) is a valid special case of Bell-like bases with 2^m terms.
- Target-register size equals m.
- The 'cascade' variant uses an upper-triangular invertible GF(2) matrix A, so the output states stay orthonormal.
- The runner prepares label states |i>_c|j>_t in the computational basis.

## Unresolved issues

- The paper's two multi-qubit controlled-unitary gates are not defined in the abstract and are not reproduced.
- Entanglement and monogamy-score comparisons between bases are out of scope.
- The 'copy' and 'cascade' variants are related by local-style linear maps on the target and may not reproduce the entanglement differences the paper reports.

## Equation mapping

- `eq_1`: implemented; build_circuit: Hadamard loop on control qubits followed by controlled-X layer (copy or cascade). For basis-state inputs the circuit outputs a superposition of 2^m distinct computational basis states x_k = (k, A k xor j). Each has amplitude s_k/sqrt(2^m) with s_k = (-1)^(i.k).
- `eq_2`: background; no code location. Orthonormality follows from unitarity of the circuit acting on orthonormal basis-state inputs. No code is needed. The circuit does not construct or check the inner products.

## Specification changes

- eq_1, eq_2: Narrowed to a concrete 2m-qubit construction (m controls, m targets) with two controlled-X variants, 'copy' and 'cascade'. These stand in for the paper's two unspecified multi-qubit controlled-unitary gates. Reason: The abstract does not define the paper's gates or circuits. A well-defined, validated construction needs a concrete choice, and this one gives exactly 2^m terms with +-1/sqrt(2^m) amplitudes.
- eq_1: The specification's step order (label X gates, then H, then controlled-unitary) is reduced to H then controlled-X. Label preparation is left to the runner. The label dependence of the signs is the standard (-1)^(i.k) from Hadamards acting on the control label bits. Reason: The task requires an operation with no input-state preparation. The abstract does not fix the sign pattern.
- eq_2: The specification's inverse-circuit measurement and the entanglement and monogamy-score analysis are not implemented. Reason: The task forbids measurements and analysis code in the module, and the abstract does not define these measures.
