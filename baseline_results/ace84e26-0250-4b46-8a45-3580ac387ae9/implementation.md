# Equation to Qiskit

Qiskit module implementing the single-qudit (Gedik-type) permutation-class algorithm F^dagger U_sigma F for a ququart (d=4 encoded in 2 qubits), generalized to d=2^n with n<=12. The circuit is the operation only: QFT on the register, the dihedral permutation oracle (cyclic shift k->k+m or reflection k->m-k, built from X gates and multi-controlled-X incrementers), then the inverse QFT. Fed with |1>, the ideal output is |1> for shifts and |d-1> (=|3> for d=4) for reflections, up to a global phase.

Source equation run: `3e35e113-7103-4198-8f48-c43e124dea2c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q[0]: least significant bit of the ququart label k; polarization bit p (H=0, V=1) in the photonic encoding
- q[1]: most significant bit of k; spatial-mode bit s, so k = 2*s + p (eq_1)
- Total qubits for the example: 2 (d=4). General instance: n = log2(d) qubits, n <= 12
- Runner input: |k=1> = |q1=0, q0=1>; ideal output |1> (shift class) or |3> = |q1=1, q0=1> (reflection class), up to global phase

## Assumptions

- The experiment's 'parity' means shift class vs reflection class of the dihedral permutations, as in the Gedik-type algorithm.
- Ideal noiseless gates; the linear-optical implementation (wave plates, beam splitters) is out of scope.
- Global phases omega^{-m} / omega^{m} in eq_5 are irrelevant to the measured outcome.
- Multi-controlled X gates (mcx) are synthesized by Qiskit without ancillas; for the d=4 example only cx and x gates occur.

## Unresolved issues

- The abstract does not state which permutations were actually tested experimentally; the example instance uses the reflection sigma^-_0 (k -> -k mod 4).
- Whether the experiment prepared |psi_1> directly or via an explicit QFT stage is unknown; the module includes an explicit QFT stage so the runner can input |1>.

## Equation mapping

- `eq_1`: implemented; module docstring and register layout comment in build_circuit; QuantumRegister(n, 'q') with q[0]=p (LSB), q[1]=s (MSB). Ququart label k = 2s + p is realized by the two-qubit register with Qiskit little-endian ordering, so q[0] carries the polarization bit and q[1] the spatial-mode bit.
- `eq_2`: implemented; build_circuit: qc.append(QFTGate(n), qubits). QFTGate implements |j> -> d^{-1/2} sum_k exp(2 pi i jk/d)|k>, exactly the single-qudit Fourier transform F of eq_2 for d=2^n (omega=i for d=4).
- `eq_3`: implemented; _permutation_oracle, _add_constant, _add_power_of_two. Cyclic shift k->k+m mod d built from multi-controlled-X incrementers; reflection k->m-k mod d built as bitwise complement (X on all qubits, k->d-1-k) followed by addition of m+1 mod d.
- `eq_4`: background; no code location. Eigen/mapping identity of the permutation acting on the Fourier state; it is a derived property of the composed circuit, not a separate gate.
- `eq_5`: implemented; build_circuit: full sequence QFTGate(n), _permutation_oracle, QFTGate(n).inverse(). The returned operation is F^dagger U_sigma F; applied to |1> it yields |1> (shift) or |d-1> (reflection) up to global phase. The computational-basis measurement itself is left to the runner.

## Specification changes

- eq_1: Physical qubit order fixed to Qiskit little-endian: q[0] = polarization bit p (LSB), q[1] = spatial bit s (MSB), consistent with k = 2s + p. Reason: Qiskit index 0 is the least significant bit; QFTGate's convention requires this ordering for eq_2 to hold as written.
- eq_2, eq_3, eq_5: Generalized from d=4 to any d = 2^n with n <= 12 qubits; the ququart instance is d=4 (n=2). Reason: Allows the operation to be built for varying valid parameters as required; the d=4 case is the paper's instance.
- eq_3: Reflection sigma^-_m realized as X on all qubits (k -> d-1-k) followed by addition of (m+1) mod d, instead of a direct 4x4 permutation matrix. Reason: Dense unitaries are disallowed; the decomposition is exactly equal to the permutation k -> m-k mod d.
- eq_5: Input-state preparation of |1> and the computational-basis measurement are excluded from the module; only the unitary F^dagger U_sigma F is returned. Reason: Task requires an operation, not an experiment; the runner supplies inputs and measurements.
- eq_3: Permutation set restricted to the 8-element dihedral family (shifts and reflections), not all 24 elements of S_4. Reason: The single-qudit Fourier-probe algorithm is only deterministic on this family; follows the math-stage scope.
