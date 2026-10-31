# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Approximately synthesize an n-qubit diagonal unitary D = diag(e^{i\theta(x)}) having k distinct phases over the Clifford+T gate set to operator-norm precision \varepsilon, using only about k phase-rotation gates (one per distinct phase) plus reversible Boolean logic, so that the total T-count is bounded by k C_0 \log_2(1/\varepsilon) + E(n,k).

Scope: Scoped to ONE smallest construction: (i) write D as a product of k commuting phase factors exp(i\theta_j \Pi_j), one per distinct phase, (ii) realize each factor with an ancilla that stores the indicator f_j(x) of the phase class S_j, a single-qubit phase gate on the ancilla approximated in Clifford+T, and uncomputation, (iii) allocate the error budget \varepsilon/k per rotation. Tiny explicit instance (assumption): n=2, k=2, D = diag(1,1,1,e^{i\theta}) with \theta = \pi/5, \varepsilon = 10^{-3}. Outside scope: the paper's specific entanglement-cost function E(n,k) and its optimized predicate/phase-context circuitry, the exact value of C_0 for a given Rz-synthesis method, the optimal decision boundary in (n,k,\varepsilon)-space versus prior techniques, and the claimed exponential-in-n T-count reduction; none of these can be reconstructed from the abstract alone.

## Symbols

- $n$: number of data qubits acted on by the diagonal operator; domain: positive integer
- $x$: computational-basis label, integer encoding of the n-bit string x_{n-1}\dots x_0 with qubit 0 the least significant bit; domain: \{0,\dots,2^n-1\}
- $\theta(x)$: phase angle of the diagonal entry at basis state x; domain: [0,2\pi)
- $k$: number of distinct values taken by \theta(x); domain: integer, 1 \le k \le 2^n
- $\theta_j$: the j-th distinct phase value; domain: [0,2\pi), j=1,\dots,k
- $S_j$: set of basis labels x with \theta(x)=\theta_j (partition of \{0,\dots,2^n-1\}); domain: subset of \{0,\dots,2^n-1\}
- $\Pi_j$: orthogonal projector onto span\{|x\rangle : x\in S_j\}; domain: 2^n \times 2^n Hermitian idempotent matrix
- $f_j$: Boolean indicator of membership in S_j; domain: \{0,1\}^n \to \{0,1\}
- $\varepsilon$: target operator-norm precision of the whole synthesized circuit; domain: (0,1)
- $\varepsilon_j$: precision allocated to the j-th rotation approximation; domain: (0,1)
- $C_0$: quality factor of the single-qubit Rz Clifford+T synthesis method; domain: real, 1 < C_0 < 4 (per abstract)
- $E(n,k)$: total entanglement cost in T gates of the reversible logic (computing/uncomputing indicators); domain: non-negative integer-valued function
- $P(\theta)$: single-qubit phase gate diag(1,e^{i\theta}), equal to e^{i\theta/2} R_z(\theta); domain: 2\times 2 unitary
- $\|\cdot\|$: operator (spectral) norm; domain: non-negative real

## eq_1: Diagonal operator with k distinct phases

$$
D = \sum_{x=0}^{2^n-1} e^{i\theta(x)} |x\rangle\langle x| = \sum_{j=1}^{k} e^{i\theta_j}\,\Pi_j,\qquad \Pi_j = \sum_{x\in S_j}|x\rangle\langle x|,\quad \sum_{j=1}^k \Pi_j = I
$$

Definition of the target n-qubit diagonal unitary, regrouped by its k distinct phase values; the S_j partition the basis labels.

Provenance: `abstract_inferred`. The abstract defines k as the number of distinct phases of a diagonal n-qubit unitary; grouping equal diagonal entries into projectors is the direct mathematical restatement.

Abstract evidence: $k$ is the number of distinct phases in the diagonal $n$-qubit unitary

Equation assumptions:

- Basis ordering: |x\rangle with x the integer whose bit i is the state of qubit i (qubit 0 least significant).

## eq_2: Exact factorization into k commuting phase factors

$$
D = \prod_{j=1}^{k} \exp\!\left(i\theta_j \Pi_j\right),\qquad \exp(i\theta_j\Pi_j) = I + (e^{i\theta_j}-1)\Pi_j
$$

Because the projectors are orthogonal and commute, D is exactly the product of k factors, each applying phase e^{i\theta_j} only on S_j; one factor can be removed as a global phase, leaving k-1 nontrivial rotations.

Provenance: `abstract_inferred`. A T-count term of k C_0 log_2(1/\varepsilon) is what one obtains from about k independently synthesized phase rotations, which indicates a one-rotation-per-distinct-phase factorization; the identity itself is exact linear algebra.

Abstract evidence: minimizes the number of phase-rotation gates in the synthesized approximation circuit. The equivalent $T$-count of the synthesized circuit is bounded by $kC_{0}\log_{2}(1/\varepsilon)+E(n,k)$

Equation assumptions:

- The paper's actual grouping/ordering of rotations may differ (e.g., k-1 rotations after removing a global phase).

## eq_3: Ancilla-based implementation of one phase factor

$$
O_j\,|x\rangle|a\rangle = |x\rangle|a\oplus f_j(x)\rangle,\qquad U_j = O_j^{\dagger}\,\big(I_{2^n}\otimes P(\theta_j)\big)\,O_j,\qquad U_j\,|x\rangle|0\rangle = e^{i\theta_j f_j(x)}|x\rangle|0\rangle
$$

Compute the indicator f_j(x) of S_j into a clean ancilla with reversible (Toffoli/CNOT-type) logic O_j, apply a single phase gate P(\theta_j)=diag(1,e^{i\theta_j}) on the ancilla, then uncompute. Restricted to ancilla |0\rangle this equals exp(i\theta_j\Pi_j)\otimes I. The T gates in O_j and O_j^\dagger constitute the entanglement cost.

Provenance: `assumption`. Smallest generic construction realizing eq_2 with exactly one phase rotation per distinct phase; the abstract names an entanglement cost E(n,k) but does not specify its circuit, so this ancilla/indicator realization is a proposed stand-in, not the paper's construction.

Equation assumptions:

- One clean ancilla qubit is available (plus any work ancillas needed by the Toffoli network).
- f_j is computed by a reversible Boolean circuit whose T-count depends on the structure of S_j; its sum over j is a surrogate for E(n,k).

## eq_4: Clifford+T approximation of a single phase rotation

$$
\|P(\theta_j) - \tilde P_j\| \le \varepsilon_j,\qquad T\text{-count}(\tilde P_j) \le C_0 \log_2(1/\varepsilon_j) + O(1)
$$

Each single-qubit phase gate (equivalently R_z(\theta_j) up to global phase) is replaced by a Clifford+T word \tilde P_j produced by an Rz-synthesis method whose T-count scales as C_0 log_2(1/\varepsilon_j).

Provenance: `standard_background`. Known Clifford+T Rz-synthesis results give T-counts of the form C \log_2(1/\varepsilon)+O(1) (e.g., C\approx 3 for ancilla-free optimal synthesis, lower with ancillas/measurement); the abstract's range 1<C_0<4 is consistent with this.

Equation assumptions:

- The O(1) additive term is neglected or absorbed into E(n,k) when stating the global bound.

## eq_5: Error accumulation and per-rotation budget

$$
\|D\otimes I - \tilde D\| \le \sum_{j=1}^{k} \varepsilon_j,\qquad \varepsilon_j = \varepsilon/k \;\Rightarrow\; \|D\otimes I - \tilde D\| \le \varepsilon
$$

Operator-norm errors of sequentially composed unitaries add at most linearly (triangle inequality, unitary invariance), so a uniform budget \varepsilon/k guarantees total precision \varepsilon. With this allocation eq_4 yields per-rotation cost C_0 \log_2(1/\varepsilon) + C_0\log_2 k, i.e. an extra k C_0 \log_2 k term relative to eq_6 unless it is accounted for in E(n,k) or the paper uses a different allocation.

Provenance: `standard_background`. Standard subadditivity of approximation error for products of unitaries; \tilde D denotes the product of the U_j with P(\theta_j) replaced by \tilde P_j.

Equation assumptions:

- Uniform error allocation; the paper's actual allocation is not stated in the abstract.

## eq_6: Total T-count bound

$$
T\text{-count} \le k\,C_0\log_2(1/\varepsilon) + E(n,k),\qquad 1 < C_0 < 4
$$

Headline resource bound of the paper: k rotation syntheses each costing about C_0 log_2(1/\varepsilon) T gates plus the entanglement cost of the reversible logic.

Provenance: `abstract_explicit`. Stated verbatim in the abstract; the functional form of E(n,k) is not given.

Abstract evidence: The equivalent $T$-count of the synthesized circuit is bounded by $kC_{0}\log_{2}(1/\varepsilon)+E(n,k)$

## eq_7: Tiny explicit instance (n=2, k=2)

$$
D = \mathrm{diag}(1,1,1,e^{i\theta}),\quad \theta=\pi/5,\quad S_1=\{00,01,10\},\;S_2=\{11\},\quad f_2(x_1,x_0)=x_1\wedge x_0,\quad \varepsilon = 10^{-3}
$$

Two data qubits, two distinct phases (\theta_1=0 taken as the trivial factor, \theta_2=\theta). Only U_2 is nontrivial: a Toffoli computes f_2 into the ancilla, \tilde P_2 approximates P(\theta) to \varepsilon_2=\varepsilon/2, then the Toffoli is uncomputed. Entanglement cost here is that of two Toffolis (7 T each in the standard decomposition, or less with measurement-based uncomputation).

Provenance: `assumption`. Chosen as the smallest instance exercising one indicator computation and one rotation synthesis; this is a controlled-phase gate, for which other decompositions (e.g., three Rz rotations) also exist, so it does not demonstrate the paper's advantage regime k \ll 2^n.

Equation assumptions:

- \theta_1 = 0 treated as global phase so k-1 = 1 rotation is synthesized.
- Standard 7-T Toffoli decomposition assumed for the instance's entanglement cost estimate.

## Registers

- data: n (instance: 2) qubits; holds the computational-basis superposition on which the diagonal unitary D acts; ordering x = x_{n-1}...x_0, qubit 0 least significant
- anc: 1 (plus optional work qubits for Toffoli networks) qubits; clean ancilla receiving the indicator f_j(x); the single Clifford+T-approximated phase gate acts on it; returned to |0> after uncomputation

## Initial state

|\psi\rangle_{data} \otimes |0\rangle_{anc}, with |\psi\rangle an arbitrary n-qubit state (the construction is a unitary synthesis, not a state-preparation task).

## Classical postprocessing

None required for the synthesized unitary itself. All nontrivial classical work is compilation-side: phase grouping, error-budget allocation, Rz-to-Clifford+T synthesis, and T-count accounting (k C_0 log_2(1/\varepsilon) + E(n,k)) to compare against alternative decompositions.

## Algorithm steps

1. Classical preprocessing: scan the diagonal of D, collect the k distinct phases \theta_j and their index sets S_j; drop one phase as a global phase if desired. (eq_1, eq_2)
2. Classical preprocessing: choose per-rotation precisions \varepsilon_j (uniform \varepsilon/k in this reconstruction) and synthesize Clifford+T words \tilde P_j approximating P(\theta_j). (eq_4, eq_5)
3. For each j with nontrivial \theta_j: apply reversible logic O_j computing f_j(x) into the ancilla. (eq_3)
4. Apply the synthesized Clifford+T word \tilde P_j to the ancilla. (eq_3, eq_4)
5. Uncompute f_j by applying O_j^\dagger, restoring the ancilla to |0\rangle; proceed to the next j. The product of all stages approximates D\otimes I to precision \varepsilon with T-count as in eq_6. (eq_3, eq_5, eq_6)
6. Instance walkthrough: n=2, D=diag(1,1,1,e^{i\pi/5}); Toffoli(data_1,data_0 -> anc), \tilde P_2 on anc with \varepsilon_2 = 5\times10^{-4}, Toffoli uncompute. (eq_7)

## Assumptions

- No experiment_scope was supplied, so a single ancilla-indicator construction and the n=2, k=2 instance D=diag(1,1,1,e^{i\pi/5}), \varepsilon=10^{-3} were chosen by the reconstructor.
- Error is measured in operator norm and allocated uniformly as \varepsilon/k per rotation; the paper's allocation and norm convention are not given in the abstract.
- C_0 is treated as a method-dependent constant in (1,4); no specific Rz-synthesis algorithm is asserted as the paper's choice.
- E(n,k) is modeled as the T-count of computing and uncomputing the k indicator functions with Toffoli-based logic; this is a surrogate for, not a reconstruction of, the paper's entanglement-cost function.
- Little-endian integer encoding of basis labels (qubit 0 = least significant bit).

## Missing information

- Closed-form or algorithmic definition of the entanglement cost E(n,k) and the specific reversible-logic/phase-context circuit the paper uses to achieve it.
- How the paper handles the extra log_2 k factor from distributing \varepsilon over k rotations (or whether a different error allocation is used).
- The precise Rz-synthesis method(s) and the corresponding value of C_0 the paper assumes.
- The optimal decision boundary in (n,k,\varepsilon)-space and the identity of the compared state-of-the-art techniques (e.g., Walsh-function-based diagonal decompositions).
- Quantitative evidence for the exponential-in-n T-gate reduction when k \ll 2^n (no numerical results are available from the abstract).
- Whether ancilla qubits, measurement-based uncomputation, or specific Toffoli decompositions are assumed in the paper's cost model.
