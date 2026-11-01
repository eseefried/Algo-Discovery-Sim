# Equation to Qiskit

Measurement-free derivative-based Bernstein-Vazirani circuit that exactly encodes all coefficients of a multilinear F_2 polynomial (n<=3, d<=2) into a computational basis state. Each block i uses an ancilla and a register for the other variables, and applies two restricted phase-oracle calls (x_i=1, then x_i=0) between Hadamard layers. A constant block reads c_0. To meet the 12-qubit cap, the z register and the unused x_i qubit in each block were removed, giving n^2+1 qubits (10 for n=3). Not query-optimal.

Source equation run: `a605b6e7-34fd-45a1-94d8-e04d1c39dc05`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Single register q of n^2+1 qubits (n=3: 10 qubits); qubit 0 is least significant
- Block i (1..n) starts at base=(i-1)*n: qubit base = ancilla a_i, output c_i
- Block i qubits base+1.. hold the variables j != i in ascending order; output bit is c_ij
- n=3: q0=a1, q1=x1[x_2] (c_12), q2=x1[x_3] (c_13)
- n=3: q3=a2, q4=x2[x_1] (c_12), q5=x2[x_3] (c_23)
- n=3: q6=a3, q7=x3[x_1] (c_13), q8=x3[x_2] (c_23)
- q9 (index n^2)=a0, output c_0
- Encoding: output is a computational basis state with c_i, c_ij as bits; c_ij appears redundantly in blocks i and j
- Input state: all |0>; the circuit prepares the Hadamard inputs itself, as in the spec

## Assumptions

- q=2, multilinear polynomial of degree at most d<=2, coefficients classical in {0,1}
- Coefficient keys are digit strings of strictly increasing variable indices, with '0' for the constant
- Variable j of the polynomial is x_j for j=1..n
- Missing coefficient keys are treated as 0
- The Hadamard input preparation is part of the operation, as in the spec

## Unresolved issues

- The paper's optimal exact quantum algorithm is not implemented
- No general q or d
- The oracle is compiled from explicit coefficients, so it is not a black-box query model and queries are not certified

## Equation mapping

- `eq_1`: implemented; _parse (coefficient dict over monomials S, validation) and monomial loop in _restricted_oracle. Coefficients c_S of the multilinear polynomial are parsed as classical build parameters. Each monomial with c_S=1 is compiled into a phase gate.
- `eq_2`: implemented; _restricted_oracle and _phase. Controlled phase oracle compiled as Z/CZ/CCZ on the control and monomial variables, with x_i fixed to a constant in the derivative blocks.
- `eq_3`: implemented; build_circuit derivative loop (two _restricted_oracle calls with val=1 then val=0). The derivative f(x+e_i)+f(x) is realized as the product of the oracle with x_i=1 and the oracle with x_i=0. Terms without x_i cancel, leaving c_i + sum_j c_ij x_j.
- `eq_4`: implemented; build_circuit: H layers around the derivative loop. Controlled-derivative BV block per direction i. H, then the phase (-1)^{b D_i f(x)}, then H gives |c_i>|l^(i)>. The x_i qubit is omitted because D_i f does not depend on x_i.
- `eq_5`: implemented; build_circuit: 'if mons.get((),0): qc.z(a0)' between H on a0. With the z register fixed to |0..0>, the controlled oracle reduces to Z on a0 when c_0=1, and H Z H reads c_0. The z register is elided to save qubits.

## Specification changes

- eq_4, eq_5: Removed the z register (3 qubits). The controlled oracle on |000> is replaced by Z on a0 when c_0=1. Reason: The spec's 16 qubits exceed the 12-qubit cap. A controlled oracle acting on a fixed |0...0> register is exactly a phase on the control, so this is the same operation.
- eq_3, eq_4: Each x_i register has n-1 qubits (variables j != i only), not n. The derivative is compiled as two restricted oracle calls with x_i fixed to 1 and 0, instead of oracle, X_i, oracle, X_i on a full register. Reason: D_i f does not depend on x_i, so the x_i qubit is unnecessary. This reduces the qubit count to n^2+1 (10 for n=3), within the cap.
- eq_1, eq_2: The builder accepts n in {1,2,3} and d in {1,2} with q=2. Coefficients come from the instance dict (keys '0','1','12',...). Nonzero coefficients above degree d are rejected. The spec fixed n=3, d=2. Reason: Parametrization requirement; the 12-qubit cap limits n to at most 3.
- eq_4, eq_5: Register layout and output decoding change: c_ij is read from the x_i block position of variable j instead of the spec's 1-indexed x_i[j] with an unused diagonal qubit. Reason: Consequence of removing the unused x_i qubit.
- eq_2, eq_3, eq_4: No query-complexity claim. The scheme uses naive derivative blocks, not the paper's O(n^(d-1)) exact algorithm. Reason: The paper's construction is not given in the abstract; this follows the spec's declared narrow scope.
