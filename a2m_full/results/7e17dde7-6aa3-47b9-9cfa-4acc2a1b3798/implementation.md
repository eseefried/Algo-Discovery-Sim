# Equation to Qiskit

Single-qubit Pauli+V approximation of Rz(theta) to operator-norm error epsilon up to global phase. build_circuit searches levels k=0..max_k and finds integer quaternions (a,b,c,d) with norm 5^k. It solves b^2+c^2=5^k-a^2-d^2 by integer square roots and keeps candidates with |a cos(theta/2)+d sin(theta/2))|/5^(k/2) >= 1-eps^2/2, which is the operator-norm criterion up to global phase. The best candidate is factored by left-division by the six V-type quaternions 1+-2i, 1+-2j, 1+-2k into a V-word times a Pauli unit, and emitted as rx/ry/rz gates (V = R_sigma(2 atan2(+-2,1))) plus x/y/z and a global phase. The circuit has no state preparation or measurement.

Source equation run: `116eec31-7c8c-405b-94ed-97dc1eb1e832`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: single data qubit, computational basis, Qiskit little-endian (only one qubit)

## Assumptions

- theta, epsilon and max_k are instance parameters. The example uses theta=pi/5 and epsilon=0.3, for which the k=1 quaternion 2+k (V-word 1-2k times a Pauli Z factor) is accepted.
- Error is the operator-norm distance up to global phase.
- Global phase of the output circuit is set so the unitary equals the SU(2) element of the quaternion, up to the +-1 sign.
- Each V gate is a single rx/ry/rz rotation by 2*atan2(+-2,1).

## Unresolved issues

- The paper's actual deterministic search procedure, the exact slab region and enumeration order, and the depth bounds are not reconstructed.
- The Hurwitz half-integer case is not handled, so an accepted Lipschitz quaternion that fails integral left-division by the six generators is skipped.
- No claim is made that the resulting word is globally shortest or canonical, or that the expected depth of about 3 log_5(1/epsilon) is attained.

## Equation mapping

- `eq_1`: implemented; _gens, _axis, _reduce and the gate emission loop in build_circuit. The quaternion-to-SU(2) map i,j,k -> -iX,-iY,-iZ is used to turn V-type quaternions 1+-2e and the Pauli units into rx/ry/rz and x/y/z gates, with the global phase tracked exactly.
- `eq_2`: implemented; _search (ch, sh). The target Rz(theta) is the quaternion direction (cos(theta/2),0,0,sin(theta/2)). It is used in the overlap test.
- `eq_3`: background; no code location. The heuristic slab region is not used as an enumeration filter. The full disk a^2+d^2<=5^k is scanned and acceptance is by the direct overlap criterion of eq_5.
- `eq_4`: implemented; _search (t = rem - b*b, math.isqrt). For each accepted (a,d), b^2+c^2 = 5^k-a^2-d^2 is solved by brute force over b with an integer square root for c, which gives all (b,c) including signs.
- `eq_5`: implemented; _search (thr and the p test). For SU(2) elements, min over global phase of the operator-norm distance equals sqrt(2-2|p|) with p=(a cos(theta/2)+d sin(theta/2))/5^(k/2). The test |p| >= 1-eps^2/2 is equivalent to distance <= eps.

## Specification changes

- eq_1: Fixed the convention U_q = a I - i(bX+cY+dZ) so that V=(I+2iX)/sqrt5 corresponds to quaternion 1-2i (b=-2), not 1+2i. The six generators 1+-2i, 1+-2j, 1+-2k are all included. Reason: The spec text was sign-ambiguous. Both signs are generators, so the group is unchanged.
- eq_3: The slab region is not used. Candidates are accepted only by the direct criterion of eq_5. Reason: The spec says the slab bounds are heuristic and that the direct condition is the actual acceptance test.
- eq_4, eq_5: Scope narrowed to brute-force enumeration with max_k capped at 4. Within a level, accepted candidates are ordered by overlap, with ties broken by the quaternion tuple. The first one that factors into a V-word is used, and the minimal k is searched first. Reason: This keeps enumeration tiny and deterministic. The paper's actual deterministic-search algorithm, its proofs and its depth bounds are not reproduced.
- eq_1: Word reduction is done by DFS left-division by the six V-type quaternions, leaving a final Lipschitz unit (+-1, +-i, +-j, +-k) that is emitted as a Pauli gate plus a global phase. Candidates that do not factor are skipped. Reason: The spec leaves the reduction procedure open. Trial division with unit tracking is the stated primitive reduction.
