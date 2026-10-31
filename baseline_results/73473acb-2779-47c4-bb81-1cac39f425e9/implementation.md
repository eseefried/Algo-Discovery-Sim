# Equation to Qiskit

Implements the two-qubit Repeat-Until-Success unitary W of eq_W_construction for a user-supplied exact solution (z, y, L) of the norm equation |z|^2 + y^2 = 2^L with z in Z[omega] and y in Z[sqrt2]. W = |0><0|_t (x) M_0 + |1><1|_t (x) M_1 with M_1 = 2^{-L/2}[[z,-y],[y,z*]] and M_0 = conj(M_1); on ancilla outcome 0 the target receives diag(z*,z)/|z| = R_z(2 arg z), on outcome 1 it receives the identity. Using z = |z| e^{i phi}, cos(th) = |z|/sqrt(2^L), sin(th) = y/sqrt(2^L) the controlled pair of single-qubit unitaries factorizes exactly as W = RZZ(phi) . RY(2 th)_ancilla . RZZ(phi), which is emitted with standard gates (3 gates, 2 qubits). The norm equation is checked exactly in integer arithmetic; invalid instances raise ValueError. Measurement, ancilla reset and repetition (the RUS loop) are left to the runner; exact Clifford+T synthesis of W and the paper's classical search for (z, y, L) are out of scope.

Source equation run: `623b2686-aff9-4256-9a46-2ddda149674a`

Generation: **generated**; validation: **failed**.

Generated source was not executed: ValueError: Module constants must be literals or small numeric expressions.

Paper fidelity has not been independently verified.

## Register layout

- q[1] = RUS ancilla a (ancilla_index=1, most significant bit so the joint computational-basis index is 2a+t as in the specification); runner prepares |0>, measures after W: outcome 0 = success, outcome 1 = failure (identity on target)
- q[0] = target/data qubit t carrying |psi>; receives R_z(2 arg z) = R_z(2 arg(2+omega)) ~ R_z(0.5110) on success for the example instance (success probability (5+2 sqrt2)/8 ~ 0.9786)
- Instance encoding: z = a + b omega + c omega^2 + d omega^3 given as [a,b,c,d]; y = e + f sqrt2 given as [e,f]; L with 2^L = |z|^2 + y^2 (checked exactly)

## Assumptions

- The instance supplies an exact solution (z, y, L) of |z|^2 + y^2 = 2^L; the paper's probabilistically polynomial classical search for such solutions given (theta, epsilon) is not implemented.
- The failure branch is restricted to the identity (y real in Z[sqrt2]), as in the specification.
- The runner prepares the ancilla (default Qiskit qubit 1) in |0> and the target (qubit 0) in an arbitrary |psi>, and performs the ancilla measurement/repetition externally.
- Rotation angles phi = arg z and 2 th = 2 atan2(y, |z|) are computed in double precision; the unitary is exact up to floating-point rounding of these angles.
- L is capped at 60 only to keep 2^L an ordinary integer comparison; the circuit always uses exactly 2 qubits.

## Unresolved issues

- The paper's actual two-qubit RUS circuit template and its T-count as a function of L are unknown; the emitted W is the specification's proposed realization, not necessarily the paper's.
- No exact Clifford+T decomposition of W is produced, so the T-count claims of the abstract cannot be checked with this module.
- The specification's distance metric is assumed but unused here since the module implements exact rotations for a supplied z.

## Equation mapping

- `eq_rus_structure`: implemented; build_circuit (comment block before qc.rzz) and module docstring: W's ancilla-0 block A = diag(z*,z)/2^{L/2} and ancilla-1 block C = y I/2^{L/2}. The unitary part of the RUS block (W acting on |0>_a (x) |psi>_t with success block proportional to R_z(2 arg z) and failure block proportional to the identity) is realized by the emitted circuit. The ancilla measurement, probability p and geometric repetition are semantics executed by the runner, not part of the returned operation.
- `eq_distance`: background; no code location. The approximation metric is only needed to select z for a target angle theta; the module takes an already-chosen exact (z, y, L) and implements R_z(2 arg z) exactly on success, so no distance is computed.
- `eq_norm_equation`: implemented; _check_norm_equation (exact Z[sqrt2] integer check of |z|^2 + y^2 = 2^L) and _angles (p = |z|^2/2^L enters via cos th = |z|/sqrt(2^L)). The cyclotomic parametrization is enforced exactly: both the rational and sqrt2 coefficients of |z|^2 + y^2 - 2^L must vanish, y is real by construction (Z[sqrt2]), and the success branch is diag(z*,z)/sqrt(2^L).
- `eq_W_construction`: implemented; build_circuit: qc.rzz(phi, a, t); qc.ry(2*th, a); qc.rzz(phi, a, t). W = |0><0|_t (x) M_0 + |1><1|_t (x) M_1 with M_1 = 2^{-L/2}[[z,-y],[y,z*]], M_0 = conj(M_1) is factorized exactly as RZZ(phi) RY(2 th)_a RZZ(phi) with phi = arg z, cos th = |z|/sqrt(2^L), sin th = y/sqrt(2^L).
- `eq_exact_synthesis`: out_of_scope; no code location. W has entries in Z[omega, 1/sqrt2] and is therefore exactly Clifford+T synthesizable, but the module emits W with continuous RZZ/RY rotations rather than an exact Clifford+T gate sequence; implementing an exact synthesis algorithm (Kliuchnikov-Maslov-Mosca / Giles-Selinger) is beyond this scope.
- `eq_euler`: out_of_scope; no code location. Only a single axial Z-rotation RUS block is implemented; the Euler-angle assembly of three blocks with Hadamards for a general single-qubit unitary is not included.
- `eq_tcount_claim`: out_of_scope; no code location. Expected T-count T(W)/p and the paper's numerical 2.5x claim are cost statements about an exact Clifford+T realization and are not computed or reproduced by the module.
- `eq_toy_instance`: implemented; example_instance_json: {"z": [2,1,0,0], "y": [-1,1], "L": 3} i.e. z = 2 + omega, y = sqrt2 - 1, 2^3 = 8. The example instance is exactly the toy solution; _check_norm_equation verifies 5 + 3 = 8 and sqrt2 part 2 - 2 = 0, and build_circuit produces W implementing R_z(2 arg(2+omega)) on success with p = (5+2 sqrt2)/8.

## Specification changes

- eq_W_construction, eq_rus_structure: Qubit index mapping: the specification labels the ancilla 'qubit 0 (most significant, joint index 2a+t)'. In Qiskit qubit 0 is the least significant bit, so the ancilla is placed on Qiskit qubit 1 (default ancilla_index = 1) and the target on qubit 0; this preserves the matrix of W as written (basis index 2a+t). ancilla_index = 0 is accepted as an option for the swapped layout. Reason: Resolve the big-endian labeling in the specification against Qiskit's little-endian convention while keeping the specified matrix form of W.
- eq_W_construction, eq_exact_synthesis: W is realized exactly by three continuous-angle standard gates (RZZ(phi), RY(2 th), RZZ(phi)) instead of an exact Clifford+T gate sequence; eq_exact_synthesis is therefore marked out of scope and no T-count is reported. Reason: Exact Clifford+T synthesis algorithms are a separate, substantial construction not reconstructible from the abstract; the gate-level factorization reproduces the same unitary W exactly (up to floating-point angle rounding).
- eq_rus_structure, eq_tcount_claim: The ancilla measurement, feed-forward, reset and repeat-until-success loop are not part of the returned circuit; only the unitary W is emitted. Reason: The task requires a measurement-free unitary operation; the RUS control flow is an experiment-level procedure executed by the runner.
- eq_norm_equation: Instances with y = 0 (p = 1, W reduces to a target-controlled Z-rotation pair) and negative y are accepted; z = 0 is rejected. Reason: y = 0 and y < 0 are valid solutions of the norm equation with the identity failure branch; z = 0 leaves the success-branch rotation undefined.
