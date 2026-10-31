# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Unitary Permutation problem: given n black-box unitary gates U_1,...,U_n (same dimension) and a permutation sigma of {1,...,n}, implement the composite U_{sigma(n)} o ... o U_{sigma(1)}. The abstract reports (i) in the standard query model a fixed circuit using n^2-2n+4 calls to the U_i suffices, with a lower bound n^2-o(n^{7/4+eps}) under an extra assumption on the gate family, via connections with Karp's 'permutation as substring/subsequence' problem; (ii) in the quantum-switch model n log2(n)+Theta(n) switches are necessary and sufficient.

Scope: Scoped to the query-model upper bound only: a fixed (sigma-independent) circuit that reads a quantum control register |sigma> and applies U_sigma to a data register using exactly L=|w| black-box calls, where w is a word over {1,...,n} containing every permutation as a subsequence (Karp's problem). Smallest useful instance chosen: n=3, single-qubit gates, w=1213121 of length 7=3^2-2*3+4. Outside scope: the quantum-switch construction achieving n log2(n)+Theta(n) switches and its matching lower bound; the query lower bound n^2-o(n^{7/4+eps}) and the 'additional assumption on the family of gates'; general-n constructions of optimal Karp words. These are the paper's main contributions beyond the upper bound and are not reconstructed here.

## Symbols

- $n$: number of black-box unitary gates; domain: positive integer; instance n=3
- $U_i$: i-th black-box unitary gate, accessible only by calls; domain: U(d), i in {1,...,n}; instance d=2
- $\sigma$: permutation specifying the application order; sigma(k) is the index of the k-th gate applied; domain: S_n (symmetric group on {1,...,n})
- $U_\sigma$: target composite unitary U_{sigma(n)} ... U_{sigma(1)}; domain: U(d)
- $w = w_1 \cdots w_L$: fixed word (query schedule) over the gate alphabet; the j-th call is to U_{w_j}; domain: {1,...,n}^L
- $L$: length of w = number of black-box calls; domain: positive integer; L = n^2-2n+4 claimed sufficient; instance L=7
- $p_\sigma(k)$: position in w where the k-th gate of sigma is embedded (chosen embedding of sigma as a subsequence of w); domain: {1,...,L}, strictly increasing in k
- $a_j(\sigma)$: activity bit: 1 if call j acts on the data register for permutation sigma, 0 if it is diverted to a dummy register; domain: {0,1}
- $m_i$: multiplicity of symbol i in w; domain: non-negative integer; sum_i m_i = L
- $C$: control register holding |sigma>; domain: n*ceil(log2 n) qubits; block k (k=1 leftmost) holds binary of sigma(k)-1
- $D$: data register carrying |psi>; domain: d-dimensional; one qubit in the instance
- $A_i$: dummy register reserved for diverted calls to U_i; domain: d-dimensional; one qubit each in the instance; needed only if m_i >= 2
- $t$: one-qubit ancilla temporarily holding a_j(sigma); domain: qubit
- $|g\rangle$: final sigma-independent state of the dummy registers; domain: state of A_1 ... A_n

## eq_1: Target composite unitary

$$
U_{\sigma} := U_{\sigma(n)} \circ \cdots \circ U_{\sigma(1)} = U_{\sigma(n)} U_{\sigma(n-1)} \cdots U_{\sigma(1)}
$$

The unitary that must be implemented: U_{sigma(1)} is applied first, U_{sigma(n)} last.

Provenance: `abstract_explicit`. Directly stated as the definition of the Unitary Permutation problem.

Abstract evidence: in performing $U_{\sigma(n)}\circ\ldots\circ U_{\sigma(1)}$

Equation assumptions:

- All U_i act on the same d-dimensional system.

## eq_2: Fixed circuit controlled by a quantum permutation register

$$
W\big(|\sigma\rangle_{C} \otimes |\psi\rangle_{D} \otimes |0\rangle_{A_1\cdots A_n t}\big) = |\sigma\rangle_{C} \otimes \big(U_{\sigma}|\psi\rangle\big)_{D} \otimes |g\rangle_{A_1\cdots A_n} \otimes |0\rangle_{t}, \quad \forall\, \sigma \in S_n,\ \forall\, |\psi\rangle,\ \text{with } |g\rangle \text{ independent of } \sigma,\psi
$$

Correctness condition for a single sigma-independent circuit W that contains L black-box calls; by linearity it also works on superpositions of permutations because the residual ancilla state is sigma-independent.

Provenance: `abstract_inferred`. If sigma were a fixed classical parameter, n calls would trivially suffice, so nontrivial bounds of order n^2 only make sense for a single circuit that must work for every sigma supplied as input (as in the second-order/quantum-switch setting of [7]). The sigma-independence of |g> is my requirement to make the circuit valid on superpositions.

Abstract evidence: the complexity measure is the number of calls to any of the unitary gates $U_{i}$ in a quantum circuit which solves the problem

Equation assumptions:

- sigma is supplied as a computational-basis state of register C (possibly in superposition).
- Ancilla registers may be left in a fixed sigma-independent state.

## eq_3: Karp permutation-supersequence word (query schedule)

$$
w = w_1 w_2 \cdots w_L \in \{1,\ldots,n\}^{L},\quad L = n^{2}-2n+4,\quad \forall \sigma \in S_n\ \exists\, p_\sigma(1) < p_\sigma(2) < \cdots < p_\sigma(n):\ w_{p_\sigma(k)} = \sigma(k)\ (k=1,\ldots,n)
$$

A word over the gate alphabet containing every permutation of {1,...,n} as a (not necessarily contiguous) subsequence; its length equals the number of calls of the circuit.

Provenance: `abstract_inferred`. The abstract ties both query bounds to Karp's problem; the stated numbers n^2-2n+4 and n^2-o(n^{7/4+eps}) coincide (to my recollection) with the known upper bound (Adleman; Galbiati–Preparata) and the Kleitman–Kwiatkowski lower bound on the shortest sequence containing all permutations as subsequences. I therefore infer that the circuit calls the gates in the order given by such a word. The existence of such a word for every n is recalled background, not verified here.

Abstract evidence: $n^{2}-2n+4$ calls are sufficient to solve this problem in the standard quantum circuit model. We prove, with an additional assumption on the family of gates used in the circuits, that $n^{2}-o(n^{7/4+\epsilon})$ queries are required, for any $\epsilon>0$. The upper and lower bounds for the standard quantum circuit model are established by pointing out connections with the permutation as substring problem introduced by Karp.

Equation assumptions:

- Existence of a word of length n^2-2n+4 with the all-permutations-subsequence property (recalled from the literature for n >= 3; for n=3 verified by the explicit instance eq_7).

## eq_4: Activity bits and per-call routing operator

$$
a_j(\sigma) = \begin{cases} 1 & j \in \{p_\sigma(1),\ldots,p_\sigma(n)\} \\ 0 & \text{otherwise} \end{cases}, \qquad G_j = \sum_{\sigma \in S_n} |\sigma\rangle\langle\sigma|_{C} \otimes \Big( a_j(\sigma)\,(U_{w_j})_{D} + (1-a_j(\sigma))\,(U_{w_j})_{A_{w_j}} \Big)
$$

The j-th call to U_{w_j} acts on the data register if position j belongs to the chosen embedding of sigma, otherwise on the dummy register reserved for gate w_j. Identity on all unmentioned registers.

Provenance: `assumption`. My proposed realisation of the 'subsequence -> circuit' connection: exactly n of the L calls are routed to the data register, in the order sigma(1),...,sigma(n). Any deterministic rule for choosing p_sigma (e.g. greedy leftmost embedding) may be used.

Equation assumptions:

- A fixed deterministic embedding p_sigma is chosen classically for each sigma.
- Controlled operations conditioned on C are allowed and do not count as queries.

## eq_5: Implementation of G_j with one black-box call

$$
G_j = T_j^{\dagger}\; \mathrm{CSWAP}^{(t=0)}_{D,A_{w_j}}\; (U_{w_j})_{D}\; \mathrm{CSWAP}^{(t=0)}_{D,A_{w_j}}\; T_j, \qquad T_j\,|\sigma\rangle_{C}|0\rangle_{t} = |\sigma\rangle_{C}|a_j(\sigma)\rangle_{t}
$$

T_j is a reversible classical computation of the activity bit into ancilla t; CSWAP^{(t=0)} swaps D and A_{w_j} when t=0 (identity when t=1). The single black-box call U_{w_j} is always applied to wire D; routing is done by the swaps, so no controlled-U_i is required. t is uncomputed afterwards.

Provenance: `assumption`. Black-box calls cannot be controlled directly in the query model, so routing of the data by controlled swaps is the standard way to make a call act conditionally; this uses exactly one query per j.

Equation assumptions:

- Controlled-SWAP and the classical reversible circuit T_j are free (not counted as queries).

## eq_6: Full circuit, residual ancilla state and query count

$$
W = G_L \cdots G_2 G_1, \qquad |g\rangle = \bigotimes_{i=1}^{n} \big(U_i^{\,m_i-1}|0\rangle\big)_{A_i},\quad m_i = |\{j : w_j = i\}|, \qquad \#\text{calls} = L = n^{2}-2n+4
$$

Composing the G_j realises eq_2: the n active calls apply U_{sigma(1)},...,U_{sigma(n)} to D in order; each gate i is diverted exactly m_i-1 times to its own dummy A_i, so the dummy state does not depend on sigma. Exact equality, no approximation.

Provenance: `assumption`. Follows from eq_3–eq_5 by direct composition: for each sigma the data register sees exactly the subsequence w_{p_sigma(1)},...,w_{p_sigma(n)} = sigma(1),...,sigma(n); every symbol i occurs once actively, hence m_i-1 times passively, independent of sigma. The query count equals |w|, matching the abstract's upper bound.

Equation assumptions:

- Dummy registers are initialised to |0> (any fixed state works).

## eq_7: Explicit tiny instance n=3

$$
n=3,\ d=2,\ w = 1\,2\,1\,3\,1\,2\,1,\ L = 7 = 3^2-2\cdot 3+4,\ (m_1,m_2,m_3)=(4,2,1); \quad \text{e.g. } \sigma=(3,2,1):\ (p_\sigma(1),p_\sigma(2),p_\sigma(3))=(4,6,7),\ a(\sigma)=(0,0,0,1,0,1,1),\ U_\sigma = U_1 U_2 U_3
$$

The word 1213121 contains all six permutations of {1,2,3} as subsequences (123:1,2,4; 132:1,4,6; 213:2,3,4; 231:2,4,5; 312:4,5,6; 321:4,6,7). Registers: C = 6 qubits (three 2-qubit blocks holding sigma(k)-1), D = 1 qubit, A_1 and A_2 = 1 qubit each (A_3 unnecessary since m_3=1), t = 1 qubit.

Provenance: `assumption`. Smallest n for which the abstract's formula n^2-2n+4 equals the (recalled) optimal Karp length; chosen as the concrete instance in the absence of an experiment scope. Subsequence check done by hand above.

Equation assumptions:

- Single-qubit gates U_1,U_2,U_3 as black boxes.
- Encoding of sigma as listed.

## eq_8: Quantum switch (second-order primitive, background only)

$$
S(U,V)\,\big(|c\rangle \otimes |\psi\rangle\big) = \begin{cases} |0\rangle \otimes V U |\psi\rangle & c=0 \\ |1\rangle \otimes U V |\psi\rangle & c=1 \end{cases}
$$

A quantum switch takes two unitaries as inputs and applies them in one of two orders controlled coherently by a qubit; the switch-model complexity counts such primitives. Only the definition is recalled; the n log2(n)+Theta(n) construction is not reconstructed.

Provenance: `standard_background`. Standard definition of the quantum switch as used in Colnaghi et al. and the indefinite-causal-order literature; included to make the scope boundary explicit.

Equation assumptions:

- Convention for which order corresponds to c=0 is arbitrary.

## Registers

- C: n*ceil(log2 n) qubits (6 for n=3) qubits; holds the permutation |sigma>; block k (k=1 leftmost) stores sigma(k)-1 in binary; unchanged by the circuit
- D: log2 d qubits (1 for the instance) qubits; data register on which U_sigma is applied
- A_i (i=1..n): log2 d qubits each (1 each; A_i omitted if m_i = 1) qubits; dummy register absorbing the m_i-1 inactive calls to U_i; ends in the sigma-independent state U_i^{m_i-1}|0>
- t: 1 qubit qubits; ancilla holding the activity bit a_j(sigma) during call j; returned to |0>

## Initial state

|sigma>_C (or any superposition of permutation basis states) ⊗ |psi>_D ⊗ |0...0>_{A_1...A_n} ⊗ |0>_t, with register order C ⊗ D ⊗ A_1 ⊗ ... ⊗ A_n ⊗ t.

## Algorithm steps

1. Fix the query schedule: choose a word w over {1,...,n} of length L containing every permutation as a subsequence (instance: w=1213121), and for each sigma fix an embedding p_sigma and the activity bits a_j(sigma). (eq_3, eq_4, eq_7)
2. For j = 1,...,L: compute a_j(sigma) into t (T_j); if t=0 swap D with A_{w_j}; call U_{w_j} on wire D (one query); if t=0 swap back; uncompute t (T_j^dagger). (eq_4, eq_5)
3. After all L calls the data register holds U_sigma|psi>, C is unchanged, and the dummy registers hold the sigma-independent state |g>; total queries L = n^2-2n+4 (7 for n=3). (eq_1, eq_2, eq_6)

## Assumptions

- The permutation sigma is provided as a quantum register input (as in the second-order setting of Colnaghi et al.), so a single sigma-independent circuit is required; otherwise the problem is trivial with n calls.
- Black boxes U_i can only be invoked as plain calls on a chosen wire (no controlled-U_i); routing via controlled-SWAP and classical reversible logic conditioned on C is free.
- All gates act on the same d-dimensional system; the instance uses d=2 (single-qubit gates) and n=3.
- Existence of a word of length n^2-2n+4 containing all permutations of {1,...,n} as subsequences is recalled from the literature on Karp's problem and only verified here for n=3.
- The per-gate dummy-register construction (eq_4–eq_6) is my proposed realisation of the abstract's Karp connection, not a verified reproduction of the paper's circuit.
- Equation eq_8 is background only; the switch-model results are not reconstructed.

## Missing information

- The paper's explicit quantum-switch circuit achieving n log2(n)+Theta(n) switches and the proof of the matching lower bound.
- The 'additional assumption on the family of gates' under which the n^2-o(n^{7/4+eps}) query lower bound holds, and the reduction to Karp's problem used in the proof.
- Whether the paper's query model treats sigma as a classical description or a quantum control register, and what output is required on ancillas.
- The specific Karp word of length n^2-2n+4 used for general n and the paper's own routing/ancilla scheme.
- The dimension d of the gates and any restrictions on the gate family.
