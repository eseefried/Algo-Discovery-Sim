# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Bounded-occurrence Max E3LIN2: given linear equations over GF(2), each with exactly three boolean variables and right-hand side 0 or 1, with each variable in at most D equations, find a string satisfying as many equations as possible using level-one QAOA.

Scope: Problem definition and the stated approximation guarantees only. Circuit-level QAOA details (cost Hamiltonian, mixer, angles) are not given in the abstract; any such detail would be standard background or assumption.

## Symbols

- $D$: Maximum number of equations any variable appears in; domain: positive integer
- $z$: Boolean assignment string to the variables; domain: {0,1}^n
- $m$: Number of equations; domain: positive integer
- $f$: Guaranteed fraction of satisfied equations, with random-string baseline 1/2; domain: [0,1]

## eq_1: Random baseline

$$
f_{\mathrm{random}}=\frac{1}{2}
$$

A random string satisfies half of the equations on average.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: A random string will satisfy 1/2 of the equations.

## eq_2: Level-one QAOA worst-case guarantee

$$
f_{\mathrm{QAOA}}\ge\frac{1}{2}+\frac{1}{101D^{1/2}\ln D}
$$

Fraction of satisfied equations guaranteed by level-one QAOA.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: \left(\frac{1}{2}+\frac{1}{101D^{1/2}\,ln\,D}\right)

## eq_3: Typical-case QAOA fraction

$$
f_{\mathrm{typ}}=\frac{1}{2}+\frac{1}{2\sqrt{3e}\,D^{1/2}}
$$

Fraction satisfied in the typical case.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: \left(\frac{1}{2}+\frac{1}{2\sqrt{3e}\,D^{1/2}}\right)

## eq_4: Classical comparison

$$
f_{\mathrm{cl}}=\frac{1}{2}+\frac{c}{D^{1/2}}
$$

Classical algorithm guarantee with an unspecified constant c.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: \left(\frac{1}{2}+\frac{constant}{D^{1/2}}\right)

## Registers

- z: n (one qubit per boolean variable) qubits; Holds the candidate assignment string; measured in the computational basis

## Initial state

Uniform superposition over all n-bit strings (|+>^{\otimes n}), the standard QAOA start state (assumed, not in abstract)

## Measurement

Measure all n qubits in the computational basis to obtain a candidate string z (standard QAOA readout, assumed). Repeat as needed; the abstract's guarantees concern the satisfied fraction of the output string.

## Classical postprocessing

Evaluate the number of satisfied equations for each sampled z classically and keep the best string. Sampling count and any high-probability argument are not given in the abstract.

## Algorithm steps

1. Prepare |+>^n on the variable register (standard QAOA background). (no equation reference)
2. Apply level-one (p=1) phase-separation unitary from the cost Hamiltonian encoding the equations, with an angle gamma (assumed standard form; not in abstract). (eq_2)
3. Apply the p=1 mixing unitary with transverse-field angle beta (assumed standard); angles are chosen so the expected satisfied fraction exceeds the 1/2 random baseline. (eq_1, eq_2, eq_3)

## Assumptions

- Level-one QAOA uses the standard form: uniform start, one cost layer, one mixer layer, with one qubit per variable.
- Computational-basis measurement with classical evaluation of satisfied equations is assumed.

## Missing information

- QAOA cost Hamiltonian, mixer and angles are not in the abstract
- Explicit gamma, beta values and their dependence on D are not given in the abstract
- Number of samples and success probability or concentration argument are not given
- Precise meaning of 'typical case' is not defined in the abstract
- Value of the classical constant is not given
- Number of samples and concentration argument not given
- Precise meaning of 'typical case' not defined
