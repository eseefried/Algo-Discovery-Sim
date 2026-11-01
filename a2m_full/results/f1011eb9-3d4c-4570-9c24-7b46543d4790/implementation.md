# Equation to Qiskit

Operation-only circuit for the continuous-time quantum-walk search evolution U ~ exp(-i H t) on the complete graph K_N (N=2^n, n<=12), with H = -gamma*A - |w><w| and A = N|s><s| - I. It uses a Trotter product (first or second order) of two exactly implementable phase-projector exponentials, exp(i*gamma*N*t/r |s><s|) and exp(i*t/r |w><w|). No state preparation, measurement, Lanczos or t* search is included.

Source equation run: `7d89cd56-e408-4396-9d67-85b74378e6af`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Single register 'q' of n qubits (example n=3): qubit i = bit i of the vertex index (little-endian, index = sum q_i 2^i)
- Marked vertex w=5 = binary 101: qubit0=1, qubit1=0, qubit2=1
- No ancilla qubits
- Input state (e.g. uniform superposition |s> via Hadamards) is prepared by the runner, not by this circuit

## Assumptions

- Adjacency (not Laplacian) form of H on the complete graph without broken links
- Vertex index is little-endian: qubit i holds bit i of the vertex label
- Global phase exp(-i*gamma*t) is included via qc.global_phase
- Time t is non-negative; steps capped at 200 and order in {1,2}
- The runner prepares |s> (or any other input) and handles measurement and comparison

## Unresolved issues

- Trotter error at finite N=8 and chosen steps is unquantified; accuracy depends on 'steps' and 'order'
- For N=8 the optimal t* and gamma differ from asymptotic values; the example t=(pi/2)sqrt(8) is only approximate
- The paper's graph families (star, broken links, XY chain, transport) are not implemented

## Equation mapping

- `eq_1`: implemented; build_circuit: the two Trotter factors apply_s(a) and phase_on_pattern(wbits, b), plus qc.global_phase. The circuit approximates exp(-iHt) for H=-gamma*A-|w><w|; the oracle term enters via the |w><w| phase, the adjacency term via the |s><s| phase.
- `eq_2`: implemented; build_circuit: apply_s (H^n, phase on |0..0>, H^n) and the global_phase line. A=N|s><s|-I makes the adjacency term a rank-one projector exponential; the +gamma*I part becomes the global phase -gamma*t.
- `eq_3`: background; no code location. Classical Lanczos recursion used offline to understand the invariant subspace; not part of the quantum operation.
- `eq_4`: background; no code location. Asymptotic resonance gamma=1/N and t~(pi/2)sqrt(N) are only used to choose example gamma and t; they are supplied as instance parameters, not computed in the circuit.
- `eq_5`: background; no code location. Success probability and t* maximization are classical post-processing/comparison done by the runner on the circuit output; no measurement is included.
- `eq_6`: implemented; build_circuit: Trotter loop over 'steps' with 'order' 1 or 2. Product-formula realization of exp(-iHt) = e^{-i gamma t} e^{i gamma N t|s><s|} e^{i t|w><w|} (non-commuting projectors, so Trotterized). The |s><s| exponential is H^n conjugation of a multi-controlled phase; |w><w| is a multi-controlled phase with X conjugation on zero bits of w.

## Specification changes

- eq_6: Used a Trotter product (first or second order, selectable via 'order' and 'steps') of exact projector exponentials instead of exact PauliEvolutionGate evolution. Reason: PauliEvolutionGate requires SparsePauliOp from qiskit.quantum_info, which is not an allowed import; the two projectors do not commute so the product is approximate with error vanishing as steps grows.
- eq_6: Corrected the equation: the displayed factorization is exact only up to Trotter error; the sign of the |s><s| exponent is +i*gamma*N*t because H contains -gamma*N|s><s|. Reason: Consistency with eq_2 and the non-commutation of the projectors.
- eq_1, eq_2, eq_6: Scope narrowed to the generic complete graph K_N with N=2^n (n up to 12) and arbitrary marked vertex w, with t, gamma, steps supplied by the instance; the spec's fixed instance N=8, w=5 appears only as the example. Reason: Operation must work for varying valid parameters; star graphs, broken-link graphs, transport and XY-chain bound are out of scope.
- eq_3, eq_4, eq_5: Lanczos reduction, t* optimization, initial |s> preparation (Hadamards) and measurement are excluded from the circuit. Reason: The circuit must be a pure operation with no input preparation or measurement; the classical steps are background.
- eq_2: Gamma defaults to 1/N when omitted from the instance. Reason: Resonance value from eq_4 gives a sensible default.
