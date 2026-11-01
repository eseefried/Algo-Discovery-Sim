# Equation to Qiskit

Builds the n-qubit Clifford basis-change circuit U_k (k=0..2^n) of a complete set of 2^n+1 mutually unbiased bases. U_0 is the identity (computational basis). For k>=1, U_k = H^{⊗n} D_a^†, where D_a = diag(i^{x^T M_a x}) and M_a[i][j] = Tr(a·x^(i+j)) is a symmetric GF(2^n) trace form. Differences M_a - M_b are nonsingular mod 2, so the bases are unbiased. The circuit uses only Sdg, CZ and H gates. It replaces the unspecified cyclic generator W with this explicit construction and does not include state preparation or measurement.

Source equation run: `783428f8-11fc-4a85-8e3b-2daaad0aeb90`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0..q(n-1): system qubits, q0 least significant bit (little-endian); outcome j = sum_i b_i 2^i
- No ancillas, no classical bits; example n=3 uses qubits 0,1,2

## Assumptions

- GF(2^n) is built with the hardcoded irreducible polynomials x+1, x^2+x+1, x^3+x+1, x^4+x+1, x^5+x^2+1, x^6+x+1, x^7+x+1, x^8+x^4+x^3+x+1, x^9+x^4+1, x^10+x^3+1, x^11+x^2+1 and x^12+x^6+x^4+x+1.
- The field element a is the integer k-1 read as polynomial coefficients, with bit i the coefficient of x^i.
- Basis vectors are |psi_{k,j}> = U_k^dagger|j> = D_a H^{⊗n}|j> with D_a = diag(i^{x^T M_a x}). Here x_i is bit i of the basis state x, and M_a is lifted to integer entries 0/1.

## Unresolved issues

- The paper's specific cyclic generator W and its entanglement classes are not reproduced.
- The MUB property follows from a Gauss-sum argument and is not verified in the module. The runner should check the overlaps numerically.

## Equation mapping

- `eq_1`: implemented; build_circuit: Sdg/CZ diagonal D_a^dagger followed by H layer, with a = k-1 and M_a from _gf_trace. The MUB condition holds by construction. The binary matrices M_a-M_b = M_{a+b} are nonsingular for a≠b, so the Fourier spectrum of the quadratic phase is flat and every overlap has modulus squared 1/d. The circuit does not check this numerically.
- `eq_2`: implemented; build_circuit: k selects a=k-1 and the circuit U_k. Replaced by a non-cyclic explicit family. k=0 gives the identity, and k=1..2^n gives H^{⊗n} D_{k-1}^dagger. No generator W is used, and the cyclic indexing is not reproduced.
- `eq_3`: background; no code location. Born-rule probabilities come from the runner's measurement after U_k. The module contains no measurement.
- `eq_4`: background; no code location. Classical linear-inversion postprocessing is outside the operation. The module only supplies U_k, from which |psi_kj> = U_k^dagger|j>.
- `eq_5`: background; no code location. This is a parameter-counting identity and needs no circuit.

## Specification changes

- eq_2: The cyclic generator W of the paper is replaced by a finite-field family of Clifford circuits. The phase diagonal is D_a = diag(i^{x^T M_a x}), with M_a the trace form Tr(a x^(i+j)) over GF(2^n). The basis-change unitary is U_k = H^{⊗n} D_{k-1}^dagger. Reason: The abstract does not give W or its CZ graph. This explicit Clifford construction, which also uses only H and CZ plus S-type gates, provably yields a complete MUB set.
- eq_1, eq_2, eq_3, eq_4, eq_5: The scope is narrowed to one circuit U_k, selected by instance, instead of the full tomography protocol. The circuit has no state preparation or measurement. n is allowed from 1 to 12 instead of only 3 or 4. An optional 'inverse' flag returns U_k^dagger. Reason: The task requires a measurement-free unitary operation. The same code serves n=3 and generalizes to other sizes.
- eq_2: The entanglement-class structure of the paper's bases is not reproduced. The generated bases have whatever entanglement structure this construction produces. Reason: The abstract gives no information on the classes.
