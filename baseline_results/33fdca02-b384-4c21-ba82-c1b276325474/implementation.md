# Equation to Qiskit

Implements the Bernstein-Vazirani operation of the specification for an arbitrary n-variable Boolean function f supplied as a truth table (or a named function). The circuit acts on n input qubits (qubit j-1 carries x_j / output bit y_j) plus one ancilla qubit (index n) which the runner must prepare in |1>. Sequence: H on all n+1 qubits, bit-flip oracle U_f built from the algebraic normal form (Reed-Muller/Mobius transform) of f as a product of multi-controlled X gates onto the ancilla, then H on the n input qubits. The output state on the input register is sum_y fhat(y)|y>, so a computational-basis measurement (done by the runner) gives y_i=1 with probability Inf_i(f). Example instance is n=2, f=AND (truth table [0,0,0,1]) whose oracle reduces to a single Toffoli gate.

Source equation run: `24e3f6e3-848b-4cd6-b82a-13e66f05a95e`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: input x_1 (output bit y_1), register 'x'[0]
- qubit 1: input x_2 (output bit y_2), register 'x'[1]
- qubit 2: oracle ancilla 'anc'[0]; runner must prepare it in |1> (turned into |-> by the first Hadamard layer)
- Truth table index k = x_1 + 2*x_2 (little-endian, x_1 on qubit 0); [0,0,0,1] is f = x_1 AND x_2, whose ANF has the single monomial x_1 x_2 so the oracle is one Toffoli (mcx) with controls qubits 0,1 and target qubit 2
- Expected after the operation on |00>|1>: input register in (1/2)(|00>+|01>+|10>-|11>), each y_i = 1 with probability 1/2 = Inf_i(AND)

## Assumptions

- f is supplied classically as a full truth table of length 2^n (or as one of the named functions and/or/parity/majority/constant0/constant1); the oracle is the standard bit-flip oracle.
- Runner prepares the ancilla (qubit n) in |1> and the input register in |0^n>; if the ancilla is left in |0> there is no phase kickback and the input register returns to |0^n>.
- Multi-controlled X gates (qc.mcx) are acceptable standard-library gates; their decomposition is left to the transpiler.
- Qubit cap 12 implies 1 <= n <= 11.
- The paper's 'dependence degree' is identified with the standard influence Inf_i(f) = Pr_x[f(x) != f(x xor e_i)].

## Unresolved issues

- The paper's exact approximation algorithm, error guarantee and query complexity are unknown; only the single-run circuit whose output marginals equal the influences is implemented.
- Junta analysis and probabilistic learning algorithms from the paper are not implemented.

## Equation mapping

- `eq_1`: implemented; _append_oracle and _anf_monomials: U_f realised as X / CX / MCX gates onto the ancilla, one per monomial of the algebraic normal form of f. Bit-flip oracle |x>|b> -> |x>|b xor f(x)>; with the ancilla in |-> this gives the (-1)^{f(x)} kickback.
- `eq_2`: implemented; build_circuit: Hadamard layer on all n+1 qubits, oracle, Hadamard layer on the n input qubits (comments 'eq_2 step 1/2/3'). Produces sum_y fhat(y)|y>|-> on the registers when the runner supplies |0^n>|1>.
- `eq_3`: background; no code location. Born-rule output distribution Pr[y] = fhat(y)^2 and the marginal Pr[y_i=1] = Inf_i(f); this is the property of the state produced by build_circuit, verified by the runner's measurement, not a gate sequence.
- `eq_4`: background; no code location. Classical combinatorial definition of influence; used only to interpret the measurement statistics.
- `eq_5`: out_of_scope; no code location. Repetition over T runs and the frequency estimator with Hoeffding bound are classical post-processing/experiment control, not part of the unitary operation.
- `eq_6`: implemented; example_instance_json {n: 2, truth_table: [0,0,0,1]}; _anf_monomials yields the single mask 0b11 so _append_oracle emits one mcx (Toffoli). Tiny AND instance: Toffoli oracle, uniform output distribution, Pr[y_1=1] = Pr[y_2=1] = 1/2.

## Specification changes

- eq_2, eq_6: The initial state |0^n>|1> (including the ancilla |1>) is not prepared inside the circuit; the runner must supply it. The circuit begins with the Hadamard layer that turns |1>_anc into |->. Reason: The generated module must be an operation without input-state preparation.
- eq_3, eq_5: No measurement or repetition is included; the circuit stops after the final Hadamard layer on the input register. Reason: Measurement-free unitary operation is required; sampling and estimation are performed by the runner.
- eq_1: The abstract oracle U_f is concretely realised as the XOR of multi-controlled Toffoli gates following the algebraic normal form (Mobius transform) of the user-supplied truth table. Reason: Opaque dense unitaries are disallowed; the ANF decomposition gives an exact gate-level bit-flip oracle for any f.
- eq_2: Index convention fixed: specification position j (x_j, y_j) is Qiskit qubit j-1, and truth tables are indexed with x_1 as the least significant bit. Reason: Qiskit qubit 0 is the least significant bit; a convention had to be chosen and is disclosed.
