# Equation to Qiskit

Implements one explicitly scoped construction from the specification for q = 2: a single exact derivative-based Bernstein-Vazirani step (eq_3 + eq_4) for a fixed index set S. The circuit acts on n variable qubits plus one target qubit: it prepares the target in |-> by gates (X, H), applies H to the free variable qubits (those not in S), then for every A subset of S performs the shift 1_A (X gates on A), one additive query O_p built from the instance's monomial list as multi-controlled X gates onto the target (eq_1/eq_2), an optional phase correction (-1)^{p_known(x)} for already-learned higher-degree monomials (multi-controlled phase pi), and undoes the shift. Finally H (= F_2^{-1}) is applied to the free qubits and the target is returned to |0> by H, X. Starting from |0...0>, the free qubits are predicted to end in the computational basis state encoding the degree-(|S|+1) coefficients c_{S u {i}} for i not in S, with S-qubits and target back in |0> (up to global phase). No measurement is included; recursion over levels, enumeration of the sets S and the classical query p(0) are left to the runner.

Source equation run: `b7c52bc0-1e56-456b-bfb9-fa88c62803d2`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: variable x_1 (in S; held at |0>, shifted by X gates between queries)
- qubit 1: variable x_2 (free; predicted read-out c_{{1,2}} = 1 for the example)
- qubit 2: variable x_3 (free; predicted read-out c_{{1,3}} = 0 for the example)
- qubit 3: target qubit of the additive oracle O_p, prepared in |-> by X,H and returned to |0> by H,X
- Qiskit qubit 0 is the least significant bit; the example polynomial is p = x1 x2 + x2 x3 + x1 + 1 over F_2 (an RM(2,3) codeword), d = 2, S = {1}; from input |0000> the predicted output is |a> with a = (c_{12}, c_{13}) = (1, 0) on qubits 1,2, i.e. basis state with bit 1 set (integer 2), up to global phase.

## Assumptions

- q = 2 (binary field); coefficients are given implicitly as the list of monomials with coefficient 1.
- Variable indices in the instance are 1-based (x_1..x_n) and are mapped to Qiskit qubits 0..n-1; the target qubit is qubit n; total qubits n+1 <= 12.
- The runner supplies the all-zero input state |0>^{n+1}; the circuit then predicts the deterministic output |a> on the free qubits with a_i = c_{S u {i}} (not verified here).
- The additive oracle model |x>|b> -> |x>|b + p(x)> is used; the oracle is built from the instance's full knowledge of p (the runner plays the oracle).
- Multi-controlled X (mcx) and multi-controlled phase (mcp) gates from the Qiskit standard library are acceptable as oracle primitives; they are not opaque dense unitaries.
- Known higher-degree monomials passed in 'known_monomials' are assumed to have coefficient 1 in p (they must appear in 'monomials'); learned coefficients equal to 0 need no correction and are simply not listed.

## Unresolved issues

- The construction (finite differences + exact Bernstein-Vazirani) is the reconstruction's proposal consistent with the abstract's O(n^{d-1}) exact-query claim; the paper's actual algorithm and constants are unknown.
- Non-prime and odd-prime q are not supported (would require qudits and trace characters).
- No simulation or verification has been performed; the predicted output for the example (a = (1,0) on qubits 1,2) is a mathematical expectation, to be checked by the runner.
- The number of mcx controls equals the monomial degree; for large degree and n up to 11 the transpiled depth may be substantial, but correctness does not depend on it.

## Equation mapping

- `eq_1`: implemented; _apply_oracle: the instance's 'monomials' list encodes the coefficients c_M = 1 of the multilinear polynomial; each monomial becomes a multi-controlled X onto the target. The unknown polynomial p is parametrised by its set of monomials with nonzero (=1) coefficient over F_2, exactly as in eq_1 with q = 2.
- `eq_2`: implemented; _apply_oracle (additive oracle O_p) and build_circuit lines 'qc.x(target); qc.h(target)' (preparation of |psi_1> = |->) with the matching uncompute at the end. Additive oracle |x>|b> -> |x>|b + p(x) mod 2> realised by (multi-)controlled X gates; with the target in |-> each query imprints (-1)^{p(x)} on the input register.
- `eq_3`: implemented; build_circuit: loop 'for mask in range(2 ** num_s)' applying X on A, the oracle, the known-part phase correction, and X on A again. Realises D_S p(y) = sum_{A subset S} p(1_A + y) via 2^{|S|} phase queries at shifted inputs; for q = 2 all signs (-1)^{|S|-|A|} equal +1, so a single |-> target state suffices.
- `eq_4`: implemented; build_circuit: the two layers 'for qb in free_qubits: qc.h(qb)' before and after the derivative loop. For q = 2 the qudit QFT F_2 and its inverse are both the Hadamard gate; H^{\otimes m} on the free qubits turns the phase pattern (-1)^{c_S + a.y} into the basis state |a>, giving the coefficients c_{S u {i}} exactly.
- `eq_5`: background; no code location. Asymptotic query complexity statements (classical lower bound, quantum upper bound and optimality) are not circuit constructions; the generated circuit only instantiates one step whose query count is consistent with the O(n^{d-1}) scaling.
- `eq_6`: background; no code location. Query count of the full recursive algorithm; the circuit implements one level-k step for one set S with 2^{|S|} oracle calls (one summand of eq_6). The eq_6 assumption that queries to p - p_{>k} are simulated by a classical phase correction is realised in _apply_known_phase, but the total count over all S and levels is managed by the runner, not the module.

## Specification changes

- eq_1, eq_2, eq_3, eq_4: Scope narrowed to the binary field q = 2 (qubits); the general-q qudit oracle, Fourier states |psi_{+-1}> and F_q^{-1} are specialised to |->, X/multi-controlled-X and Hadamard gates. Reason: Qiskit provides qubits only; q = 2 is the Reed-Muller case explicitly highlighted in the abstract and in the specification's tiny instance.
- eq_3, eq_4, eq_6: The module builds the circuit for a single derivative step (one set S at one level k = |S|+1); the enumeration over all sets S, the recursion over degree levels and the classical query p(0) for c_emptyset are left to the runner. The removal of already-learned higher-degree coefficients is exposed through the optional 'known_monomials' key and implemented as multi-controlled phase gates (-1)^{x^M}. Reason: build_circuit must return one measurement-free unitary operation; the full algorithm is an adaptive sequence of such operations with intermediate measurements.
- eq_2: The preparation of the target in |-> (X then H) and its uncomputation (H then X) are included as gates inside the returned circuit, so the operation maps |0^n>|0> to |a>|0> on the S-complement qubits (S qubits and target return to |0>) up to a global phase (-1)^{c_S}. Reason: The runner prepares inputs (assumed |0...0>) and the circuit must be a pure gate sequence without initialize; including the target preparation as gates keeps the operation self-contained.
- eq_3: Measurement of the free qubits after the inverse QFT is omitted; the circuit ends after the final Hadamard layer. Reason: The requested artifact is an operation, not an experiment; measurement is left to the runner.
- eq_3: Added validation requiring every monomial of degree > |S|+1 in the instance to be listed in known_monomials (so the effective polynomial has degree <= |S|+1), rejecting other instances with ValueError. Reason: Eq_3 is only an affine identity when the effective polynomial has degree at most |S|+1; otherwise the exact read-out of eq_4 does not hold.
