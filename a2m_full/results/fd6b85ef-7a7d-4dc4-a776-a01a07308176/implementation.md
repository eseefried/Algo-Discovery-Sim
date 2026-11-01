# Equation to Qiskit

One-qubit circuit builder for the final assembly step of the Clifford-cyclotomic exact-synthesis specification: given n (even) and a synthesized product word over {H,S,Sdg,X,Y,Z,Rz(pi/n),Rz(-pi/n)} written left-to-right as a matrix product U = F_1...F_k, it emits the circuit that applies the factors right-to-left (time order). The classical synthesis search (height proxy and greedy descent) is NOT implemented, because its definitions are unresolved in the specification.

Source equation run: `2155749d-787d-4740-890a-39903aa69bdf`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: single data qubit q[0] (no ancilla); Qiskit index 0 is the least significant bit; the input state is prepared by the runner

## Assumptions

- Global phase is ignored when comparing with a target U; Qiskit rz differs from T by a global phase for n=4.
- The supplied word is already a valid synthesis output; the builder only assembles it.
- The word is given in matrix-product order, leftmost factor last in time.
- Instance schema: {"n": even int in [2,1024], "word": list of tokens among h,s,sdg,x,y,z,r,rdg}.

## Unresolved issues

- The exact height definition, per-rotation height drop, and optimality criterion for general n are not specified, so the synthesis algorithm is not implemented.
- Synthesizability criterion for n other than 4 is not available.
- No public validation contract or target instances were supplied.

## Equation mapping

- `eq_1`: implemented; build_circuit: theta = math.pi / n and qc.rz(+/-theta, 0). Rotation gate Rz(pi/n) = diag(e^{-i pi/2n}, e^{i pi/2n}) is emitted with Qiskit's rz convention. For n=4 it equals T up to global phase.
- `eq_2`: background; no code location. Ring characterization for n=4 is a theorem context for which unitaries are synthesizable. The builder does not check ring membership; it only assembles a given word.
- `eq_3`: background; no code location. Galois-conjugate unitarity is part of the synthesizability test and is not used when assembling a supplied word.
- `eq_4`: out_of_scope; no code location. The height proxy is an unconfirmed placeholder and belongs to the classical search, which is not implemented.
- `eq_5`: implemented; build_circuit: loop over reversed(word). Only the assembly part is implemented: for U = R_1...R_m U_m given as a left-to-right product word, the circuit applies factors in reversed order. The greedy descent that finds the word is not implemented.

## Specification changes

- eq_4, eq_5: Scope narrowed: the classical greedy height-descent synthesis is not performed inside build_circuit. The synthesized product word is supplied via the instance and the module only builds the corresponding 1-qubit circuit. Reason: The height definition and per-rotation drop are unresolved placeholders in the specification, and the operation must be a unitary circuit without classical simulation or operator construction.
- eq_1: Added tokens 'rdg' (Rz(-pi/n)) and Clifford tokens sdg, y, z in the word alphabet, beyond the stated H, S, X, Rz(pi/n). Reason: These are Clifford group elements or inverses and make words easier to express without changing the gate-set meaning; Rz(-pi/n) is the inverse of the rotation.
- eq_5: The word is interpreted in matrix-product order (leftmost factor applied last); the circuit reverses it into time order. Reason: The specification states the product is written right-to-left and that the recorded product must be reversed when building.
- eq_2: No ring-membership, unitarity, or synthesizability validation is performed; any word over the allowed alphabet is built for any even n in [2,1024]. Reason: These checks need exact cyclotomic arithmetic that is outside the narrowed construction.
