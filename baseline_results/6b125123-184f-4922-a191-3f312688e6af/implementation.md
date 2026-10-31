# Equation to Qiskit

Implements the discretised search-Hamiltonian evolution operator U(delta,m) = [exp(-i delta |s><s|) exp(-i delta |t><t|)]^m on an n-qubit search register (no state preparation, no measurement). Two step modes are supported: 'trotter' (Lie-Trotter small steps, delta = T/m with T = pi*sqrt(N)/2, eq_3) and 'reflection' (maximal step delta = pi, each factor an exact reflection, so m steps equal m Grover iterations up to global phase, eq_4/eq_5). Each projector exponential is realised exactly as an X-conjugated multi-controlled phase gate (marked-state term) and its H^{\otimes n}-conjugate (uniform-superposition term). Example: n=2, t=3, reflection mode, 1 step, which maps |s> to |11> exactly (up to global phase).

Source equation run: `77f3a41f-64a7-425a-9c99-24a791c701c3`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- search[0] = qubit 0: least significant bit x_0 of the database index x
- search[1] = qubit 1: most significant bit x_1 of the database index x (for n=2)
- Basis state |x> = |x_1 x_0>, little-endian; marked item t=3 is |11>
- Input state |s> = H^{(x)2}|00> is prepared by the runner; expected output for the example is |11> up to global phase -1

## Assumptions

- Hamiltonian is the projector-sum H = |s><s| + |t><t| (Farhi-Gutmann), as assumed in the specification.
- Single marked item, N = 2^n, little-endian encoding with qubit 0 the least significant bit.
- Units hbar = 1; the 'reflection operators' are the delta = pi exponentials of the two projectors.
- mcp(-delta) on all qubits after X-conjugation realises exp(-i delta |t><t|) exactly (no approximation); for n=1 a single p gate is used.
- Total qubit count equals n and is capped at 12 by validation before allocation.

## Unresolved issues

- The paper's actual Hamiltonian, splitting and error measure are unknown; the power-law exponent and the mechanism for logarithmic error dependence in the reflection trajectory are not reconstructible from the abstract and are not modelled.
- For general N, the number of reflection steps k = round(pi/(4 theta) - 1/2) is left to the instance ('steps'); the module does not choose it automatically.
- Multi-controlled phase gates (mcp) are decomposed by Qiskit at transpile time; gate counts are not optimised.

## Equation mapping

- `eq_1`: background; no code location. Defines H = |s><s| + |t><t| and the initial state |s>; |s> is prepared by the runner, and the two projectors appear only through their exponentials in _projector_phase and _uniform_projector_phase.
- `eq_2`: implemented; build_circuit: total_time = math.pi * math.sqrt(big_n) / 2.0 (trotter branch). The exact evolution time T = pi*sqrt(N)/2 is used to set the Trotter step delta = T/m; the exact exp(-iHT) itself is not built (it is the target the discretisations approximate).
- `eq_3`: implemented; build_circuit loop with step_mode='trotter'; _projector_phase, _uniform_projector_phase. The first-order product formula [exp(-i delta |s><s|) exp(-i delta |t><t|)]^m with delta = T/m, each factor realised exactly as an (H-conjugated) X-conjugated multi-controlled phase gate. The error bound itself is not computed in code.
- `eq_4`: implemented; build_circuit with step_mode='reflection' (delta = math.pi); docstrings of _projector_phase and _uniform_projector_phase. With delta = pi, mcp(-pi) gives exactly 1 - 2|t><t| and the H-conjugate gives exactly 1 - 2|s><s|; m steps equal (-1)^m G^m, i.e. the Grover iteration up to global phase.
- `eq_5`: implemented; example_instance_json (n=2, marked=3, steps=1, step_mode='reflection'). The N=4, t=3 instance: one reflection step. For n=2 the marked-state factor becomes X-conjugation-free cp(-pi) = CZ and the uniform factor becomes H^2 X^2 CZ X^2 H^2, reaching |11> exactly up to global phase.

## Specification changes

- eq_3, eq_4: Within each product-formula step the marked-state (oracle) factor exp(-i delta |t><t|) is applied first and the uniform factor exp(-i delta |s><s|) second, i.e. the operator product is [exp(-i delta P_s) exp(-i delta P_t)]^m rather than the written [exp(-i delta P_t) exp(-i delta P_s)]^m. Reason: Matches the Grover ordering G = (2|s><s|-1)(1-2|t><t|) and step 4 of the specification; the two orderings differ only by a boundary conjugation and, acting on |s>, by a global phase in the first factor, so the first-order error scaling is unchanged.
- eq_4, eq_5: The reflection-mode circuit implements (1-2P_s)(1-2P_t) = -G per step, so the output equals G^m|s> up to a global phase (-1)^m. Reason: exp(-i pi |s><s|) = 1 - 2|s><s| differs from the diffusion operator 2|s><s| - 1 by a sign; implementing the exponential exactly preserves the Hamiltonian-evolution meaning and the global phase is unobservable.
- eq_1, eq_2: The module returns only the discretised evolution operator; preparation of |s> (H^{(x)n}) and the final measurement are excluded. Reason: Task requires a measurement-free operation with inputs prepared by the runner.
- eq_3: The Trotter error bound and the claimed power-law/logarithmic complexity scalings are not computed or verified; only the circuits for the two discretisations are provided. Reason: Scope narrowing: the module is an operation generator; error analysis is left to the runner/analysis stage.
