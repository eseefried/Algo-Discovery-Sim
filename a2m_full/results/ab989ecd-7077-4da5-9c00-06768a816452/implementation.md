# Equation to Qiskit

Digitized first-order Trotter adiabatic evolution on n data qubits from H_B=-sum X_i towards a diagonal EC3 problem Hamiltonian. Each clause on a triple (a,b,c) contributes the cost (x_a+x_b+x_c-1)^2 and is built from RZ and RZZ rotations. Each slice applies the H_P factor first and then RX(-2(1-s_k)dt) on every qubit. Slices are applied in order k=1..M. The circuit is an operation only: the runner must prepare |+>^n, and there is no measurement or ancilla.

Source equation run: `23431dfd-4e8d-4404-9708-f4161d41fbd2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: data variables x_0..x_{n-1}; qubit i is bit i (least significant first) of the computational-basis index
- no ancilla qubit; total qubits = n <= 12
- expected runner input: |+>^n (ground state of H_B), prepared outside this module; no measurements

## Assumptions

- First-order Trotter with a uniform dt=T/M and the H_P factor applied before the H_B factor in each slice
- The global phase from the constant clause terms is tracked in qc.global_phase
- The example clause set is believed to have the unique solution x=(0,0,1,0), by hand analysis only and not verified
- M<=200 and the clause count <=50 are arbitrary caps
- The runner prepares |+>^n

## Unresolved issues

- The paper's fast-signal sequences and randomized Trotter formula are not reconstructed
- A gap-based local-adiabatic schedule must be supplied externally through explicit s_values
- The abstract does not specify the concrete EC3 instance or schedule used in the paper
- Adiabatic fidelity depends on T and M, and no convergence is claimed

## Equation mapping

- `eq_1`: implemented; build_circuit: the per-slice RX(-2(1-s_k)dt) layer realizes the H_B weight, and the s_k*dt scaling of the H_P rotations realizes the s weight. The interpolation is realized through the Trotter slices. exp(-i(1-s)dt(-sum X)) = prod RX(-2(1-s)dt).
- `eq_2`: implemented; build_circuit: the loop over clauses accumulating h, J, const, followed by the rz/rzz calls. Uses the squared-sum clause cost (x_a+x_b+x_c-1)^2 = 1 - (Za+Zb+Zc)/2 + (ZaZb+ZaZc+ZbZc)/2. It is diagonal, with exp(-i th h Z)=RZ(2 th h), exp(-i th J ZZ)=RZZ(2 th J), and the constant tracked as global phase.
- `eq_3`: implemented; build_circuit: the main loop over sched. Each slice applies the H_P factor and then the H_B factor, matching U_k=e^{-i(1-s_k)H_B dt}e^{-i s_k H_P dt}. Slices run k=1..M in order (operator product U_M...U_1), with dt=T/M.
- `eq_4`: out_of_scope; no code location. The gap-based local schedule needs classical diagonalization, which is not done in the module. The schedule is instead 'linear' (midpoint s_k=(k+0.5)/M) or user-supplied s_values, which can carry a precomputed local-adiabatic schedule.
- `eq_5`: out_of_scope; no code location. The ancilla phase-kick filter is a sketch that reduces to the identity as written, and it is not the paper's fast-signal method. It is omitted, so no ancilla is allocated.
- `eq_6`: out_of_scope; no code location. Readout and success probability involve measurement and post-processing, which are excluded from an operation-only circuit and are left to the runner.

## Specification changes

- eq_2: The clause cost is the squared-sum form (x_a+x_b+x_c-1)^2, which gives weights 1 (two or zero ones) and 4 (three ones), not a uniform indicator penalty on forbidden triples. Clauses must be 3 distinct variables from a general n in [3,12]. The example uses n=4 with 3 clauses. Reason: The squared-sum form is the stated alternative in the specification and expands exactly into Z and ZZ terms. A unique satisfying assignment cannot exist for n=3 with distinct-variable clauses, since a single clause on 3 variables has 3 solutions.
- eq_4: The gap-based local schedule is not computed. The schedule is linear midpoint or explicit. Reason: The module must avoid operator construction and diagonalization.
- eq_5: The filter is dropped and there is no ancilla. Reason: The filter is unverified and trivially the identity as written.
- eq_1, eq_3, eq_6: The initial |+>^n preparation (the Hadamard step) and the measurement are removed from the circuit. Reason: The module returns an operation only. Input states are prepared by the runner and measurement is done outside.
- eq_1, eq_2, eq_3, eq_4, eq_5, eq_6: Narrowed to the noiseless first-order Trotter digitized AQC. The paper's fast random or regular signals, randomized Trotter formula, decoherence, and trapped-ion implementation are not represented. Reason: These details are absent from the specification.
