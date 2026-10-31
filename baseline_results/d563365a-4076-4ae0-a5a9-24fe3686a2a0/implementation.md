# Equation to Qiskit

Qiskit module implementing the query-model upper-bound construction for the Unitary Permutation problem: a single sigma-independent circuit reads a permutation register |sigma>, and makes exactly L=|w| black-box calls following a Karp all-permutations-supersequence word w (default 1213121 for n=3, L=7=n^2-2n+4). For each call j the activity bit a_j(sigma) (greedy leftmost embedding) is computed into an ancilla by multi-controlled X gates, the data qubit is swapped with the dummy qubit of symbol w_j when inactive, U_{w_j} is applied once to the data wire, and the routing and ancilla are uncomputed. Black boxes are supplied as u(theta,phi,lam) single-qubit gates. Only n in {2,3} fits the 12-qubit cap (n=3 uses 10 qubits).

Source equation run: `fc0cf9d5-d7ed-441f-8a84-275a5537d5f5`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Total 10 qubits for the example (n=3, b=2).
- q[0..5] = C (permutation register): block k=0 -> q[0] (LSB), q[1] stores sigma(1)-1; block k=1 -> q[2], q[3] stores sigma(2)-1; block k=2 -> q[4], q[5] stores sigma(3)-1. Unchanged by the circuit.
- q[6] = D (data qubit); receives U_sigma = U_{sigma(3)} U_{sigma(2)} U_{sigma(1)}.
- q[7] = A_1 (dummy for gate 1, m_1=4), ends in U_1^3|0>; q[8] = A_2 (dummy for gate 2, m_2=2), ends in U_2|0>; no dummy for gate 3 (m_3=1).
- q[9] = t (activity ancilla), starts and ends in |0>.
- Example: sigma=(3,2,1) is encoded as sigma(1)-1=2 -> q[1]q[0]=10, sigma(2)-1=1 -> q[3]q[2]=01, sigma(3)-1=0 -> q[5]q[4]=00; the circuit then applies U_1 U_2 U_3 to q[6] (calls 4,6,7 active).

## Assumptions

- sigma is supplied as a computational-basis state (or superposition) of register C; non-permutation basis states of C are not rejected and simply follow whatever routing the circuit defines for them.
- Black-box calls are plain u gates on the data wire; controlled-SWAP and multi-controlled X on the control register are free (not counted as queries).
- Dummy and ancilla qubits are provided in |0> by the runner.
- The 'word' key is optional; when absent the default Karp word for n=2 or n=3 is used.

## Unresolved issues

- The paper's own circuit and ancilla scheme are not known from the abstract; the dummy-register routing construction is the reconstruction agent's realisation of the Karp connection.
- The quantum-switch construction (n log2 n + Theta(n)) and the query lower bound with its 'additional assumption on the family of gates' are not implemented.
- Multi-controlled X gates with up to 6 controls are left to Qiskit synthesis; the circuit is not depth-optimised.

## Equation mapping

- `eq_1`: implemented; module docstring and build_circuit main loop (ordered active calls realise U_{sigma(n)}...U_{sigma(1)} on D). The composite is produced on the data qubit by the n active calls in order sigma(1),...,sigma(n).
- `eq_2`: implemented; build_circuit. Single sigma-independent circuit controlled by register C; ancillas t returned to |0>, dummies end in sigma-independent |g>.
- `eq_3`: implemented; DEFAULT_WORDS, _greedy_embedding check in build_circuit. Word w with the all-permutations-subsequence property is used as the query schedule; property validated at build time, ValueError otherwise.
- `eq_4`: implemented; _greedy_embedding, flags list in build_circuit, _activity. Greedy leftmost embedding defines a_j(sigma); G_j routing realised by activity bit plus controlled swaps.
- `eq_5`: implemented; _activity (T_j) and _routed_call (CSWAP^{t=0}, U_{w_j} on D, CSWAP^{t=0}). T_j implemented as projector-controlled X (mcx with X-conjugated controls) for each sigma with a_j=1; routing via cswap controlled on t=0; one u gate per call.
- `eq_6`: implemented; build_circuit main loop over word. W = G_L...G_1 with exactly |w| black-box calls; dummy registers only created for symbols with m_i>=2.
- `eq_7`: implemented; DEFAULT_WORDS[3] and example_instance_json. n=3, w=1213121, L=7, registers C(6), D(1), A_1, A_2, t.
- `eq_8`: background; no code location. Quantum switch definition is background; the switch-model construction is out of the implemented scope.

## Specification changes

- eq_3, eq_7: Only n in {2,3} can be built: n=4 needs at least 8 control + 1 data + 3 dummy + 1 ancilla = 13 qubits, over the 12-qubit cap. For n=2 the default word is 121 (length 3), shorter than the formula n^2-2n+4=4, which is stated for n>=3. Reason: Qubit cap and the fact that at least three symbols must repeat in any n=4 supersequence.
- eq_4, eq_5: For a symbol occurring exactly once in w the call is applied directly to D without ancilla or routing, since a_j(sigma)=1 for every sigma. T_j is realised as a sum over active sigma of multi-controlled X gates (not a minimised Boolean circuit). Embedding positions are 0-based in code. Reason: Simplification preserving the operator exactly; multi-controlled X is the straightforward reversible realisation of T_j.
- eq_2, eq_7: Control encoding fixed explicitly to Qiskit little-endian: block k occupies indices [k*b,(k+1)*b) with the lowest index as LSB of sigma(k+1)-1; the spec's 'block 1 leftmost' ket-string convention is replaced by this index convention. Reason: Qiskit index 0 is the least significant bit; an explicit layout is required.
- eq_1: Black-box gates are concretised as single-qubit u(theta,phi,lam) gates supplied via the instance (d=2). Reason: A buildable circuit requires explicit gates; opaque dense unitaries are disallowed.
