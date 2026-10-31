# Equation to Qiskit

Implements the scoped d_A = d_B = 2 instance of the controlled-unitary decomposition: a generic two-qubit unitary written (via its cosine-sine decomposition) as the product of exactly three controlled unitaries U = C^A_P · C^B_theta · C^A_Q, matching the abstract's bound N = 2 d_A - 1 = 3 for d_A = 2. The instance supplies the CSD factors as parameters (Euler angles + phase for the four target unitaries Q_0, Q_1, P_0, P_1 and the two CSD angles theta_k); the module emits only standard gates (X, CU, CRY). Qubit 0 is system B (least significant), qubit 1 is system A (most significant), matching the specification's index j*d_B + k.

Source equation run: `ae43105e-1062-43d8-bdd2-b8fd1bf63496`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: register 'b' (system B, d_B = 2, least significant bit k)
- qubit 1: register 'a' (system A, d_A = 2, most significant bit j)
- Composite basis |j>_A |k>_B has integer index 2*j + k, matching the specification's ordering j*d_B + k
- Instance 'Q'[j] = [theta, phi, lam, gamma] parameterises Q_j = exp(i gamma) U(theta, phi, lam) applied to B when A = j; likewise 'P'[j] for P_j; 'theta'[k] is the CSD angle theta_k giving Ry(2 theta_k) on A when B = k

## Assumptions

- Composite basis ordering |j>_A |k>_B with A most significant; realised as Qiskit qubit 1 = A, qubit 0 = B.
- Instance parameters are the exact CSD factors of the intended U; the module does not verify unitarity of U or recompute the decomposition.
- Qiskit CU(theta, phi, lam, gamma) applies exp(i gamma) U(theta, phi, lam) on the target when the control is |1>; Ry(2 theta_k) reproduces the CSD cosine-sine block in the stated basis.
- The count N = 3 is reported as the number of controlled-unitary factors, not the number of elementary Qiskit gates (each factor is expanded into two controlled gates plus X conjugations).

## Unresolved issues

- The paper's actual proof technique for the 2 d_A - 1 bound is unknown; the CSD-based construction coincides with the bound only at d_A = 2.
- Extension to d_B > 2 would require decomposing arbitrary d_B x d_B target unitaries into standard gates, which is not implemented.

## Equation mapping

- `eq_1`: implemented; _a_controlled (A-controlled unitary sum_j |j><j|_A (x) W_j) and _b_controlled_ry (B-controlled unitary sum_k V_k (x) |k><k|_B). Both controlled-unitary types are realised with computational-basis controls using CU / CRY gates, with X-conjugation of the control for the j = 0 or k = 0 branch.
- `eq_2`: background; no code location. Existence bound; the circuit realises N = 3 = 2 d_A - 1 factors for d_A = 2 (noted in the final comment of build_circuit), but the general-d_A constructions are not implemented.
- `eq_3`: background; no code location. The cosine-sine decomposition is the classical preprocessing that produces P_j, Q_j, theta_k; the module takes these factors as instance parameters rather than computing the CSD of a dense U (see specification_changes).
- `eq_4`: implemented; _a_controlled (block-diagonal outer factors) and _b_controlled_ry (middle [[C,-S],[S,C]] block as controlled Ry(2 theta_k)). The tensor-product identification of the CSD factors is what each helper appends; Qiskit ry(2t) matches the [[cos t, -sin t],[sin t, cos t]] block with A as the row index.
- `eq_5`: implemented; build_circuit (sequence: _a_controlled with Q, _b_controlled_ry, _a_controlled with P). The three factors are appended in right-to-left operator order (C^A_Q first, C^A_P last), giving the full decomposition U = C^A_P C^B_theta C^A_Q.
- `eq_6`: out_of_scope; no code location. n-partite bound stated in the abstract; no construction available and outside the scoped bipartite d_A = 2 instance.

## Specification changes

- eq_3: The classical CSD preprocessing step (computing P_0, P_1, Q_0, Q_1, theta_k from a dense 4x4 unitary U) is moved outside the module: the instance supplies the CSD factors directly as Euler-angle-plus-phase parameters for each 2x2 target unitary and the two CSD angles. Reason: The module may not construct or embed dense unitaries, and a robust numerical CSD (including matching of singular vectors across blocks for degenerate cosines) is not available with the permitted imports. The emitted circuit still realises exactly the operator product of eq_5 for the supplied factors.
- eq_1, eq_4, eq_5: Each 2x2 target unitary is parameterised as exp(i gamma) U(theta, phi, lam) (Qiskit CU convention) so that an arbitrary element of U(2), including its global phase, is covered; controls are restricted to the computational basis. Reason: Generic U(2) targets are needed to reproduce an arbitrary two-qubit U; in the CSD-based construction all controls are in the computational basis, so arbitrary control bases (allowed in eq_1) are not needed.
- eq_2: Scope narrowed to d_A = d_B = 2; other dimensions raise ValueError. Reason: No experiment_scope was supplied and the paper's general 4 d_A - 5 and 2 d_A - 1 constructions are not recoverable from the abstract; only the d_A = 2 case has an explicit construction (via CSD) in the specification.
