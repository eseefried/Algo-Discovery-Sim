# Equation to Qiskit

Qiskit module implementing the discrete-time multi-step quantum walk search operator U_k^q = (W^k Q_w)^q (eq_3) on an n-dimensional hypercube (N=2^n vertices, degree d=n) with a Grover coin and bit-flip shift (eq_2) and a phase-flip oracle on the marked vertex w (eq_1). The circuit is the bare operation on vertex and coin registers; input-state preparation (uniform superposition) and measurement are left to the runner. Continuous-time comparison (eq_4) and success-probability/speedup analysis (eq_5) are outside the circuit scope.

Source equation run: `0d2a3977-960c-4ecc-870d-a28801d64d9c`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1: vertex register (n=2 qubits), qubit j = bit j of vertex label x in {0,1,2,3}; marked vertex w=0 is |00>
- qubit 2: coin register (m=log2(n)=1 qubit), direction c in {0,1} selects which vertex bit the shift flips
- Total 3 qubits for the example; general instance uses n + log2(n) qubits (n in {2,4,8})
- Expected runner input: uniform superposition H^{(x)3}|000> (eq_3 initial state, not prepared by the module)

## Assumptions

- The graph is the n-dimensional hypercube with bit-flip shift and Grover coin, as chosen in the specification; this is a reconstruction choice, not the paper's graph.
- The multi-step algorithm is formalized as one oracle application followed by exactly k walk steps per counted query, repeated q times.
- The coin register's d=n basis states are all valid directions (n is a power of two), so no padding states exist.
- The uniform initial superposition over vertex and coin registers is prepared by the runner before applying the returned operation.

## Unresolved issues

- The paper's actual graph family, choice of k(N), and runtime scalings are unknown from the abstract; the implemented instance cannot exhibit or test the claimed cubic speedup.
- No simulation or verification was performed here; correctness of the assembled unitary is to be checked by downstream software.

## Equation mapping

- `eq_1`: implemented; _oracle (phase flip I_N - 2|w><w| on the vertex register via X-conjugated multi-controlled Z in _reflect_zero). Oracle Q_w acts on the vertex register only, flipping the sign of all coin states at vertex w; one call per counted query.
- `eq_2`: implemented; _walk_step, _grover_coin, _shift. Grover coin C = 2|s><s| - I built as H^m (I - 2|0><0|) H^m with global phase pi to fix the overall sign; hypercube shift flips vertex bit c controlled on coin value c via mcx with X-conjugated zero controls.
- `eq_3`: implemented; build_circuit main loop (q repetitions of _oracle followed by k _walk_step calls). Implements U_k^q = (W^k Q_w)^q; the uniform initial state |psi_0> is not prepared because inputs are supplied by the runner.
- `eq_4`: out_of_scope; no code location. Continuous-time Hamiltonian search and its Trotter interpretation are comparison-only background in the specification and not part of the chosen discrete-time construction.
- `eq_5`: out_of_scope; no code location. Success probability, query complexity and speedup exponents are measurement/post-processing quantities; the module returns only the unitary operation with no measurement.

## Specification changes

- eq_3: Initial-state preparation (Hadamards for |psi_0>) and the vertex-register measurement were removed from the circuit; the module returns only the operator (W^k Q_w)^q. Reason: Task requires an operation without state preparation or measurement; the runner supplies inputs.
- eq_2, eq_3: Generalized from the fixed N=4, k=2 instance to any hypercube dimension n in {2,4,8} (d=n a power of two), arbitrary marked vertex w, arbitrary k>=1 and q>=0, within a 12-qubit cap. Reason: Requirement to implement the operation for varying valid instance parameters; power-of-two degree keeps the coin register exactly d-dimensional so the Grover coin is exact without padding.
- eq_2: Grover coin realized as -(H^m (I - 2|0><0|) H^m) with qc.global_phase += pi per application to make it exactly 2|s><s| - I rather than its negative. Reason: Circuit-level reflection about |0> yields I - 2|0><0|; the sign is corrected by a tracked global phase so the exact unitary of eq_2 is preserved.
