# Equation to Qiskit

Implements the fixed-configuration one-step unitaries U_K = S_K (I_N x C) of the dynamic-percolation coined quantum walk on a finite one-dimensional chain (eq_1-eq_3), composed over a user-supplied sequence of edge configurations K_1..K_t, i.e. the circuit is U_{K_t}...U_{K_1} (one Kraus-branch realisation of Phi^t). The reflecting shift S_K of eq_2 is synthesised exactly from standard gates via the identity S_K = (I x X) * prod_{(x,x+1) in K} SWAP(|x,R>,|x+1,L>), each transposition being a CNOT-conjugated multi-controlled X. Sampling of configurations from pi(K), averaging over branches, and the attractor analysis (eq_4, eq_5) are classical tasks for the runner and are not part of the returned operation.

Source equation run: `1c13d7d7-7f1b-453a-8a09-50f0ac39d408`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin register 'coin' (1 qubit), |0> = L, |1> = R (least significant bit of the basis integer 2x+c)
- qubits 1-2: position register 'pos' (n = ceil(log2 N) = 2 qubits for N=4), x = pos[0]*1 + pos[1]*2, i.e. qubit 1 is the least significant position bit, qubit 2 the most significant
- basis state |x,c> of the specification corresponds to Qiskit integer 2*x + c; e.g. the spec initial state |1,R> is integer 3 = |0 1 1> (qubit2 qubit1 qubit0)
- total qubits = n + 1 <= 12, so 2 <= N <= 2048; the example uses 3 qubits
- the runner must prepare the input state (e.g. |1,R>) and supply one circuit per sampled configuration sequence; averaging over sequences estimates Phi^t

## Assumptions

- Dynamic percolation is modelled as i.i.d. Bernoulli(p) edges resampled every step; the circuit itself is agnostic to p and takes the configuration sequence as data.
- Reflecting (coin-flip) rule at broken edges and at both chain ends, open boundary conditions (no wrap-around).
- Coin is applied before the shift in each step.
- Configurations in instance['configs'] are ordered in time, configs[0] = K_1 applied first.
- Multi-controlled X (qc.mcx) with up to 11 controls is synthesised by the runner's transpiler.

## Unresolved issues

- The paper's actual rule at missing edges and its coin/boundary choices for the 1D chain are unknown; a different rule would change the implemented S_K.
- The explicit attractor basis and asymptotic states for the 1D chain (the paper's main result) cannot be reconstructed from the abstract and are left to classical computation via eq_4/eq_5.
- Two-dimensional lattice and Grover-coin results are entirely out of scope.

## Equation mapping

- `eq_1`: implemented; build_circuit (register construction) and module docstring; pi(K) is not sampled in-circuit. Hilbert space C^N (x) C^2 realised as a 1-qubit coin register plus an n-qubit position register with x = sum_k pos[k] 2^k. The Bernoulli(p) product distribution pi(K) is only validated (optional key 'p'); sampling K from it is a classical runner task, the configurations enter via instance['configs'].
- `eq_2`: implemented; _apply_shift and _swap_pair. S_K is synthesised exactly as (I x X) times the disjoint transpositions |x,R> <-> |x+1,L> for every present edge, which reproduces the moving/reflecting rules of eq_2 including reflection at both chain ends.
- `eq_3`: implemented; build_circuit loop (comment 'eq_3: U_K = S_K (I_N x C)') and _apply_coin. For each supplied configuration the circuit applies the coin then S_K, giving U_K; the loop yields the product U_{K_t}...U_{K_1}, one Kraus branch of Phi^t. The convex average over K (the map Phi itself) is not a unitary and is left to classical averaging by the runner.
- `eq_4`: background; no code location. Attractor (intertwining) equations are a classical linear-algebra problem on the 2N x 2N unitaries, not a quantum operation.
- `eq_5`: background; no code location. Asymptotic-state formula is classical post-processing used to predict the long-time limit; it is not implemented in the circuit.
- `eq_6`: implemented; example_instance_json together with _apply_coin ('H') and build_circuit (N=4). The tiny instance parameters N=4 and Hadamard coin are realised by the example instance; p=1/2 is recorded but only used classically; the initial state |1,R> is not prepared because the module returns an operation only.

## Specification changes

- eq_1, eq_3: The random per-step configurations K_s are not drawn inside the circuit; they are supplied explicitly as instance['configs'] (list of N-1 bit lists) and the circuit implements the single Kraus branch U_{K_t}...U_{K_1}. The random unitary map Phi and its iterate Phi^t are obtained by the runner by classically sampling sequences from pi(K) and averaging. Reason: A QuantumCircuit must be a bound unitary operation; a convex mixture of unitaries is not unitary and in-circuit randomness/environment access is disallowed.
- eq_2: S_K is implemented through the algebraic identity S_K = (I x X) * prod_{(x,x+1) in K} SWAP(|x,R>,|x+1,L>), each transposition realised by CNOT conjugation of a multi-controlled X (with X gates for zero controls). Reason: Needed to express the configuration-dependent permutation with standard gates; the identity is exact and reproduces eq_2 case by case.
- eq_1, eq_6: Qubit ordering: the coin is Qiskit qubit 0 (least significant) and the position bits are qubits 1..n, so |x,c> maps to integer 2x+c. This matches |x> (x) |c> with the coin last but differs from reading the register list from the specification's 'position first' description as Qiskit indices. Reason: Qiskit index 0 is the least-significant bit; the layout is disclosed so the runner prepares |1,R> as integer 3 for N=4.
- eq_1: General N >= 2 is accepted (not only powers of two); padding positions x >= N are decoupled from valid positions and merely receive a coin flip each step. Reason: Keeps the operation unitary on the full register while allowing arbitrary chain lengths within the 12-qubit cap (N <= 2048).
- eq_6: The coin may be chosen from {H, X, Y, Z, I}; the example uses H. No input-state preparation is included. Reason: The abstract does not fix the coin; the module returns an operation only, inputs are prepared by the runner.
