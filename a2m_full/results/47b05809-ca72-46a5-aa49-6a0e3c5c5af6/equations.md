# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Pattern classification by a Trugenberger-style quantum Hamming-distance computation: load N binarized training patterns with class labels in superposition, imprint the Hamming distance to a query as a relative phase on an ancilla, interfere, post-select a=0, and read the class by a cos^2-weighted vote.

Scope: One tiny instance (assumed): n=2 pattern bits, m=1 label bit, N=4 training patterns with 2 per class, one ancilla, loaded by standard gates (X plus multi-controlled X on a basis-state index scheme, or via an index register). The query is classical and loaded by X gates, so the x register can be dropped. Outside scope: the paper's exact MNIST preprocessing, the exact loading procedure, resource analysis, and any claimed advantage over classical classifiers. The exact paper algorithm is not reproduced, only the Trugenberger-based family.

## Symbols

- $n$: number of pattern bits (binarized downscaled pixels); domain: positive integer
- $m$: number of label qubits; domain: positive integer
- $N$: number of training patterns; domain: positive integer, N<=2^n
- $p_k$: k-th training pattern; domain: {0,1}^n
- $c_k$: class label of pattern k; domain: {0,1}^m
- $x$: classical query bitstring; domain: {0,1}^n
- $d_k$: Hamming distance between p_k and x; domain: {0,...,n}
- $a$: ancilla/control qubit for interference; domain: qubit

## eq_1: Training superposition

$$
|\psi_0\rangle=\frac{1}{\sqrt{N}}\sum_{k=1}^{N}|p_k\rangle_p|c_k\rangle_c\otimes|0\rangle_a
$$

Uniform-weight superposition of patterns entangled with labels, ancilla in |0>.

Provenance: `assumption`. Standard Trugenberger memory state; the abstract only names his Hamming-distance proposal. Uniform weights are assumed.

Equation assumptions:

- equal weights
- loaded with standard gates, not initialize

## eq_2: Query XOR encoding

$$
|p_k\rangle\to|p_k\oplus x\rangle=|d_k^{(1)}\ldots d_k^{(n)}\rangle,\quad d_k^{(j)}=p_{k,j}\oplus x_j,\quad d_k=\sum_j d_k^{(j)}
$$

Apply X on p qubits where x_j=1 (classical query). The qubit j is 1 where the pattern disagrees with the query, so the Hamming weight is d_k. The sketch's extra X for XNOR would give n-d_k instead, so omit it.

Provenance: `assumption`. Hamming distance equals weight of the XOR. This is a choice of encoding.

Equation assumptions:

- query is classical
- no extra X layer, otherwise d is replaced by n-d

## eq_3: Distance phase on ancilla

$$
H_a;\ \prod_{j}\mathrm{CP}_{a\to p_j}(-\pi/n)\text{ with }a\text{ in }|1\rangle\text{ branch};\ \Rightarrow\ \frac{1}{\sqrt{2}}\left(|0\rangle+e^{-i\pi d_k/n}|1\rangle\right)
$$

After H on a, a controlled phase of angle -pi/n on each pattern qubit (control a) gives the 1 branch the phase exp(-i pi d_k/n). To get the sketch's half angle exp(-i pi d/(2n)) relative phase symmetrically, use angle pi/(2n) per qubit with Z/phase compensation on a, or use a phase of pi/(2n) per qubit directly (the P gate then has angle -pi/(2n)).

Provenance: `standard_background`. Recalled from Trugenberger's phase-estimation-free Hamming distance scheme. The angle convention is fixed here so that the final probability matches eq_4.

Equation assumptions:

- use per-qubit angle theta=-pi/(2n)*... chosen so total relative phase is -pi d_k/(2n)*2 or -pi d_k/(2n) consistently with eq_4

## eq_4: Ancilla outcome probability

$$
P(a=0\mid k)=\cos^2\!\left(\frac{\pi d_k}{2n}\right)
$$

After the final H on a, interference gives P(a=0) for pattern k. This requires relative phase exp(-i pi d_k/n) between the branches, i.e. P=(1+cos(phi))/2 with phi=pi d_k/n.

Provenance: `abstract_inferred`. Inferred from the Trugenberger scheme and the sketch. The relative phase pi d/n gives cos^2(pi d/(2n)), so the per-qubit phase must be pi/n, not pi/(2n).

Abstract evidence: draws on Trugenberger’s proposal for measuring the Hamming distance on a quantum computer

Equation assumptions:

- relative phase phi=pi d_k/n

## eq_5: Class posterior and decision

$$
P(c\mid a=0)=\frac{\sum_{k:c_k=c}\cos^2(\pi d_k/2n)}{\sum_{k}\cos^2(\pi d_k/2n)},\quad \hat c=\arg\max_c P(c\mid a=0)
$$

Classification by the post-selected distribution over the class register.

Provenance: `assumption`. Follows from eq_1 and eq_4 with uniform weights; the paper's exact decision rule is not known.

Equation assumptions:

- post-selection on a=0
- enough shots

## Registers

- p: n qubits; pattern register, becomes the XOR/difference register
- c: m qubits; class label register
- a: 1 qubits; interference ancilla, measured
- loader ancillas: unknown, depends on loading scheme qubits; index register or work qubits for state preparation, to be uncomputed

## Initial state

all qubits |0>; loading yields eq_1

## Measurement

Measure a and c only. Qiskit little-endian: if classical bits are ordered [c0..c_{m-1}, a], the counts key string reversed gives bit i at index i.

## Classical postprocessing

Filter counts with a=0, marginalize onto c bits (reverse the key string to index by bit), take the argmax label; ties broken arbitrarily. Optionally compare with the exact cos^2-weighted vote computed classically.

## Algorithm steps

1. Load training superposition of (pattern,label) pairs with standard gates (for example a small index register with H, then multi-controlled X to write p_k and c_k, then uncompute the index if feasible; otherwise keep the index as an extra register and do not measure it). (eq_1)
2. Apply X on p_j for each j where x_j=1, so p holds the difference bits. (eq_2)
3. Apply H on a, then controlled-phase gates from a onto each p_j with angle -pi/n. (eq_3)
4. Apply H on a, measure a and c (and nothing else). (eq_4)
5. Postprocess: keep shots with a=0, tally c, take argmax. (eq_5)

## Assumptions

- Tiny instance n=2, m=1, N=4 chosen by me; the real task may differ
- Binarized, downsampled patterns
- Uniform weights
- Post-selection is acceptable
- No oracle or black box is used; the query is loaded by X gates

## Missing information

- The paper's exact state-loading method
- The paper's exact phase/angle convention and decision rule
- Whether the paper uses a different measurement or amplification scheme
- The MNIST preprocessing details
