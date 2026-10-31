# Equation to Qiskit

Qiskit module implementing the operation U^t = (S C)^t of a discrete-time coined quantum-walk search on a 4-regular circulant graph (vertices Z_n, n a power of two, offsets +-1 and +-m). The coin C is a Grover coin on unmarked vertices and -I on the single marked vertex w, encoded without any oracle as a multi-controlled Z conditioned on the classical bits of w. The shift S is a coin-controlled modular constant adder in the QFT basis (p/cp/mcp phases between QFTGate and its inverse). No state preparation or measurement is included; the runner supplies the input state (e.g. the uniform superposition of eq_2).

Source equation run: `5a21f803-cbf6-415a-91a6-c004c53aae90`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0-2: position register pos[0..2], vertex label x in {0..7} in binary, pos[j] = bit 2^j (qubit 0 least significant)
- qubit 3: coin[0] = c0 (low bit of the direction c)
- qubit 4: coin[1] = c1 (high bit of the direction c); c = c0 + 2*c1 selects displacement (+1, -1, +3, -3) for c = (0, 1, 2, 3)
- In tensor-product notation |c> (x) |x> the coin register is the most significant (highest-index) factor, consistent with Qiskit little-endian ordering
- Total qubits = log2(n) + 2 (5 for the example); general instances allow n up to 1024 (12 qubits)

## Assumptions

- The twisted toroid family is modelled by a degree-4 circulant graph with offsets +-1 and +-m; the paper's actual family may differ.
- Discrete-time coined walk with Grover coin on unmarked vertices and -I on the single marked vertex, coin applied before shift, coin-preserving (moving) shift.
- Degree d = 4 is fixed (2 coin qubits); n is a power of two so vertex labels fill the position register exactly.
- Multi-controlled phase gates (mcp) are counted as composite gates; their decomposition into 2-qubit gates is left to the transpiler and is not part of the claimed gate count.
- The number of steps t is an instance parameter; the optimal t is not derived here.

## Unresolved issues

- Exact definition of the paper's twisted toroid graph family and the other graph families is unknown.
- The paper's actual walk model, coin operators, shift convention and explicit circuit decompositions are not available from the abstract.
- No validation contract was supplied; the success probability P_w(t) for the stand-in instance has not been evaluated and the O(sqrt(n) log n) scaling is not checked for this graph.

## Equation mapping

- `eq_1`: implemented; _shift (comment 'eq_3 with the eq_1 graph'): offsets +-1 and +-m mod n = 2^npos define the circulant stand-in graph; _validate enforces n power of two and 1 < m < n/2. The graph structure enters the circuit only through the four displacement values and the modular arithmetic of the QFT adder.
- `eq_2`: out_of_scope; no code location. Input-state preparation (uniform superposition via Hadamards) is excluded by the operation-only contract; the runner prepares the input state.
- `eq_3`: implemented; _shift: QFTGate, p/cp/mcp phase ladder realising delta_c = a + b c0 + e c1 + f c0 c1, then QFTGate.inverse(). Coin-preserving (moving) modular shift implemented as a coin-controlled constant adder in the Fourier basis.
- `eq_4`: implemented; _grover_coin (C_0 on the coin with exact global_phase) and _marked_correction (controlled -C_0 on x = w via X-mapping of w's zero bits and a multi-controlled Z). C = C_0 (x) (I-|w><w|) + (-I) (x) |w><w| is realised as D * (C_0 (x) I) with D = I (x) (I-|w><w|) + (-C_0) (x) |w><w|; the marked vertex is a classical constant in the circuit, so no oracle is used.
- `eq_5`: implemented; build_circuit: loop 'for _ in range(t)' applying coin then shift. U = S C repeated t times; t = 0 yields the identity (empty) circuit.
- `eq_6`: out_of_scope; no code location. Success probability, measurement and the asymptotic gate-count statement are experiment/analysis quantities, not part of the returned unitary operation.

## Specification changes

- eq_2, eq_6: Initial-state preparation and the final position measurement / success-probability evaluation are removed from the generated module; build_circuit returns only the unitary U^t. Reason: Operation-only contract: inputs are prepared and measurements performed by the runner.
- eq_4: The marked-dependent coin is implemented as the product D * (C_0 (x) I) with D = I (x) (I-|w><w|) + (-C_0) (x) |w><w|, using HH XX (multi-controlled Z) XX HH on the coin controlled by the position register; the -1 sign of C_0 = -(HH XX CZ XX HH) is tracked exactly via qc.global_phase += pi per step. Reason: Gives an exact (not merely up-to-phase) realisation of the specified coin using standard gates and no oracle.
- eq_3: The four coin-controlled modular adders are merged into a single QFT-basis adder with the constant decomposition delta_c = 1 - 2 c0 + (m-1) c1 + (2-2m) c0 c1 (p, cp, mcp phases). Reason: Equivalent unitary with fewer multi-controlled gates; relies on n being a power of two so that addition mod 2^npos is natural in the Fourier basis.
- eq_1, eq_2: Register ordering fixed to Qiskit little-endian: position qubits 0..npos-1, coin qubits npos (c0) and npos+1 (c1); the tensor factor |c> of |c>(x)|x> is therefore the high-index register. Reason: The specification's abstract ordering must be mapped to a concrete physical qubit order; disclosed to avoid misinterpretation of basis-state labels.
- eq_1: Instance generalised beyond the fixed n = 8, m = 3 example to any power-of-two n with 8 <= n <= 1024 and 1 < m < n/2, w in [0, n), t >= 0; invalid values raise ValueError. Reason: Requirement to implement the operation for varying valid parameters within the 12-qubit cap.
