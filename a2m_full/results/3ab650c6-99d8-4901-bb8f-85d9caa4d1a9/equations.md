# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Implement a bipartite permutation unitary P on C^{dA} x C^{dB} (|a,b> -> |pi(a,b)>) using only standard gates, with few CNOTs across the A|B cut, via the operator-Schmidt decomposition and a nonnegative-rank-style protocol. Verify on tiny instances (e.g. dA=dB=2) by reading the unitary or statevector.

Scope: One tiny instance: dA=dB=2 (1 qubit each), P = CNOT with A as control, operator-Schmidt rank r=2. Build it as a sum of 2 product terms using one ebit/CNOT-equivalent across the cut, in a gate-teleportation style (non-local CNOT through a Bell pair), and check unitary equality with P and ancillas returning to |0>. The general r_+ protocol, the 4dA-5 and 2dA-1 controlled-unitary bounds, the n-partite bound, and the log-rank link are outside scope.

## Symbols

- $P$: bipartite permutation unitary, P|a,b>=|pi(a,b)>; domain: unitary on C^{dA} x C^{dB}
- $A_k,B_k$: operator-Schmidt factors; domain: operators on C^{dA}, C^{dB}
- $r$: operator-Schmidt rank of P; domain: positive integer
- $M$: communication matrix M[(a,a');(b,b')]=<a,b|P|a',b'>; domain: 0/1 matrix of size dA^2 x dB^2
- $r_+$: nonnegative rank of M; domain: integer, r_+ >= r
- $\pi$: permutation of [dA]x[dB]; domain: bijection

## eq_1: Operator-Schmidt decomposition

$$
U=\sum_{k=1}^{r}A_k\otimes B_k
$$

Any bipartite operator is a sum of r product operators; r is the Schmidt rank of U.

Provenance: `abstract_inferred`. The abstract uses the Schmidt rank of the unitary as the cost parameter, which presupposes this decomposition.

Abstract evidence: as functions of the Schmidt rank of the unitary

Equation assumptions:

- Standard definition of operator-Schmidt rank

## eq_2: Permutation as 0/1 matrix and communication matrix

$$
M[(a,a');(b,b')]=\langle a,b|P|a',b'\rangle\in\{0,1\},\quad r=\operatorname{rank}M
$$

P is a real 0/1 matrix; its operator-Schmidt rank equals the rank of the reshaped (communication) matrix M.

Provenance: `abstract_inferred`. The link to log-rank and nonnegative rank implies this reshaping. The rank equality is standard linear algebra.

Abstract evidence: related to the log-rank conjecture in communication complexity theory via the link of nonnegative rank

Equation assumptions:

- Reshaping is by row index (a,a') and column index (b,b')

## eq_3: Nonnegative factorization

$$
M=\sum_{k=1}^{r_+}u_k v_k^{T},\quad u_k\ge0,\ v_k\ge0,\quad r\le r_+
$$

Nonnegative rank gives the number of rounds or terms in the protocol.

Provenance: `abstract_inferred`. The abstract links the cost to nonnegative rank. The explicit form is the standard definition.

Abstract evidence: related to the log-rank conjecture in communication complexity theory via the link of nonnegative rank

Equation assumptions:

- Cost is proportional to r_+ in a simple protocol, as the sketch says; the abstract does not give the exact form

## eq_4: Toy instance: CNOT as two product terms

$$
P=\mathrm{CNOT}_{A\to B}=|0\rangle\langle0|\otimes I+|1\rangle\langle1|\otimes X
$$

The chosen instance has rank 2 and uses one ebit via non-local CNOT.

Provenance: `assumption`. Smallest nontrivial permutation across the cut, chosen as the scoped instance.

Equation assumptions:

- dA=dB=2

## eq_5: Success criterion

$$
\left(\langle0|_{anc}\otimes I\right)W\left(|0\rangle_{anc}\otimes I\right)=P,\quad W|a,b,0_{anc}\rangle=|\pi(a,b)\rangle|0_{anc}\rangle
$$

The circuit W acts as P on the data registers and returns the ancillas to |0>.

Provenance: `assumption`. Check required by the runner: compare the unitary or statevector against P.

Equation assumptions:

- Ancillas start in |0>

## Registers

- A: ceil(log2 dA) (1 in toy) qubits; Alice's data
- B: ceil(log2 dB) (1 in toy) qubits; Bob's data
- E: 2 qubits; Bell-pair ancillas, one on each side of the cut, returned to |0>

## Initial state

|a>_A|b>_B|00>_E; for the unitary check, prepare the Bell pair inside the circuit and uncompute it at the end

## Classical postprocessing

Classical: compute M from pi, its rank r (numpy), and optionally a nonnegative factorization to estimate r_+. Compare the circuit's unitary block to P.

## Algorithm steps

1. Prepare a Bell pair on E (H on e0, CNOT e0->e1). This CNOT is local to ancilla preparation, but e1 is placed on Bob's side, so it counts as the one cut-crossing resource. (eq_4)
2. Non-local CNOT through the Bell pair: Alice does CNOT A->e0 and measures-free coherent correction. In a unitary-only version, implement the CNOT directly across the cut with one CNOT as a reference and compare it against the teleportation-style version. (eq_1, eq_3, eq_4)
3. Uncompute the flag and Bell pair by the reverse round so the ancillas return to |0>. (eq_5)
4. Read the full unitary (no measurements), restrict to ancilla=|0>, and compare to P up to global phase. Also check basis inputs |a,b>. (eq_2, eq_5)

## Assumptions

- Cost is the CNOT count across the A|B cut, with local gates free
- Ancillas have fixed size and return to |0>
- Tiny instance dA=dB=2 chosen as scope
- P is real 0/1 so nonnegative factorization applies
- No measurements are used because the unitary or statevector is checked

## Missing information

- The exact protocol construction is not in the abstract; the coherent, measurement-free uncompute of the teleportation-style gate is unspecified
- The precise relation between CNOT cost and r_+ (the abstract states only the link)
- The dimension-independent bounds
- The controlled-unitary decomposition counts are not used here
