# Equation to Qiskit

Coinless (staggered, tessellation) 1D quantum walk on a cycle of N=2^n sites, using n position qubits and no ancilla or coin. One step is U=U1 U0 with U_i=2P_i-I. The even-odd reflection U0 acts on the least significant qubit, and U1=S U0 S^dagger, where S is the +1 mod N incrementer built from an MCX ladder. Pair states are cos(theta)|even>+sin(theta)|odd>. theta=pi/4 gives the specified uniform pairs, and other theta values are an optional generalisation. The coined-walk equivalence is out of scope.

Source equation run: `d85a81e3-f2c7-484d-a3f9-c860cbebab89`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: pos register, little-endian, site x = sum_i q_i 2^i, N = 2^n sites on a cycle
- no coin qubit and no ancilla in this coinless construction
- total qubits = n (<= 12)

## Assumptions

- Cycle length N=2^n, n between 2 and 12
- Two-polygon tessellations: pairs (2k,2k+1) for U0 and (2k+1,2k+2 mod N) for U1
- Little-endian site encoding
- Input state is prepared by the runner
- Defaults: steps must be given explicitly, theta defaults to pi/4

## Unresolved issues

- The exact coinless-to-coined transformation, the second coin and the invariant subspace remain unspecified and are not implemented
- The paper's specific family of evolution operators is unknown, so theta is only a plausible parametrisation
- Mixing time and limiting distribution must be computed by the runner from statevectors

## Equation mapping

- `eq_1`: implemented; build_circuit (per-step loop: _reflect_pairs; _decrement; _reflect_pairs; _increment). U=U1U0 with U_i=2P_i-I. U0 is applied first, then U1=S U0 S^dagger.
- `eq_2`: implemented; _reflect_pairs together with the _increment/_decrement conjugation. P0 = I_high (x) |a><a| on the least significant qubit, so pairs are (2k,2k+1). P1 = S P0 S^dagger gives pairs (2k+1,2k+2 mod N). At theta=pi/4 the pair states are exactly the uniform (|j>+|j+1>)/sqrt2.
- `eq_3`: out_of_scope; no code location. The coined-walk equivalence is not derived in the specification (the exact coin and shift-back are unknown), so it is not implemented.
- `eq_4`: background; no code location. Position marginal is a classical readout of the statevector. The circuit has no measurement.
- `eq_5`: background; no code location. Total variation distance, mixing time and time averaging are classical postprocessing, not part of the operation.

## Specification changes

- eq_3: Scope narrowed to the coinless walk only. No coined circuit or equivalence is built. Reason: The coinless-to-coined mapping and invariant subspace are unresolved in the specification, and only one construction is to be implemented.
- eq_1, eq_2: Added an optional parameter theta (default pi/4) that generalises the uniform pair states to cos(theta)|even>+sin(theta)|odd>. The reflection is RY(2theta)Z. Reason: With theta=pi/4 each reflection reduces to X on the LSB. U is then a deterministic permutation and the walk has no interference. The parameter lets the same construction cover nontrivial members of the family. The default reproduces the specified construction exactly.
- eq_2: Projectors are realised as a qubit-0 reflection (U0) and its shifted conjugate (U1). No dense matrix or projector sum is built. Reason: Dense unitaries are disallowed, and P0 factorises as identity on the high bits times a single-qubit projector.
