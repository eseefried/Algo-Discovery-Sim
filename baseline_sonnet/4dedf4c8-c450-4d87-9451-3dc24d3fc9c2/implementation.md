# Equation to Qiskit

Builds a product of N controlled unitaries CU_k = sum_i |i><i|_A (x) V_{k,i}, with A an n_a-qubit control register (d_A = 2^n_a) and B a single target qubit (d_B = 2). Each V_{k,i} = exp(i*alpha) * U3(theta, phi, lam) comes from the instance. N is checked against the power-of-two bound 2*d_A - 1. The module does not compute the decomposition of a given U.

Source equation run: `d6a3005c-0a55-43ef-b589-d0365ce98611`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n_a-1: register A (control, little-endian: qubit j holds bit j of the basis index i, d_A = 2^n_a)
- Qubit n_a: register B (single target qubit, d_B = 2)
- Example: n_a=1, so qubit 0 = A and qubit 1 = B

## Assumptions

- Controlled unitaries are block diagonal in the computational basis of A.
- Gates are applied in list order, with the first entry acting first.
- The example instance has d_A = d_B = 2 and N = 3, which meets the bound 2d_A-1 = 3.

## Unresolved issues

- The explicit algorithm that decomposes an arbitrary U into at most 4d_A-5 or 2d_A-1 controlled unitaries is not available.
- The control direction and ordering of the factors in the original method are unknown.
- The complex permutation result, the local-unitary decomposition and the CNOT/entanglement cost bounds are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: inner loop over i (X-conjugated multi-controlled UGate plus phase on A==i). Each CU_k is built as sum_i |i><i|_A (x) V_{k,i}, with V_{k,i} = exp(i*alpha) U3(theta, phi, lam) on B.
- `eq_2`: implemented; build_circuit: outer loop over parsed gates. The circuit is the ordered product of the N supplied controlled unitaries. The factors are user-supplied, not derived from a target U.
- `eq_3`: background; no code location. d_A = 2^n_a is always a power of two, so the tighter eq_4 bound is the one enforced. 4d_A-5 >= 2d_A-1 for d_A >= 2.
- `eq_4`: implemented; build_circuit: check len(gates) <= 2*d_a - 1. The number of controlled unitaries is validated against 2 d_A - 1.
- `eq_5`: out_of_scope; no code location. The n-partite bound is not part of the bipartite construction implemented here.

## Specification changes

- eq_2, eq_3, eq_4: The module implements the decomposition form (a product of at most 2d_A-1 controlled unitaries) with caller-supplied V_{k,i}. It does not compute the V_{k,i} that reproduce a given target U. Reason: The abstract and specification do not give the explicit construction, so the factors cannot be derived.
- eq_1: d_B is restricted to 2 (one target qubit). Each V_{k,i} is parameterized as exp(i*alpha) U3(theta, phi, lam), and d_A is restricted to powers of two (n_a qubits). Reason: This avoids opaque dense unitaries and keeps the circuit built from standard gates within the 12-qubit cap.
- eq_2: Every factor is controlled from A onto B. Factors controlled from B are not supported. Reason: The control direction of each factor in the true method is unspecified, so the simplest consistent choice was made.
