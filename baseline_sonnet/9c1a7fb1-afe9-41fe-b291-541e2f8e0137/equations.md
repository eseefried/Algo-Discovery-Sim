# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Approximately synthesize a single-qubit rotation exp(-i f(phi_1,...,phi_k) X) whose angle is a smooth computable function of input angles, using a Repeat-Until-Success (RUS) framework with few ancilla qubits. The abstract does not give the two primitives or the circuits, so only the target operation and generic RUS background can be specified.

Scope: One smallest construction: the target rotation for the product f(phi_1,phi_2)=phi_1*phi_2, plus the generic RUS success/failure structure and the per-attempt success probability. The abstract's actual two primitives, 3-ancilla multiplication and reciprocal circuits, and conventional-arithmetic cost analysis are outside the scope.

## Symbols

- $\phi_j$: input rotation angles encoded in the input rotation gates; domain: real numbers, j=1..k
- $f$: smooth computable function of the input angles; domain: smooth function from R^k to R
- $X$: Pauli X operator; domain: 2x2 matrix
- $R_f$: target single-qubit rotation e^{-i f X}; domain: SU(2)
- $\epsilon$: target approximation error; domain: positive real
- $p_s$: probability that an RUS attempt succeeds; domain: [0,1]
- $K$: Kraus operator associated with a successful ancilla outcome; domain: 2x2 matrix
- $K_{fail}$: Kraus operator associated with the failure outcome; domain: 2x2 matrix

## eq_1: Target rotation

$$
R_f(\phi_1,\ldots,\phi_k)=e^{-i f(\phi_1,\ldots,\phi_k)X}=\cos f\, I-i\sin f\, X
$$

Single-qubit rotation to be synthesized approximately; the second equality is exact for any real f since X^2=I.

Provenance: `abstract_explicit`. The abstract states the form of the target rotation; the expansion is a standard identity.

Abstract evidence: e^{-if(\phi_{1},\ldots,\phi_{k})X}

## eq_2: Approximation criterion

$$
\left\|K/\sqrt{p_s}-R_f\right\|\le\epsilon
$$

The rotation produced upon success approximates the target within error epsilon (operator norm, up to global phase).

Provenance: `assumption`. The abstract says synthesis is approximate but does not define the error metric. The operator norm is assumed.

Equation assumptions:

- Operator norm up to global phase is the error measure

## eq_3: RUS Kraus completeness

$$
K^\dagger K+K_{fail}^\dagger K_{fail}=I
$$

Measuring the ancilla yields success (apply K) or failure (apply K_fail). On failure the state is recovered or corrected and the attempt is repeated.

Provenance: `standard_background`. Generic RUS measurement structure; not the paper's specific circuits.

Equation assumptions:

- Single ancilla measurement outcome flags success
- Failure is correctable to repeat the attempt

## eq_4: Expected number of attempts

$$
\mathbb{E}[N]=1/p_s
$$

For independent attempts with constant success probability p_s, the number of attempts is geometric with this mean.

Provenance: `standard_background`. Geometric distribution under the assumption that failures can be fully recovered.

Equation assumptions:

- Constant p_s per attempt
- Failure leaves a state allowing an identical retry

## eq_5: Multiplication target

$$
f(\phi_1,\phi_2)=\phi_1\phi_2,\quad R_f=e^{-i\phi_1\phi_2 X}
$$

The scoped instance for approximate multiplication.

Provenance: `abstract_inferred`. The abstract claims RUS circuits for approximate multiplication; taking f as the product of two angles is an inferred interpretation, and the exact encoding is not given.

Abstract evidence: RUS circuits for approximate multiplication and reciprocals

Equation assumptions:

- Multiplication means multiplying the two rotation angles

## Registers

- data: 1 qubits; qubit on which R_f is approximately applied
- ancilla: 3 (the abstract's 'as few as 3' ancilla qubits for multiplication and reciprocal RUS circuits) qubits; RUS ancillas measured to flag success or failure

## Initial state

Arbitrary single-qubit data state |psi> with ancillas in |0>; the ancilla preparation is an assumption.

## Measurement

Ancilla measurement in the computational basis, with a designated outcome signalling success. The outcome pattern is assumed.

## Classical postprocessing

Classical control decides whether to repeat. No further postprocessing is justified by the abstract.

## Algorithm steps

1. Prepare the data qubit and ancillas in |0>. (no equation reference)
2. Apply the RUS primitive circuit built from input rotations by phi_1 and phi_2. The actual two primitives are not given in the abstract. (eq_5)
3. Measure the ancillas. On success the data qubit has undergone K, approximating R_f. (eq_1, eq_2, eq_3)
4. On failure, correct or reset the state and repeat. The expected number of attempts is 1/p_s. (eq_3, eq_4)

## Assumptions

- The scope is restricted to f=phi_1*phi_2 as the smallest useful instance.
- The error metric is operator norm up to global phase.
- The failure branch is recoverable.
- The specific primitives, circuits, and success probabilities of the paper are not reconstructed.

## Missing information

- The two basic primitives used to synthesize f
- The explicit RUS circuits and gate sets
- How inputs phi_j are encoded
- Success probabilities and error scaling
- The reciprocal construction
- The conventional-arithmetic qubit cost analysis
- Failure recovery details
