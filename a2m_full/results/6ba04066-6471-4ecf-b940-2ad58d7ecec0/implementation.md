# Equation to Qiskit

Z_2 Deutsch / two-element group-multiplication operation: one query to the oracle U_f|x>|y>=|x>|y xor f(x)> on a control qubit x and target qubit y, followed by H on x. With the runner preparing |+>|->, the control ends in |f0 xor f1>, the Z_2 product of the two tuple elements. This narrows the scope to G=Z_2.

Source equation run: `7b9ec76c-e84b-4818-acc5-d07486771b78`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: x / control, expected input |+>, output |f0 xor f1> in the computational basis
- qubit 1: y / target, expected input |->, left unchanged up to global phase
- little-endian: qubit 0 is the least significant bit

## Assumptions

- The runner prepares qubit 0 in |+> and qubit 1 in |->.
- The Z_2 elements are encoded as bits 0 and 1, with the group operation XOR.
- The oracle is a standard permutation oracle U_f|x>|y>=|x>|y xor f(x)>.

## Unresolved issues

- Explicit group-multiplication query protocol for general G is not specified.
- Group Fourier transform circuit for non-abelian G is not implemented.
- S_3 conjugation (hidden conjugating element) instance is not implemented.
- Whether the 2/|G| strategy uses the regular representation is unknown.

## Equation mapping

- `eq_1`: background; no code location. General optimal-state formula. For Z_2 the relevant input |+>|-> is prepared by the runner, so no state preparation is implemented here.
- `eq_2`: background; no code location. General success-probability formula. Not implemented as code, since it is a classical figure of merit and the circuit contains no measurement.
- `eq_3`: background; no code location. For |G|=2 the value 2/|G| equals 1, which is the expected deterministic outcome of this circuit. It is a property of the construction, not code.
- `eq_4`: implemented; build_circuit: the oracle block (X/CX gates) followed by qc.h(0). Z_2 phase-kickback oracle with one query, then H on the control. For input |+>|-> the phase (-1)^(f0+f1) is kicked back and H maps the control to |f0 xor f1>.
- `eq_5`: out_of_scope; no code location. The S_3 conjugation oracle and the hidden conjugating element problem are not implemented. They need a group Fourier transform for non-abelian G, which the specification leaves unresolved.

## Specification changes

- eq_4: The oracle is parameterised by two Z_2 elements f0, f1, so the oracle is U_f with f(x) in {f0,f1}. The hidden quantity is a=f0 xor f1. The specification's single hidden-a oracle is not used. Reason: The specification gave no explicit group-multiplication query protocol for two elements. The standard Deutsch oracle is the Z_2 case of the stated generalisation.
- eq_4: The final H on the control is included in the operation. The inputs |+> and |-> are left to the runner. The phase relation is stated as (|0>+(-1)^a|1>)/sqrt2 -> |a>, not as H(-1)^a|->. Reason: The circuit must be a state-preparation-free unitary. The original notation was ambiguous.
- eq_1, eq_2, eq_3, eq_5: Scope is narrowed to G=Z_2. There is no general-G or S_3 circuit. Reason: The general group Fourier transform and the multiplication protocol for arbitrary G are listed as missing information.
- eq_1, eq_2: Normalisation remark corrected: the weights sum to 1 exactly when sum_rho d_rho*min(d_rho,m_rho)=|G|. This does not simply mean that R contains every irrep. It requires m_rho>=d_rho for all rho. Reason: The earlier statement was imprecise.
