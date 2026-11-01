# Equation to Qiskit

Builds the coin-then-shift discrete-time quantum walk on a cycle of N=2^n sites for t steps, followed by an optional fixed single-qubit correction D on the coin. The coin C is I, X, H or Ry(theta). The shift is a coin-controlled modular increment (coin 0) or decrement (coin 1) built from X and multi-controlled X gates. There is no state preparation or measurement; the runner supplies the input and checks the transfer fidelity.

Source equation run: `7630d59b-03ee-4dcd-95b2-d8c913701f5b`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: position register 'pos', little-endian integer x=sum x_i 2^i, walker starts at site 0 (runner prepares |0...0>)
- qubit n: coin qubit 'coin', carries the unknown state a|0>+b|1> supplied by the runner
- example n=3: qubits 0,1,2 = position; qubit 3 = coin (4 qubits total)

## Assumptions

- Coin-then-shift ordering and coin-0=right convention, as in the specification
- The runner prepares the walker at |0> on the position register and the unknown qubit on the coin qubit (index n)
- Step count t is capped at 1000 and n at 11 so total qubits are at most 12
- The correction D is a single-qubit U gate on the coin; omitting it means D=I

## Unresolved issues

- The exact coin and shift ordering used in the paper is unknown
- The explicit D for Hadamard and biased coins is not specified
- The paper's arbitrary-distance construction on a line is not reproduced
- The paper's definition of distance and target site convention is unknown

## Equation mapping

- `eq_1`: implemented; _shift. Coin-controlled modular increment (coin=0, right) and decrement (coin=1, left) on the little-endian position register, built from X and multi-controlled X gates.
- `eq_2`: implemented; build_circuit (loop over t steps, then final u gate). The coin C is applied first, then the shift S, repeated t times. The optional fixed correction D, a U(theta,phi,lam) gate, is applied to the coin qubit only.
- `eq_3`: out_of_scope; no code location. The transfer criterion is evaluated from the statevector on the four test inputs. That happens in the runner's postprocessing, not in the operation.
- `eq_4`: background; no code location. Analytic prediction for C=I on the cycle (t=N/2, d=N/2, D=I). It is reproduced by build_circuit with coin 'I' and t=N/2 and is not coded separately.
- `eq_5`: background; no code location. Analytic behaviour of the flip coin under coin-then-shift ordering. It follows from the implemented circuit with coin 'X' and is not coded separately.
- `eq_6`: out_of_scope; no code location. The periodicity search for the minimal T is classical postprocessing over many circuit instances. build_circuit only constructs U^t.

## Specification changes

- eq_2, eq_3: D is not derived. It is supplied by the caller as explicit U(theta,phi,lam) parameters, or omitted for D=I. The circuit does not compute the 'inverse of coin-block unitary' mentioned in the steps. Reason: The paper's D for Hadamard and biased coins is unknown, and the circuit may not simulate or search at build time.
- eq_1, eq_2, eq_3, eq_4, eq_5, eq_6: Scope narrowed to the cycle with N=2^n and n between 1 and 11. The line walk, the arbitrary-distance theorems, the fidelity scan over (t,d), and the period search are not implemented in the circuit. Reason: The 12-qubit cap and the rule that the circuit must be an operation without measurement or analysis. The line-walk construction is also unspecified.
- eq_1, eq_2: Convention assumed from the specification: coin 0 moves right (+1), coin 1 moves left (-1), and the coin is applied before the shift. The Ry(theta) coin is parameterised by the 'theta' field and I, X and H are selected by name. Reason: The abstract does not fix the ordering or direction convention.
