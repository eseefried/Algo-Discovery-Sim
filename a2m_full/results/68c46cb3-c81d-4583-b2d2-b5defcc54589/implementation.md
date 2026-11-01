# Equation to Qiskit

One-qubit operation implementing k sequential applications of the noisy amplitude-error pi pulse U = exp(-i*pi*(1+epsilon)/2 * sigma_x) = Rx(pi(1+epsilon)), where k is given either directly or as 2^stage. An optional known ideal X pulse removes the leftover ideal pulse for odd k, so the net operation is a pure rotation by k*phi about x (phi = pi*epsilon) up to global phase. State preparation, basis change, measurement and all classical estimation (atan2, branch unwrapping, scaling) are left to the runner and the classical post-processing.

Source equation run: `ae82899d-fcfd-4403-af5c-748d701366a4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: q[0], the single data qubit; U^k acts on it (little-endian trivial, 1 qubit)

## Assumptions

- Axis n = x, no off-resonance error, no drift.
- The ideal pulse correction for odd k is an optional exact X gate (known pi pulse), which differs from the exact remainder only by a global phase.
- Power is capped at 1024 and stage at 10 to bound circuit size.

## Unresolved issues

- The sign and offset convention for sin/cos quadratures in eq_3 is not fixed in the circuit and is left to the runner's state preparation and basis change.
- Robust theorem constants, off-resonance estimator and universal gate-set sequences from the paper are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit: theta = pi*(1+epsilon) and qc.rx(theta, 0). Rx(theta) = exp(-i*theta/2*sigma_x) is exactly the noisy gate U. The factorization into an ideal pulse times a rotation by phi is an algebraic identity, realized implicitly.
- `eq_2`: implemented; build_circuit: loop of k qc.rx calls and optional qc.x for odd k. k sequential copies of U give U^k. For even k this equals the pure rotation exp(-i*(k/2)*phi*sigma_x) up to global phase. For odd k the optional known X cancels the ideal pulse, up to global phase.
- `eq_3`: out_of_scope; no code location. The SPAM signal model (visibility, bias) concerns state preparation and measurement, which the runner handles. The operation includes no SPAM.
- `eq_4`: out_of_scope; no code location. atan2 readout is classical post-processing of measured counts. No measurement is allowed in the circuit.
- `eq_5`: out_of_scope; no code location. Branch unwrapping and refinement is classical adaptive post-processing across stages.
- `eq_6`: background; no code location. Heisenberg scaling is an asymptotic statement about estimation error versus query count. It motivates the choice k=2^stage but is not a circuit.

## Specification changes

- eq_1, eq_2, eq_3, eq_4, eq_5, eq_6: Scope narrowed to the coherent U^k operation for a single stage (single k) on one qubit. The full multi-stage adaptive estimation protocol is not built. Reason: The task requires a single measurement-free unitary operation, with preparation, measurement and classical estimation excluded.
- eq_2: The task spec writes U^{2k} = (-1)^k exp(-i k phi sigma_x), a pure rotation by 2k*phi. The code handles general k (even or odd) by repeated U, with an optional X to cancel the ideal pulse for odd k, so the net rotation angle is k*phi for the k applications. Reason: The estimation stages use k=2^j applications, so the operation is parametrized by number of applications, not by 2k.
- eq_1: Restricted to axis n=x with |epsilon|<=0.5, with no off-resonance component. Reason: Matches the stated narrow amplitude-error-only scope. The bound is an input validation limit.
