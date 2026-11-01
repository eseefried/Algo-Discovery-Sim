# Equation to Qiskit

Gate-level Grover search on n qubits (default n=4, N=16, marked state w=5, k=3 iterations). The unitary starts with H on every qubit, then repeats k times: a phase oracle X^{wbar} MCZ X^{wbar}, a diffusion operator H X MCZ X H with a global phase of pi, and an optional second-neighbour RZZ layer with angle phi/2. It is measurement-free and contains no state preparation. The pulse-level spin-chain Hamiltonian, Rabi-frequency scan and fidelity tracking are not implemented.

Source equation run: `4c151187-c0c5-47a7-987c-0262a8d32b91`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0 = qubit index 0 = least significant bit of x (spin 0)
- q1 = qubit index 1 (spin 1)
- q2 = qubit index 2 (spin 2)
- q3 = qubit index 3 = most significant bit (spin 3)
- All qubits are data qubits; there are no ancillas. Encoding is little-endian: x = sum_j x_j 2^j, and the circuit is applied to |0000>.

## Assumptions

- The runner prepares |0...0> and applies the circuit, so the Hadamard layer inside the circuit creates |s>.
- Little-endian encoding: qubit 0 is the least significant bit of the marked integer w.
- There is a single marked state, supplied explicitly as the integer w.
- Nearest-neighbour Ising terms are omitted. phi=0 gives the ideal Grover algorithm.
- Allowed instance keys are n, w, k and phi. Any other key raises ValueError.

## Unresolved issues

- The actual spin-chain Hamiltonian parameters, pulse sequences, Rabi-frequency scan and 2πk-condition maxima are not reproduced.
- The marked state used in the original work is unknown, so w=5 is an arbitrary default.
- mcx on n-1 controls is left to Qiskit's default synthesis, so the gate count for larger n is not optimised.

## Equation mapping

- `eq_1`: implemented; build_circuit: initial loop applying H to all qubits. The Hadamard layer is the first part of the built unitary, so acting on |0..0> it yields the uniform superposition |s>.
- `eq_2`: implemented; build_circuit: Grover loop (oracle block, then diffusion block). One Grover iteration G = D O_w is compiled from the explicit marked integer w.
- `eq_3`: implemented; _mcz and the oracle and diffusion blocks in build_circuit. The oracle is X on the zero bits of w, then MCZ (H, mcx, H), then X again. The diffusion is H X MCZ X H plus a global phase of pi, so it equals D exactly.
- `eq_4`: implemented; build_circuit: k_default computation. The default iteration count is round(pi/4 sqrt(N) - 1/2), which is 3 for N=16, and k can be overridden. The success probability sin^2((2k+1)theta) is a property of the result and is not built into the circuit.
- `eq_5`: implemented; build_circuit: 'if phi != 0' block with qc.rzz. The optional ZZ layer after each G is implemented as rzz(phi/2, j, j+2) for j in 0..n-3, which gives exp(-i phi Z_j Z_{j+2}/4). The fidelity F_t is computed outside the circuit by the runner and is not built in.

## Specification changes

- eq_1, eq_2, eq_3, eq_4, eq_5: The construction is generalised from fixed n=4 to a parameter n in 2..12, with defaults n=4, w=5 (5 mod N if n<3), k=round(pi/4 sqrt(N)-1/2) and phi=0. The ZZ layer runs over j=0..n-3, which is j=0,1 for n=4. Reason: The task asks for the operation to work for varying valid parameters. The defaults reproduce the specified 4-qubit, k=3 instance.
- eq_3: A global phase of pi is added to each diffusion block so that it equals D exactly rather than up to a global phase. Reason: This makes the unitary exactly G^k. It has no observable effect.
- eq_5: The fidelity F_t is not computed in the circuit, and the ZZ error layer is the proposed simplification rather than the paper's Hamiltonian model. Reason: The circuit must be measurement-free and unitary. The abstract gives no coupling values, pulse sequences or nearest-neighbour terms.
- eq_4: The iteration count rounds with floor(x+0.5) rather than Python's round(), and k can be overridden by the instance. Reason: This avoids banker's rounding. For n=4 it gives the specified k=3.
