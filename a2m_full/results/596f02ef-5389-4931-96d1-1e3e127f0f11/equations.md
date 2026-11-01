# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Monotonicity testing of f:{0,1}^n->{0,1} with one-sided error: always accept monotone f, reject eps-far f w.p. >=2/3, using Otilde(n^{1/4} eps^{-1/2}) queries via amplitude amplification over a random-edge violation checker.

Scope: Smallest useful construction: n=3 (index register 2 qubits, i in {0,1,2}, value 3 unused), a fixed small f given as an XOR oracle placeholder, one checker unitary and a fixed number k of Grover iterations, then measurement of x, i, flag and classical verification of the returned edge. Outside scope: the paper's actual algorithm achieving the n^{1/4}eps^{-1/2} polylog bound, the path or hypercube-line tester, exponential search over iteration counts when eps is unknown, and the Chakrabarty-Seshadhri / Khot-Minzer-Safra proofs.

## Symbols

- $n$: number of input bits; domain: positive integer, n=3 for the small instance
- $\varepsilon$: distance of f from monotone (fraction of 2^n); domain: (0,1]
- $x$: n-bit input; bit j is qubit j of register X (little-endian); domain: {0,1}^n
- $i$: edge direction (bit index); domain: {0,...,n-1}
- $x^{i\to b}$: x with bit i set to b; domain: {0,1}^n
- $p$: probability that a uniformly random (x,i) is a violated edge; domain: [0,1]
- $\theta$: amplitude angle with sin^2 theta = p; domain: [0,\pi/2]
- $k$: number of Grover iterations; domain: nonnegative integer
- $v(x,i)$: violation indicator for the edge: f(x^{i\to 0})=1 and f(x^{i\to 1})=0; domain: {0,1}

## eq_1: Edge violation predicate

$$
v(x,i)=f(x^{i\to 0})\wedge\neg f(x^{i\to 1})
$$

An edge (x^{i->0}, x^{i->1}) is violated iff the lower endpoint has value 1 and the upper endpoint has value 0. It is independent of x_i, so the check queries both endpoints.

Provenance: `standard_background`. Definition of a monotonicity violation on a hypercube edge; the abstract only says the algorithm accepts monotone functions.

Equation assumptions:

- f is queried through an XOR oracle on ancilla qubits
- both endpoints are queried explicitly, giving 2 queries per check plus 2 for uncompute

## eq_2: Checker unitary and success probability

$$
U_{check}|0\rangle=\frac{1}{\sqrt{n2^n}}\sum_{x,i}|x\rangle|i\rangle|v(x,i)\rangle|\mathrm{junk}=0\rangle,\quad p=\frac{1}{n2^n}\sum_{x,i}v(x,i)
$$

Hadamards on X and index registers (uniform over i requires n a power of 2 or a padded or rejected invalid index), then compute both oracle values into ancillas, a Toffoli with a negated control writes v into the flag, and the oracle calls are uncomputed. The flag=1 amplitude squared is p.

Provenance: `assumption`. Construction proposed in the sketch; the exact checker of the actual paper is not given in the abstract.

Equation assumptions:

- for n=3 an index value 3 is treated as nonviolating (v=0)
- the normalisation then uses 4*2^n index-x pairs so p is rescaled by n/4

## eq_3: Amplitude amplification

$$
\Pr[\text{flag}=1]=\sin^2((2k+1)\theta),\ \sin^2\theta=p,\ k\approx\frac{\pi}{4\theta}-\frac12
$$

Grover iterations Q=-U_check S_0 U_check^dagger S_flag, where S_flag flips the sign of flag=1, give this success probability. With p about eps/sqrt(n) this needs k=O(n^{1/4}eps^{-1/2}).

Provenance: `standard_background`. Standard amplitude amplification formula.

Equation assumptions:

- p known or lower-bounded from assumed eps

## eq_4: Edge density to iteration count

$$
p\gtrsim \frac{\varepsilon}{\sqrt n}\ \Rightarrow\ k=O\!\left(\frac{1}{\sqrt p}\right)=O\!\left(n^{1/4}\varepsilon^{-1/2}\right)
$$

Assumed per-edge violation probability for eps-far functions, matching the claimed query complexity up to polylog factors.

Provenance: `abstract_inferred`. The query bound is consistent with amplifying a success probability of eps/sqrt(n) with O(1) queries per iteration. The edge-density bound itself comes from the Chakrabarty-Seshadhri / Khot-Minzer-Safra analyses, which is background not stated in the abstract.

Abstract evidence: makes $\widetilde{O}(n^{1/4}\varepsilon^{-1/2})$ queries

Equation assumptions:

- constant queries per iteration

## eq_5: Verification and decision rule

$$
\text{reject}\iff \text{flag}=1\wedge v(x,i)=1\text{ (classical recheck)};\quad f\text{ monotone}\Rightarrow v\equiv0\Rightarrow\Pr[\text{reject}]=0
$$

After measurement, the returned (x,i) is verified with 2 direct queries. Monotone f is always accepted.

Provenance: `abstract_inferred`. Accepting monotone f always is the one-sided error behaviour; the classical recheck is from the sketch.

Abstract evidence: accepts a monotone function, and rejects a function that is $\varepsilon$-far from being monotone

Equation assumptions:

- error reduction by constant repetition gives success >=2/3

## Registers

- X: n (3) qubits; input x, qubit j = bit j
- I: ceil(log2 n) (2) qubits; edge direction index, uniform superposition by H
- A: 2 qubits; ancillas holding f(x^{i->0}) and f(x^{i->1}) temporarily, uncomputed to 0
- F: 1 qubits; flag qubit holding v(x,i)
- W: about 2 to 4 qubits; work qubits for setting bit i to 0 or 1 (controlled on I) and for the multi-controlled gates; copy of x with bit i forced

## Initial state

All qubits |0>; U_check applies H to X and I.

## Measurement

Measure X (n bits), I (2 bits) and F. In a Qiskit counts key the last character is classical bit 0, so reverse the string before indexing. Use e.g. creg order [X bits, I bits, F].

## Classical postprocessing

For each shot with F=1, recompute v(x,i) from two direct oracle queries; reject if any verified shot is violated, else accept. Repeat O(log) times for error reduction.

## Algorithm steps

1. Apply Hadamards on X and I to make a uniform superposition over (x,i). (eq_2)
2. Compute the lower and upper endpoints (bit i forced to 0 and 1) into work copies controlled on I, query f on each via the placeholder oracle, and compute the flag by a Toffoli with negated control on the upper value. Uncompute the queries and copies, leaving the flag. (eq_1, eq_2)
3. Apply k Grover iterations with the flag as marked bit (phase flip on F=1, then U_check^dagger, reflection about |0>, U_check). (eq_3, eq_4)
4. Measure X, I, F, then classically query f at the two endpoints and apply the decision rule. (eq_5)

## Assumptions

- n=3 or 4 and a fixed small f chosen for the test, such as a non-monotone function with a few violated edges
- k is fixed from an assumed eps or known p
- the oracle is an XOR oracle, so it can be uncomputed
- a padded index value (n not a power of 2) is treated as non-violating
- polylog overhead and the path tester are omitted

## Missing information

- the actual algorithm of the paper, which is likely more refined than the edge tester
- the precise sampling distribution or tester giving the polylog-optimal bound
- how the paper handles unknown eps
- the exact constants in the query count
