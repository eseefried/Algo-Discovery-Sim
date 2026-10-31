# Equation to Qiskit

Qiskit module implementing t steps of the lackadaisical discrete-time quantum walk search on the complete graph K_N with l self-loops per vertex: phase-flip oracle on the marked vertex (eq_3), Grover coin on the (N-1+l)-dimensional coin space (eq_2), and flip-flop shift with self-loops acting as identity (eq_4), composed as U = S C Q repeated `steps` times (eq_5). The construction is restricted to N and d = N-1+l both powers of two (so that modular arithmetic and the Grover coin are exact with standard gates), with l >= 1. Coin directions are relabeled so that c in {1,...,N-1} points to (v+c) mod N and c = 0 or c >= N are self-loops; the flip-flop shift then becomes v += c mod N, c -> -c mod N, controlled on the high coin bits being zero. The modular adder uses a QFTGate-based Draper adder; negation uses bitwise complement plus an mcx increment cascade. Initial state preparation and measurement are left to the runner.

Source equation run: `ac26f9e9-c924-4658-9731-db0563c9a985`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-1: vertex register |v>, little-endian integer v in {0,1,2,3} (qubit 0 = least significant bit)
- qubits 2-3: coin register |c>, little-endian integer c in {0,1,2,3}; c=1,2,3 is the edge from v to (v+c) mod 4, c=0 is the single self-loop (l=1)
- total 4 qubits; the circuit is U^steps with U = S C Q and carries a global phase of pi per step from the coin construction
- runner should prepare the uniform state H^{\otimes 4}|0000> (eq_1) and measure qubits 0-1 to estimate p(t)

## Assumptions

- Grover coin on the enlarged d-dimensional coin space with self-loops weighted equally to ordinary edges.
- Operator ordering U = S C Q (oracle, then coin, then shift), as in the specification.
- Little-endian integer encoding for both registers with the vertex register on the low qubits and the coin register on the high qubits.
- Instance keys are N, l, marked, steps as Python integers; steps >= 1.
- mcx and mcp multi-controlled gates with up to about 11 controls are acceptable standard gates for the transpiler.

## Unresolved issues

- The l=0 reference walk (peak success probability 1/2 in the abstract) cannot be built because d = N-1 is not a power of two under this restriction, so the 1/2 -> 1 comparison must be done against an external l=0 implementation.
- The abstract's claimed probabilities are large-N asymptotics; the example instance N=4 will not reproduce them exactly and the optimal step count must be found by scanning.
- Whether the original paper uses exactly this coin weighting and the flip-flop shift is inferred, not confirmed from the abstract.

## Equation mapping

- `eq_1`: background; build_circuit: QuantumRegister allocation (vertex n_v qubits, coin n_c qubits) and module docstring. The Hilbert space factorisation and register dimensions follow eq_1 with d = 2^{n_c}; the uniform initial state |psi_0> is not prepared because the module returns an operation only (runner prepares inputs).
- `eq_2`: implemented; _grover_coin. Grover coin 2|s_c><s_c| - I_d realised as H^n (X^n MCZ X^n) H^n with a recorded global phase pi so the implemented operator equals C_0 exactly; requires d to be a power of two.
- `eq_3`: implemented; _phase_flip. Sign flip of all amplitude at the marked vertex a via X-conjugated multi-controlled Z on the vertex register, identity on the coin register.
- `eq_4`: implemented; _shift. Flip-flop shift with self-loops fixed, using a relabelled direction encoding (c in 1..N-1 -> (v+c) mod N; c=0 and c>=N self-loops) so that S = [v += c mod N, c -> -c mod N] controlled on the high coin bits being zero; adder via QFTGate-based Draper circuit, negation via complement plus mcx increment cascade.
- `eq_5`: implemented; build_circuit (loop over steps applying _phase_flip, _grover_coin, _shift). One step U = S C Q is applied `steps` times; the success-probability p(t) is a measurement quantity left to the runner.
- `eq_6`: out_of_scope; no code location. Asymptotic peak-success-probability claims (1/2 for l=0, 1 for l=1, decreasing for l>1) are experimental targets to be scanned over t by the runner, not circuit components; moreover l=0 is not supported by the chosen encoding.

## Specification changes

- eq_4: Direction encoding relabelled: edge directions are c in {1,...,N-1} pointing to (v+c) mod N (instead of c in {0,...,N-2} pointing to (v+c+1) mod N), and self-loops are c=0 together with c in {N,...,d-1}. Under this encoding the flip-flop reversal is c -> (-c) mod N and the whole shift is the identity on c=0 automatically, so only the high coin bits need to be controlled. Reason: Makes the shift an exact permutation implementable with a QFT-based modular adder and a two's-complement negation using standard gates; it is a bijective relabelling of the coin basis and does not change the walk dynamics.
- eq_1, eq_2, eq_4: Restricted to N a power of two and d = N-1+l a power of two (hence l >= 1 and l = 2^k - N + 1 for some k with 2^k >= N), e.g. (N,l) = (2,1), (4,1), (4,5), (8,1), (8,9), (16,1), ..., (64,1). Reason: Avoids state-preparation subcircuits for a non-power-of-two uniform coin state and non-power-of-two modular arithmetic; keeps all operations exact with standard gates and QFTGate. The l=0 baseline (d=N-1) is therefore not constructible with this module.
- eq_2: The coin circuit H^n X^n MCZ X^n H^n implements -(2|s><s|-I); a global phase of pi per coin application is added to the circuit's global_phase attribute so that the circuit unitary equals S C Q exactly. Reason: Physically irrelevant global phase, recorded so that the returned operator matches the specified unitary without sign ambiguity.
- eq_1, eq_5, eq_6: Initial uniform state preparation, measurement of the vertex register, scanning over t and comparison with the 1/2 vs 1 claim are left to the runner; the module returns only U^steps. Reason: Required by the implementation contract (operation only, no state preparation or measurement).
