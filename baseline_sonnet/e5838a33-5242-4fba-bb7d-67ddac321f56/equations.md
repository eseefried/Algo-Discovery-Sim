# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Bounded-occurrence Max E3LIN2: given m equations x_a+x_b+x_c = b (mod 2) over boolean variables, each variable in at most D equations, use level-one QAOA to output a string satisfying a fraction 1/2 + advantage of equations.

Scope: Define the E3LIN2 cost function, the level-one QAOA state and expectation objective, and the abstract's stated guarantees. Detailed level-one expectation formulas, the optimization of angles, and the proofs of the guarantees are outside scope. A tiny instance is not chosen beyond the generic form.

## Symbols

- $n$: number of boolean variables; domain: positive integer
- $m$: number of equations; domain: positive integer
- $z_j$: spin value of variable j, z_j = (-1)^{x_j}; domain: {+1,-1}
- $b_k$: right-hand side of equation k; domain: {0,1}
- $D$: maximum number of equations containing any variable; domain: positive integer
- $C_k$: clause operator, equal to 1 if equation k is satisfied and 0 otherwise; domain: diagonal operator
- $C$: total cost operator, the number of satisfied equations; domain: diagonal operator
- $\gamma,\beta$: level-one QAOA angles; domain: real
- $s_k$: sign of equation k, s_k = (-1)^{b_k}; domain: {+1,-1}

## eq_1: Clause operator

$$
C_k=\frac{1}{2}\left(1+s_k Z_{a_k}Z_{b_k}Z_{c_k}\right),\quad C=\sum_{k=1}^m C_k
$$

Clause k is satisfied iff the parity of its three variables equals b_k, which is expressed through a product of Pauli Z operators.

Provenance: `standard_background`. The standard encoding of a mod-2 equation into a Z-product; the abstract only states the equation form.

Equation assumptions:

- Z eigenvalue (-1)^{x}

## eq_2: Level-one QAOA state

$$
|\gamma,\beta\rangle=e^{-i\beta B}e^{-i\gamma C}|+\rangle^{\otimes n},\quad B=\sum_{j=1}^n X_j
$$

Standard level-one QAOA state with a phase-separation step followed by a mixer step.

Provenance: `standard_background`. The abstract refers to a level-one QAOA but gives no explicit definition, so this is recalled standard form.

Equation assumptions:

- Standard transverse-field mixer
- Initial uniform superposition

## eq_3: Objective

$$
F(\gamma,\beta)=\langle\gamma,\beta|C|\gamma,\beta\rangle
$$

Expected number of satisfied equations, to be maximized over the angles.

Provenance: `standard_background`. Standard QAOA objective; the specific angle choice that gives the abstract's bounds is not reconstructed here.

## eq_4: Worst-case guarantee

$$
\frac{\mathbb{E}[\#\text{sat}]}{m}\ge\frac{1}{2}+\frac{1}{101\,D^{1/2}\ln D}
$$

Claimed satisfied fraction for level-one QAOA on bounded-occurrence instances.

Provenance: `abstract_explicit`. Stated in the abstract. Whether it holds in expectation or with high probability is not specified, so the expectation form here is an interpretation.

Abstract evidence: We show that the level one QAOA will efficiently produce a string that satisfies $\left(\frac{1}{2}+\frac{1}{101D^{1/2}\,ln\,D}\right)$ times the number of equations.

Equation assumptions:

- Interpreted as an expected or achievable fraction

## eq_5: Typical-case guarantee

$$
\frac{\#\text{sat}}{m}\approx\frac{1}{2}+\frac{1}{2\sqrt{3e}\,D^{1/2}}
$$

Claimed typical-case satisfied fraction.

Provenance: `abstract_explicit`. Stated in the abstract. The meaning of 'typical case' is not defined there.

Abstract evidence: We also show that in the typical case the quantum computer will output a string that satisfies $\left(\frac{1}{2}+\frac{1}{2\sqrt{3e}\,D^{1/2}}\right)$ times the number of equations.

Equation assumptions:

- 'Typical case' is undefined in the abstract

## Registers

- q: n qubits; one qubit per boolean variable, with qubit j encoding x_j in the computational basis

## Initial state

|+>^{\otimes n}, assumed standard uniform superposition

## Measurement

Measure all qubits in the computational basis to obtain a candidate string x.

## Classical postprocessing

Count satisfied equations for the measured string and optionally repeat to keep the best string.

## Algorithm steps

1. Prepare the uniform superposition on n qubits. (eq_2)
2. Apply the phase-separation unitary exp(-i gamma C) built from the Z_aZ_bZ_c clause terms. (eq_1, eq_2)
3. Apply the mixer exp(-i beta sum X_j). (eq_2)
4. Choose angles (gamma, beta) to meet the claimed guarantees; the specific values are not given in the abstract. (eq_3, eq_4, eq_5)

## Assumptions

- Standard QAOA ansatz and Z-product clause encoding are assumed, not taken from the abstract.
- Angle choices are not specified.

## Missing information

- Explicit angle schedule or optimal (gamma,beta) as a function of D
- Closed-form level-one expectation for a clause given its neighboring clauses
- Precise definition of 'typical case' and of the success criterion (expectation vs. high probability)
- Proofs of the bounds, and the classical comparison algorithm details
