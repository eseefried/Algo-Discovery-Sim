# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Characterize the time-averaged probability distribution of the recycled-coin quantum walk on the cycle graph C_N, and how it depends on the real memory parameter (between 0 and 8) in the coin flip operator, the initial state, and N mod 4. Also relate this model to another recently proposed memory-based quantum walk.

Scope: Abstract-level reconstruction of the cycle-graph study: definition of the time-averaged distribution and the parameter dependence. The explicit recycled-coin operator and the proofs are not given in the abstract and are not reconstructed.

## Symbols

- $N$: number of vertices of the cycle graph; domain: positive integer
- $\bar{P}(x)$: time-averaged probability of finding the walker at vertex x; domain: [0,1]
- $P_t(x)$: probability of finding the walker at vertex x after t steps; domain: [0,1]
- $m$: memory parameter of the coin flip operator; domain: real, 0 to 8

## eq_1: Time-averaged distribution

$$
\bar{P}(x)=\lim_{T\to\infty}\frac{1}{T}\sum_{t=0}^{T-1}P_t(x)
$$

Definition of the time-averaged distribution over the cycle vertices.

Provenance: `abstract_inferred`. The abstract studies the time averaged distribution. The explicit limit formula is the standard definition.

Abstract evidence: time averaged distribution

Equation assumptions:

- Limit exists for the finite cycle

## eq_2: Uniform limit

$$
\bar{P}(x)=\frac{1}{N}\ \ \forall x
$$

Uniform behavior, which the abstract suggests holds for most parameter values m.

Provenance: `abstract_inferred`. Non-uniform behavior is rare, so uniform is the generic case. The exact conditions are not stated.

Abstract evidence: only a few produce non-uniform behavior

Equation assumptions:

- Applies to generic m and initial states

## Registers

- position: ceil(log2 N) qubits (N basis states) qubits; walker vertex x on the cycle C_N
- coin: unknown (abstract does not specify; assumed one qubit) qubits; coin state, recycled between steps and acted on by the m-dependent flip operator

## Initial state

Unspecified in the abstract; the abstract says the initial state affects behavior. Assume a localized walker at x=0 with a chosen coin state, to be varied.

## Measurement

Measure the position register in the computational basis after t steps, repeated over many runs to estimate P_t(x); the coin is not needed for the distribution. Repeat for various t, m, initial states and N mod 4 classes.

## Classical postprocessing

Average the estimated P_t(x) over t (eq_1 truncated at finite T) to approximate the time-averaged distribution, and compare with 1/N (eq_2), e.g. via total variation distance, to classify uniform vs non-uniform behavior for each m.

## Algorithm steps

1. Prepare the position register at a vertex and the coin in a chosen initial state. (no equation reference)
2. Apply the memory-parameter-dependent coin flip operator (explicit form not given in the abstract), recycling the coin between steps. (no equation reference)
3. Apply the conditional shift on the cycle, then repeat for t steps and accumulate P_t(x) to form the time average. (eq_1, eq_2)

## Assumptions

- The time-averaged distribution is the standard Cesaro limit.
- Coin is assumed to be a single qubit; the circuit is a generic coined-walk skeleton, not the paper's exact construction.
- Single-qubit coin and localized initial position assumed for the circuit skeleton.
- Measurement is a position-basis measurement; the abstract does not specify the measurement protocol.

## Missing information

- Explicit recycled-coin coin operator as a function of m
- Which parameter values give non-uniform behavior
- Details of the relationship to the other memory-based walk
- Exact coin dimension and initial states studied
