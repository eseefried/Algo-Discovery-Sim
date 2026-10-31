# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Perfect transfer of an unknown qubit state via a discrete-time quantum walk on a line or circle, using an extra final coin operator independent of the state. Determine which coin operators permit perfect state transfer over arbitrary versus only finite distances, and show that walks ending in perfect state transfer are periodic.

Scope: Abstract-level reconstruction of the PST scheme: walk with coin C, shift, final extra coin operator; claims about identity/flip coins versus biased/Hadamard coins and periodicity. Detailed derivations, the final coin's explicit form, and the transfer-distance bounds are not in the abstract.

## Symbols

- $|\psi\rangle=\alpha|0\rangle+\beta|1\rangle$: unknown qubit state to be transferred (encoded in the coin state); domain: normalized, |\alpha|^2+|\beta|^2=1
- $C$: coin operator driving the walk; domain: 2x2 unitary
- $S$: conditional shift operator; domain: unitary on position⊗coin
- $C_f$: additional final coin operator, independent of the state; domain: 2x2 unitary
- $d$: transfer distance; domain: integer
- $t$: number of walk steps; domain: nonnegative integer

## eq_1: Walk step

$$
U=S\,(I_{x}\otimes C)
$$

One step of the discrete-time quantum walk: coin then conditional shift.

Provenance: `standard_background`. Standard definition of the discrete-time quantum walk.

Equation assumptions:

- Standard coined walk form

## eq_2: Perfect state transfer condition

$$
(I_x\otimes C_f)\,U^{t}\,|0\rangle_x|\psi\rangle=|d\rangle_x|\psi\rangle
$$

Final state has the qubit state at position d, with the final coin applied last, for all psi.

Provenance: `abstract_inferred`. Formalizes the stated goal; the explicit form is an assumption of this reconstruction.

Abstract evidence: perfect transfer of an unknown qubit state

Equation assumptions:

- The state is initially encoded in the coin at the origin
- Target coin state equals psi (could differ by a fixed, state-independent unitary)

## Registers

- position: infinite line or N-site circle (symbolic) qubits; walker position register |x>
- coin: 1 qubit qubits; carries the unknown qubit state |psi>

## Initial state

|0>_x ⊗ (alpha|0>+beta|1>)_coin, walker at origin with the unknown qubit in the coin

## Measurement

Not specified in the abstract. For verification, one could measure the position register to confirm location d and perform state tomography on the coin qubit to compare with psi.

## Classical postprocessing

None specified in the abstract. Verification only: compare the reconstructed coin state with psi via fidelity; check periodicity of the walk by repeating over t.

## Algorithm steps

1. Prepare walker at origin with the unknown qubit in the coin register. (eq_2)
2. Apply t steps of the walk U (coin C then conditional shift S). (eq_1)
3. Apply the additional final coin operator C_f to the coin register, independent of psi. (eq_2)
4. Check that the walker is at position d with coin state psi (perfect transfer). (eq_2)

## Assumptions

- Initial walker position is the origin with the qubit stored in the coin.
- Register sizes and the measurement/verification procedure are assumed, not from the abstract.
- Registers are position plus a single coin qubit.
- Measurement is a verification-only assumption.
- eq_2 is a plausible formalization, not the paper's stated equation; the identity/flip coin results and periodicity are not encoded as equations.
- eq_2 is an inferred formalization; the target coin state may differ from psi by a fixed unitary in the paper.

## Missing information

- Explicit form of the final coin operator
- Exact bounds on finite transfer distances for Hadamard/biased coins
- Periodicity statement details and periods
- Paper's actual initial state and measurement protocol, if any
- Whether the final coin acts as a unitary correction or otherwise
- Whether the walk is single-coin homogeneous and how the circle size relates to d.
