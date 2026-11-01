# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate a diagonal n-qubit unitary D=sum_x exp(i theta(x))|x><x| with only k distinct phase values using about k phase rotations (Clifford+T approximated) plus an entangling index-computation cost E(n,k), instead of 2^n rotations.

Scope: One tiny instance (assumed n=3, k=3 phases on 8 basis states, m=2 index ancillas). Construction: compute phase-index j(x) into an m-qubit register, apply the diagonal on the index register via parity Rz rotations, uncompute. Out of scope: the paper's actual E(n,k) optimization, the optimal decision boundary in (n,k,epsilon), the proof of the C0 bounds, and the comparison against other synthesis methods.

## Symbols

- $n$: number of data qubits; domain: positive integer
- $k$: number of distinct phases in D; domain: integer, 1<=k<=2^n
- $m$: index register size, ceil(log2 k); domain: positive integer
- $\varepsilon$: target total approximation precision; domain: (0,1)
- $C_0$: quality factor of the rotation synthesis method; domain: (1,4)
- $E(n,k)$: entanglement cost of the index oracle, in T gates; domain: nonnegative integer
- $j(x)$: index of the level set containing x; domain: {0,...,k-1}
- $\phi_j$: j-th distinct phase value; domain: real, mod 2\pi
- $U_j$: reversible oracle |x>|0> -> |x>|j(x)>; domain: unitary on n+m qubits

## eq_1: Target diagonal

$$
D=\sum_{x=0}^{2^n-1}e^{i\phi_{j(x)}}|x\rangle\langle x|,\quad j(x)\in\{0,\dots,k-1\}
$$

D takes k distinct phase values determined by level sets of x.

Provenance: `abstract_inferred`. Defines D from the abstract's k distinct phases; the level-set form is the sketch's construction.

Abstract evidence: $k$ is the number of distinct phases in the diagonal $n$-qubit unitary

Equation assumptions:

- The partition is known classically at compile time

## eq_2: Compute-phase-uncompute

$$
D\otimes I_{anc}=U_j^{\dagger}\,(I_n\otimes \Delta)\,U_j,\quad U_j|x\rangle|0\rangle=|x\rangle|j(x)\rangle,\quad \Delta=\sum_{j<k}e^{i\phi_j}|j\rangle\langle j|+\text{(any phases on unused }j\ge k)
$$

Phase is written on the index register, then the index is uncomputed, returning ancillas to |0>.

Provenance: `assumption`. Proposed construction from the sketch; the abstract only implies an entanglement cost.

Equation assumptions:

- Ancillas start in |0>
- Unused index values never occur

## eq_3: Parity (Walsh) decomposition of index diagonal

$$
\Delta=e^{i\gamma}\prod_{s\in P}\exp\!\left(-i\tfrac{\alpha_s}{2}Z^{s}\right),\quad \phi_j=\gamma-\tfrac12\sum_{s\in P}\alpha_s(-1)^{s\cdot j},\; |P|\le 2^m-1
$$

The index diagonal is a product of Rz rotations on parities Z^s of index bits. Coefficients alpha_s come from the Walsh-Hadamard transform of phi_j. The sketch claims at most k-1 are needed.

Provenance: `standard_background`. Standard phase-polynomial/Walsh expansion. For k=2^m there are 2^m-1 nontrivial parities. The k-1 reduction for general k needs free phases on unused indices, which is an assumption.

Equation assumptions:

- Unused index values may take free phases
- Global phase gamma is ignored

## eq_4: T-count bound

$$
T_{\text{total}}\le k\,C_0\log_2(1/\varepsilon)+E(n,k)
$$

Equivalent T-count bound of the synthesized circuit.

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: The equivalent $T$-count of the synthesized circuit is bounded by $kC_{0}\log_{2}(1/\varepsilon)+E(n,k)$

Equation assumptions:

- 1<C_0<4

## eq_5: Per-rotation precision

$$
\varepsilon_{rot}=\varepsilon/k,\quad \text{T per rotation}\approx C_0\log_2(k/\varepsilon)
$$

Linear error accumulation across k rotations. The log k term is dropped in the stated bound, which treats it as lower order.

Provenance: `assumption`. Triangle inequality for operator-norm errors; the sketch says precision epsilon/k.

Equation assumptions:

- Errors add linearly

## Registers

- data: n (assumed 3) qubits; input qubits on which D acts
- index: m=ceil(log2 k) (assumed 2) qubits; ancilla holding j(x); returned to |0>
- toffoli_work: 0 to a few qubits; optional extra ancillas for multi-controlled gate decomposition

## Initial state

Arbitrary data state (test on all basis states or the full unitary); index and work ancillas in |0>.

## Classical postprocessing

Compare the circuit's unitary or statevector, restricted to ancillas |0>, against D up to global phase (compare diag(D) after removing the phase of entry 0), with tolerance epsilon. Optionally count T gates against eq_4.

## Algorithm steps

1. Classically group the 2^n basis states into k level sets by phase and assign index j. (eq_1)
2. Build the reversible oracle U_j with CNOT/Toffoli/multi-controlled X gates, e.g. via ESOP or XOR-sum synthesis, writing j(x) into the index register. (eq_2)
3. Compute Walsh coefficients alpha_s of phi_j. For each parity s, CNOT the parity into one index qubit, apply Rz(alpha_s), and uncompute the CNOTs. (eq_3)
4. Optionally replace each Rz by a Clifford+T approximation at precision epsilon/k. For exact-rotation simulation, keep Rz. (eq_5, eq_4)
5. Apply U_j^dagger to uncompute the index register, so the ancillas return to |0>. (eq_2)

## Assumptions

- Tiny instance n=3, k=3 is a choice, not from the abstract
- Phases and level sets are known at compile time
- Index has ceil(log2 k) qubits plus optional work qubits within the cap
- Standard Rz Clifford+T synthesizer such as gridsynth
- E(n,k) comes from a generic reversible synthesis, not an optimum
- No measurements; the runner reads the unitary or statevector

## Missing information

- The paper's actual oracle synthesis and E(n,k) formula
- The decision boundary in (n,k,epsilon) space
- Definition of C_0 and how it relates to the synthesis method
- Whether the paper uses this exact index-register construction
- Exact treatment of phases on unused indices when k is not a power of 2
