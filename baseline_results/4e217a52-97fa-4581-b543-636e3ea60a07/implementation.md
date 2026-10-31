# Equation to Qiskit

Qiskit module implementing the scoped single-walker discrete-time quantum walk (DTQW) perfect state transfer of one unknown coin qubit from site x=0 to site x=d on a line, using a position/time-dependent coin schedule drawn from {I, X}. The shift S is realised as a QFT-basis conditional incrementer/decrementer, the site-selective coin flips as multi-controlled X gates on the coin, and the known correction V^dagger = X is applied at the end (optional). The schedule's final flip site was corrected from x=T-2 to x=T-1=d+1 so that the two components actually recombine at x=d.

Source equation run: `b0854ca1-c24e-4b75-ab63-d24eb2b32bb0`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Example d=2: n_p=3 position qubits + 1 coin qubit = 4 qubits total.
- qubits 0,1,2 : position register 'pos', y = x + 1 stored as unsigned integer with qubit m = bit m of y (qubit 0 least significant).
- qubit 3 : coin register 'coin'; carries the unknown qubit |phi> at input and (after the final X correction) |phi> at output.
- Expected input: pos = |y=1> = |001> (x = 0), coin = |phi>. Expected output: pos = |y=3> = |011> (x = d = 2), coin = |phi> (or X|phi> if apply_correction=false).

## Assumptions

- Shift convention: coin 0 moves x -> x+1, coin 1 moves x -> x-1.
- Coin operators restricted to {I, X}; the coin schedule of eq_5 (as corrected) is an assumption of this reconstruction, not the paper's protocol.
- The position register is sized so that no wrap-around occurs (max y = d+2 < 2^n_p); modular arithmetic of the QFT adder is therefore never exercised.
- Input state is prepared externally as |y=1>_P (x = 0) tensored with the unknown coin qubit; no preparation is included in the circuit.
- Qubit cap of 12 limits d to at most 2045 (n_p <= 11); large d produce deep circuits (T = d+2 steps, each with two QFTs).

## Unresolved issues

- The paper's actual encoding of an arbitrary two-qubit state in the walk and its specific coin-flipping settings remain unknown; this module implements a single-qubit analogue.
- Multi-dimensional network distribution between every pair of sites and the routing architecture are out of scope and would need additional structural information.
- Correctness of the transfer (unit fidelity, V = X) is asserted from the derivation in eq_6 and has not been simulated here.

## Equation mapping

- `eq_1`: implemented; module docstring and build_circuit register allocation; sizing in _validate (n_p = (d+2).bit_length()). Position register P tensored with a one-qubit coin register C; positions x in [-1, d+1] are encoded as y = x+1 on n_p qubits.
- `eq_2`: implemented; _shift. Coin-conditioned shift implemented as a QFT-basis adder: unconditional +1 phases plus coin-controlled -2 phases between QFTGate(n) and its inverse, giving y -> y+1 for coin 0 and y -> y-1 for coin 1.
- `eq_3`: implemented; _walk_step and _flip_coin_at. One walk step applies the site-dependent coin (X at one selected site via a multi-controlled X with X-conjugated zero controls, I elsewhere) followed by the shift.
- `eq_4`: implemented; build_circuit (product of walk steps followed by the V^dagger = X correction). The returned circuit is the full operator U_T...U_1 (optionally followed by X on the coin), which is the operation whose action on |0>_P|phi>_C is asserted by eq_4; the transfer property itself is left to external validation.
- `eq_5`: implemented; build_circuit main loop (comment block 'eq_5 coin schedule'). Flip at x=-1 (y=0) in step 2, identity coins in steps 1 and 3..T-1, final flip in step T; final flip site corrected to x = T-1 = d+1 (y = d+2), see specification_changes.
- `eq_6`: background; no code location. Derived trajectory/result; it is not an operation but fixes V = X, which motivates the final qc.x(coin) correction in build_circuit.

## Specification changes

- eq_5, eq_6: The final coin flip in step T is applied at x = T-1 = d+1 (y = d+2), not at x = T-2 as written in eq_5. Reason: By eq_6, after step T-1 the components sit at x = T-1 and x = T-3; flipping at x = T-2 would act on no amplitude. Flipping the leading component at x = T-1 and shifting brings both components to x = T-2 = d with coin a|1>+b|0>, as eq_6 states.
- eq_1: Position register uses Qiskit little-endian ordering (qubit m holds bit m of y) instead of the 'big-endian' wording in the registers description; the sender basis state is |y=1> = qubit 0 set, all others clear. Reason: Qiskit qubit index 0 is the least significant bit; the QFT-based adder and the multi-controlled flips are written consistently with this convention.
- eq_4: The known correction V^dagger = X on the coin is included inside the returned circuit (toggle via instance key apply_correction, default true). Reason: The specification's final step says the correction may be applied or absorbed by the receiver; including it makes the circuit map |0>_P|phi>_C directly to |d>_P|phi>_C for validation.
- eq_1, eq_2, eq_3, eq_4, eq_5, eq_6: Scope narrowed to a single walker on a line transferring one coin qubit with coins in {I, X}; the paper's two-qubit encoding, multi-dimensional network, multi-qubit entangled-state distribution, and routing are not implemented. Reason: The abstract gives no equations or encodings for those parts; the single-qubit line transfer is the smallest explicit construction consistent with the specification.
