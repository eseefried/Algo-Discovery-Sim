# Equation to Qiskit

Implements the diagonal bipartite gate U = sum_{j,k} exp(i phi_jk)|jk><jk| on two n-qubit registers (N = 2^n), with the phases supplied as an N x N matrix (the matrix A, as angles) or a flat list of length N^2. The diagonal is synthesized exactly from a Walsh-Hadamard (parity) expansion of the phases, using CX ladders and RZ gates plus a global phase. The auxiliary state rho and its entropy are classical post-processing and are not part of the circuit.

Source equation run: `69ee6693-bf0f-4ef1-be91-916bad820143`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0..n-1: register B_k, little-endian bits of column index k
- qubit n..2n-1: register A_j, little-endian bits of row index j
- computational basis index x = j*N + k, N = 2^n; for the N=2 example: qubit 0 = k, qubit 1 = j
- U acts as exp(i*phases[j][k]) on |j>|k>

## Assumptions

- N is a power of two, so each subsystem is n = log2 N qubits.
- Row-major reshaping: diagonal index x = j*N + k, with k on the low (least significant) qubits.
- Phases are provided as real angles, either an N x N matrix or a flat list of length N^2.
- The global phase is tracked via the circuit global_phase (the S=0 Walsh coefficient).

## Unresolved issues

- The exact relation between entangling power and S(rho) is not in the specification, so no entangling-power circuit was built.
- Moment formulas, the Borel-triangle conjecture and the mean-entropy result are not implemented because they are analytic results.
- The circuit uses O(N^2) parity rotations with CX ladders, so it is not gate-efficient for larger N.

## Equation mapping

- `eq_1`: implemented; build_circuit (diagonal gate, row-major index x=j*N+k) with _parse (reshape of phases into A) and _wht. Gate diag(exp(i phi_jk)) is synthesized exactly via a Walsh-Hadamard parity expansion; the phases are given as inputs (the runner or caller may draw them i.i.d. uniform).
- `eq_2`: background; no code location. rho = A A^dagger / N^2 is classical post-processing of the phases and is not part of the circuit.
- `eq_3`: background; no code location. Property of unimodular A (rho_jj = 1/N); no circuit operation corresponds to it.
- `eq_4`: background; no code location. Von Neumann entropy is a classical quantity, not implemented in the circuit.
- `eq_5`: out_of_scope; no code location. The N=2 illustration has a garbled rho_12 expression. It is only usable as an input instance (N=2 and phases), and the entropy computation is outside the circuit.

## Specification changes

- eq_5: The printed rho_12 expression is not used. With A=[[1,e^{ia}],[e^{ib},e^{ic}]], the correct element is rho_12 = (A A^dagger)_{12}/4 = (e^{-ib}+e^{i(a-c)})/4, which the abstract spec already states as the replacement. No circuit code depends on it. Reason: The latex in eq_5 is internally inconsistent and the circuit does not need rho.
- eq_1: Narrowed scope to implementing only the diagonal gate U, with the phases supplied as input rather than sampled inside the circuit. N is restricted to powers of two with 2*log2(N) <= 12, i.e. N <= 64. The matrix A is represented by its phase-angle matrix. Reason: The circuit must be a deterministic unitary operation for a given instance, and qubit registers require N = 2^n.
- eq_2, eq_3, eq_4: The auxiliary state, the entropy and the entangling-power relation are not built into the circuit, which only implements U. Reason: These are classical post-processing steps. The exact relation between entangling power and S(rho) is missing from the specification.
