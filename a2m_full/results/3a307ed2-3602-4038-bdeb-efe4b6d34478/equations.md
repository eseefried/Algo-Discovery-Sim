# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Bounded-occurrence Max E3LIN2: m equations, each x_a+x_b+x_c = b_k mod 2 on three distinct boolean variables, each variable in at most D equations. Goal: a string satisfying more than 1/2 of the equations, using level-one (p=1) QAOA.

Scope: One tiny explicit instance (n about 4-6 variables, a handful of equations, no black box) with the p=1 QAOA circuit, exact statevector expectation, a grid search over (gamma,beta), and sampling with best-string selection. The D^{-1/2} and D^{-1/2}/ln D advantage proofs, the worst-case ln D analysis, and the comparison to the classical algorithm are outside scope.

## Symbols

- $n$: number of boolean variables = number of qubits; domain: positive integer under the qubit cap
- $m$: number of equations; domain: positive integer
- $D$: maximum number of equations containing any one variable; domain: positive integer
- $s_k$: sign of equation k: +1 if right-hand side is 0, -1 if it is 1; domain: {+1,-1}
- $a_k,b_k,c_k$: the three distinct variable indices of equation k; domain: {0..n-1}
- $\gamma,\beta$: QAOA phase-separator and mixer angles; domain: real
- $C$: cost operator, the number of satisfied equations; domain: Hermitian diagonal operator
- $z$: measured bit string, bit i (bits[::-1][i] in Qiskit counts) is variable i; domain: {0,1}^n

## eq_1: Cost operator

$$
C=\sum_{k=1}^{m}\frac{1}{2}\left(1-s_k Z_{a_k}Z_{b_k}Z_{c_k}\right)
$$

Counts satisfied equations: the term is 1 when the parity of the three bits equals the right-hand side, otherwise 0. The sign convention is Z=+1 for bit 0.

Provenance: `abstract_inferred`. Standard encoding of a parity constraint as a Z-string; the exact form is taken from the sketch and not stated in the abstract.

Abstract evidence: each equation says that the sum of the variables mod 2 is 0 or is 1

Equation assumptions:

- Z eigenvalue (-1)^{z_i}
- s_k=(-1)^{b_k}

## eq_2: p=1 QAOA state

$$
|\gamma,\beta\rangle=e^{-i\beta B}e^{-i\gamma C}|+\rangle^{\otimes n},\quad B=\sum_j X_j
$$

Level-one QAOA state. The phase separator is a product of commuting ZZZ rotations, up to a global phase, and the mixer is RX(2*beta) on every qubit.

Provenance: `abstract_inferred`. The abstract names level-one QAOA. The exact angle conventions are standard background and are not given in the abstract.

Abstract evidence: We apply our recent Quantum Approximate Optimization Algorithm [1]

Equation assumptions:

- Angle sign and scale convention may be flipped, because the grid search covers both signs

## eq_3: Per-equation gate decomposition

$$
e^{i\gamma s_k Z_aZ_bZ_c/2}=\mathrm{CX}_{a\to c}\,\mathrm{CX}_{b\to c}\,R_Z^{(c)}(-\gamma s_k)\,\mathrm{CX}_{b\to c}\,\mathrm{CX}_{a\to c}
$$

The CX pair computes the parity a xor b xor c onto c, RZ acts on c, then the parity is uncomputed. This uses R_Z(θ)=e^{-iθZ/2}. The overall sign is a convention, and a sign flip equals gamma -> -gamma.

Provenance: `standard_background`. Standard parity-phase gadget; the sign is fixed so that it matches e^{-i gamma C} up to global phase.

Equation assumptions:

- Qiskit RZ convention
- global phase ignored

## eq_4: Objective and satisfied fraction

$$
F(\gamma,\beta)=\langle\gamma,\beta|C|\gamma,\beta\rangle,\quad \frac{F}{m}=\frac12-\frac{1}{2m}\sum_k s_k\langle Z_{a_k}Z_{b_k}Z_{c_k}\rangle
$$

Expected number of satisfied equations. A random string gives m/2. The advantage is the deviation of F/m from 1/2.

Provenance: `abstract_inferred`. Follows directly from eq_1 and the abstract's baseline of 1/2.

Abstract evidence: A random string will satisfy 1/2 of the equations.

## eq_5: Claimed advantage targets

$$
\frac{F}{m}\ge\frac12+\frac{1}{101D^{1/2}\ln D}\ \text{(worst case)},\qquad \frac{F}{m}\approx\frac12+\frac{1}{2\sqrt{3e}\,D^{1/2}}\ \text{(typical)}
$$

Reference values to compare against the simulated F/m. On tiny instances these asymptotic bounds are only indicative, since D is small.

Provenance: `abstract_explicit`. Both values are stated in the abstract. The typical-case value is quoted from the abstract's second expression.

Abstract evidence: \left(\frac{1}{2}+\frac{1}{101D^{1/2}\,ln\,D}\right)

Equation assumptions:

- Asymptotic in large D; not expected to be tight for small instances

## Registers

- q: n qubits; one qubit per boolean variable, with qubit i = variable i; no ancillas
- c: n qubits; classical bits for the final readout, with measure(i,i)

## Initial state

|0>^n followed by H on every qubit, giving |+>^n

## Measurement

Measure all n qubits in the computational basis only if counts are required. Variable i is bits[::-1][i] of the Qiskit counts key. Omit measurements if the statevector is read.

## Classical postprocessing

For each sampled z, count the equations with (z_a+z_b+z_c) mod 2 = b_k. Report the mean (an estimate of F) and the best string.

## Algorithm steps

1. Apply H to all n qubits. (eq_2)
2. For each equation k, apply CX(a,c), CX(b,c), RZ on c with angle ±gamma*s_k, CX(b,c), CX(a,c). (eq_1, eq_3)
3. Apply RX(2*beta) on every qubit. (eq_2)
4. Grid-search (gamma,beta) over the exact statevector expectation F. Initial guesses are gamma ~ 1/sqrt(D) and beta ~ pi/8. Use the maximizing angles. (eq_4)
5. If counts are required, measure all qubits, sample repeatedly, evaluate the satisfied-equation count of each string classically, and keep the best string. (eq_4)

## Assumptions

- Smallest useful instance: a few equations on 4-6 variables, chosen by the later stage
- p=1 only
- The angle sweep covers both signs, so the RZ sign convention does not matter
- No black-box oracle or query; the equations are compiled directly into gates
- The qubit count n is under the cap

## Missing information

- The paper's analytic light-cone formula for <ZZZ> is not given in the abstract. The sketch's form sin(4beta) sin(gamma) cos(gamma)^k is unverified, so I do not state it as an equation.
- The exact angles used in the worst-case ln D analysis are not specified.
- The explicit rule for choosing gamma and beta in the proofs is not stated in the abstract.
- No concrete instance is given.
