# Equation to Qiskit

Qiskit construction of canonical amplitude estimation for the mean of f:{0,1}^n->[0,1]. It uses A = H^n on x followed by multiplexed Ry rotations onto a, the Grover iterate Q = -A S_0 A^-1 S_chi, controlled-Q^(2^j) from counting qubit c_j, and QFTGate(t).inverse() on the counting register. The circuit is unitary, measurement-free and bound. It covers only the standard amplitude-estimation reconstruction, not the paper's novel algorithm, the Aharonov variant or the median algorithm.

Source equation run: `012a1d40-badb-4cb1-8eec-fff649e2a8b6`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n-1: index register x (little-endian, x=sum x_i 2^i); example: qubits 0,1
- qubit n: value qubit a, the |1> amplitude carries sqrt(f); example: qubit 2
- qubits n+1..n+t: counting register c, qubit n+1+j has weight 2^j in y; example: qubits 3,4,5
- total qubits n+1+t, at most 12; example uses 6

## Assumptions

- f values are already in [0,1] and given as a list of length 2^n; f(x) is indexed by the little-endian integer of the x register.
- The oracle is a direct multiplexed rotation, with no query-counting ancillas.
- Only the standard amplitude-estimation reconstruction is implemented, as stated in the specification.

## Unresolved issues

- The paper's novel optimal algorithm, the Aharonov-style variant and the median algorithm are not implemented because the abstract does not specify them.
- The variance-based rescaling for unbounded f is not implemented.
- Circuit depth grows as 2^t controlled-Q uses, so t is capped at 8.

## Equation mapping

- `eq_1`: implemented; _prep(n, f). H on every x qubit, then for each x a multi-controlled Ry(2*asin(sqrt f(x))) on a with ctrl_state=x. Output is the stated A|0>, so P(a=1) is the mean of f.
- `eq_2`: implemented; _body(n, A) and the p(pi) on the control in build_circuit. Q = -A S_0 A^-1 S_chi. S_chi is Z on a. S_0 is X-conjugated multi-controlled Z. The global -1 is applied as a phase gate on the control qubit of each controlled-Q use.
- `eq_3`: background; no code location. Eigenphase structure of Q that justifies phase estimation. It is not coded separately; the circuit performs the phase estimation.
- `eq_4`: out_of_scope; no code location. Classical postprocessing p_hat = sin^2(pi y/M) and the error bound involve measurement and analysis, which the operation does not include.
- `eq_5`: implemented; build_circuit: qc.append(QFTGate(t).inverse(), cnt). Inverse QFTGate on counting qubits listed in increasing index order, with controlled-Q^(2^j) controlled by cnt[j]. The little-endian integer y is then readable with qubit j weighted 2^j. Measurement is not included.

## Specification changes

- eq_1, eq_2, eq_3: The module generalises the tiny instance to a parametrised n, t and f table, with f rescaled into [0,1] by the caller. Reason: The operation must work for varying valid instances and validate parameters.
- eq_1, eq_3: The circuit includes the initial H on the counting register and the state preparation A, so it acts on the all-zero input as the full amplitude-estimation unitary. Reason: A is part of the algorithm in the specification; I treated it as part of the operation rather than as input-state preparation.
- eq_2: The overall -1 in Q is applied as a phase gate on the control qubit per controlled-Q use, rather than as a global phase on the body. Reason: A global phase becomes a relative phase once Q is controlled, so it must be explicit.
- eq_5: The inverse QFT is QFTGate(t).inverse() on the counting qubits in increasing index order, with no hand-built factorized QFT or extra swap handling. Reason: QFTGate includes the bit-reversal swaps, which gives the little-endian weight convention.
- eq_4, eq_5: Measurement and the postprocessing for y and p_hat are omitted. Reason: The task requires a measurement-free operation.
- eq_1, eq_2, eq_3: The counting register is capped at t<=8, and n>=1. Reason: This keeps circuit size (2^t-1 controlled-Q repetitions) bounded.
