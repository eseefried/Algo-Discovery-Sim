# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Spatial quantum search (Tulsi-type walk search with one control/ancilla qubit) on an N-vertex graph for a single marked vertex w, modified so that the control qubit is projectively measured every tau steps; quantify the success probability, control-walker correlations (mutual information, cumulative correlation measure) and the scaling exponent of the optimal search time with N as a function of tau and of the angular parameter delta.

Scope: One smallest useful instance chosen as an assumption: a 2D periodic grid of sqrt(N) x sqrt(N) with N = 16 (4 position qubits), a 2-qubit coin, one control qubit (7 qubits total), a single marked vertex w, a fixed angular parameter delta, and measurement lapses tau in {1, 2, T} where tau = T means no intermediate measurement. The scope covers: state space and initial state, a schematic Tulsi-like step unitary U_delta, the control-measurement channel applied every tau steps, the success probability, the control-walker mutual information, and the operational definition of the scaling exponent. Outside scope (paper contributions not reconstructable from the abstract): the paper's specific 'different choice' of delta, the exact definition of the Cumulative Correlation Measure, the specific set of tau and N values, the reported numerical probability/correlation relationships, and the precise order estimates for each tau other than the stated O(N) for tau = 1.

## Symbols

- $N$: Number of vertices (search space size); for the chosen instance N = 16 on a 4 x 4 periodic grid; domain: positive integer, N = n^2
- $w$: Marked (target) vertex; domain: element of {0,...,N-1}
- $\delta$: Angular parameter of the control-qubit rotation in Tulsi's algorithm (paper uses a non-standard choice, value not given in abstract); domain: real, 0 < \delta < \pi/2
- $\tau$: Time lapse (number of walk steps) between successive measurements of the control qubit; domain: positive integer, 1 \le \tau \le T
- $t$: Discrete time step index; domain: non-negative integer
- $T$: Total number of walk steps run; domain: positive integer
- $\rho_t$: Joint (generally mixed) state of control, coin and position registers after t steps; domain: density operator on \mathbb{C}^2 \otimes \mathbb{C}^4 \otimes \mathbb{C}^N
- $R_\delta$: Single-qubit rotation by angle delta acting on the control qubit; domain: 2 x 2 real orthogonal matrix
- $S$: Flip-flop shift operator of the coined walk on the grid; domain: unitary on coin \otimes position
- $C$: Coin operator (Grover diffusion on the 4-dimensional coin); domain: unitary on \mathbb{C}^4
- $P_w(t)$: Probability of finding the walker at the marked vertex when the position register is measured at time t; domain: [0,1]
- $I(C\!:\!W)_t$: Quantum mutual information between the control qubit and the walker (coin+position) at time t; domain: [0, 2]
- $T^*(N)$: Optimal (first-maximum or threshold) search time as a function of N; domain: positive integer
- $\alpha$: Scaling exponent of T^*(N) \propto N^{\alpha}; alpha = 1 corresponds to classical brute-force O(N); domain: real, typically 1/2 \le \alpha \le 1

## eq_1: Initial state

$$
|\psi_0\rangle = |0\rangle_C \otimes |c_u\rangle \otimes |s\rangle,\quad |s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle,\quad |c_u\rangle = \frac{1}{2}\sum_{d\in\{\uparrow,\downarrow,\leftarrow,\rightarrow\}}|d\rangle,\quad \rho_0 = |\psi_0\rangle\langle\psi_0|
$$

Control qubit in |0>, coin and position registers in uniform superposition; register order is control (most significant) ⊗ coin ⊗ position, position x = n*x_1 + x_2 with n = sqrt(N) encoded in binary.

Provenance: `standard_background`. Standard initial state for coined-walk spatial search algorithms including Tulsi's; the abstract does not state the initial state.

Equation assumptions:

- Control qubit initialised to |0>; Tulsi's original may use a different control basis convention
- Uniform superposition over position and coin

## eq_2: Tulsi-like step unitary with control rotation

$$
U_\delta = \big(I_C\otimes S\big)\big(I_C \otimes C \otimes I_{pos}\big)\Big(R_\delta\otimes I_{coin}\otimes|w\rangle\langle w| + I_C\otimes I_{coin}\otimes (I_{pos}-|w\rangle\langle w|)\Big),\qquad R_\delta = \begin{pmatrix}\cos\delta & -\sin\delta\\ \sin\delta & \cos\delta\end{pmatrix}
$$

One step: a rotation by delta on the control qubit conditioned on the walker being at the marked vertex, followed by the coin and flip-flop shift. In Tulsi's original algorithm the coin action is additionally controlled by the control qubit; this schematic form is only a placeholder for the exact operator.

Provenance: `assumption`. The abstract names Tulsi's algorithm and an angular parameter but gives no operator; this is a schematic reconstruction of a controlled rotation entering the walk step, marked as an assumption because the exact Tulsi operator and the paper's modification of delta are not available here.

Equation assumptions:

- Exact structure of Tulsi's controlled coin/shift is not reproduced; only the delta-rotation on the control conditioned on the marked vertex is modeled
- Coin C is the 4-dimensional Grover diffusion operator; S is the flip-flop shift on the periodic grid
- Value of delta chosen by the paper ('a different choice') is unknown and must be set as a free parameter

## eq_3: Evolution with intermediate control measurements every tau steps

$$
\mathcal{M}(\rho) = \sum_{b\in\{0,1\}} \big(|b\rangle\langle b|_C\otimes I\big)\,\rho\,\big(|b\rangle\langle b|_C\otimes I\big),\qquad \rho_{k\tau} = \mathcal{M}\big(U_\delta^{\tau}\,\rho_{(k-1)\tau}\,U_\delta^{\dagger\,\tau}\big),\quad k = 1,\dots,\lfloor T/\tau\rfloor
$$

Between measurements the state evolves unitarily for tau steps; at each measurement the control qubit is measured in the computational basis and the outcome is not post-selected (averaged, giving a dephasing channel on the control). tau = 1 means a measurement after every step; tau >= T recovers the unmeasured algorithm.

Provenance: `abstract_inferred`. Inferred from the stated intermediate measurements of the control and the 'time lapses between measurements'; the computational basis and non-post-selected (ensemble-averaged) treatment are reconstruction choices.

Abstract evidence: intermediate measurements of the control is presented

Equation assumptions:

- Projective measurement in the computational basis of the control
- Measurement outcomes are not used for feedback or post-selection; the ensemble-averaged state is tracked

## eq_4: Success probability at the marked vertex

$$
P_w(t) = \mathrm{Tr}\big[(I_C\otimes I_{coin}\otimes |w\rangle\langle w|)\,\rho_t\big]
$$

Probability that a final measurement of the position register at time t yields the marked vertex.

Provenance: `abstract_inferred`. The abstract refers to probabilities in a quantum search; the success probability at the marked vertex is the standard quantity, here written for the mixed state produced by eq_3.

Abstract evidence: finding close relationships between probabilities and correlations

Equation assumptions:

- The 'probabilities' in the abstract refer (at least) to the success probability of locating the marked vertex

## eq_5: Control-walker mutual information

$$
I(C\!:\!W)_t = S(\rho_C) + S(\rho_W) - S(\rho_t),\qquad S(\sigma) = -\mathrm{Tr}[\sigma\log_2\sigma],\quad \rho_C = \mathrm{Tr}_W\rho_t,\ \rho_W = \mathrm{Tr}_C\rho_t
$$

Quantum mutual information between the control qubit C and the walker W = coin ⊗ position, evaluated on the state of eq_3.

Provenance: `standard_background`. The abstract names 'Mutual Information' as one correlation measure; this is its standard quantum definition. The 'Cumulative Correlation Measure' is not defined in the abstract and is not reconstructed.

Equation assumptions:

- Mutual information is computed between the control qubit and the remaining registers; the exact bipartition used by the paper is not stated

## eq_6: Optimal time and scaling exponent (order estimate)

$$
T^*(N) = \arg\max_{0\le t\le T} P_w(t),\qquad T^*(N) \approx a\,N^{\alpha}\ \Rightarrow\ \alpha \approx \frac{\Delta \log T^*(N)}{\Delta \log N},\qquad \alpha|_{\tau=1} \approx 1
$$

The order of the algorithm is estimated from the growth of the optimal search time with N via a log-log fit; the abstract states that measuring at every step (tau = 1) yields O(N) scaling, i.e. alpha ≈ 1, while some tau values improve the performance.

Provenance: `abstract_inferred`. The abstract states the order is estimated and gives O(N) for tau = 1; the definition of T^* as the first-maximum time and the log-log fit are standard reconstruction choices, the approximate relation is a fit, not an exact equality.

Abstract evidence: became of order $O(N)$ (classical brute force search) when the measurement is taken in every step

Equation assumptions:

- Order is estimated from the time to the first maximum of P_w(t); the paper may use a threshold criterion or account for success probability via amplitude amplification

## Registers

- control: 1 qubits; Tulsi's control/ancilla qubit rotated by R_delta and projectively measured every tau steps
- coin: 2 qubits; Four-direction coin of the 2D coined walk
- position: 4 qubits; Vertex of the 4 x 4 periodic grid (N = 16), x = 4*x_1 + x_2 in binary; marked vertex w

## Initial state

|0>_C ⊗ |c_u> ⊗ |s> as in eq_1: control in |0>, coin and position in uniform superposition (7 qubits total for N = 16).

## Measurement

Intermediate: computational-basis projective measurement of the single control qubit every tau steps. Final: computational-basis measurement of the position register; success if the outcome equals w (eq_4).

## Classical postprocessing

From the recorded P_w(t) determine T^*(N) (first maximum), fit log T^*(N) versus log N to extract alpha for each tau (eq_6); compare the time series of P_w(t) with the correlation measures (eq_5) to identify the relationships referred to in the abstract.

## Algorithm steps

1. Prepare the initial product state with control |0> and uniform superposition on coin and position registers. (eq_1)
2. Apply tau steps of the Tulsi-like walk unitary U_delta (controlled rotation by delta on the control at the marked vertex, coin, shift). (eq_2)
3. Measure the control qubit in the computational basis (no post-selection), yielding the dephased joint state; repeat the evolve-tau-steps/measure cycle until T steps are reached. (eq_3)
4. At each time t record the success probability P_w(t) and the control-walker mutual information I(C:W)_t. (eq_4, eq_5)
5. Repeat for several N (and tau) and estimate the scaling exponent alpha from T^*(N). (eq_6)

## Assumptions

- No experiment scope was supplied; the N = 16 4 x 4 grid, 2-qubit Grover coin, single marked vertex and tau in {1, 2, T} were chosen as the smallest useful instance
- The step unitary of eq_2 is a schematic Tulsi-like controlled-rotation walk; the exact operator of Tulsi's algorithm and the paper's modification are not reproduced from source
- The angular parameter delta is left as a free parameter because the abstract states a 'different choice' without giving it
- Control measurements are modeled as non-post-selected projective measurements (dephasing channel on the control)
- Order estimation uses the first-maximum time of the success probability

## Missing information

- Exact form of Tulsi's step operator used in the paper (how the control qubit conditions the coin/shift)
- The paper's specific 'different choice' of the angular parameter delta and its dependence on N
- Definition of the Cumulative Correlation Measure
- The set of time lapses tau and sizes N studied, and the resulting numerical probabilities, correlations and order estimates for tau > 1
- Whether measurement outcomes of the control are post-selected or used for feedback
- Whether the initial control state and measurement basis match this reconstruction
