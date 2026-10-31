# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Property testing of monotonicity on the Boolean hypercube: given quantum query access to f:{0,1}^n→{0,1}, accept (with probability ≥ 2/3) if f is monotone and reject (with probability ≥ 2/3) if f is ε-far from every monotone function, using Õ(n^{1/4} ε^{-1/2}) queries according to the abstract.

Scope: The abstract states only the problem, the acceptance/rejection criteria, and the query bound; it gives no construction. This specification (i) defines monotonicity, ε-farness, violated edges and the quantum query oracle, (ii) records the claimed complexity and its relation to known classical bounds, and (iii) fixes ONE smallest useful baseline construction: a Grover/amplitude-amplified edge tester on a tiny instance (n=4, f(x)=1-x_1, which is 1/2-far from monotone). This baseline achieves only O(sqrt(n/ε)) queries and is NOT the paper's algorithm; the paper-specific mechanism yielding the n^{1/4} ε^{-1/2} scaling (presumably a more refined use of the directed-path/pair tester analysis combined with quantum search or quantum-walk techniques) cannot be reconstructed from the abstract and is listed as missing. The super-quadratic/cubic separation claims are recorded but not derived.

## Symbols

- $n$: number of input bits / dimension of the hypercube; domain: positive integer
- $f$: Boolean function being tested; domain: f:\{0,1\}^n\to\{0,1\}
- $\varepsilon$: distance parameter of the property tester; domain: real, 0<\varepsilon\le 1
- $x\preceq y$: bitwise partial order on the hypercube: x_i\le y_i for all i; domain: x,y\in\{0,1\}^n
- $e_i$: i-th standard basis vector of \{0,1\}^n; domain: i\in\{1,\dots,n\}
- $\mathrm{dist}(f,g)$: normalized Hamming distance between two Boolean functions; domain: [0,1]
- $\mathcal{M}_n$: set of all monotone functions \{0,1\}^n\to\{0,1\}; domain: set of Boolean functions
- $O_f$: standard bit-flip quantum query oracle for f; domain: unitary on (n+1) qubits
- $p$: success probability of a randomized one-shot test (fraction of violated edges); domain: [0,1]
- $Q(n,\varepsilon)$: quantum query complexity of the monotonicity tester; domain: positive integer (asymptotic)

## eq_1: Monotone function

$$
f\in\mathcal{M}_n \iff \forall x,y\in\{0,1\}^n:\; x\preceq y \Rightarrow f(x)\le f(y)
$$

Definition of the property being tested; the tester must accept every such f.

Provenance: `abstract_inferred`. The abstract names monotonicity of f:{0,1}^n→{0,1}; the standard definition with respect to the bitwise partial order is the only one consistent with the hypercube setting.

Abstract evidence: accepts a monotone function

Equation assumptions:

- Partial order is the standard bitwise order on {0,1}^n.

## eq_2: ε-far from monotone

$$
\mathrm{dist}(f,g)=\Pr_{x\sim\{0,1\}^n}[f(x)\ne g(x)],\qquad f\text{ is }\varepsilon\text{-far} \iff \min_{g\in\mathcal{M}_n}\mathrm{dist}(f,g)\ge\varepsilon
$$

Rejection condition: f must be rejected (with probability ≥ 2/3) whenever its normalized Hamming distance to every monotone function is at least ε.

Provenance: `abstract_inferred`. Standard property-testing meaning of ε-far under the uniform distribution; the abstract uses the phrase without redefining it.

Abstract evidence: rejects a function that is $\varepsilon$-far from being monotone

Equation assumptions:

- Uniform distribution over inputs; bounded error means success probability ≥ 2/3.

## eq_3: Quantum query oracle and violated edge

$$
O_f\,|x\rangle|b\rangle=|x\rangle|b\oplus f(x)\rangle,\qquad V_f=\{(x,i): x_i=0,\; f(x)=1,\; f(x\oplus e_i)=0\}
$$

Standard bit-flip query oracle used to count queries, and the set of violated hypercube edges (a witness of non-monotonicity).

Provenance: `standard_background`. Standard query model for Boolean functions; a violated edge is the canonical local certificate that f is not monotone.

Equation assumptions:

- Query complexity counts applications of O_f (or its controlled version).

## eq_4: Edge-tester detection probability

$$
p=\Pr_{x\sim\{0,1\}^n,\;i\sim[n]}\big[(x,i)\in V_f\text{ or }(x\oplus e_i,i)\in V_f\big]\;\ge\;\frac{\varepsilon}{n}\quad\text{whenever } f\text{ is }\varepsilon\text{-far}
$$

Classical fact: if f is ε-far from monotone, a uniformly random hypercube edge is violated with probability at least ε/n (up to the normalization convention). If f is monotone, p=0.

Provenance: `standard_background`. Recalled from the classical edge-tester analysis (Goldreich–Goldwasser–Lehman–Ron–Samorodnitsky / Dodis et al.); used only as the baseline marking predicate. Not evidence about the paper's method.

Equation assumptions:

- Constant factors in the ε/n bound are omitted.

## eq_5: Amplitude-amplified edge tester (baseline, not the paper's bound)

$$
|\psi_0\rangle=\frac{1}{\sqrt{n2^n}}\sum_{x\in\{0,1\}^n}\sum_{i=1}^{n}|x\rangle|i\rangle,\qquad G=-\mathcal{A}S_0\mathcal{A}^{\dagger}S_{V_f},\qquad T=O\!\left(\frac{1}{\sqrt{p}}\right)=O\!\left(\sqrt{\frac{n}{\varepsilon}}\right)\text{ iterations}
$$

Baseline construction: prepare the uniform superposition over edges with A, mark violated edges with S_{V_f} (built from two uses of O_f per iteration), and apply amplitude amplification; O(sqrt(n/ε)) queries suffice to find a violated edge with constant probability when f is ε-far. This is a quadratic speedup of the classical edge tester and is strictly worse than the abstract's Õ(n^{1/4} ε^{-1/2}).

Provenance: `assumption`. Chosen as the smallest useful quantum construction consistent with the problem; combines eq_3, eq_4 and standard amplitude amplification. Explicitly not the paper's algorithm.

Equation assumptions:

- p is unknown, so a standard exponential-guess (or fixed-point) amplitude amplification schedule over T is assumed with only constant overhead.
- The marking unitary S_{V_f} is implemented via two oracle calls (f(x) and f(x⊕e_i)) plus uncomputation.

## eq_6: Claimed quantum query complexity and classical comparison

$$
Q(n,\varepsilon)=\widetilde{O}\!\left(n^{1/4}\varepsilon^{-1/2}\right),\qquad R(n,\varepsilon)=\widetilde{O}\!\left(\sqrt{n}\,\varepsilon^{-2}\right)\;\Rightarrow\;\frac{R}{Q}\Big|_{\varepsilon=1/\sqrt{n}}=\widetilde{\Theta}(n)=\widetilde{\Theta}(Q^{2})
$$

The abstract's query bound Q. The best known randomized bound R (Khot–Minzer–Safra path tester) is recalled as background; at ε=1/√n one gets Q=Õ(n^{1/2}) and R=Õ(n^{3/2}), consistent with the abstract's statement of a cubic improvement.

Provenance: `abstract_explicit`. The Q bound is stated verbatim in the abstract; the R bound and the ratio computation are background consistency checks, not derivations of the algorithm.

Abstract evidence: makes $\widetilde{O}(n^{1/4}\varepsilon^{-1/2})$ queries

Equation assumptions:

- The classical bound R=Õ(√n ε^{-2}) is recalled background, not quoted from the abstract.

## Registers

- x (input register): n qubits; holds the hypercube vertex x queried to O_f; for the tiny instance n=4
- i (direction register): \lceil\log_2 n\rceil qubits; holds the edge direction index i so that the edge is (x, x⊕e_i)
- a (oracle answer qubits): 2 qubits; receive f(x) and f(x⊕e_i) via O_f; used to compute the violated-edge predicate then uncomputed
- m (marker qubit): 1 qubits; stores the predicate [(x,i) violated]; its phase kick-back realizes S_{V_f}

## Initial state

|0\rangle^{\otimes n}|0\rangle^{\otimes\lceil\log_2 n\rceil}|0\rangle^{\otimes 2}|0\rangle, mapped by A (Hadamards on x, uniform superposition over i) to |\psi_0\rangle of eq_5. Bit ordering: x = x_1 x_2 ... x_n with x_1 the leftmost/most significant qubit; i encoded in binary as an integer in {0,...,n-1} representing direction i+1.

## Measurement

Computational-basis measurement of registers x and i after amplitude amplification; outcome (x,i) is a candidate violated edge.

## Classical postprocessing

Verify the candidate edge with two classical queries f(x), f(x⊕e_i); output REJECT if it is a violation (eq_3), else ACCEPT. Monotone f never produces a violation, so acceptance is one-sided; for ε-far f the amplified success probability is boosted to ≥ 2/3 by constant repetition.

## Algorithm steps

1. Prepare the uniform superposition over hypercube edges (x,i) using A = H^{⊗n} ⊗ (uniform state over i). (eq_5)
2. Evaluate the violated-edge predicate: query O_f on x and on x⊕e_i (computed by a controlled bit flip), compute m = [x_i=0 ∧ f(x)=1 ∧ f(x⊕e_i)=0] (or the mirrored case with roles swapped), apply a Z on m, and uncompute the answer qubits and the flip. This realizes S_{V_f} with two queries. (eq_3, eq_4)
3. Apply the diffusion operator -A S_0 A^† and repeat the Grover iterate G for T=O(sqrt(n/ε)) iterations (with an exponential-guess schedule since p is unknown). (eq_5)
4. Measure x and i; classically verify whether the edge (x, x⊕e_i) is violated using two further classical queries; reject if so, otherwise accept. For the tiny instance (n=4, f(x)=1-x_1) every direction-1 edge is violated so p=1/4 and a single Grover iteration suffices. (eq_1, eq_2, eq_3)

## Assumptions

- No experiment_scope was supplied; the baseline amplitude-amplified edge tester with tiny instance n=4, f(x)=1-x_1 (distance 1/2 from monotone) was chosen as the single smallest useful construction.
- The baseline achieves O(sqrt(n/ε)) queries, not the abstract's Õ(n^{1/4} ε^{-1/2}); it is a stand-in, not a reconstruction of the paper's algorithm.
- Bounded error is interpreted as success probability ≥ 2/3; Õ hides polylog(n) factors.
- Classical bound R=Õ(√n ε^{-2}) attributed to the KMS path tester is recalled from background knowledge.

## Missing information

- The actual quantum algorithm achieving Õ(n^{1/4} ε^{-1/2}): which classical tester (e.g., directed random-path/pair tester) and which quantum primitive (amplitude amplification, quantum walk, or other) are combined, and how the ε^{-1/2} rather than ε^{-1} dependence arises.
- The precise classical lemma (detection probability of the underlying randomized test as a function of n and ε) on which the quantum speedup is built.
- Error analysis, constants and the polylogarithmic factors hidden in Õ.
- Any lower bounds or optimality discussion, and the formal derivation of the 'super-quadratic for all ε=o(1)' claim.
