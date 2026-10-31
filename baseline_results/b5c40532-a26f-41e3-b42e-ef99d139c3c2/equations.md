# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct the time-averaged position distribution of a discrete-time coined quantum walk on the cycle graph C_N whose coin operator depends on a real 'memory parameter' lambda in [0,8] (the recycled-coin model), and the criterion for deciding whether that distribution is uniform or non-uniform as a function of lambda, the initial state, and N mod 4.

Scope: One smallest useful construction: a generic coined quantum walk on the N-cycle with a 2-dimensional coin, a lambda-dependent coin unitary C(lambda) whose explicit form is NOT given by the abstract and is left as an unspecified unitary placeholder, the standard conditional shift, and the time-averaged distribution over T steps compared against the uniform distribution 1/N. Tiny explicit instance (assumed): N = 4 vertices (2 position qubits), 1 coin qubit, T = 8 time steps, initial state |x=0> tensor |c=0>. Out of scope: the exact recycled-coin dynamics (how the coin is 'recycled' rather than reset), the specific functional dependence of the coin on lambda, the classification of which lambda values give non-uniform behavior, the N mod 4 analysis, and the proven relationship to the other memory-based quantum walk.

## Symbols

- $N$: Number of vertices of the cycle graph; domain: positive integer, N >= 3 (instance: N = 4)
- $n$: Number of position qubits, n = \lceil \log_2 N \rceil; domain: positive integer (instance: n = 2)
- $x$: Vertex (position) label on the cycle; domain: x \in \mathbb{Z}_N = \{0,\dots,N-1\}
- $c$: Coin state (direction of travel); domain: c \in \{0,1\}
- $\lambda$: Memory parameter of the recycled-coin walk, controlling the coin flip operator; domain: real, \lambda \in [0,8]
- $C(\lambda)$: Coin flip unitary depending on the memory parameter; domain: 2 \times 2 unitary matrix (explicit form unknown)
- $S$: Conditional shift operator moving the walker along the cycle; domain: unitary on \mathbb{C}^N \otimes \mathbb{C}^2
- $U(\lambda)$: One step of the walk; domain: unitary on \mathbb{C}^N \otimes \mathbb{C}^2
- $|\psi_t\rangle$: Walker state after t steps; domain: unit vector in \mathbb{C}^N \otimes \mathbb{C}^2
- $P_t(x)$: Probability of finding the walker at vertex x after t steps; domain: [0,1], \sum_x P_t(x)=1
- $\bar P_T(x)$: Time-averaged position distribution over the first T steps; domain: [0,1], \sum_x \bar P_T(x)=1
- $T$: Number of time steps included in the time average; domain: positive integer (instance: T = 8)

## eq_1: State space and computational basis

$$
\mathcal{H} = \mathcal{H}_P \otimes \mathcal{H}_C,\quad \mathcal{H}_P = \mathrm{span}\{|x\rangle : x \in \mathbb{Z}_N\},\quad \mathcal{H}_C = \mathrm{span}\{|0\rangle,|1\rangle\}
$$

Position register encodes the vertex x of the N-cycle as an integer in binary (little-endian, n qubits, values x >= N unused); the coin register is one qubit. Register ordering: position first, coin last.

Provenance: `standard_background`. Standard Hilbert-space structure of a coined discrete-time quantum walk on a degree-2 graph (the cycle).

Equation assumptions:

- Coin space is 2-dimensional; the recycled-coin model may use a different coin structure not determinable from the abstract.

## eq_2: Conditional shift on the cycle

$$
S\,|x\rangle|c\rangle = |(x + (-1)^{c}) \bmod N\rangle\,|c\rangle
$$

Coin value 0 moves the walker one vertex clockwise (+1), coin value 1 moves it counter-clockwise (-1), with modular (periodic) wrap-around on the cycle.

Provenance: `standard_background`. Standard flip-flop-free shift for coined walks on the cycle graph; the modular reduction encodes the cycle topology.

Equation assumptions:

- Direction convention (c=0 -> +1) is a choice; the paper may use the opposite convention.

## eq_3: Parameter-dependent coin and one-step walk operator

$$
U(\lambda) = S\,\big(I_N \otimes C(\lambda)\big),\quad C(\lambda) \in U(2),\ \lambda \in [0,8],\quad |\psi_t\rangle = U(\lambda)^t\,|\psi_0\rangle
$$

One step of the walk applies the lambda-dependent coin to the coin register and then the shift; t steps are t repeated applications. The explicit matrix C(lambda) is not given by the abstract and is a placeholder.

Provenance: `abstract_inferred`. The abstract states the memory parameter is real in [0,8] and enters through the coin flip operator; the coin-then-shift product structure is the standard form inferred for a coined walk. The recycled-coin mechanism may modify this product structure in ways not inferable here.

Abstract evidence: a real parameter, between zero and eight, which affects the walk’s coin flip operator

Equation assumptions:

- The walk is time-homogeneous (same U each step).
- The recycled-coin dynamics can be written as a single unitary of the form S(I tensor C(lambda)); the actual model may differ.

## eq_4: Position distribution at time t

$$
P_t(x) = \sum_{c \in \{0,1\}} \big|\langle x, c | \psi_t\rangle\big|^2
$$

Marginal probability of the position register obtained by tracing out (summing over) the coin.

Provenance: `standard_background`. Born rule applied to a computational-basis measurement of the position register.

## eq_5: Time-averaged distribution

$$
\bar P_T(x) = \frac{1}{T}\sum_{t=0}^{T-1} P_t(x),\qquad \bar P(x) = \lim_{T\to\infty} \bar P_T(x)
$$

Finite-T time average (exact arithmetic mean over the first T steps) and its limiting value; the abstract's object of study is the limiting average, which the finite instance only approximates.

Provenance: `abstract_inferred`. Standard definition of the time-averaged (Cesàro) distribution of a quantum walk, which is what 'time averaged distribution' conventionally denotes.

Abstract evidence: we will consider its time averaged distribution

Equation assumptions:

- The paper uses the standard Cesàro mean; the averaging window convention (0..T-1 vs 1..T) is a choice.

## eq_6: Uniformity criterion

$$
\text{uniform} \iff \bar P(x) = \frac{1}{N}\ \ \forall x \in \mathbb{Z}_N;\qquad \Delta_T = \sum_{x} \Big|\bar P_T(x) - \frac{1}{N}\Big|
$$

Non-uniform behavior means the limiting time average deviates from 1/N on some vertex; Delta_T is a finite-T total-variation-style diagnostic (approximation to the limiting statement).

Provenance: `abstract_inferred`. The abstract contrasts uniform and non-uniform time-averaged behavior; comparison against the uniform distribution 1/N on N vertices is the natural formalization.

Abstract evidence: only a few produce non-uniform behavior

Equation assumptions:

- The deviation diagnostic Delta_T is a proposed measure, not one stated in the abstract.

## Registers

- position: n = \lceil \log_2 N \rceil (instance: 2 qubits for N = 4) qubits; Encodes the vertex x of the cycle as an unsigned integer (little-endian); shift acts as modular +/-1 adder
- coin: 1 qubits; Direction of travel; acted on by C(lambda) and controls the shift

## Initial state

|\psi_0\rangle = |x=0\rangle \otimes |c=0\rangle (assumed localized instance; the abstract states the initial state matters but does not specify which initial states are studied)

## Measurement

Computational-basis measurement of the n position qubits after t steps (coin register discarded), repeated over shots for each t in 0..T-1 to estimate P_t(x).

## Classical postprocessing

Estimate P_t(x) from shot frequencies for each t, form the arithmetic mean over t (eq_5), compute Delta_T (eq_6), and repeat for a grid of lambda values in [0,8], several initial states, and cycle sizes N with different residues mod 4 to probe the dependence described in the abstract.

## Algorithm steps

1. Prepare the position register in |0> and the coin register in |0> (assumed initial state). (eq_1)
2. For each time t in {0,...,T-1}: apply U(lambda) = S(I tensor C(lambda)) t times to the initial state, using the chosen placeholder coin C(lambda) and the modular shift. (eq_3, eq_2)
3. Measure the position register in the computational basis to estimate P_t(x) for each t. (eq_4)
4. Average the estimated P_t(x) over t = 0..T-1 to obtain the finite-T time-averaged distribution and compare with 1/N. (eq_5, eq_6)

## Assumptions

- No experiment_scope was supplied; the tiny instance N = 4, T = 8, initial state |0>|0> is a reconstruction choice.
- The recycled-coin walk is modeled as a standard coined walk with a 2-dimensional coin and a time-homogeneous step operator; the true recycled-coin mechanism may require a different coin space or coupling and cannot be recovered from the abstract.
- C(lambda) is treated as an unspecified 2x2 unitary placeholder; no explicit lambda-dependence is invented.
- Position encoding is unsigned little-endian binary with modular wrap-around; the direction convention c=0 -> +1 is a choice.

## Missing information

- Explicit form of the coin flip operator C(lambda) and how the real parameter lambda in [0,8] enters it.
- Precise definition of the 'recycled coin' dynamics (how the coin is reused/recycled rather than reset, and the dimension of the coin space).
- Which specific lambda values yield non-uniform time-averaged behavior and the corresponding analytical or numerical evidence.
- The initial states considered and the exact dependence of the results on cycle size N modulo 4.
- The statement and proof of the relationship between the recycled-coin model and the other memory-based quantum walk.
