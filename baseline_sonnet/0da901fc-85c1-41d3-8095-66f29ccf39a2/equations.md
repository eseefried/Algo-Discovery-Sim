# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Unstructured search over N items with a control-qubit-based modification of Tulsi's quantum search, with intermediate measurements of the control every few steps. The abstract states no explicit equations, so only background Grover/Tulsi-style relations and a small assumed instance can be given.

Scope: Smallest useful construction: standard Grover-type search iterate on an n-qubit data register (N=4, one marked item) with one control qubit measured every k steps (assumed), plus the success probability and a generic measurement-dephasing channel on the control. Tulsi's specific control-qubit construction, the paper's alternative angular parameter, MI and CCM correlation measures, and order estimates are outside scope.

## Symbols

- $N$: number of database items; domain: N=2^n, positive integer
- $n$: number of data qubits; domain: positive integer
- $w$: marked item index; domain: {0,...,N-1}
- $\theta$: angular parameter of the search rotation (paper's alternative choice unspecified); domain: real, \sin\theta=1/\sqrt{N} in the standard case
- $k$: number of steps between control measurements (time lapse); domain: positive integer
- $t$: iteration count; domain: nonnegative integer
- $G$: search iterate on data register; domain: unitary on 2^n dimensions
- $\rho$: joint state of data register and control qubit; domain: density operator
- $P_c$: projector onto control basis state c; domain: c in {0,1}

## eq_1: Standard Grover iterate

$$
G=-(I-2|s\rangle\langle s|)(I-2|w\rangle\langle w|),\quad |s\rangle=N^{-1/2}\sum_{x=0}^{N-1}|x\rangle
$$

Baseline search iterate that Tulsi-type algorithms modify.

Provenance: `standard_background`. Textbook Grover operator; not the paper's modified operator.

Equation assumptions:

- Single marked item
- Control qubit not yet included

## eq_2: Success probability

$$
p_t=\sin^2\big((2t+1)\theta\big),\quad \sin\theta=1/\sqrt N
$$

Probability of measuring the marked item after t iterations without intermediate measurements.

Provenance: `standard_background`. Standard Grover result; the paper uses a different angular parameter choice, which is not given.

Equation assumptions:

- Ideal unitary evolution

## eq_3: Controlled step with control qubit

$$
U=|0\rangle\langle 0|_c\otimes I+|1\rangle\langle 1|_c\otimes G
$$

Assumed generic control-qubit structure; Tulsi's actual construction is not reproduced.

Provenance: `assumption`. Placeholder to make control-qubit measurement well-defined.

Equation assumptions:

- Control initialized in |+> so that it acts as a control
- Actual Tulsi construction differs/unknown

## eq_4: Intermediate control measurement

$$
\rho\mapsto\sum_{c\in\{0,1\}}(P_c\otimes I)\rho(P_c\otimes I)\quad\text{applied after every }k\text{ steps}
$$

Non-selective projective measurement of the control qubit every k steps, which dephases it.

Provenance: `abstract_inferred`. The abstract says the control is measured at intermediate times; the non-selective channel form is an inference.

Abstract evidence: search algorithm with intermediate measurements of the control

Equation assumptions:

- Computational-basis measurement
- Outcomes not post-selected

## eq_5: Total evolution

$$
\rho_T=\big(\mathcal M\circ \mathcal U^{k}\big)^{T/k}(\rho_0),\quad \mathcal U(\rho)=U\rho U^\dagger
$$

Evolution with measurement every k steps; k=1 corresponds to measuring every step.

Provenance: `assumption`. Composition of the assumed step and measurement; k divides T.

Equation assumptions:

- k divides T
- \mathcal M is the channel in eq_4

## Registers

- data: n (n=2 in tiny instance, N=4) qubits; search register holding the item index, computational-basis integer encoding
- control: 1 qubits; control qubit measured at intermediate times

## Initial state

|+\rangle_c\otimes|s\rangle_data with |s\rangle uniform superposition (assumed)

## Measurement

Intermediate computational-basis measurements of the control every k steps; final measurement of the data register in the computational basis.

## Classical postprocessing

Estimate success probability versus step count for several k and fit scaling of the required steps with N. Mutual Information and Cumulative Correlation Measure computation not specified.

## Algorithm steps

1. Prepare control and data registers in the initial state. (no equation reference)
2. Apply the controlled search step U (assumed construction) k times. (eq_1, eq_3)
3. Measure the control qubit non-selectively; repeat until T steps. (eq_4, eq_5)
4. Evaluate marked-item probability p_t versus the unmeasured baseline. (eq_2)

## Assumptions

- Tiny instance N=4, one marked item
- Generic controlled-G structure replaces Tulsi's unspecified construction
- Measurement modeled as non-selective dephasing

## Missing information

- Tulsi's exact modified operator and control-qubit role
- The paper's alternative angular parameter choice
- Definitions of MI and CCM used
- Order-estimation method and the time lapses studied
- Quantitative results
