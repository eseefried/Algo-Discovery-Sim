# Equation to Qiskit

Builds the operation (W^k O)^T for a coined discrete-time quantum walk on a cycle of N=2^n vertices with a 1-qubit coin. O is a phase-flip oracle on one marked vertex, applied once per iteration. W is a coin step followed by a coin-controlled increment or decrement shift mod N. The initial state and the measurement are left to the runner.

Source equation run: `6e3cb61a-de9a-4447-8f27-dd4b1564250e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: vertex register, little-endian integer v=sum_i b_i 2^i (qubit 0 is least significant)
- qubit n: coin qubit (1 = step +1, 0 = step -1 mod N)
- example (n=3): vertex = qubits 0,1,2; coin = qubit 3; 4 qubits total
- no flag ancilla is used

## Assumptions

- The circuit's qubit count is n+1, with n between 1 and 11, so it stays within the 12-qubit cap.
- The marked vertex is an integer in 0..2^n-1 and is validated.
- k and T are integers in [1,200] with k*T at most 2000. This is an implementation limit I chose.
- The oracle is a phase-flip placeholder with a single marked vertex, one use per iteration, and acts as identity on the coin.
- The example uses the Hadamard coin to avoid the trivial X-coin walk.

## Unresolved issues

- The paper's exact walk (Szegedy vs coined) and graph family are unknown.
- The exact relation between k, the spectral gap and the oracle strength is not resolved.
- The cubic speedup is not expected to show at tiny N, and this circuit does not demonstrate it.
- The torus and 2-qubit coin variant is not implemented.
- The runner's query budget and the final choice of k and T are unspecified.

## Equation mapping

- `eq_1`: implemented; _oracle. The phase flip I-2|m><m| on the vertex register is built from X conjugation and a multi-controlled phase (Z for n=1). The coin is untouched. It is applied once per iteration.
- `eq_2`: implemented; _walk_step and _shift. A coin step is followed by a coin-controlled shift. The shift is an increment (coin=1) or decrement (coin=0) mod 2^n, built from multi-controlled X ladders. The 1-qubit Grover coin reduces to X; an optional Hadamard coin is available.
- `eq_3`: implemented; build_circuit (loop over T iterations of O then k walk steps). The operator (W^k O)^T is implemented. The initial uniform state is prepared by the runner, not by this circuit.
- `eq_4`: out_of_scope; no code location. This is a heuristic for choosing k and T. Both are caller-supplied instance parameters and are not derived in the circuit.
- `eq_5`: background; no code location. The success probability is a Born-rule measurement on the vertex register, which the runner performs. The circuit has no measurements.

## Specification changes

- eq_3: The circuit omits the initial-state preparation H^{⊗n}|0>|s_c> and implements only the operator (W^k O)^T. Reason: The task requires an operation without input-state preparation; the runner prepares inputs.
- eq_2: An optional 'coin':'hadamard' mode replaces the coin reflection by H. The default 'grover' uses X, the 1-qubit Grover reflection. Reason: The spec notes that the 1-qubit Grover coin gives a trivial walk. H is a non-reflection substitute and is not the paper's walk.
- eq_1, eq_2, eq_3, eq_4, eq_5: The scope is narrowed to a cycle graph with 2^n vertices, 1-qubit coin, single marked vertex and no flag qubit. The torus and the 2-qubit coin are not implemented. Reason: The paper's exact walk and graph are unknown, and the torus variant was only optional in the spec.
- eq_4, eq_5: No scan or optimization over T and k is performed in the module. Reason: The module must return a single operation; scanning is left to external software.
