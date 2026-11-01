# Equation to Qiskit

Phase-encoding operation of the generalized Kitaev scheme: for each qubit k, n_k sequential phase gates U=diag(1,e^{i phi}) are applied, with the n_k distributed arbitrarily over M<=12 qubits and N=sum n_k. The circuit is a product of single-qubit gates (no entanglement), so on a runner-prepared |+>^M input it yields the product probe state of eq_2 and eq_3. State preparation, measurement and estimation are excluded.

Source equation run: `9f28a4ff-bb3c-419a-84d1-bb0aab7dd10d`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubit k-1 (Qiskit index k-1) is probe qubit q_k for k=1..M, with M=len(n)<=12
- Each qubit is expected to be prepared in |+> = (|0>+|1>)/sqrt(2) by the runner
- Each qubit carries computational-basis encoding; qubit 0 is the least significant bit
- Example: index 0 receives 3 phase gates, index 1 receives 1 phase gate

## Assumptions

- Phase gate U=diag(1,e^{i phi}) is implemented with qc.p(phi, qubit)
- The phase phi is a known classical parameter bound in the instance
- The input state |+>^M is prepared by the runner
- No loss or noise is modeled
- Gates on each qubit are applied sequentially n_k times rather than merged into a single p(n_k*phi), which is mathematically equivalent

## Unresolved issues

- The optimal gate distributions n_k from the paper are not specified in the abstract and are not computed
- The measurement basis and estimator are not specified
- The loss model and the Bayesian bound are not implemented

## Equation mapping

- `eq_1`: implemented; _parse (validation of n_k, N=sum n_k) and the gate loop in build_circuit. The distribution n_k is given in the instance; the total N is its sum and is checked against an optional 'N' field. The gate loop applies exactly sum n_k gates.
- `eq_2`: implemented; build_circuit inner loop: qc.p(phi, q[k]) repeated n_k times. n_k applications of diag(1,e^{i phi}) map |+> to (|0>+e^{i n_k phi}|1>)/sqrt2. The |+> preparation is done by the runner, not by the circuit.
- `eq_3`: implemented; build_circuit (only single-qubit gates, no entangling operations). Because the operation is a tensor product of single-qubit phase gates, a product input gives the product probe state.
- `eq_4`: background; no code location. Mean square error is an evaluation cost function for measurement and estimation outcomes, not part of the unitary operation.
- `eq_5`: out_of_scope; no code location. Scaling claims for optimal distributions require optimization, an estimator and statistical analysis, which are outside this operation.

## Specification changes

- eq_2, eq_3: The circuit contains only the phase-encoding operation. The |+> input preparation is excluded and left to the runner. Reason: The task requires an operation with no input-state preparation.
- eq_4: No measurement, estimator or error evaluation is included. Reason: The task forbids measurements and sampling in the circuit, and the abstract does not specify the estimator.
- eq_1: The M=2 scope is generalized to any M from 1 to 12, with the distribution n_k supplied by the user. No optimal distribution is computed. N is capped at 4096. Reason: The construction is the same for any M and the optimal distributions are not given in the abstract. The qubit cap is 12 and the gate cap bounds circuit size.
- eq_5: The scaling claims are not implemented. Reason: They require optimization and statistical analysis that are not part of the circuit.
