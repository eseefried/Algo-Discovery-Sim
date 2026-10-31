# Equation to Qiskit

Qiskit module implementing t steps of the barrier-hindered discrete-time coined quantum-walk search operator U_eps = S_eps (I x C) Q on the complete graph K_N (N a power of two, self-loop coin directions retained). The oracle Q is a multi-controlled phase flip on the position register, the Grover coin C is H^n X^n MCZ X^n H^n with a tracked global phase, and the barrier shift S_eps = eps I + i sqrt(1-eps^2) S = exp(i*theta*S), theta = arccos(eps), is realised ancilla-free by diagonalising each qubit-pair SWAP to a CZ and applying the parity phase via an inclusion-exclusion family of multi-controlled phase gates. No state preparation or measurement is included; the runner supplies |s>|s> and measures the position register.

Source equation run: `da57fddc-1c33-47fb-93c8-cdd0d4a48bb4`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Total qubits for the example: 4 (2 per register); general: 2*log2(N) <= 12, so N <= 64.
- Qubits 0..n-1 (n = log2 N): position register |u>, qubit k holds bit k of u (qubit 0 = least significant bit).
- Qubits n..2n-1: coin register |v>, qubit n+k holds bit k of v (qubit n = least significant bit).
- Shift pairs: position qubit k is swapped (hindered) with coin qubit n+k.
- Example (N=4): qubits 0,1 = position u; qubits 2,3 = coin v; marked vertex w=0 corresponds to position bits 00.
- Expected runner input: uniform superposition |s>|s> on all 2n qubits (Hadamard on every qubit); output quantity: probability that position qubits read w after measurement.

## Assumptions

- Barrier model eq_4 (stay amplitude eps, hop amplitude i sqrt(1-eps^2), uniform over all edges, acting only on the shift) is taken as given from the math stage; the paper's exact model may differ.
- Self-loop coin directions |u,u> are kept so that the coin register is a full log2(N)-qubit register.
- Instance keys are N (int), marked (int in [0,N)), epsilon (real in [0,1]), steps (non-negative int); steps = 0 yields the identity circuit on 2n qubits.
- The runner prepares |s>|s> by Hadamards on all 2n qubits and measures only the position qubits 0..n-1 to estimate p_eps(t) (eq_5).
- qc.mcp with up to 11 controls (N = 64) is assumed available in Qiskit 2.6.1; gate count grows as 2^n multi-controlled phases per step, acceptable for n <= 6.

## Unresolved issues

- The exact barrier/failure-amplitude model, phase conventions, and treatment of the coin in the original paper are not available from the abstract; eq_6's threshold can only be tested for the assumed model.
- No reference numerical values for p_eps(t) or t* are available, so the threshold scaling must be inferred from sweeps over N in {2,...,64} and epsilon, a small range for asymptotic claims.
- The continuous-time version of the result is not implemented.

## Equation mapping

- `eq_1`: background; no code location. Initial state |s>|s> is input-state preparation, excluded from the returned operation; module docstring documents that the runner must prepare it (Hadamards on all 2n qubits).
- `eq_2`: implemented; _oracle (Q) and _coin (C). Q is X-conjugated multi-controlled Z on the position register flipping the phase of |w>; C = 2|s><s| - I is implemented exactly as -(H^n X^n MCZ X^n H^n) with the minus sign tracked in global_phase.
- `eq_3`: implemented; build_circuit loop (operator order Q, then I x C, then shift) and _barrier_shift with theta = pi/2 when epsilon = 0. The flip-flop shift S is the product of qubit-pair SWAPs between position and coin registers; at epsilon = 0, exp(i*pi/2*S) = iS, i.e. S up to a global phase i, and the step ordering U = S (I x C) Q is realised by the loop.
- `eq_4`: implemented; _barrier_shift (theta = acos(epsilon) computed in build_circuit). S_eps = eps I + i sqrt(1-eps^2) S = exp(i theta S) is implemented exactly (no Trotterisation) by diagonalising each pair SWAP to a CZ and applying the parity phase exp(i theta prod CZ_k) with an inclusion-exclusion family of multi-controlled phase gates.
- `eq_5`: background; no code location. Success probability and runtime t* require measurement of the position register and classical post-processing over a sweep of steps, which are performed by the runner, not the operation.
- `eq_6`: background; no code location. The threshold scaling claim is a theoretical statement to be tested by the runner by comparing peak times across N and epsilon; it is not an operation.

## Specification changes

- eq_1, eq_2, eq_3, eq_4: Scope narrowed to N a power of two with 2*log2(N) <= 12 (N in {2,4,8,16,32,64}); non-power-of-two N and larger N raise ValueError. Reason: Each register must be exactly log2(N) qubits for the self-loop-inclusive tensor-product Hilbert space, and the 12-qubit cap applies.
- eq_1, eq_5: Initial-state preparation and the position measurement are removed from the generated circuit; build_circuit returns only U_eps^t. Reason: Contract requires a measurement-free operation with inputs prepared by the runner.
- eq_3, eq_4: S_eps is implemented as exp(i*theta*S) with theta = arccos(epsilon); at epsilon = 0 this equals i*S rather than S, i.e. the ideal shift is reproduced up to a global phase i per step (tracked via qc.global_phase). Reason: The identity eps I + i sqrt(1-eps^2) S = exp(i theta S) holds exactly because S^2 = I; using it gives an exact ancilla-free circuit and the global phase is physically irrelevant to p_eps(t).
- eq_2: The Grover coin's overall sign (C = -H^n X^n MCZ X^n H^n) and the e^{i theta} prefactor of the shift are recorded in the circuit global_phase instead of being dropped. Reason: Keeps the implemented unitary equal to the specified operator rather than merely equal up to phase.
