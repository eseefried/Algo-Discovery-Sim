# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given black-box unitaries U_1..U_n on a d-qubit data register and a permutation sigma (held as basis-state control data), implement U_{sigma(n)} ... U_{sigma(1)} on the data register using a fixed-length string of controlled placements of the U_i, with ancillas returned to |0>.

Scope: Standard-circuit-model upper bound only, for tiny n (n=3, string length n^2-2n+4=7, assuming such a string exists). The string must contain every permutation of {1,2,3} as a contiguous substring. The switch-model bound n log2 n + Theta(n), the lower bounds, and the Karp-connection proofs are out of scope.

## Symbols

- $n$: number of unitary gates; domain: integer >= 2; tiny instance n=3
- $U_i$: opaque placeholder gate on the d-qubit data register; domain: i in {1..n}
- $\sigma$: permutation giving the application order; domain: S_n
- $s=s_1\ldots s_L$: fixed classical string over {1..n} containing every permutation as a contiguous substring; domain: s_t in {1..n}
- $L$: string length, equal to the number of queries; domain: integer, n^2-2n+4 claimed
- $k_t$: progress counter: number of gates of sigma applied after step t; domain: {0..n}
- $|\psi\rangle$: data register input state; domain: C^{2^d}

## eq_1: Target operation

$$
V_\sigma=U_{\sigma(n)}\cdots U_{\sigma(2)}U_{\sigma(1)}
$$

Unitary to be implemented on the data register.

Provenance: `abstract_explicit`. Directly stated problem definition.

Abstract evidence: in performing $U_{\sigma(n)}\circ\ldots\circ U_{\sigma(1)}$

## eq_2: Query upper bound

$$
L=n^{2}-2n+4
$$

Number of calls sufficient in the standard model, equal to the string length (n=3 gives 7).

Provenance: `abstract_explicit`. Stated in the abstract. Identifying the calls with a string of this length follows the sketch and the stated link to the permutation-as-substring problem.

Abstract evidence: $n^{2}-2n+4$ calls are sufficient to solve this problem in the standard quantum circuit model

Equation assumptions:

- A suitable string of this length exists for the tested n

## eq_3: Substring property

$$
\forall\sigma\in S_n\ \exists t:\ s_{t+1}s_{t+2}\cdots s_{t+n}=\sigma(1)\sigma(2)\cdots\sigma(n)
$$

Every permutation occurs as a contiguous window of s.

Provenance: `abstract_inferred`. Inferred from the stated connection to Karp's problem. The exact construction in the paper is not given in the abstract.

Abstract evidence: pointing out connections with the permutation as substring problem introduced by Karp

Equation assumptions:

- The string is a Karp-type permutation-containing string

## eq_4: Counter-controlled step

$$
W_t=\sum_{k=0}^{n}\Big(\big[\,s_t=\sigma(k+1),\ k<n\,\big]\,|k+1\rangle\langle k|\otimes U_{s_t}+\big[\,\text{else}\,\big]\,|k\rangle\langle k|\otimes I\Big)
$$

At step t, if the counter is k and s_t=sigma(k+1), apply U_{s_t} and increment k. Otherwise do nothing. The comparison is read from the basis-state sigma register.

Provenance: `assumption`. Proposed from the sketch. It is not shown in the abstract. As written it applies gates greedily, so the first matching symbols also advance the counter, even outside the window that finally completes sigma. The result is correct only if the counter is reset or the condition is restricted to the window.

Equation assumptions:

- Greedy matching is not guaranteed to give V_sigma
- Counter increments and ancilla uncomputation must be defined without a query

## eq_5: Desired net action

$$
\Big(\prod_{t=L}^{1}W_t\Big)\,|\sigma\rangle|0\rangle_{anc}|\psi\rangle=|\sigma\rangle|0\rangle_{anc}\,V_\sigma|\psi\rangle
$$

Target check: data register equals V_sigma applied to psi, ancillas return to |0>, no measurement.

Provenance: `assumption`. Statement of the readout criterion from the task, to be checked by statevector simulation.

Equation assumptions:

- Ancilla uncomputation without extra queries is achievable

## Registers

- data: d qubits; holds |psi> and receives the placeholder gates U_i
- sigma: n*ceil(log2 n) (6 for n=3) qubits; basis-state control data encoding sigma(1..n)
- counter: ceil(log2(n+1)) (2 for n=3) qubits; progress counter k
- flag: 1 qubits; comparison flag used as the control for U_{s_t}

## Initial state

|sigma>_sigma |0>_counter |0>_flag |psi>_data, with sigma a computational-basis value

## Classical postprocessing

None. The runner compares the data-register statevector or unitary with V_sigma, with ancillas in |0>.

## Algorithm steps

1. Fix the classical string s of length L and the tiny instance (n=3). (eq_2, eq_3)
2. For t=1..L: compute the flag by comparing s_t with sigma(k+1) given counter k. Apply the placeholder U_{s_t} on data controlled on the flag. Increment the counter when the flag is set. Then uncompute the flag. (eq_4)
3. Uncompute the counter to |0> using the sigma register, with no extra queries. Check the data register against V_sigma. (eq_1, eq_5)

## Assumptions

- Sigma is given as basis-state control data, not hidden in a black box
- The tiny instance is n=3, L=7, with a string that contains all 6 permutations
- Each controlled placeholder costs one query
- Switch-model and lower-bound results are outside scope

## Missing information

- The explicit string and the exact windowing and reset rule that make the construction correct, since the abstract gives none
- The construction for how ancillas are uncomputed after the data gates are applied
- The paper's actual construction might not be controlled-placement-based
- The switch-model recursion and lower-bound argument
