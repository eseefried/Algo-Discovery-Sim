# Equation to Qiskit

Implements the generalized Kitaev phase-estimation probe operation on M product-state qubits: qubit j (Qiskit index j-1) receives n_j explicit applications of the phase gate P(phi)=diag(1,e^{i phi}) (sum n_j = N), followed by the local measurement phase shift P(theta_j) and a Hadamard, so that a subsequent computational-basis measurement by the runner reproduces the likelihood of eq_2. The |+>^M input is expected from the runner (an optional 'prepare_plus' flag can add the Hadamards). Bayesian postprocessing (eq_3) and asymptotic claims (eq_4, eq_5) are classical/analytic and not part of the circuit.

Source equation run: `7bbf4242-830e-4a14-aa2b-9673b31f5842`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0] (Qiskit index 0, least significant bit): spec qubit j=1, receives n_1=1 application of P(phi), then P(theta_1=0) (omitted as identity) and H; its measured bit is x_1
- q[1] (Qiskit index 1): spec qubit j=2, receives n_2=2 applications of P(phi), then P(theta_2=pi/2) and H; its measured bit is x_2
- Input expected from runner: |+>^{\otimes 2} = H^{\otimes 2}|00> (or set prepare_plus=true to prepend the Hadamards)
- Output bitstring (Qiskit little-endian) 'x_2 x_1' has probability (1/4)[1+(-1)^{x_1} cos phi][1-(-1)^{x_2} sin 2phi] (eq_6)

## Assumptions

- Phase gate is U_phi = diag(1, e^{i phi}) realised as Qiskit p(phi); it is applied n_j times explicitly so the circuit's gate count equals the resource N.
- Initial state |+>^{⊗M} is supplied by the runner (or via prepare_plus=true).
- Measurements are local, non-adaptive, with fixed phases theta_j given in the instance (default 0 = X basis).
- Lossless, noiseless setting; no error model included.
- Instance values are plain JSON numbers/lists (ints, floats, lists, bools).

## Unresolved issues

- The optimal distribution {n_j} and {theta_j} achieving the 1/N^2 scaling (eq_4) is not known from the abstract; the module accepts any user-supplied distribution.
- Whether the paper uses adaptive measurements or the periodic cost function cannot be determined; the circuit implements the non-adaptive fixed-theta variant.
- Loss model and alternative resource quantification are not represented.

## Equation mapping

- `eq_1`: implemented; build_circuit: loop commented '# eq_1: qubit j accumulates phase n_j*phi' (qc.p(phi) repeated n_j times); optional '# eq_1 initial product state' Hadamard block. Each qubit j receives n_j explicit applications of diag(1,e^{i phi}); _parse_instance enforces sum n_j = N > 0. The |+> initial state is left to the runner by default (operation-only), with an optional prepare_plus flag.
- `eq_2`: implemented; build_circuit: loop commented '# eq_2: local measurement basis rotation'. Applies P(theta_j) then H on each qubit, so that a computational-basis measurement by the runner has the Born-rule statistics p(x_j|phi) = [1+(-1)^{x_j} cos(n_j phi+theta_j)]/2 with independent qubits. The measurement itself is not included (measurement-free operation).
- `eq_3`: out_of_scope; no code location. Flat-prior Bayesian posterior, estimator and average cost are classical postprocessing over sampled outcomes and prior integration; not part of a unitary circuit.
- `eq_4`: background; no code location. Asymptotic 1/N vs 1/N^2 scaling claims are analytic results about optimized distributions; the module only builds the probe for a given {n_j}.
- `eq_5`: background; no code location. Fundamental Bayesian bound pi^2/N^2 is a reference asymptotic result, not something a finite circuit implements.
- `eq_6`: implemented; example_instance_json and build_circuit with n=[1,2], theta=[0, pi/2]. The tiny instance M=2, N=3, (n_1,n_2)=(1,2), (theta_1,theta_2)=(0,pi/2) is the provided example; the circuit realizes exactly the likelihood stated in eq_6 when fed |+>^{⊗2} and measured.

## Specification changes

- eq_1: The Hadamard preparation of |+>^{⊗M} from |0>^{⊗M} is NOT included by default; the circuit is the operation acting on a runner-prepared |+>^{⊗M}. An optional boolean 'prepare_plus' adds the Hadamards. Reason: Task requires an operation without input-state preparation; inputs are prepared by the runner.
- eq_2, eq_3: Computational-basis measurement and Bayesian postprocessing are excluded from the module. Reason: Measurement-free unitary circuit required; estimation is classical postprocessing.
- eq_1: Added practical caps: M <= 12 qubits and N = sum n_j <= 4096 phase-gate applications; N must be positive. Reason: Qubit cap mandated by the task; gate cap avoids unbounded circuit sizes.
- eq_2: Spec qubit j (1-indexed) is mapped to Qiskit index j-1; theta_j = 0 phase gates are omitted as identities. Reason: Explicit physical qubit ordering with Qiskit little-endian convention; identity gates have no effect.
