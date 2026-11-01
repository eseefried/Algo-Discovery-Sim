# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Characterize which two-outcome generalized measurements (Kraus operators with given singular values) can be decomposed into a sequence of weak measurements, each from a system-qubit probe interaction with constant Hamiltonian, interleaved with arbitrary unitary pulses and feedback.

Scope: One iteration of a weak measurement with a qubit probe, a tiny qubit-system instance, and the composition of iterations into a two-outcome Kraus operator with two distinct singular values. Excluded: the paper's characterization proof, the explicit Hamiltonian and pulse schedule, the continuous-time limit, and the feedback control rule.

## Symbols

- $M_0,M_1$: Kraus operators of a two-outcome generalized measurement; domain: complex 2x2 matrices
- $H_{SP}$: constant system-probe interaction Hamiltonian; domain: Hermitian operator on C^2 tensor C^2, unspecified
- $\epsilon$: small interaction strength/time parameter per iteration; domain: positive real, assumed small
- $U_k$: unitary pulse applied on the system before iteration k; domain: SU(2) on the system
- $|0\rangle_P$: initial probe state; domain: qubit state
- $K_{j}^{(k)}$: weak-measurement Kraus operator for probe outcome j at iteration k; domain: complex 2x2 matrices
- $s_1,s_2$: singular values of a Kraus operator; domain: nonnegative reals

## eq_1: Two-outcome completeness

$$
M_0^\dagger M_0+M_1^\dagger M_1=I
$$

Completeness relation for a two-outcome generalized measurement.

Provenance: `standard_background`. Standard definition of a two-outcome generalized measurement; the abstract only names such measurements.

## eq_2: Weak measurement via probe

$$
K_j=({}_P\langle j|\otimes I_S)\,e^{-i\epsilon H_{SP}}\,(|0\rangle_P\otimes I_S)
$$

Kraus operators on the system from a probe interaction followed by a probe measurement in a computational basis.

Provenance: `assumption`. The abstract describes a qubit probe with constant interaction Hamiltonian but gives no form. This is the standard construction, with an assumed probe readout basis and initial probe state.

Equation assumptions:

- Probe starts in |0>
- Probe is read out in the computational basis
- Exact H_SP is not specified

## eq_3: Iterated feedback composition

$$
M_{\mathbf{j}}=K_{j_n}U_n\cdots K_{j_1}U_1,\quad \sum_{\mathbf{j}}M_{\mathbf{j}}^\dagger M_{\mathbf{j}}=I
$$

Product of weak-measurement Kraus operators interleaved with unitary pulses; a trajectory outcome record j is later coarse-grained into the two outcomes of the target measurement.

Provenance: `abstract_inferred`. Inferred from the stated iterated weak measurements with unitary pulses; the coarse-graining rule is not given.

Abstract evidence: even given the ability to perform arbitrary unitary pulses throughout the continuous decomposition

Equation assumptions:

- Pulses occur between iterations
- Stopping rule and outcome coarse-graining are unspecified

## eq_4: Singular-value constraint on achievable measurements

$$
M_a=V_a\,\mathrm{diag}(s_{a,1},s_{a,2})\,W_a,\quad s_{a,1}\neq s_{a,2}\ \text{for the achievable class}
$$

Singular value decomposition of an achievable Kraus operator; the abstract states that only measurements with two distinct singular values are achievable, which is the generic qubit case.

Provenance: `abstract_inferred`. Direct reading of the abstract claim stated as an SVD, which is a standard background tool; the exact condition is paraphrased.

Abstract evidence: only generalized measurements with two distinct singular values are achievable

Equation assumptions:

- Applies to qubit system, per Kraus operator

## Registers

- S: 1 qubit (assumed) qubits; system being measured
- P: 1 qubit qubits; probe for each weak measurement iteration, fresh per iteration (assumed)

## Initial state

System in an arbitrary state |psi>; a fresh probe in |0> for each iteration (assumed).

## Measurement

Computational-basis measurement of the probe after each interaction (assumed).

## Classical postprocessing

Feedback rule choosing the next pulse and the final assignment of the outcome record to M_0 or M_1; neither is specified in the abstract.

## Algorithm steps

1. Prepare a fresh probe qubit in |0>. (eq_2)
2. Apply a system unitary pulse U_k, then evolve under the constant H_SP for a short time. (eq_2, eq_3)
3. Measure the probe to obtain outcome j_k and update the system with K_{j_k}. (eq_2)
4. Repeat with feedback-chosen pulses until a stopping condition, then compare the accumulated operator to the target M_a. (eq_3, eq_4, eq_1)

## Assumptions

- Probe readout basis, probe initial state, and the form of H_SP are assumed
- Instance is a single system qubit
- Fresh probe per iteration

## Missing information

- Explicit interaction Hamiltonian
- Pulse schedule and feedback rule
- Stopping criterion and coarse-graining of outcomes
- Precise characterization theorem and continuous-time limit
- Explicit decomposition construction
