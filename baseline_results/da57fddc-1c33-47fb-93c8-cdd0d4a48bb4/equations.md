# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Quantum-walk formulation of Grover search on N vertices where the hop (shift) operation is imperfect: a potential barrier gives the walker an amplitude to tunnel to the neighboring vertex and a residual 'failure' amplitude to stay put. The abstract's claim is that the failure amplitude must scale as O(1/sqrt(N)) for the search to retain its Theta(sqrt(N)) runtime; otherwise it degrades to classical Theta(N) time. The claim is stated for both discrete- and continuous-time walks.

Scope: One smallest useful construction, chosen as an assumption: a discrete-time coined quantum walk search on the complete graph K_N (the quantum-walk formulation of Grover's algorithm) with the ideal flip-flop shift replaced by a unitary barrier shift that mixes the shift with the identity by a failure amplitude epsilon. Tiny explicit instance: N = 4 vertices (two 2-qubit registers), one marked vertex w = 0, and a sweep of epsilon in {0, 0.1, 0.5} with step count t up to ~2N. The continuous-time version, the paper's exact barrier model, the proof of the O(1/sqrt(N)) threshold, and precise runtime constants are outside this scope.

## Symbols

- $N$: Number of vertices (database size) of the complete graph; domain: positive integer, N >= 2 (instance: N = 4)
- $u, v$: Vertex labels; |u\rangle is the walker's position, |v\rangle the coin register pointing to neighbor v; domain: integers in {0, ..., N-1}
- $w$: Marked (target) vertex; domain: integer in {0, ..., N-1} (instance: w = 0)
- $|s\rangle$: Uniform superposition over N basis states; domain: unit vector in C^N
- $S$: Ideal flip-flop shift (hop) operator; domain: Hermitian unitary on C^N \otimes C^N
- $\epsilon$: Failure amplitude: amplitude of the walker staying put instead of hopping; domain: real, 0 <= epsilon <= 1
- $S_\epsilon$: Barrier-hindered shift operator; domain: unitary on C^N \otimes C^N
- $C$: Grover coin acting on the coin register; domain: unitary on C^N
- $Q$: Oracle marking vertex w (phase flip on position register); domain: unitary on C^N \otimes C^N
- $U_\epsilon$: One step of the barrier-hindered walk; domain: unitary on C^N \otimes C^N
- $t$: Number of walk steps; domain: non-negative integer
- $p_\epsilon(t)$: Probability of measuring the marked vertex after t steps; domain: real in [0,1]
- $t^*$: First step count at which p_epsilon(t) is maximal (search runtime); domain: positive integer

## eq_1: Hilbert space and initial state

$$
|\psi_0\rangle = |s\rangle \otimes |s\rangle, \quad |s\rangle = \frac{1}{\sqrt{N}} \sum_{u=0}^{N-1} |u\rangle, \quad \mathcal{H} = \mathbb{C}^N \otimes \mathbb{C}^N
$$

Position register (first factor) tensor coin register (second factor), each of dimension N; both initialized in the uniform superposition. Self-loop states |u,u> are included for simplicity so each register is exactly log2(N) qubits.

Provenance: `assumption`. Standard starting state for quantum-walk search on the complete graph; including self-loop directions is a simplifying choice so the register is a full tensor product.

Equation assumptions:

- Complete graph K_N with self-loop coin directions retained
- Uniform initial superposition over both registers

## eq_2: Oracle and Grover coin

$$
Q = (I_N - 2|w\rangle\langle w|) \otimes I_N, \qquad C = 2|s\rangle\langle s| - I_N
$$

Q flips the phase of all states whose position is the marked vertex w; C is the Grover diffusion coin applied to the coin register.

Provenance: `standard_background`. Standard components of the discrete-time quantum-walk formulation of Grover's algorithm (coined walk on the complete graph).

Equation assumptions:

- Single marked vertex
- Grover coin rather than another coin

## eq_3: Ideal flip-flop shift and ideal walk step

$$
S|u\rangle|v\rangle = |v\rangle|u\rangle, \qquad U_0 = S\,(I_N \otimes C)\,Q
$$

The flip-flop shift swaps position and coin registers (hop to v, pointing back to u). S is Hermitian and unitary (S^2 = I). One ideal walk step is oracle, then coin, then shift.

Provenance: `standard_background`. Standard flip-flop shift; with this definition the ideal walk searches K_N in Theta(sqrt(N)) steps.

Equation assumptions:

- Flip-flop shift convention
- Operator ordering Q, then coin, then shift

## eq_4: Barrier-hindered shift with failure amplitude

$$
S_\epsilon = \epsilon\, I + i\sqrt{1-\epsilon^2}\, S, \qquad U_\epsilon = S_\epsilon\,(I_N \otimes C)\,Q
$$

The hop succeeds (tunnels) with amplitude i*sqrt(1-epsilon^2) and fails (stays put) with amplitude epsilon. Because S is Hermitian and unitary, this combination is unitary (S_epsilon = exp(i theta S) with cos theta = epsilon up to phase). Epsilon = 0 recovers the ideal walk.

Provenance: `abstract_inferred`. The abstract describes a hop with a tunneling amplitude and a staying amplitude; this is the minimal unitary model of such a hop. The exact form used in the paper (relative phase, how the coin is affected) is not given in the abstract and is an assumption.

Abstract evidence: the particle has some amplitude of tunneling through the barriers, and some amplitude of staying put

Equation assumptions:

- Relative phase i between stay and hop terms chosen to guarantee unitarity
- Barrier affects only the shift, not the coin or oracle
- Uniform epsilon on all edges

## eq_5: Success probability and runtime

$$
p_\epsilon(t) = \sum_{v=0}^{N-1} \left| \langle w, v | U_\epsilon^{\,t} | \psi_0 \rangle \right|^2, \qquad t^* = \arg\max_{t \ge 1} p_\epsilon(t)\ (\text{first maximum})
$$

Probability that measuring the position register after t steps yields the marked vertex (coin register traced out); the runtime is the first step count maximizing this probability.

Provenance: `standard_background`. Standard definition of success probability and runtime for quantum-walk search.

Equation assumptions:

- Runtime defined as first peak of success probability, not the number of repetitions needed

## eq_6: Threshold scaling of the failure amplitude

$$
\epsilon = O\!\left(\frac{1}{\sqrt{N}}\right) \;\Rightarrow\; t^* = O(\sqrt{N}), \qquad \epsilon = \omega\!\left(\frac{1}{\sqrt{N}}\right) \;\Rightarrow\; t^* = \Theta(N)
$$

The abstract's main claim: the failure amplitude must vanish at least as fast as 1/sqrt(N) to retain the quadratic speedup; otherwise the search takes classical linear time.

Provenance: `abstract_explicit`. Directly stated in the abstract; the second implication paraphrases 'otherwise' as any slower decay of epsilon. Constants and the exact dependence of t^* and peak probability on epsilon*sqrt(N) are not given.

Abstract evidence: We prove that the failure amplitude must scale as $O(1/\sqrt{N})$ for search to retain its quantum $O(\sqrt{N})$ runtime; otherwise, it searches in classical $O(N)$ time.

Equation assumptions:

- Interpretation of 'otherwise' as epsilon decaying slower than 1/sqrt(N)
- Applies to the specific barrier model in eq_4, which may differ from the paper's

## Registers

- position: log2(N) qubits (2 qubits for N = 4) qubits; Walker's vertex u on the complete graph; measured at the end
- coin: log2(N) qubits (2 qubits for N = 4) qubits; Direction register pointing to neighbor v; acted on by Grover coin C and swapped by the shift

## Initial state

|psi_0> = |s> (x) |s>, uniform superposition on both position and coin registers (eq_1); prepared from |0...0> by Hadamards on all qubits when N is a power of 2.

## Measurement

Computational-basis measurement of the position register only (coin register discarded) after t steps; outcome equals w with probability p_epsilon(t) of eq_5. Repeat shots to estimate p_epsilon(t).

## Classical postprocessing

For each (N, epsilon), build the curve p_epsilon(t) over t, find the first maximum t^* and its height; check that for epsilon = c/sqrt(N) with fixed c the peak occurs at t^* = Theta(sqrt(N)) with order-1 success probability, whereas for fixed epsilon independent of N the time to reach order-1 total success (peak height times repetitions) grows linearly in N (eq_6). Optionally verify the measured vertex is w by querying the oracle classically.

## Algorithm steps

1. Prepare the uniform superposition on position and coin registers. (eq_1)
2. Apply the oracle Q (phase flip on position = w) and then the Grover coin C on the coin register. (eq_2)
3. Apply the barrier-hindered shift S_epsilon (ideal flip-flop shift S when epsilon = 0), completing one walk step U_epsilon. (eq_3, eq_4)
4. Repeat steps 2-3 for t walk steps, for each t in a sweep up to roughly 2N, and for each chosen epsilon (e.g. 0, 0.1, 0.5) and N. (eq_4, eq_5)
5. Measure the position register and estimate the success probability p_epsilon(t); locate the first peak t^* and compare its scaling with N against the threshold claim. (eq_5, eq_6)

## Assumptions

- No experiment_scope was supplied; the discrete-time coined walk on the complete graph K_N with N = 4, w = 0 was chosen as the single smallest useful instance
- Barrier model S_epsilon = epsilon I + i sqrt(1-epsilon^2) S is a minimal unitary realization of 'tunnel or stay put'; the paper's actual model may differ (e.g. phase conventions, treatment of the coin, discrete vs continuous time)
- Self-loop coin directions are retained so each register is exactly log2(N) qubits
- Runtime is identified with the first peak of the marked-vertex probability
- Only the discrete-time case is reconstructed; the continuous-time Hamiltonian version is outside scope

## Missing information

- Exact mathematical form of the barrier/failure-amplitude model used in the paper for both discrete- and continuous-time walks
- Proof and precise constants of the O(1/sqrt(N)) threshold, including how peak success probability and t^* depend on epsilon*sqrt(N)
- Continuous-time quantum walk Hamiltonian with barriers (hopping rate gamma, potential-barrier terms) and its analysis
- Whether the paper uses the flip-flop shift on K_N exactly as assumed here, and whether self-loops are included
- Any numerical results or figures from the paper
