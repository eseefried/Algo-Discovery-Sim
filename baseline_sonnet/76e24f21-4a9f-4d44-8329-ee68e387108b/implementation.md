# Equation to Qiskit

Scoped construction: binary-fanout (f=2) shift-register trellis with one fixed start state and N decode steps. The path register holds one choice bit per step. The circuit prepares A = (additive branch-phase layer) * H^N, giving the uniform path superposition with a path-dependent phase. It then applies k generic amplitude-amplification iterations Q = A (I-2|0><0|) A^dagger (I-2|m><m|) with a caller-specified marked path m. The specialized QVA amplification, the FFT-butterfly state preparation and the speedup analysis are not implemented.

Source equation run: `35e8979d-0eab-4756-b434-954874ba378a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit t-1 (t=1..N): transition choice bit c_t at trellis step t (0 or 1), little-endian: qubit 0 is step 1
- start state fixed to 0 (S_0=1); trellis state s_t = last Q-1 choice bits (shift register), not stored in qubits
- no phase ancilla; example uses 3 qubits (N=3, Q=2)

## Assumptions

- f=2, S_0=1, shift-register trellis with memory Q-1 bits
- edge_phases[t-1] has length 2^(min(t-1,Q-1)+1), indexed by idx = sum_j c_{t-j} 2^j (bit 0 = current choice c_t, bit j = choice at step t-j)
- marked_path[i] is the choice bit at step i+1 (qubit i)
- The runner supplies the input |0...0> on the N qubits
- Because the phase layer is diagonal and the oracle marks a basis state, the marking success probability follows the standard sin^2((2k+1)theta) law with sin^2(theta)=1/2^N regardless of the phase values

## Unresolved issues

- The actual phase function g and the oracle that marks the most probable path are unspecified
- The specialized amplification procedure, FFT-butterfly state preparation and speedup/complexity claims are not reproduced
- Marking of the best path is not derived from the phases (not computed quantumly)

## Equation mapping

- `eq_1`: implemented; _prepare_A (Hadamard layer on N qubits). With f=2 and S_0=1 the path register has 2^N = f^N basis states, all legal paths; the register size is validated at N<=12.
- `eq_2`: implemented; _prepare_A. Uniform-amplitude superposition from Hadamards followed by a diagonal phase layer exp(i phi(p)).
- `eq_3`: implemented; _prepare_A phase loop over edge_phases. phi(p) is realized as the sum over steps of caller-supplied branch phases indexed by (t, previous state, choice). The function g and the HMM probabilities are replaced by these supplied angles.
- `eq_4`: implemented; build_circuit iteration loop. Generic amplitude amplification Q = -U_psi U_mark with U_psi = A(2|0><0|-I)A^dagger, realized as A(I-2|0><0|)A^dagger (I-2|m><m|), which is identical including sign.

## Specification changes

- eq_1: Restricted to fanout f=2 and a single fixed start state (S_0=1); the path register is exactly N qubits with one choice bit per step. Reason: Keeps the construction compact and the register encoding unambiguous.
- eq_2, eq_3: The unspecified phase function g(Pr(p|y)) is replaced by an additive sum of caller-supplied per-branch phase angles, which corresponds to g = log-like of the product of branch probabilities. Phases are applied by pattern-controlled phase gates, with no ancilla and no explicit score computation. Reason: The abstract gives no phase schedule; additive branch phases follow the factorized HMM form and need no workspace.
- eq_3: Trellis states are taken as a shift register (s_t = last Q-1 choice bits, with zero initial memory) so the branch metric depends on (t, s_{t-1}, c_t) via the preceding choice qubits. Reason: The abstract does not give a trellis topology; the shift-register form matches a convolutional code.
- eq_4: The marked path is supplied directly in the instance rather than found by a quantum score comparison; the specialized amplification of the paper is replaced by generic Grover iterations with a single marked path (M=1). Reason: No oracle or optimum-finding procedure is specified.
- eq_2, eq_4: The operation includes the Hadamard preparation A acting on the runner-supplied register (assumed |0...0>) as part of the operator; the initial state is not prepared by the circuit. Reason: A is part of amplitude amplification and the uniform-superposition construction.
