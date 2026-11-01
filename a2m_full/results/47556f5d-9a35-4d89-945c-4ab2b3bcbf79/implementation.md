# Equation to Qiskit

build_circuit(instance) returns one p=1 QAOA layer for a bounded-occurrence Max E3LIN2 instance, U = exp(-i*beta*sum X) * exp(-i*gamma*C), up to a global phase. Each equation (a,b,c,rhs) gets a CX-CX-RZ-CX-CX parity-phase gadget with angle -gamma*s, where s=(-1)^rhs. A mixer RX(2*beta) follows on every qubit. The initial |+>^n preparation, measurement, angle search and expectation evaluation are left to the runner.

Source equation run: `3a307ed2-3602-4038-bdeb-efe4b6d34478`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit i (0..n-1) = boolean variable x_i; qubit 0 is the least significant bit
- computational basis: Z=+1 for bit 0, Z=-1 for bit 1
- no ancilla qubits, no classical bits
- example: n=5, qubits 0..4 = x_0..x_4

## Assumptions

- Variable i is qubit i, with Z eigenvalue (-1)^{z_i}.
- s_k = (-1)^{rhs_k}, and the equation is satisfied when the parity of its three bits equals rhs_k.
- The angle convention is Qiskit rz(theta) = exp(-i*theta*Z/2) and rx(2*beta) = exp(-i*beta*X). A sign flip of gamma is covered by the runner's angle sweep.
- The runner prepares |+>^n as the input state.
- The example instance is arbitrary and illustrative, not taken from the paper.

## Unresolved issues

- The paper's analytic light-cone formula for <ZZZ> is not available from the abstract, so it is not implemented.
- The paper's rule for choosing gamma and beta in the proofs is unknown. The example angles are only plausible starting values.
- No public validation contract was supplied, and no concrete instance was given.

## Equation mapping

- `eq_1`: implemented; build_circuit: sign s = 1 - 2*rhs and the per-equation phase-separator loop. The cost operator C is implemented as exp(-i*gamma*C) through its ZZZ terms with sign s_k. The constant part of C only contributes a global phase.
- `eq_2`: implemented; build_circuit: phase-separator loop followed by the RX(2*beta) loop. Implements exp(-i*beta*B) exp(-i*gamma*C) with B = sum of X_j. The initial |+>^n is prepared by the runner, so the H layer is not in the circuit.
- `eq_3`: implemented; build_circuit: qc.cx(a,c); qc.cx(b,c); qc.rz(-gamma*s,c); qc.cx(b,c); qc.cx(a,c). Parity gadget for exp(i*gamma*s*ZaZbZc/2). The parity is computed onto qubit c, RZ(-gamma*s) is applied, and the parity is uncomputed.
- `eq_4`: background; no code location. The objective F = <gamma,beta|C|gamma,beta> and the satisfied fraction are evaluated by the runner or an external evaluator. The circuit does not compute expectations.
- `eq_5`: out_of_scope; no code location. These asymptotic advantage targets are reference values for comparison. They are not part of the circuit, and no reference results are encoded.

## Specification changes

- eq_2: The initial Hadamard layer that prepares |+>^n is omitted. build_circuit returns only exp(-i*beta*B) exp(-i*gamma*C). Reason: The task says the circuit must be an operation, and the runner prepares input states.
- eq_1, eq_3: Global phases are dropped. This includes the constant term m/2 in C and the global phase of the ZZZ gadget. Reason: Global phases are unobservable.
- eq_2, eq_4: The step that grid-searches (gamma,beta), the measurement and sampling step, and the best-string postprocessing are not included. gamma and beta are fixed instance parameters. Reason: Scope is narrowed to the single p=1 circuit construction. The circuit must be measurement-free.
- eq_1, eq_2, eq_3: Instances are validated: 3 <= n <= 12, distinct in-range variables per equation, rhs in {0,1}, finite angles, and optionally max occurrence <= D. Violations raise ValueError. Reason: The task requires validation and a 12-qubit cap. The abstract's bound on occurrences D is enforced when D is supplied.
