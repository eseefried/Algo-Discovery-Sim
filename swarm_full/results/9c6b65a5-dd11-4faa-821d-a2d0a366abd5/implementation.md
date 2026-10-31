# Equation to Qiskit

Level-one (p=1) QAOA operation for Max E3LIN2 with one qubit per variable. It applies the phase-separation unitary exp(-i*gamma*C) for C = sum_k (1 + (-1)^{b_k} Z_a Z_b Z_c)/2, built from CX parity ladders and an RZ rotation, followed by the transverse-field mixer exp(-i*beta*sum X) as RX(2*beta) on every qubit. The runner prepares |+>^n and does the measurement. The abstract's four equations are performance statements, not circuit equations, so none are implemented as gates.

Source equation run: `efcc82c0-aff8-41a7-8ec0-5c782ddb4f5f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit i (0..n-1) = boolean variable x_i, least significant bit is qubit 0
- Register 'z' of size n; computational basis encoding |x_{n-1}...x_0>; no ancillas
- Expected input prepared by runner: |+>^n (standard QAOA start state)

## Assumptions

- Cost C = sum_k (1 + (-1)^{b_k} Z_a Z_b Z_c)/2 counts satisfied equations; the constant offset gives only a global phase and is dropped.
- Phase layer uses exp(-i*gamma*C), mixer uses exp(-i*beta*sum_j X_j), with RX(2*beta) per qubit.
- Equations are given as [a, b, c, s] with distinct variable indices; the optional D field is used only to validate the occurrence bound.
- The runner prepares |+>^n and performs measurement and classical evaluation.
- n is limited to 3..12 and equation count to 200.

## Unresolved issues

- Optimal gamma, beta and their D dependence are not given in the abstract.
- Meaning of 'typical case' is undefined.
- Sampling count and concentration argument are not specified.
- Sign and normalization conventions of the original paper's cost operator may differ from this reconstruction.

## Equation mapping

- `eq_1`: background; no code location. The random-string baseline of 1/2 is a classical reference value, not a gate-level operation.
- `eq_2`: out_of_scope; no code location. Worst-case guarantee 1/2 + 1/(101 D^{1/2} ln D) is an analytic performance bound. The abstract gives no gamma, beta, or analysis needed to realize it in the circuit; gamma and beta are free inputs.
- `eq_3`: out_of_scope; no code location. Typical-case fraction is an analytic result with an undefined 'typical case' and unspecified angles; it is not a circuit construction.
- `eq_4`: background; no code location. Classical comparison with an unspecified constant; context only.

## Specification changes

- eq_1, eq_2, eq_3, eq_4: Narrowed scope to a single generic p=1 QAOA layer (phase separation plus mixer) for explicit E3LIN2 instances. The performance-bound equations are not implemented; the circuit supplies no guarantee of achieving them. Reason: The abstract's equations are fractions of satisfied equations, not operations. The cost Hamiltonian, mixer and angle form are standard QAOA assumptions, not stated in the abstract.
- eq_2, eq_3: gamma and beta are caller-supplied parameters rather than the D-dependent values of the original analysis. Reason: The abstract does not give angle values or their dependence on D.
