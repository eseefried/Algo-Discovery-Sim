# Equation to Qiskit

Mixed-radix QFT on a hybrid register of one qutrit (levels 0,1,2 stored in 2 qubits, level 3 unused) and m qubits, total dimension N=3*2^m (N=12 for m=2). The circuit applies the qutrit DFT H_3, built from two-level rotations. Then it applies a generalized controlled phase exp(2*pi*i*k1*j0/N) between the qutrit and the qubit register, and finally a QFTGate on the qubit register. This is the Cooley-Tukey factorization of F_N, so the output digits are ordered k = k1 + 3*k2.

Source equation run: `7613470c-049f-478a-b2f2-9d7af12d7f98`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: qutrit low bit (level = q0 + 2*q1; levels 0,1,2 used, level 3 unused)
- qubit 1: qutrit high bit
- qubits 2..m+1: qubit register x, little-endian (qubit 2 is the least significant bit)
- Input index j = 2^m*j1 + j0, with j1 in the qutrit and j0 in the register
- Output index k = k1 + 3*k2, with k1 in the qutrit and k2 in the register
- Example m=2: 4 qubits, N=12

## Assumptions

- The generalized Hadamard is the DFT matrix with omega=exp(+2*pi*i/3).
- The qutrit is the most significant digit of the input index.
- Level encoding is level = q0 + 2*q1.
- Qubit register values are little-endian.
- Gate decompositions use only standard gates (cx, ch, cz, cp, cry, x, QFTGate).

## Unresolved issues

- The paper's exact decomposition and gate ordering are unknown.
- The qutrit-to-qubit embedding used by the NMR emulator is unknown.
- The output digit ordering differs from natural-order F_12 and may need a permutation to match the paper.
- The behavior on the unused qutrit level 3 is a free choice.
- The implementation has not been simulated or verified.

## Equation mapping

- `eq_1`: implemented; build_circuit (whole factorized circuit; QFTGate on register qubits). F_N with N=3*2^m is factorized as H_3 on the qutrit, then a controlled phase, then F_{2^m} on the register. Since j1*k2 is an integer, that term drops out. The result equals F_N up to the output digit ordering k=k1+3*k2.
- `eq_2`: implemented; _qutrit_dft. H_3=F_3 (omega=e^{+2 pi i/3}) is embedded in the 2-qubit space on levels 0..2 and decomposed into controlled two-level rotations and phases. Level 3 is left fixed. The qubit Hadamards H_2 are not applied explicitly; they are inside QFTGate.
- `eq_3`: implemented; build_circuit (cp loop after _qutrit_dft). The qutrit-register phase exp(2 pi i k1 j0/(3*2^m)) is applied as cp(theta*2^i) on the qutrit bits weighted 1 and 2 for each register qubit i. Here d=3 and d'=2^m.

## Specification changes

- eq_1: The circuit implements F_N up to a fixed digit reordering: the output is stored as k=k1+3*k2 (qutrit holds k1, register holds k2) rather than in natural mixed-radix order. The mixed-radix output permutation is not applied. Reason: The Cooley-Tukey factorization naturally yields this order. Natural order would require a modular-arithmetic permutation that the abstract does not specify.
- eq_2, eq_3: The qubit-only part of the spec (H_2 on each qubit plus controlled phases between qubits, plus swaps) is replaced by a single QFTGate(m) on the register, which includes its own bit reversal. m is variable (1..10). Reason: This is an equivalent standard implementation of the 2^m-dimensional QFT. The abstract gives no decomposition for it.
- eq_2: The qutrit is encoded in 2 qubits as levels 0,1,2 with level 3 unused. H_3 acts as identity on level 3. The controlled phase treats level 3 as k1=3 (phase 3*theta), and the register QFT acts regardless of the qutrit level. The operation is therefore unitary on all 2^(m+2) states, but the level-3 subspace is outside the specified domain. Reason: A 3-level system cannot fill a 2-qubit space. The spec also leaves the emulator embedding unspecified.
- eq_1, eq_2, eq_3: Scope is narrowed to the unitary QFT operation only. NMR pulses, selective rotations, measurement, tomography and fidelity analysis are omitted. An optional 'inverse' flag is added. Reason: The task requires a measurement-free, unitary operation. Experimental details are not given.
