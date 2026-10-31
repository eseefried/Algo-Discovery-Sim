# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Approximate a target single-qubit unitary U to precision \varepsilon by a probabilistic protocol over a universal gate set (here Clifford+T) that terminates after a finite number of steps: one or more probabilistic multi-qubit-unitary-plus-measurement stages, followed on failure by a deterministic fallback approximation, so that the expected gate count is \log_b(1/\varepsilon)+O(\log\log(1/\varepsilon)).

Scope: Scoped (as an assumption, since no experiment_scope was supplied) to the smallest useful instance: a single-round Probabilistic Quantum Circuit with Fallback (PQF) for a single-qubit target U=R_z(\theta) using one ancilla qubit and one target qubit over Clifford+T, with a three-state absorbing Markov chain (start -> success/absorbed, start -> fail -> fallback -> absorbed). Tiny explicit instance: \theta=\pi/8 (i.e. U=\sqrt{T}, not exactly representable in Clifford+T). Outside scope: the paper's actual constructive synthesis of the stage unitary W (number-theoretic rounding/norm-equation solving), multi-round chains, the Clifford+V and Clifford+\pi/12 gate sets, the precise definition and values of the expansion constant b, and the proof of the stated asymptotic gate count.

## Symbols

- $U$: Target single-qubit unitary to be approximated; domain: SU(2)
- $\theta$: Rotation angle of the target z-rotation; domain: [0,2\pi)
- $\varepsilon$: Target approximation precision (operator-norm / trace-distance scale); domain: (0,1)
- $W$: Two-qubit unitary over the gate set acting on ancilla \otimes target, inducing one Markov-chain transition; domain: U(4), exactly synthesizable over Clifford+T
- $s$: Ancilla measurement outcome; domain: \{0,1\}
- $p$: Success probability of the probabilistic stage (outcome s=0); domain: [0,1]
- $U_0$: Unitary applied to the target on success; approximates U; domain: SU(2)
- $V_1$: Known unitary applied to the target on failure (outcome s=1); domain: SU(2)
- $F$: Deterministic ancilla-free fallback circuit approximating U V_1^{\dagger}; domain: SU(2), exactly synthesizable over Clifford+T
- $c(\cdot)$: T-count (number of T gates) of a circuit; domain: \mathbb{N}
- $\mathbb{E}[c]$: Expected T-count of the whole protocol; domain: \mathbb{R}_{\ge 0}
- $b$: Constant related to the expansion property of the universal gate set (defined in the paper, not in the abstract); domain: \mathbb{R}_{>1}
- $d(A,B)$: Distance between unitaries used to measure approximation error; domain: \mathbb{R}_{\ge 0}

## eq_1: Target unitary (tiny instance)

$$
U = R_z(\theta) = \begin{pmatrix} e^{-i\theta/2} & 0 \\ 0 & e^{i\theta/2} \end{pmatrix}, \quad \theta = \pi/8
$$

The single-qubit unitary to be approximated; chosen as a z-rotation whose angle makes it not exactly representable over Clifford+T.

Provenance: `assumption`. The abstract speaks only of 'a given single-qubit unitary'; a concrete z-rotation is chosen as the smallest useful instance.

Equation assumptions:

- Target restricted to z-rotations; general SU(2) targets reduce to this via Euler decomposition (background).
- \theta=\pi/8 is an arbitrary tiny instance.

## eq_2: Error metric

$$
d(A,B) = \sqrt{1 - \tfrac{1}{2}\,|\mathrm{tr}(A^{\dagger}B)|}, \qquad d(U,U_0)\le\varepsilon
$$

Global-phase-invariant distance commonly used in single-qubit Clifford+T synthesis; the success-branch unitary must be \varepsilon-close to the target.

Provenance: `standard_background`. Standard metric from Clifford+T synthesis literature; the abstract does not fix the metric.

Equation assumptions:

- Operator-norm error up to global phase would give equivalent asymptotics.

## eq_3: Single probabilistic stage (one Markov transition)

$$
(\langle s|_a \otimes I_t)\, W\, (|0\rangle_a \otimes I_t) = \begin{cases} \sqrt{p}\, U_0, & s=0 \\ \sqrt{1-p}\, V_1, & s=1 \end{cases}
$$

Applying the two-qubit unitary W to ancilla |0> and the target, then measuring the ancilla in the computational basis, applies U_0 (success) with probability p or a known unitary V_1 (failure) with probability 1-p. Both branches are required to be proportional to unitaries so the walk state remains a pure unitary error.

Provenance: `abstract_inferred`. Inferred from the abstract's description of transitions; the requirement that both Kraus branches be scaled unitaries is the standard RUS/PQF design condition and is not stated in the abstract.

Abstract evidence: transitions are induced by multi-qubit unitaries followed by measurements

Equation assumptions:

- Register ordering: ancilla is the left (most significant) tensor factor.
- Both measurement branches are exactly proportional to unitaries.
- W is exactly synthesizable over Clifford+T; its construction is not given in the abstract.

## eq_4: Fallback correction on failure

$$
d\big(F,\; U V_1^{\dagger}\big) \le \varepsilon \quad\Rightarrow\quad d\big(F V_1,\; U\big) \le \varepsilon
$$

On failure the protocol applies a deterministic ancilla-free Clifford+T approximation F of U V_1^dagger to the target, so that the overall implemented unitary F V_1 is within \varepsilon of U; the protocol then terminates (absorbing state).

Provenance: `abstract_inferred`. Finite termination requires a deterministic last step; a deterministic (e.g. optimal ancilla-free) approximation of the residual U V_1^dagger is the natural fallback consistent with the abstract's name 'Fallback'. Invariance of d under right-multiplication by a unitary is standard.

Abstract evidence: the presented PQF protocols terminate after a finite number of steps

Equation assumptions:

- Fallback is an ancilla-free deterministic Clifford+T approximation (abstract mentions such decompositions as the baseline).
- Single fallback stage; multi-round chains are out of scope.

## eq_5: Absorbing Markov chain and expected T-count (one round)

$$
P = \begin{pmatrix} 0 & p & 1-p \\ 0 & 1 & 0 \\ 0 & 0 & 1 \end{pmatrix} \text{ on states } (\mathrm{start},\mathrm{done},\mathrm{fail}),\qquad \mathbb{E}[c] = c(W) + (1-p)\, c(F)
$$

Three-state chain: from start, success (absorbed in done) with probability p, else fail; the fail state deterministically proceeds to done via F. The expected T-count is exactly the cost of W plus the fallback cost weighted by the failure probability.

Provenance: `abstract_inferred`. Direct formalization of the abstract's Markov-chain description for the minimal one-round case; the cost formula is the exact expectation over the two branches.

Abstract evidence: implements a walk on a discrete Markov chain in which the target unitary is an absorbing state

Equation assumptions:

- Measurement and Clifford gates are not counted (T-count metric).
- Only one probabilistic round before fallback.

## eq_6: Claimed asymptotic expected gate count

$$
\mathbb{E}[c] = \log_b(1/\varepsilon) + O\big(\log\log(1/\varepsilon)\big)
$$

The paper's headline scaling for Clifford+T, Clifford+V and Clifford+\pi/12, with b a gate-set-dependent expansion constant. This is a stated result, not derived here; achieving it requires c(W)\approx\log_b(1/\varepsilon) and (1-p)c(F)=O(\log\log(1/\varepsilon)), e.g. 1-p=O(1/\log(1/\varepsilon)).

Provenance: `abstract_explicit`. Stated verbatim in the abstract; the sufficient condition on p is an unverified remark, not a sourced derivation.

Abstract evidence: expected gate counts of $\log_{b}(1/\varepsilon)+O(\log(\log(1/\varepsilon)))$, where $b$ is a quantity related to the expansion property of the underlying universal gate set

Equation assumptions:

- The value/definition of b per gate set is not given in the abstract.

## Registers

- a (ancilla): 1 qubits; Measured ancilla whose outcome s selects the Markov transition; left/most-significant tensor factor
- t (target): 1 qubits; Qubit on which the approximation of U is implemented; right/least-significant tensor factor

## Initial state

|0\rangle_a \otimes |\psi\rangle_t with |\psi\rangle an arbitrary target state

## Measurement

Single computational-basis (Z) measurement of the ancilla qubit after W; outcome s\in\{0,1\} selects the branch. The target qubit is not measured.

## Classical postprocessing

Branch on s: s=0 -> done; s=1 -> apply fallback F. Optionally record outcomes over many runs to estimate p and the empirical expected T-count c(W)+(1-p)c(F).

## Algorithm steps

1. Fix target U=R_z(\theta) (\theta=\pi/8) and precision \varepsilon; obtain (by the paper's synthesis method, not reconstructed here) a Clifford+T two-qubit unitary W satisfying the scaled-unitary branch condition with d(U_0,U)\le\varepsilon, and a deterministic fallback F approximating U V_1^\dagger. (eq_1, eq_2, eq_3, eq_4)
2. Prepare the ancilla in |0\rangle_a and apply W to ancilla \otimes target. (eq_3)
3. Measure the ancilla in the computational basis, obtaining s. (eq_3, eq_5)
4. If s=0: U_0\approx U has been applied; terminate (absorbing state 'done'). (eq_3, eq_5)
5. If s=1: apply the fallback circuit F to the target so that F V_1 \approx U; terminate. Total expected T-count given by eq_5, targeting the scaling of eq_6. (eq_4, eq_5, eq_6)

## Assumptions

- No experiment_scope supplied; the single-round, one-ancilla Clifford+T PQF for R_z(\pi/8) is chosen as the smallest useful construction.
- Both measurement branches of W are exactly proportional to unitaries (standard RUS/PQF design condition, not stated in the abstract).
- The fallback is a deterministic, ancilla-free Clifford+T approximation of the residual unitary U V_1^\dagger.
- Cost is measured in T-count; Clifford gates and measurements are free.
- Error metric is the global-phase-invariant distance eq_2.

## Missing information

- Explicit construction of W (the paper's number-theoretic synthesis over Z[i,1/\sqrt{2}] or analogous rings) and how its T-count is bounded.
- Precise definition and numerical value of the expansion constant b for Clifford+T, Clifford+V and Clifford+\pi/12.
- Whether the paper uses one or several probabilistic rounds before fallback, and the resulting multi-state Markov chain parameters.
- How the success probability p is controlled as a function of \varepsilon to keep (1-p)c(F) within O(\log\log(1/\varepsilon)).
- Constructions for the Clifford+V and Clifford+\pi/12 gate sets.
- Any numerical gate-count comparisons against RUS or optimal deterministic decompositions.
