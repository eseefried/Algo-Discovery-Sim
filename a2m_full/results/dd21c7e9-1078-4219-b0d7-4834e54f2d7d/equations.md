# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Estimate Inf_i(f)=Pr_x[f(x)!=f(x xor e_i)] for a chosen variable i of an n-variable Boolean function f. The method is a Hadamard-test (interference) readout on one ancilla using a phase oracle. It is a deliberately different readout from the abstract's Bernstein-Vazirani (BV) position-i sampling.

Scope: One tiny instance: n=3 with a fixed hidden f, one target variable i (0-indexed), n+1=4 qubits. It covers the single-variable ancilla circuit, the shot-based estimator, and the thresholding rule for juntas. The BV-output-position circuit, the paper's approximation algorithm, the probabilistic junta-learning algorithms, the comparison with Floess et al., and the final truth-table learning step are outside this scope.

## Symbols

- $n$: number of Boolean input variables; domain: positive integer, here 3
- $f$: Boolean function f:{0,1}^n->{0,1}; domain: hidden, accessed only through U_f
- $i$: index of the target variable; input qubit i (little-endian) holds x_i; domain: {0,...,n-1}
- $e_i$: i-th unit bit-string; domain: {0,1}^n
- $U_f$: phase oracle, |x> -> (-1)^{f(x)}|x>; domain: unitary on n qubits, opaque placeholder gate
- $X_i$: Pauli X on input qubit i, so X_i|x>=|x xor e_i>; domain: unitary on n qubits
- $|s>$: uniform superposition H^{\otimes n}|0^n>; domain: n-qubit state
- $\mathrm{Inf}_i(f)$: influence of x_i on f; domain: [0,1]
- $\varepsilon,\delta$: additive accuracy and failure probability; domain: (0,1)
- $N$: number of shots; domain: positive integer
- $k$: junta size (f depends on at most k variables); domain: positive integer

## eq_1: Influence definition

$$
\mathrm{Inf}_i(f)=\Pr_{x\sim U\{0,1\}^n}\left[f(x)\ne f(x\oplus e_i)\right]=\tfrac12-\tfrac12\,\mathbb{E}_x\left[(-1)^{f(x)+f(x\oplus e_i)}\right]
$$

Influence as the probability that flipping bit i changes f, rewritten with the +/-1 correlation.

Provenance: `abstract_inferred`. The abstract equates the dependence degree with the influence. The exact formula is the standard definition, supplied as an assumption.

Abstract evidence: the influence of $x_{i}$ on $f$

Equation assumptions:

- Inputs are uniformly distributed.
- The influence is the probability definition for Boolean f.

## eq_2: Circuit state before the final Hadamard

$$
|\psi\rangle=\tfrac{1}{\sqrt2}\left(|0\rangle_a\,U_f|s\rangle+|1\rangle_a\,X_iU_fX_i|s\rangle\right)
$$

The ancilla is in |+>. The circuit CX(a->i), U_f, CX(a->i) acts on |+>_a|s>. Branch 0 applies U_f. Branch 1 applies X_i U_f X_i. Only one oracle placement is needed because U_f is applied unconditionally.

Provenance: `assumption`. This is the proposed construction from the method sketch. The sketch counts 2 queries per run, but a controlled-X conjugation around a single U_f gives the same state with 1 query.

Equation assumptions:

- CX gates are ordinary gates and are not queries.
- U_f is supplied as a phase oracle.

## eq_3: Interference overlap

$$
\langle s|U_f^{\dagger}X_iU_fX_i|s\rangle=\langle s|U_f^{\dagger}X_iU_f|s\rangle=\mathbb{E}_x\left[(-1)^{f(x)+f(x\oplus e_i)}\right]=1-2\,\mathrm{Inf}_i(f)
$$

Since X_i|s>=|s>, the overlap is a real correlation of f with its i-th shift.

Provenance: `standard_background`. Direct calculation from U_f|s>=2^{-n/2} sum_x (-1)^{f(x)}|x> and the definition of X_i.

Equation assumptions:

- Phase oracle convention as above.

## eq_4: Ancilla readout probability

$$
P(a=1)=\tfrac12\left(1-\mathrm{Re}\langle s|U_f^{\dagger}X_iU_fX_i|s\rangle\right)=\mathrm{Inf}_i(f),\qquad P(a=0)=1-\mathrm{Inf}_i(f)
$$

After H on the ancilla, P(a=1) equals the influence, read from one ancilla bit.

Provenance: `abstract_inferred`. The abstract states the BV-position claim. This circuit reproduces the same probability through an ancilla, which is an inference and not the paper's circuit. The value follows from eq_3.

Abstract evidence: the probability of getting a 1 in each position $i$ is equal to the dependence degree of $f$ on the variable $x_{i}$

Equation assumptions:

- The ancilla is measured in the computational basis after H.

## eq_5: Shot count and junta thresholding

$$
N\ge\frac{\ln(2/\delta)}{2\varepsilon^2}\Rightarrow\Pr\left[|\hat p-\mathrm{Inf}_i|\le\varepsilon\right]\ge1-\delta;\quad \text{declare }x_i\text{ relevant iff }\hat p>\tau,\ \tau=2^{-k}
$$

Hoeffding bound for the empirical frequency p-hat of ancilla=1. The threshold tau is set below the minimum nonzero influence of a k-junta, with eps<tau.

Provenance: `assumption`. Standard Hoeffding bound. The junta gap is taken from the sketch's assumption of at least 2^-k (a k-junta's nonzero influence is a multiple of 2^{1-k}, so it is at least 2^{1-k}). The exact threshold rule is not from the abstract.

Equation assumptions:

- f is a k-junta.
- Choose eps < tau, for example eps=2^{-k-1}.

## Registers

- x: n (3 in the example) qubits; input register; qubit j holds x_j (little-endian); H^n gives |s>
- a: 1 qubits; interference ancilla, initially |+>; the CX control and the measured qubit
- c: 1 classical bit qubits; records the ancilla outcome; measure(a,0), so counts key '1' means a=1

## Initial state

|0>^{n}|0>_a, then H on all n+1 qubits, giving |s>|+>_a.

## Measurement

Measure the ancilla qubit only, into classical bit 0. With Qiskit little-endian keys, read the single character of the counts key. P(1)=Inf_i.

## Classical postprocessing

p-hat = counts['1']/N is the estimate of Inf_i(f). For juntas, the relevant set is {i : p-hat_i > tau}. Learning f on the relevant variables by further queries is not specified here.

## Algorithm steps

1. Prepare |s> by applying H to every input qubit and prepare the ancilla in |+> with H. (eq_2)
2. Apply CX with control a and target input qubit i. (eq_2)
3. Apply the opaque phase-oracle placeholder U_f once to the input register. This is 1 query per run. (eq_2)
4. Apply CX with control a and target input qubit i again, giving the state in eq_2. (eq_2, eq_3)
5. Apply H to the ancilla and measure only the ancilla into classical bit 0. Do not measure the input register. (eq_4)
6. Repeat for N shots and set p-hat to the fraction of outcomes with a=1. For juntas, repeat over all i and keep those with p-hat > tau. (eq_5)

## Assumptions

- Scope choice: n=3, one target variable, a fixed hidden f. The smallest useful instance is a choice of mine, not from the abstract.
- The oracle is a phase oracle. A bit oracle would need a |-> ancilla and one more qubit.
- The influence is the probability definition.
- The CX gates are standard and are not oracle queries.
- The method is a deliberately different readout from the abstract's BV-based algorithm.
- The junta gap and threshold rule are assumptions.

## Missing information

- The abstract's actual BV-based approximation algorithm and its sample complexity.
- The probabilistic junta-learning algorithms and their runtimes.
- The speed comparison with the deterministic algorithms of Floess et al.
- The exact junta gap and thresholds used by the paper.
