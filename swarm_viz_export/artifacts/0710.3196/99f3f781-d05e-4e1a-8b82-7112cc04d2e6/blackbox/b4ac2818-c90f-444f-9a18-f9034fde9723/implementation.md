# Equation to Qiskit

Qiskit operation implementing k Grover iterations G = D·O_w on n=4 qubits (little-endian, marked state w), with an optional second-neighbour ZZ phase layer E_phi after each iteration. The initial Hadamard layer is not included because the runner prepares inputs, so the circuit acts on a prepared |s>. The pulse-level spin-chain model and the Rabi-frequency scan are not implemented.

Source equation run: `fafc4ab4-3510-4094-9765-ba410649445f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0..q3 = qubit indices 0..3, little-endian: q0 is the least significant bit of x = sum_j x_j 2^j
- Marked state w: bit j of w is the value on qubit j (w=5 -> q0=1, q1=0, q2=1, q3=0)
- No ancilla qubits; the circuit expects the runner to prepare the input, normally |s> = H^4|0000>

## Assumptions

- The marked state w is an explicit instance parameter, default 5.
- Little-endian encoding: qubit j carries bit j of w.
- The runner prepares the input state, normally the uniform superposition.
- Global phase is tracked in the circuit's global_phase attribute.
- The ZZ error layer is a proposed simplification, not the paper's model.

## Unresolved issues

- The actual spin-chain coupling constants, pulse sequences and marked state of the original work are unknown.
- The Rabi-frequency scan and the 2πk-condition maxima cannot be reproduced at this gate level.
- Nearest-neighbour Ising terms are omitted from the optional error model.

## Equation mapping

- `eq_1`: background; no code location. The uniform initial state H^{⊗4}|0000> is input preparation, which the runner performs. The circuit's diffusion step uses the same |s>, but the state itself is not built in the circuit.
- `eq_2`: implemented; _oracle, _diffusion and the loop in build_circuit. Phase oracle O_w and inversion about the mean D are applied in the order G = D·O_w, repeated k times.
- `eq_3`: implemented; _oracle and _diffusion (with _phase_flip_all_ones). X on the zero bits of w around a multi-controlled Z (mcp with angle pi) gives O_w. H and X layers around a multi-controlled Z give D. A global phase of pi is added so that D is exactly 2|s><s|-I.
- `eq_4`: implemented; default iteration count in build_circuit. The default k = round(pi/4 sqrt(N) - 1/2), which is 3 for n=4, is used unless 'iterations' is given. The success probability formula is analytic and is not part of the circuit.
- `eq_5`: implemented; _zz_layer. The optional second-neighbour ZZ phase layer E_phi is built from RZZ(phi/2) on pairs (j, j+2), applied after each iteration when phi != 0. The fidelity F_t is a post-processing quantity computed outside the circuit and is not implemented.

## Specification changes

- eq_1: The initial H^{⊗4} layer is excluded from build_circuit, so the circuit is G^k acting on a prepared input. Reason: The task requires an operation without input-state preparation. The runner should supply |s>.
- eq_2, eq_3: A global phase of pi per iteration is added so that D is exactly 2|s><s|-I rather than -D. Reason: H^n X^n CCCZ X^n H^n equals I-2|s><s| = -D, as noted in eq_3. The phase makes the unitary match eq_2 exactly.
- eq_2, eq_3, eq_4: The register size n is generalised to a validated parameter (2..12, default 4), and the number of iterations and the marked state w are instance parameters (w default 5, iterations default from eq_4). Reason: The operation must be implemented for varying valid instance parameters. The default n=4 matches the specification.
- eq_5: The E_phi pairs are generalised to (j, j+2) for j=0..n-3. exp(-i phi ZZ/4) is implemented as RZZ(phi/2), and phi defaults to 0 so the layer is omitted. Fidelity tracking is not implemented. Reason: RZZ(theta)=exp(-i theta ZZ/2), so theta=phi/2 gives the stated factor. Fidelity is a simulation quantity, not a circuit element.
- eq_1, eq_2, eq_3, eq_4, eq_5: Scope is narrowed to ideal gate-level Grover with an optional ZZ error layer. The pulse-level nuclear spin chain Hamiltonian, nearest-neighbour couplings, the Rabi-frequency scan and the 2πk condition are not reproduced. Reason: The specification marks the Hamiltonian parameters and pulse sequences as missing information.
