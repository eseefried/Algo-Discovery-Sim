# Equation to Qiskit

Implements the exact bit-flip oracle U_f (instance f = OR_n, optionally any f given as a truth table) via the diagonalisation U_f = (I x H_y) D_f (I x H_y), D_f|x,y> = (-1)^{y f(x)}|x,y>, with D_f expanded as a product of commuting parity-phase factors exp(i a_S chi_S(z)) obtained from the Walsh transform of pi*y*f(x). Each factor is a parity gate (CNOT fan-in into an ancilla, the Hadamard-conjugate of the fan-out gate), an R_Z rotation on the ancilla, and the uncomputing parity gate; ancillas return to |0>. In the fan-out + R_Z model all 2^(n+1) factors commute and can be applied in parallel (constant depth); the generated Qiskit circuit serialises them over a user-chosen small number of ancillas because of the 12-qubit cap, so Qiskit depth is not constant. This is the agent's chosen standard construction, not the paper's (unavailable) MBQC-derived one.

Source equation run: `1c882199-a71c-423c-8b7e-44a422f3b57e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-2: input register x (n=3); x_j stored on qubit n-j, i.e. x_3 on qubit 0, x_2 on qubit 1, x_1 on qubit 2 (Qiskit bitstring of the register reads x_1 x_2 x_3); for function=truth_table the index i has bit q equal to the value of qubit q
- qubit 3: target y, receives y XOR OR_3(x)
- qubits 4-5: ancillas a (num_ancilla=2), must be supplied in |0>, returned to |0>
- total 6 qubits; Qiskit index 0 is the least significant bit

## Assumptions

- Ancilla qubits are supplied in |0> by the runner; they are returned to |0> by construction.
- Bit-flip (XOR) oracle convention, as in eq_1.
- Walsh coefficients with |a_S| <= 1e-12 are treated as zero and skipped (for OR_n all 2^(n+1) coefficients are nonzero).
- The parity gate (CX fan-in into an ancilla) is taken as the Hadamard-conjugate of the fan-out gate eq_2, so the construction lives in the abstract's elementary gate set.

## Unresolved issues

- The actual MBQC-to-circuit equivalence and the paper's specific pattern/circuit are not reconstructed; the implemented construction only shares the exactness and fan-out-model constant-depth property.
- Gate count is 2^(n+1) parity-phase factors (exponential in n); acceptable for n <= 10 within the 12-qubit cap but not a scalable circuit-model implementation.
- Qiskit depth of the returned circuit grows with n; the constant-depth claim eq_6 can only be checked by counting fan-out-model layers, which the emitted circuit does not expose.

## Equation mapping

- `eq_1`: implemented; build_circuit (H on y, diagonal D_f via parity-phase factors, H on y); docstring of build_circuit. Bit-flip oracle realised as (I x H_y) D_f (I x H_y) with D_f|x,y> = (-1)^{y f(x)}|x,y>; ancillas are uncomputed so the action on (x,y) is exactly |x>|y xor f(x)>.
- `eq_2`: implemented; build_circuit, loop commented 'eq_2 (parity gate = H-conjugated fan-out)'. The parity gate z.S -> ancilla is implemented as a CNOT fan-in from the qubits in S into an ancilla; it is the Hadamard-conjugate of F_m. In Qiskit it is a sequence of CX gates, which is depth |S| rather than the depth-1 elementary fan-out of the abstract's model.
- `eq_3`: implemented; build_circuit, qc.rz(-2.0 * c, anc[t]). Arbitrary Z rotation on the parity ancilla; rz(-2a) = diag(e^{ia}, e^{-ia}) implements exp(i a_S chi_S) exactly (phase convention differs from eq_3's diag(1,e^{i theta}) by a global phase, which is tracked exactly).
- `eq_4`: implemented; _truth_table (function == 'or'). OR_n truth table: 0 only for the all-zero input, 1 otherwise, exactly 1 - [|x| = 0].
- `eq_5`: background; no code location. The Hamming-weight phase primitive is not used; the chosen construction uses parity phases chi_S(z) (Walsh expansion) instead of Hamming-weight phases.
- `eq_6`: background; no code location. The constant-depth claim is the paper's theorem; the chosen construction is constant depth only in the fan-out + R_Z model with 2^(n+1) parallel parity ancillas. The generated Qiskit circuit serialises the commuting factors over num_ancilla ancillas and has non-constant gate depth, so eq_6 is not realised as a depth property of the emitted circuit.

## Specification changes

- eq_1, eq_6: The paper's MBQC-derived constant-depth construction is unavailable; replaced by a standard construction: diagonalise U_f by Hadamards on the target, expand the diagonal (-1)^{y f(x)} into 2^(n+1) commuting parity-phase factors via the Walsh transform of pi*y*f(x), each realised by parity gate + R_Z + uncompute. Reason: Only the existence claim is given in the abstract; this construction is exact and is constant depth in the fan-out + R_Z model (all factors commute and can be parallelised on 2^(n+1) ancillas), matching the abstract's model, but it is not claimed to be the paper's method.
- eq_6, eq_2: Depth is NOT constant in the emitted Qiskit circuit: factors are serialised in batches over num_ancilla (1..11-n) ancillas, and each parity gate is a CX cascade (depth |S|) instead of a depth-1 fan-out/parity gate. Reason: 12-qubit cap forbids 2^(n+1) parallel ancillas; Qiskit has no depth-1 unbounded fan-out primitive.
- eq_1, eq_4: Oracle generalised: besides function='or' (the scoped instance), an explicit truth table for any f:{0,1}^n->{0,1} is accepted via function='truth_table'. Reason: The same Walsh/parity-phase construction applies verbatim to arbitrary f, covering the abstract's general-f statement at no extra cost; default remains OR_n.
- eq_3: R_Z realised as qc.rz(-2a) = diag(e^{ia}, e^{-ia}) rather than diag(1, e^{i theta}); the S = empty-set coefficient is applied as qc.global_phase. Reason: This makes the product of factors equal exp(i pi y f(x)) exactly (not merely up to global phase).
- eq_1: Register ordering fixed: qubits 0..n-1 hold x (x_j on qubit n-j), qubit n is y, qubits n+1.. are ancillas; truth-table index uses Qiskit little-endian bit q = qubit q. Reason: The specification left the physical qubit order unspecified; the choice makes the register bitstring read as x_1...x_n.
