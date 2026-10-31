# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Use the one-query Bernstein-Vazirani algorithm to identify a completely specified linear Boolean function with certainty, a two-query variant to identify whether a Boolean function is affine (and recover it), and apply both as bounded-error quantum algorithms (success probability at least 2/3) to certain classes of incompletely defined linear and affine Boolean functions.

Scope: Abstract-level reconstruction of the problem and a small finite-instance equation set; the two-query circuit details and the incompletely defined function classes are not given in the abstract and are left unspecified.

## Symbols

- $f$: Boolean function, linear or affine; domain: f:{0,1}^n -> {0,1}
- $a$: hidden linear coefficient string; domain: a in {0,1}^n
- $b$: affine constant bit; domain: b in {0,1}
- $U_f$: phase or standard oracle for f; domain: unitary on n (+1) qubits

## eq_1: Linear function

$$
f(x)=a\cdot x \bmod 2
$$

Linear Boolean function targeted by the one-query algorithm.

Provenance: `abstract_inferred`. Standard definition of a linear Boolean function, matching the abstract's phrase.

Abstract evidence: identify a completely specified linear Boolean function

Equation assumptions:

- Linear means over GF(2) with no constant term

## eq_2: Affine function

$$
f(x)=a\cdot x \oplus b
$$

Affine Boolean function targeted by the two-query algorithm.

Provenance: `abstract_inferred`. Standard definition of an affine function over GF(2).

Abstract evidence: if the provided Boolean function is affine

Equation assumptions:

- Affine means linear plus constant b

## eq_3: BV phase oracle output

$$
H^{\otimes n}\frac{1}{\sqrt{2^n}}\sum_x(-1)^{a\cdot x}|x\rangle=|a\rangle
$$

After Hadamards, a phase-oracle query on a linear function yields |a> deterministically.

Provenance: `standard_background`. Standard Bernstein-Vazirani mechanism, background only.

Equation assumptions:

- Phase oracle form is used

## Registers

- x: n qubits; input register queried in superposition; holds a after the final Hadamards for linear f
- anc: 1 (optional) qubits; ancilla in |-> for phase kickback if a standard oracle is used

## Initial state

|0>^n (plus ancilla |1> then Hadamard to |-> if standard oracle)

## Measurement

Measure the n-qubit input register in the computational basis after the final Hadamards. For completely specified linear f the outcome is a with certainty. For the two-query variant, measure after each query round (assumed structure).

## Classical postprocessing

Linear case: output the measured string as a. Affine case (assumed): compare the two outcomes to decide whether f is affine and recover a and b. Incompletely defined case: accept the output as correct with probability of success at least 2/3, and repeat or take a majority vote if needed; the exact rule is not given in the abstract.

## Algorithm steps

1. One-query BV: apply H^{⊗n} to |0^n>, query the phase oracle once, apply H^{⊗n}, giving |a> for linear f. (eq_1, eq_3)
2. Two-query variant for affine f (assumed structure, not given in abstract): run the BV circuit twice, each with one oracle query, so the two outputs can be compared to determine whether f is affine and to recover a and b. The exact second-query construction is unspecified. (eq_2, eq_3)

## Assumptions

- Standard GF(2) definitions of linear and affine functions used
- Second query's circuit is an assumed repetition of the BV circuit, not taken from the abstract
- Second query is a repetition or variant of the BV circuit
- Measurement is in the computational basis on the input register
- Postprocessing rule for affinity decision is assumed

## Missing information

- Two-query circuit construction
- Definition of the incompletely defined function classes
- Analysis giving success probability at least 2/3
- Exact second-query construction for affinity detection
- Exact decision rule for affinity from the measurement outcomes
