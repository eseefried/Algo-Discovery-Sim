# Equation to Qiskit

Qiskit build_circuit for a discrete-time quantum walk on a 2^n-site circle with a 1-qubit coin. Each step applies the coin (identity or X) and then a conditional shift, done in the Fourier basis with QFTGate, phase gates and a controlled phase. A final state-independent coin (identity or X, or X^t when 'auto' with the flip coin) is applied at the end. Biased coins, Hadamard, the line walk and the general final-coin construction are out of scope. Input states and x0 are prepared by the runner.

Source equation run: `f0e81bfa-f4f3-42d9-b3d7-e37917e1b5a8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: coin (computational basis |0>=move right, |1>=move left)
- qubits 1..n: position register, binary encoding of x in Z_{2^n}, qubit 1 is the least significant bit
- example: n=2, so qubits 0 (coin), 1 and 2 (position, N=4)

## Assumptions

- Shift convention: coin |0> moves x -> x+1, coin |1> moves x -> x-1, positions mod 2^n.
- The coin is applied before the shift in each step.
- The same coin is used every step.
- Position uses binary encoding with qubit 1 as the least significant bit; the QFTGate index order matches that physical order and no factorized QFT index order is used.
- The Fourier-basis shift is exact, since QFTGate maps |x> to a sum over k of exp(2*pi*i*x*k/N)|k>.

## Unresolved issues

- The explicit additional final coin for general (biased or Hadamard) coins is not specified in the abstract and is not implemented.
- The formal definition of perfect state transfer and the target positions are not given, so the circuit does not guarantee transfer for arbitrary t.
- The line walk is not implemented; only the finite circle is.
- The periodicity and distance-limit claims are not addressed.

## Equation mapping

- `eq_1`: implemented; _apply_shift. Conditional shift on the circle (coin 0 -> +1, coin 1 -> -1, mod 2^n), built as QFT on the position register, per-qubit phases p(theta_j) and cp(-2*theta_j) controlled by the coin, then inverse QFT.
- `eq_2`: implemented; build_circuit loop with _apply_coin and _apply_shift. U = S(C x I) is applied t times with the same coin C (identity or X). The initial state |psi>|x0> is prepared by the runner.
- `eq_3`: implemented; build_circuit, final coin block. Only the operation (C_f x I)U^t is built, with C_f restricted to I or X. The transfer condition is a property of the output state and is not enforced or checked in the circuit.
- `eq_4`: implemented; build_circuit, final_coin == 'auto' branch. For the flip coin, C_f = X^t is applied (X for odd t, nothing for even t). The schematic position expression in eq_4 is not implemented because it is unverified; the walker's position evolves by the actual shift circuit.

## Specification changes

- eq_4: Only the final-coin rule C_f = X^t is used. The schematic walker-position expression x0+(-1)^t... is dropped. Reason: With U = S(C x I) and the flip coin, the coin-0 component sits at 0,-1,0,... relative positions and the coin-1 component at +1,0,+1,..., so for odd t and N>2 the components are at different sites. The schematic expression was unverified and not used.
- eq_1, eq_2, eq_3, eq_4: Scope narrowed to a circle with N=2^n sites (n=1..11), identity or flip coin, and a final coin that is I or X. The line, biased and Hadamard coins, and the general final-coin construction are excluded. Reason: The abstract does not give the explicit final coin operator for general coins or the formal transfer definition. The circle size must be a power of two to be encoded in qubits.
- eq_2: The initial position x0 is not part of the circuit and is set by the runner. Reason: The task requires an operation with no state preparation.
- eq_3: The target position and the transfer condition are not encoded. Reason: The target position depends on coin, t and N, and checking it is the job of the downstream software.
