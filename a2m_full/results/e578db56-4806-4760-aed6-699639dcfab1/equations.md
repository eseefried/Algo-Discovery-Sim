# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate a single-qubit unitary U (via Euler angles, here one Rz(theta)) to precision eps using a Clifford+T repeat-until-success circuit with one ancilla: a 2-qubit Clifford+T block W is applied, the ancilla is measured, outcome 0 means the data qubit received a block-encoded operator A approximating U, and outcome 1 triggers a correction and a retry.

Scope: Smallest instance: 2 qubits (q0 data, q1 ancilla). A fixed small Clifford+T block W that block-encodes a non-unitary single-qubit operator A=<0|_anc W |0>_anc on the data qubit. Check the success-branch operator, the success probability, and the expected T-count of the retry loop. Out of scope: the paper's probabilistic polynomial-time classical synthesis algorithm (randomized Diophantine/factoring search), full exact synthesis over Z[i,1/sqrt2], and the claimed 2.5x average numerical T-count reduction. The abstract does not give the actual RUS gate sequence, so any concrete circuit is a placeholder.

## Symbols

- $U$: target single-qubit unitary; domain: SU(2)
- $\varepsilon$: target approximation precision; domain: (0,1)
- $W$: 2-qubit Clifford+T circuit on (data q0, ancilla q1); domain: U(4), entries in Z[i,1/sqrt2]/sqrt2^k
- $A$: success-branch operator on the data qubit, A=(<0|_{anc} \otimes I)W(|0>_{anc} \otimes I); domain: 2x2 complex matrix, ||A||<=1
- $p_s$: success probability for input state |psi>; domain: [0,1]
- $T_W$: T-count of one attempt of W; domain: nonnegative integer
- $\mathbb{E}[T]$: expected total T-count of the RUS loop; domain: positive real

## eq_1: Block encoding on success

$$
A=(I\otimes\langle 0|_{1})\,W\,(I\otimes|0\rangle_{1}),\quad W(|\psi\rangle|0\rangle)=A|\psi\rangle|0\rangle+B|\psi\rangle|1\rangle
$$

Outcome 0 on the ancilla leaves the data qubit in A|psi>/||A psi||; outcome 1 leaves it in B|psi>/||B psi||.

Provenance: `abstract_inferred`. One ancilla plus measurement in a Clifford+T circuit implies a post-selected, generally non-unitary branch operator; the formula is the standard block-encoding form.

Abstract evidence: Our synthesis approach uses the Clifford+$T$ basis, plus one ancilla qubit and measurement.

Equation assumptions:

- Little-endian ordering: q0 is data, q1 is ancilla
- Ancilla starts in |0>

## eq_2: Success probability

$$
p_s(\psi)=\|A|\psi\rangle\|^2,\quad A^\dagger A+B^\dagger B=I
$$

Probability of ancilla outcome 0. For a state-independent probability, A^\dagger A=p_s I, so A=sqrt(p_s)*V with V unitary.

Provenance: `standard_background`. Follows from unitarity of W.

Equation assumptions:

- RUS usefulness requires A proportional to a unitary V near U

## eq_3: Approximation criterion

$$
\left\|\,A/\sqrt{p_s}-U\right\|\le\varepsilon\ \text{(up to global phase)},\quad A=\tfrac{1}{\sqrt2^{\,k}}\begin{pmatrix}u&-v^{*}\\ v&u^{*}\end{pmatrix}$$
$$

Success-branch operator in the sketch's form, with u,v in Z[i,1/sqrt2] and normalized to a unitary V=A/sqrt(p_s) within eps of U.

Provenance: `assumption`. Taken from the sketch's matrix form. The abstract only says the RUS circuit approximates U within eps. The success-branch normalization is not derived in the abstract.

Equation assumptions:

- Operator-norm distance modulo global phase is the accuracy metric
- Exact form of u,v for the paper's construction is unknown

## eq_4: Expected T-count of RUS loop

$$
\mathbb{E}[T]=T_W/p_s \ \text{(upper bound; if the failure branch is restored by Cliffords)}
$$

With geometric number of attempts, mean attempts is 1/p_s, so the expected T cost is the per-attempt T-count over p_s.

Provenance: `standard_background`. Mean of a geometric distribution. The abstract compares expected T-count against the ancilla-free bound.

Equation assumptions:

- Independent attempts, failure restored by Cliffords or a state-independent fixup
- Failure branches may have different T costs; the formula is then modified

## eq_5: Ancilla-free lower bound reference

$$
T_{\text{anc-free}}\ge 3\log_2(1/\varepsilon)
$$

The reference bound the RUS expected T-count is compared against.

Provenance: `abstract_explicit`. Stated directly in the abstract. The claim is about the average ratio being 2.5, so E[T] is about 1.2 log2(1/eps) on average.

Abstract evidence: theoretical lower bound of $3\log_{2}(1/\varepsilon)$ for ancilla-free single-qubit circuit decomposition

Equation assumptions:

- Asymptotic/average statement, not a bound on every instance

## Registers

- q0: 1 qubits; data qubit (Qiskit bit 0, rightmost in counts keys)
- q1: 1 qubits; ancilla, initialized to |0>, measured to flag success (0) or failure (1)

## Initial state

|psi>_{q0} \otimes |0>_{q1}

## Measurement

Measure ancilla q1 only (classical bit 0 holds it). Outcome 0 means success. For a single-shot simulator, postselect on ancilla=0 and read the data qubit state or its statistics.

## Classical postprocessing

Retry on outcome 1. Compute the empirical success rate and the operator distance of the post-selected data state to U|psi>. Compute E[T]=T_W/p_s.

## Algorithm steps

1. Choose the target U (e.g. Rz(theta)) and eps. Classically find W over Clifford+T whose success branch A approximates U. The paper's randomized polynomial-time search is not reconstructed; use a fixed hand-chosen W in a toy instance. (eq_3, eq_5)
2. Apply W from the gate set {h,s,t,tdg,cx} to q0,q1 starting from the ancilla in |0>. (eq_1)
3. Measure q1. If 0, the data qubit holds A|psi>/||A psi|| and the loop stops. If 1, apply the Clifford correction or restore a known state, then repeat. (eq_1, eq_2)
4. Estimate the expected T-count as per-attempt T-count over success probability and compare with 3 log2(1/eps). (eq_4, eq_5)

## Assumptions

- Scope choice: a single Rz-like target on one data qubit with one ancilla
- Mid-circuit measurement with classical control is available, or the loop is simulated by postselection
- Success probability is bounded away from zero
- The sketch's description of the fallback pattern, arccos(1/3) angles and the specific 1.2 log2(1/eps) cost is not established by the abstract

## Missing information

- Actual RUS circuit family and gate sequence
- Form of the failure branch and its correction
- Randomized synthesis algorithm and its number-theoretic details
- How to guarantee A is proportional to a unitary for the chosen (u,v)
- Numerical benchmark data
