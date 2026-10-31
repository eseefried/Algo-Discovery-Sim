# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Learn an unknown n-bit parity function f_s(x) = s·x mod 2 (i.e. recover the hidden string s in {0,1}^n) from a quantum example oracle whose n+1 output qubits are each subjected to depolarizing noise at a constant rate p, using a number of oracle queries and computation that grows at most logarithmically beyond the noiseless case, in contrast to the classical Learning Parity with Noise (LPN) problem.

Scope: One smallest useful construction: the Bernstein–Vazirani-style Hadamard-transform learner applied to noisy quantum examples, for a tiny explicit instance n = 3, hidden string s = (1,0,1), single-qubit depolarizing rate p = 0.1 applied independently to all n+1 oracle output qubits, with m repeated queries and a per-bit correlation estimate as classical postprocessing. Outside scope: the paper's precise noise model and algorithm (only inferred here), the formal proof that noise costs only a logarithmic factor, the classical LPN hardness comparison, the 'few hundred qubits' resource estimate, and the claim that noise is essential for the separation.

## Symbols

- $n$: Number of input bits of the parity function; also number of data qubits; domain: positive integer (instance: n = 3)
- $s$: Hidden parity string defining the target concept; domain: \{0,1\}^n (instance: s = (1,0,1))
- $x$: Input string to the parity function / computational basis label of the data register; domain: \{0,1\}^n
- $f_s(x)$: Parity of x on the support of s; domain: \{0,1\}
- $p$: Depolarizing rate applied to each oracle output qubit; domain: [0,1) constant (instance: p = 0.1)
- $\Lambda_p$: Single-qubit depolarizing channel; domain: CPTP map on 2x2 density matrices
- $H$: Single-qubit Hadamard gate; domain: 2x2 unitary
- $c$: Latent branch bit of a single measured sample (which GHZ-like branch is observed); domain: \{0,1\}, uniform
- $e_i$: Effective bit-flip noise on measured qubit i; domain: \{0,1\}, Bernoulli(p/2), independent over i
- $(y,b)$: Measured outcome: y on the n data qubits, b on the label qubit; domain: \{0,1\}^n \times \{0,1\}
- $m$: Number of oracle queries (repetitions); domain: positive integer
- $\delta$: Target failure probability of the learner; domain: (0,1)

## eq_1: Parity concept class

$$
f_s(x) = s \cdot x \bmod 2 = \bigoplus_{i=1}^{n} s_i x_i, \qquad s, x \in \{0,1\}^n
$$

Definition of the n-bit parity function labelled by the hidden string s; the learning task is to recover s exactly.

Provenance: `abstract_inferred`. The abstract names the concept class; the standard definition of a parity function is the inner product mod 2 with a hidden string.

Abstract evidence: learning the class of $n$-bit parity functions

Equation assumptions:

- Standard definition of parity functions; no affine offset is included.

## eq_2: Noiseless quantum example oracle state

$$
|\psi_s\rangle = \frac{1}{\sqrt{2^n}} \sum_{x \in \{0,1\}^n} |x\rangle_{D} \, |f_s(x)\rangle_{L}
$$

Each oracle query returns the uniform superposition of labelled examples; register D (qubits 1..n, qubit i holds x_i) carries the input and register L (qubit n+1) the label.

Provenance: `standard_background`. The Bshouty–Jackson quantum example oracle under the uniform distribution is the standard meaning of 'quantum example oracle'; the abstract does not write the state explicitly.

Equation assumptions:

- Examples are drawn from the uniform distribution over inputs.
- Register ordering: data qubits 1..n then label qubit n+1.

## eq_3: Single-qubit depolarizing noise on oracle output

$$
\Lambda_p(\rho) = (1-p)\rho + p\,\frac{I}{2}, \qquad \rho_{\mathrm{out}} = \Lambda_p^{\otimes (n+1)}\big(|\psi_s\rangle\langle\psi_s|\big)
$$

Every one of the n+1 output qubits is depolarized independently at constant rate p before the learner acts.

Provenance: `standard_background`. Textbook depolarizing channel; the abstract says the output qubits are depolarized at a constant rate but does not specify whether noise is per-qubit i.i.d., so the product form is a modelling choice.

Equation assumptions:

- Independent, identical depolarizing noise on each output qubit with the same rate p.
- Noise acts only at the oracle output; the learner's gates and measurements are noiseless.

## eq_4: Hadamard transform of the noiseless example state (exact)

$$
H^{\otimes (n+1)} |\psi_s\rangle = \frac{1}{\sqrt{2}}\left( |0^n\rangle_{D}|0\rangle_{L} + |s\rangle_{D}|1\rangle_{L} \right)
$$

The Bernstein–Vazirani identity: a Hadamard on all qubits maps the example state to an equal superposition of the all-zero branch and the branch revealing s with label 1. This equality is exact.

Provenance: `standard_background`. Standard Fourier-sampling computation: sum over x of (-1)^{y·x + b(s·x)} vanishes unless y = b s.

## eq_5: Computational-basis outcome distribution of one noisy sample

$$
\Pr[(y,b)] = \sum_{c \in \{0,1\}} \frac{1}{2} \prod_{i=1}^{n} \left(\tfrac{p}{2}\right)^{[y_i \neq c s_i]} \left(1-\tfrac{p}{2}\right)^{[y_i = c s_i]} \left(\tfrac{p}{2}\right)^{[b \neq c]} \left(1-\tfrac{p}{2}\right)^{[b = c]}
$$

Equivalently y_i = c s_i ⊕ e_i and b = c ⊕ e_{n+1} with c uniform and e_i i.i.d. Bernoulli(p/2). Uses that Λ_p commutes with H and acts as a bit-flip with probability p/2 on computational-basis statistics; off-diagonal (coherence) terms do not affect this distribution.

Provenance: `assumption`. Derived by combining eq_3 and eq_4 for the chosen construction; the actual paper's measurement procedure is not given in the abstract.

Equation assumptions:

- Learner applies H^{⊗(n+1)} then measures all n+1 qubits in the computational basis.
- Noise model of eq_3.

## eq_6: Per-bit correlation statistic distinguishing s_i

$$
\Pr[y_i = b] = \begin{cases} 1 - p + \tfrac{p^2}{2}, & s_i = 1 \\ \tfrac{1}{2}, & s_i = 0 \end{cases}
$$

For s_i = 1, y_i and b agree iff the two noise bits agree; for s_i = 0, y_i is pure noise and b carries the uniform branch bit, so agreement is exactly 1/2. The gap 1/2 - p + p^2/2 is a positive constant for any constant p < 1.

Provenance: `assumption`. Direct consequence of eq_5; chosen as a simple classical estimator consistent with the abstract's claim that constant-rate noise costs only a logarithmic factor.

Equation assumptions:

- Estimator choice is the reconstructor's; the paper may use a different postprocessing rule.

## eq_7: Query complexity under noise (asymptotic, not exact)

$$
m = O\!\left( \frac{\log(n/\delta)}{(\tfrac{1}{2} - p + \tfrac{p^2}{2})^2} \right) \;\Rightarrow\; \Pr[\hat{s} \neq s] \le \delta
$$

By a Hoeffding bound on the empirical agreement frequency for each bit and a union bound over n bits, m noisy queries suffice; for constant p this is O(log n) versus O(1) queries in the noiseless case, i.e. at most a logarithmic increase.

Provenance: `abstract_inferred`. The abstract asserts the logarithmic overhead; the specific bound follows from eq_6 via standard concentration inequalities for the assumed estimator.

Abstract evidence: Depolarizing the qubits at the oracle’s output at any constant nonzero rate does not increase the computational (or query) complexity of quantum learning more than logarithmically.

Equation assumptions:

- Independence of samples across queries.
- Big-O hides constants; this is an upper bound, not an exact count.

## Registers

- D (data): n (instance: 3) qubits; Holds the example input x; qubit i encodes x_i. After Hadamard, reveals s on the b=1 branch.
- L (label): 1 qubits; Holds the parity label f_s(x); after Hadamard indicates which branch (all-zero or s) was observed.

## Initial state

Per query, the oracle supplies ρ_out = Λ_p^{⊗(n+1)}(|ψ_s⟩⟨ψ_s|) on registers D⊗L (eq_2, eq_3); the learner holds no additional qubits. Instance: n = 3, s = (1,0,1), p = 0.1.

## Measurement

Computational-basis measurement of all n+1 qubits after the Hadamard layer on each of the m queries; outcome (y,b) ∈ {0,1}^n × {0,1} per query.

## Classical postprocessing

For each i, compute a_i = (1/m) Σ_k [y_i^{(k)} = b^{(k)}]; set ŝ_i = 1 if a_i > (1/2 + 1 - p + p²/2)/2 = 3/4 - p/2 + p²/4, else ŝ_i = 0. Optionally verify ŝ against a few fresh samples. For the instance p = 0.1 the two agreement probabilities are 0.905 (s_i = 1) and 0.5 (s_i = 0).

## Algorithm steps

1. Query the noisy quantum example oracle once to obtain ρ_out on the n+1 qubits D⊗L. (eq_1, eq_2, eq_3)
2. Apply H to every qubit of D and L (noise commutes with H, so the state is Λ_p^{⊗(n+1)} applied to the GHZ-like state of eq_4). (eq_4)
3. Measure all n+1 qubits in the computational basis, obtaining (y,b) distributed as in eq_5. (eq_5)
4. Repeat the query–Hadamard–measure cycle m times, collecting samples (y^{(k)}, b^{(k)}), k = 1..m. (eq_7)
5. Classically estimate each s_i from the agreement frequency between y_i^{(k)} and b^{(k)}, thresholding at the midpoint of the two values in eq_6. (eq_6, eq_7)

## Assumptions

- No experiment_scope was provided; the n = 3, s = (1,0,1), p = 0.1 instance and the Hadamard-plus-correlation learner are the reconstructor's choice of smallest useful construction.
- The quantum example oracle is the Bshouty–Jackson uniform-distribution oracle.
- Depolarizing noise is i.i.d. per output qubit at rate p and the learner's own operations are noiseless.
- The per-bit agreement estimator (eq_6) is a plausible, not sourced, realization of the paper's efficient noisy learner.

## Missing information

- The paper's exact noise model (whether depolarizing is per-qubit i.i.d., the rate parameterization, and whether the label qubit is treated differently).
- The paper's actual algorithm and proof giving the logarithmic overhead, including explicit constants in the query and computational complexity.
- Details of the classical LPN comparison and the quantitative resource estimate behind 'a few hundred noisy qubits'.
- The argument that noise is essential for the quantum–classical separation.
