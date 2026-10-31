# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Given a (completely positive, trace-preserving) qudit channel E on a d-dimensional system and an error tolerance epsilon, produce a quantum circuit procedure (using one ancillary qudit plus classical dits) whose implemented channel is within diamond-norm distance epsilon of E, by classically decomposing E into a convex combination of generalized extreme channels and then randomly selecting and executing the circuit for one of them.

Scope: Reconstructed here: (i) the convex-decomposition target relation and its diamond-norm accuracy criterion, (ii) the single-ancilla Stinespring dilation circuit for one generalized extreme channel (Kraus rank at most d), (iii) the randomized execution protocol with classical dits and the resulting error budget, (iv) a tiny explicit instance with d=2: the qubit channel E = 3/4 * AmplitudeDamping(gamma=1/2) + 1/4 * (X . X), which is already a convex combination of two generalized extreme channels. Outside scope (not recoverable from the abstract): the specific set of nonlinear coupled algebraic equations and their optimization method, the parametrization of generalized extreme qudit channels used by the paper, the number of extreme terms in the decomposition, the explicit O(d^2) gate construction for the dilation unitary, and the precise Solovay-Kitaev exponent used in the logarithmic run-time claim.

## Symbols

- $d$: Hilbert-space dimension of the system qudit (and of the ancillary qudit); domain: integer, d >= 2 (instance: d = 2)
- $\mathcal{E}$: Target qudit channel to be simulated; domain: completely positive trace-preserving linear map on d x d density matrices
- $\mathcal{E}_k$: k-th generalized extreme channel (Kraus rank at most d) in the decomposition; domain: CPTP map on d x d density matrices, k = 1,...,M
- $\tilde{\mathcal{E}}_k$: Channel actually implemented by the compiled fault-tolerant circuit approximating E_k; domain: CPTP map on d x d density matrices
- $p_k$: Classical probability weight of E_k in the convex combination; domain: real, p_k >= 0, sum_k p_k = 1
- $M$: Number of generalized extreme channels in the decomposition; domain: positive integer (upper bound not given in abstract)
- $K_i^{(k)}$: i-th Kraus operator of E_k; domain: d x d complex matrix, i = 0,...,d-1
- $U_k$: Dilation unitary on system tensor ancilla implementing E_k; domain: d^2 x d^2 unitary matrix
- $\epsilon$: Pre-specified total error tolerance in diamond norm; domain: real, epsilon > 0
- $\epsilon_{\mathrm{dec}}, \epsilon_{\mathrm{SK}}$: Error budget split between the classical convex decomposition and the gate compilation of each U_k; domain: reals, epsilon_dec + epsilon_SK <= epsilon
- $\|\cdot\|_\diamond$: Diamond norm (completely bounded trace norm) on superoperators; domain: nonnegative real
- $\rho$: Input state of the system qudit; domain: d x d density matrix
- $\gamma$: Amplitude-damping parameter in the tiny instance; domain: real in [0,1] (instance: gamma = 1/2)

## eq_1: Convex decomposition into generalized extreme channels

$$
\mathcal{E} \approx \sum_{k=1}^{M} p_k\, \mathcal{E}_k, \qquad p_k \ge 0, \quad \sum_{k=1}^{M} p_k = 1, \qquad \Big\| \mathcal{E} - \sum_{k=1}^{M} p_k \mathcal{E}_k \Big\|_\diamond \le \epsilon_{\mathrm{dec}}
$$

The classical algorithm outputs weights p_k and generalized extreme channels E_k whose convex combination approximates E in diamond norm; equality is only approximate up to the decomposition tolerance.

Provenance: `abstract_explicit`. Directly stated in the abstract; the approximate (rather than exact) equality follows from the stated pre-specified diamond-norm error tolerance.

Abstract evidence: decomposing a quantum channel into a convex combination of generalized extreme channels

Equation assumptions:

- Approximation (not exact equality) is allowed within the tolerance; the abstract does not state whether the decomposition is exact.
- The value of M and the parametrization of E_k are not given by the abstract.

## eq_2: Generalized extreme channel: Kraus form with rank at most d

$$
\mathcal{E}_k(\rho) = \sum_{i=0}^{d-1} K_i^{(k)} \rho\, K_i^{(k)\dagger}, \qquad \sum_{i=0}^{d-1} K_i^{(k)\dagger} K_i^{(k)} = \mathbb{1}_d
$$

A generalized extreme (quasi-extreme) channel on a d-dimensional system admits a Kraus decomposition with at most d Kraus operators; extreme channels additionally have {K_i^dagger K_j} linearly independent.

Provenance: `standard_background`. Choi's characterization: extreme points of the CPTP convex set on dimension d have Kraus rank at most d; 'generalized extreme' is taken as the closure of this set (Kraus rank <= d), which is what makes a single d-dimensional ancilla sufficient.

Equation assumptions:

- 'Generalized extreme channel' is interpreted as a channel of Kraus rank at most d.

## eq_3: Single-ancilla Stinespring dilation of E_k

$$
U_k \big( |\psi\rangle_S \otimes |0\rangle_A \big) = \sum_{i=0}^{d-1} \big( K_i^{(k)} |\psi\rangle \big)_S \otimes |i\rangle_A, \qquad \mathcal{E}_k(\rho) = \mathrm{Tr}_A\!\left[ U_k \big( \rho \otimes |0\rangle\langle 0|_A \big) U_k^\dagger \right]
$$

Because E_k has at most d Kraus operators, one ancillary qudit of dimension d (initialized to |0>) suffices: the ancilla level |i> records which Kraus operator acted; the ancilla is then discarded. Register order is system (first) tensor ancilla (second); U_k is any unitary extension of the specified isometry.

Provenance: `abstract_inferred`. The abstract states one ancillary qudit suffices; combined with Kraus rank <= d (eq_2), the standard Stinespring/isometric dilation gives exactly this construction.

Abstract evidence: requires only a single ancillary qudit plus classical dits

Equation assumptions:

- The ancilla is initialized in |0> and traced out (not measured) at the end; the abstract does not specify ancilla handling.
- The explicit O(d^2) gate decomposition of U_k used in the paper is not reconstructed.

## eq_4: Randomized execution and total diamond-norm error budget

$$
\tilde{\mathcal{E}} = \sum_{k=1}^{M} p_k\, \tilde{\mathcal{E}}_k, \qquad \| \mathcal{E} - \tilde{\mathcal{E}} \|_\diamond \le \Big\| \mathcal{E} - \sum_k p_k \mathcal{E}_k \Big\|_\diamond + \max_k \| \mathcal{E}_k - \tilde{\mathcal{E}}_k \|_\diamond \le \epsilon_{\mathrm{dec}} + \epsilon_{\mathrm{SK}} \le \epsilon
$$

Sampling index k with probability p_k (stored in classical dits) and running the compiled circuit for E_k implements the mixture exactly; the total error is bounded by triangle inequality and convexity of the diamond norm. The diamond norm is ||Phi||_diamond = sup_n ||Phi tensor id_n||_{1->1}.

Provenance: `abstract_inferred`. The abstract specifies a randomly chosen extreme-channel circuit and a diamond-norm tolerance; averaging over the classical random choice yields the convex combination, and the error bound follows from the triangle inequality and convexity of the diamond norm.

Abstract evidence: The resultant circuit is a randomly chosen generalized extreme channel circuit

Equation assumptions:

- The error tolerance is split additively between decomposition error and gate-compilation error; the paper's actual split is not given.

## eq_5: Fault-tolerant compilation cost (Solovay-Kitaev)

$$
N_{\mathrm{gates}}(U_k) = O\!\left( d^2 \, \log^{c}\!\left( 1/\epsilon_{\mathrm{SK}} \right) \right), \quad c \approx 3.97 \text{ (standard SK)}
$$

Each dilation unitary is decomposed into O(d^2) elementary two-level/qudit gates, each compiled from a finite fault-tolerant gate set to accuracy epsilon_SK/O(d^2) with polylogarithmic overhead, giving run-time logarithmic in the tolerance and quadratic in d.

Provenance: `abstract_inferred`. The abstract asserts log(1/epsilon) and d^2 scaling; the Solovay-Kitaev theorem is the standard background mechanism for the logarithmic dependence, and O(d^2) is the stated dimension scaling. The exact exponent c and constant factors used in the paper are not known.

Abstract evidence: run-time is logarithmic with respect to the error tolerance and quadratic with respect to Hilbert space dimension

Equation assumptions:

- Solovay-Kitaev (or an equivalent polylog compiler) is the source of the logarithmic scaling; the paper's exact exponent is unknown.
- The O(d^2) count presumes a specific structure of the dilation unitary not derivable from the abstract.

## eq_6: Tiny instance: d = 2 qubit channel

$$
\mathcal{E}(\rho) = \tfrac{3}{4}\, \mathcal{E}_{\mathrm{AD}}(\rho) + \tfrac{1}{4}\, X \rho X, \quad \mathcal{E}_{\mathrm{AD}}(\rho) = K_0 \rho K_0^\dagger + K_1 \rho K_1^\dagger, \quad K_0 = |0\rangle\langle 0| + \sqrt{1-\gamma}\,|1\rangle\langle 1|, \; K_1 = \sqrt{\gamma}\,|0\rangle\langle 1|, \; \gamma = \tfrac{1}{2}; \quad U_1 |0\rangle_S|0\rangle_A = |0\rangle_S|0\rangle_A, \; U_1 |1\rangle_S|0\rangle_A = \sqrt{1-\gamma}\,|1\rangle_S|0\rangle_A + \sqrt{\gamma}\,|0\rangle_S|1\rangle_A, \quad U_2 = X_S \otimes \mathbb{1}_A
$$

Explicit instance with M = 2, p_1 = 3/4, p_2 = 1/4: amplitude damping (Kraus rank 2, extreme for 0 < gamma < 1) and the unitary bit-flip channel (Kraus rank 1, extreme). Here eq_1 holds exactly (epsilon_dec = 0). One classical bit samples k; one ancilla qubit implements U_1 (a controlled rotation structure) and is then discarded.

Provenance: `assumption`. No scope was provided, so a smallest useful instance was chosen in which the decomposition is already explicit, isolating the circuit-execution part of the method for later circuit generation.

Equation assumptions:

- Instance choice (channel, gamma, weights) is the reconstructor's, not from the paper.
- U_1 is any unitary completion of the stated action on the |0>_A subspace; e.g. a controlled rotation on the ancilla followed by a controlled-X back on the system.

## Registers

- S: 1 qudit of dimension d (instance: 1 qubit) qubits; System register carrying the input state rho on which the channel acts
- A: 1 qudit of dimension d (instance: 1 qubit) qubits; Single ancillary qudit for the Stinespring dilation; initialized to |0>, discarded (traced out) after U_k
- C: ceil(log_d M) classical dits (instance: 1 classical bit) qubits; Classical register holding the randomly sampled index k drawn with probability p_k

## Initial state

rho_S tensor |0><0|_A, with classical register C holding a sample k drawn from {1,...,M} with probability p_k (register order: S first, A second).

## Measurement

No measurement is intrinsic to the channel simulation; the ancilla is traced out (equivalently measured and the result ignored). Any downstream measurement of the system is application-dependent and not specified by the abstract.

## Classical postprocessing

None required for the simulation itself beyond the random index sampling; if validating, one may estimate the implemented channel by process tomography averaged over many runs (each with a fresh sample of k) and compare to E, but this is not part of the method described.

## Algorithm steps

1. Classical preprocessing: given E and tolerance epsilon_dec, solve the (paper-specific, unreconstructed) nonlinear coupled algebraic optimization to obtain weights p_k and generalized extreme channels E_k (Kraus operators K_i^(k)) satisfying the convex decomposition relation. In the tiny instance this step is trivial since E is given already decomposed. (eq_1, eq_2, eq_6)
2. Classical sampling: draw k with probability p_k and store it in the classical dit register C. (eq_4)
3. Prepare the ancilla qudit A in |0> alongside the system input rho. (eq_3)
4. Apply the compiled fault-tolerant circuit for the dilation unitary U_k (selected by the classical value k) on S tensor A, with compilation accuracy epsilon_SK. (eq_3, eq_5, eq_6)
5. Discard (trace out) the ancilla A; the system register now holds E~_k(rho), and averaged over the classical randomness the implemented channel is sum_k p_k E~_k, within epsilon of E in diamond norm. (eq_3, eq_4)

## Assumptions

- Generalized extreme channel is interpreted as a channel of Kraus rank at most d (closure of the extreme set), which is what makes a single d-dimensional ancilla sufficient.
- Ancilla initialized in |0> and discarded rather than measured.
- Error tolerance split additively between decomposition error and gate-compilation error.
- The logarithmic run-time scaling is attributed to Solovay-Kitaev-type compilation; the paper's exact exponent is unknown.
- The tiny instance (d=2, E = 3/4 AD(gamma=1/2) + 1/4 X.X, M=2) is the reconstructor's choice because no experiment_scope was supplied.
- Register ordering is system first, ancilla second; ancilla level |i> labels Kraus operator index i.

## Missing information

- The explicit set of nonlinear coupled algebraic equations and the optimization method used for the convex decomposition.
- The parametrization of generalized extreme qudit channels (e.g., number of real parameters, canonical form) used by the paper.
- The number of extreme channels M in the decomposition and any bound on it (e.g., whether d^2 terms suffice).
- The explicit gate-level construction of U_k achieving O(d^2) elementary gates and the chosen fault-tolerant gate set.
- The precise relation between the pre-specified diamond-norm tolerance and the per-gate compilation accuracy, including the Solovay-Kitaev exponent.
- Any numerical results, benchmark channels, or convergence guarantees for the classical optimization.
