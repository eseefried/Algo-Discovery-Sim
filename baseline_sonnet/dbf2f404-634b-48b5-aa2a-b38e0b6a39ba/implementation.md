# Equation to Qiskit

Coinless two-tessellation (staggered) quantum walk operation on a 2^n-site cycle using n site qubits. One step is U = U1 U0, repeated t times. U0 is the reflection about the cells {2j,2j+1}, which equals X on qubit 0. U1 is the reflection about the cells {2j+1,2j+2}, built as S X0 S^dagger, where S is the cyclic increment x -> x+1 mod N implemented with QFTGate, phase gates, and the inverse QFT. No state preparation or measurement is included.

Source equation run: `1b91bb8a-a023-407f-a4a0-2c31efe9a14a`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1 form register 'site' holding the binary site index x (qubit 0 = least significant bit), x in 0..2^n-1, N=2^n
- Example: n=2 gives N=4 sites, qubits 0 and 1
- No ancilla, coin or classical registers

## Assumptions

- Tessellations are the two edge tessellations of the cycle, as in eq_2, which is an assumed example rather than taken from the paper
- Site x is encoded as binary with qubit 0 as LSB
- Step order U = U1 U0 is a convention
- steps is capped at 64 and num_qubits must be between 2 and 12

## Unresolved issues

- The paper's specific family of evolution operators and its coined-walk equivalence are not reconstructed
- Odd or non-power-of-two cycle lengths are unsupported

## Equation mapping

- `eq_1`: implemented; build_circuit: qc.x(0) for U0; _increment(-1), qc.x(0), _increment(+1) for U1. Each tessellation reflection 2*sum|alpha><alpha| - I is realized exactly. For tessellation 0 the cells are |j>|+>, so the reflection equals X on qubit 0. For tessellation 1 the cells are the tessellation-0 cells shifted by one site, so U1 = S X0 S^dagger.
- `eq_2`: implemented; build_circuit (U0 and U1 construction) and _increment. Cell states (|2j>+|2j+1>)/sqrt2 correspond to |j>|+> with qubit 0 as LSB. The shifted cells (|2j+1>+|2j+2>)/sqrt2 are obtained via the cyclic increment S, with indices mod N.
- `eq_3`: implemented; build_circuit: loop over steps. U = U1 U0 is applied 'steps' times, with U0 applied first in circuit order, so the circuit is U^t.
- `eq_4`: out_of_scope; no code location. Measurement and the Born-rule distribution are not part of the operation; the runner handles them.
- `eq_5`: background; no code location. The dimension comparison is only a motivating statement; the circuit uses the N-dimensional site space and no coin.

## Specification changes

- eq_2, eq_3: Generalized the N=4 instance to N=2^n for n in 2..12, so N must be a power of two (even). Reason: The sites are encoded in a binary qubit register, which makes the cyclic shift implementable with QFT.
- eq_1: The reflection about the tessellation-0 cells is written in closed form as Pauli X on the least significant qubit, and tessellation 1 is obtained by conjugating with the cyclic shift. Reason: This is an exact identity that avoids opaque dense unitaries.
- eq_3: The initial state |0> and measurement steps of the spec are not included in the circuit. Reason: The task requires an operation only; the runner prepares the input state.
- eq_4, eq_5: Scope narrowed to the staggered walk operator only. The coinless-to-coined transformation, mixing times and limiting distributions are not implemented. Reason: The abstract and spec give no explicit formulas for these.
