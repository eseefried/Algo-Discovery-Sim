# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Quantum-walk formulation of Grover search on N items where each hop has a failure (stay-put) amplitude epsilon due to potential barriers; the abstract claims epsilon must be O(1/sqrt(N)) to retain O(sqrt(N)) runtime, otherwise runtime is O(N).

Scope: Smallest useful construction: a generic noisy-hop model with hop amplitude sqrt(1-epsilon^2) and stay amplitude epsilon, plus the scaling condition from the abstract, with Grover's search as background. The paper's actual walk operator, barrier model, proof, and continuous-time treatment are outside scope.

## Symbols

- $N$: number of database items (vertices); domain: positive integer
- $\epsilon$: failure (stay-put) amplitude of a hop; domain: [0,1]
- $T$: search runtime (number of hop/walk steps); domain: positive integer or real
- $|u\rangle$: uniform superposition over N items; domain: state in C^N
- $|w\rangle$: marked item; domain: basis state

## eq_1: Failure amplitude scaling condition

$$
\epsilon = O(1/\sqrt{N}) \Rightarrow T = O(\sqrt{N}); \quad \text{otherwise } T = O(N)
$$

Condition on hop failure amplitude for retaining quantum speedup

Provenance: `abstract_explicit`. Direct statement of the main result; the precise proof and constants are not available.

Abstract evidence: the failure amplitude must scale as $O(1/\sqrt{N})$ for search to retain its quantum $O(\sqrt{N})$ runtime; otherwise, it searches in classical $O(N)$ time

Equation assumptions:

- epsilon is the per-hop failure amplitude as in the abstract

## eq_2: Noisy hop single-edge model

$$
H_{\epsilon}|a\rangle = \sqrt{1-\epsilon^2}\,|b\rangle + \epsilon\,|a\rangle
$$

Hop from vertex a to b with tunneling amplitude and stay-put amplitude epsilon (unitary completion not specified)

Provenance: `assumption`. Abstract describes some amplitude of tunneling and some of staying put; this parametrization is a proposed normalization.

Equation assumptions:

- Amplitudes normalized as shown
- Relative phase between terms unspecified

## eq_3: Grover iteration (background)

$$
G = (2|u\rangle\langle u| - I)(I - 2|w\rangle\langle w|),\quad |u\rangle=\tfrac{1}{\sqrt N}\sum_x|x\rangle
$$

Standard Grover iterate underlying the walk formulation

Provenance: `standard_background`. Standard textbook; the paper's walk-based version is not given.

Equation assumptions:

- Single marked item

## eq_4: Ideal Grover iteration count (background)

$$
T_{\mathrm{ideal}} \approx \frac{\pi}{4}\sqrt{N}
$$

Ideal number of iterations for one marked item among N

Provenance: `standard_background`. Standard result for ideal Grover search.

Equation assumptions:

- Single marked item, large N

## eq_5: Heuristic cumulative no-failure amplitude

$$
(1-\epsilon^2)^{T/2} \approx e^{-\epsilon^2 T/2}
$$

Heuristic: with T hops the total no-failure amplitude is O(1) only when epsilon^2 T = O(1), consistent with epsilon = O(1/sqrt(N)) at T ~ sqrt(N)? This is not the paper's proof.

Provenance: `assumption`. Illustrative scaling check only; with T~sqrt(N) it would suggest epsilon ~ N^{-1/4}, which differs from the abstract's claim, so the paper's mechanism must differ.

Equation assumptions:

- Independent failures per hop
- Not equivalent to the paper's proof

## Registers

- vertex: ceil(log2 N) qubits (assumed) qubits; position of the walker on the search graph (e.g., complete graph on N vertices)

## Initial state

Assumed uniform superposition over N vertices, |u>.

## Measurement

Computational-basis measurement of the vertex register after T steps (assumed).

## Classical postprocessing

Check whether the measured vertex is marked using one oracle query (assumed).

## Algorithm steps

1. Prepare uniform superposition over vertices. (eq_3)
2. Alternate marked-vertex phase/coin step with noisy hop operations carrying failure amplitude epsilon. (eq_2, eq_3)
3. Compare required runtime against the scaling condition on epsilon. (eq_1, eq_4, eq_5)

## Assumptions

- Complete-graph-like search walk with single marked vertex
- Hop failure modeled as per-hop stay-put amplitude epsilon
- Discrete-time setting only; continuous-time case omitted

## Missing information

- Exact quantum walk operator and barrier model
- Proof and constants for the epsilon threshold
- Continuous-time Hamiltonian
- Definition of failure amplitude in the full unitary
- Explicit circuit-level decomposition
