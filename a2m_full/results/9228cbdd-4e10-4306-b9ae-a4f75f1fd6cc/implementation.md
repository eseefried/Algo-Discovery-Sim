# Equation to Qiskit

Qiskit circuit for T steps of the assumed memory-coupled coined quantum walk on an N-cycle (N a power of two, 4 <= N, at most 12 qubits in total). Each step U = S (I_pos ⊗ C(p)) applies C(p) = SWAP_{c,m} CX_{m->c} (Ry(pi p/8) on coin), then a coin-controlled mod-N shift on the position register (coin 0 gives +1, coin 1 gives -1), built from multi-controlled X ripple incrementer and decrementer gates. The circuit is an operation only. State preparation, probability marginals, time averaging and TV distance are left to the runner.

Source equation run: `20ca5bfd-dca3-42c0-bbc4-1833c24fb52f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qiskit qubit indices are little-endian; qubits 0..n-1 = pos (position x, bit i of x on qubit i), n = log2(N)
- qubit n = coin (direction: 0 gives +1, 1 gives -1)
- qubit n+1 = mem (memory qubit)
- Example N=4: n=2, so qubits 0,1 = pos, qubit 2 = coin, qubit 3 = mem (4 qubits)

## Assumptions

- One memory qubit and the guessed C(p) of eq_2
- Linear map theta = pi p / 8
- Shift is +1 for coin 0 and -1 for coin 1, mod N
- N is a power of two so that the binary incrementer wraps mod N
- The runner supplies the initial state, e.g. all-zero for |0>_x|0>_c|0>_m
- The runner does the time averaging over steps t=0..T-1 by building circuits with different `steps`

## Unresolved issues

- The actual recycled-coin operator and its p dependence are unknown
- The exact meaning of the 0 to 8 range of the memory parameter is unknown
- The other memory-based walk and the proven relation to it are not addressed
- Non-power-of-two cycle sizes such as N=5, 6, 7 are not implemented
- Which p values give non-uniform behavior is not determined here

## Equation mapping

- `eq_1`: implemented; _theta. Assumed linear map theta = pi p / 8 used as the Ry angle.
- `eq_2`: implemented; _coin_step. Assumed coin-memory unitary: ry on coin, then cx with memory as control and coin as target, then swap of coin and memory.
- `eq_3`: implemented; _shift and build_circuit. Each step applies C(p) then the coin-controlled mod-N shift, repeated for `steps` steps to give U^t. The initial state |0>|0>|0> is not prepared inside the circuit; the runner supplies inputs, and the all-zero default matches it.
- `eq_4`: out_of_scope; no code location. Position marginals and the classical time average are post-processing of statevector probabilities, not part of the unitary operation.
- `eq_5`: out_of_scope; no code location. The total variation distance from uniform is classical post-processing.
- `eq_6`: background; no code location. Fourier block decomposition is an analytic tool for understanding the walk. It is not a circuit construction here.

## Specification changes

- eq_3: The cycle size N is restricted to powers of two (N>=4, with n+2<=12 qubits in total). Non-power-of-two N would need a modular incrementer with invariant unused states and is not implemented. Reason: A plain binary incrementer wraps mod 2^n, which is exact only for power-of-two N.
- eq_3: The circuit has the integer parameter `steps` (0..512) and applies U^steps. The initial state is excluded from the operation. Reason: build_circuit must return an operation without input-state preparation. The runner prepares the input and averaging over t is done classically.
- eq_4, eq_5: Time averaging and TV distance are not implemented in the circuit. Reason: They are classical post-processing and the module may contain no simulation or measurement.
- eq_2: The operator product is read right-to-left as circuit order: Ry on coin, then CX(mem->coin), then SWAP(coin,mem). Reason: This matches the standard operator-product convention for the stated formula.
- eq_1, eq_2: The angle map and coin unitary remain unverified assumptions about the paper's recycled-coin operator and are not claimed to be the paper's exact operator. Reason: The abstract does not define the coin operator or its dependence on p.
