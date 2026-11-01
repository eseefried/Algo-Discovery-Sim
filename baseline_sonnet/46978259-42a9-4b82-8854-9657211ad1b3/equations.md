# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Pattern classification via quantum measurement of Hamming distance between an input pattern and stored training patterns, following Trugenberger's proposal; the abstract gives no explicit equations, so only a generic background construction is reconstructed.

Scope: Tiny instance: Hamming-distance estimation between an n-bit input and a small set of p stored n-bit patterns using a Trugenberger-style phase-encoding construction (background), followed by nearest-pattern class assignment. Excluded: the paper's specific classifier design, MNIST encoding, preprocessing, advantage analysis, and any performance results.

## Symbols

- $n$: number of bits per pattern; domain: positive integer
- $p$: number of stored training patterns; domain: positive integer, p <= 2^n
- $x^k$: k-th stored pattern; domain: {0,1}^n
- $x$: input pattern to classify; domain: {0,1}^n
- $d_H(x,x^k)$: Hamming distance between input and stored pattern k; domain: integer in [0,n]
- $c_k$: class label of stored pattern k; domain: finite label set

## eq_1: Stored memory superposition

$$
|M\rangle=\frac{1}{\sqrt{p}}\sum_{k=1}^{p}|x^k\rangle|c_k\rangle
$$

Uniform superposition of training patterns with class labels (assumed encoding).

Provenance: `assumption`. A proposed construction for a tiny instance; the abstract does not specify how patterns are stored.

Equation assumptions:

- Uniform amplitudes over training patterns
- Labels stored in a separate register

## eq_2: Hamming distance definition

$$
d_H(x,y)=\sum_{j=1}^{n}(x_j\oplus y_j)
$$

Number of differing bits between two n-bit strings.

Provenance: `standard_background`. Standard definition; the abstract only names the Hamming distance.

## eq_3: Distance-encoded phase

$$
U=e^{i\frac{\pi}{2n}\hat d},\quad U|x^k\rangle|x\rangle=e^{i\frac{\pi}{2n}d_H(x,x^k)}|x^k\rangle|x\rangle
$$

Phase proportional to Hamming distance, typically via per-bit XOR followed by controlled phase rotations on an ancilla.

Provenance: `standard_background`. Recalled from the general form of Trugenberger's approach; details of the actual paper's variant are not verified.

Equation assumptions:

- Ancilla in |+> control state
- Exact phase schedule of the paper not known

## eq_4: Ancilla measurement probability

$$
P(\text{anc}=0,\,k)=\frac{1}{p}\cos^2\!\left(\frac{\pi}{2n}d_H(x,x^k)\right)
$$

Probability of ancilla outcome 0 together with pattern k after Hadamard interference; favors small distances.

Provenance: `standard_background`. Follows from the phase in eq_3 with a final Hadamard on the ancilla, in the Trugenberger style.

Equation assumptions:

- Ancilla Hadamard-interference form of eq_3
- Uniform amplitudes from eq_1

## eq_5: Classification rule

$$
\hat c=\arg\max_{c}\sum_{k:\,c_k=c}P(\text{anc}=0,\,k)
$$

Predicted class is the label with highest post-selected probability mass, estimated from measurement frequencies.

Provenance: `assumption`. A natural decision rule for pattern classification; not stated in the abstract.

Equation assumptions:

- Majority/probability-mass vote over labels

## Registers

- pattern: n qubits; holds stored patterns |x^k> in superposition
- input: n qubits; holds input pattern |x>
- class: ceil(log2(#classes)) qubits; holds class label c_k
- ancilla: 1 qubits; control qubit for phase encoding and interference

## Initial state

All registers in |0>; ancilla prepared in |+>; pattern and class registers prepared into |M> (eq_1); input register set to |x>.

## Measurement

Measure the ancilla and the class register (optionally the pattern register) in the computational basis over repeated runs; post-select on ancilla = 0.

## Classical postprocessing

Tally class frequencies among post-selected shots and output the most frequent label.

## Algorithm steps

1. Prepare the memory state |M> and the input register |x>. (eq_1)
2. Compute bitwise differences between pattern and input registers and apply the controlled distance-dependent phase. (eq_2, eq_3)
3. Apply Hadamard to the ancilla, uncompute the XOR, and measure the ancilla and class register. (eq_4)
4. Post-select on ancilla 0 and aggregate class counts to classify. (eq_5)

## Assumptions

- The abstract has no explicit equations; all equations are background or proposed.
- Tiny instance such as n=2-4 and p=2-4 patterns instead of MNIST.
- Trugenberger-style phase encoding stands in for the paper's actual algorithm.

## Missing information

- Paper's exact state preparation and training-set storage method
- Exact quantum circuit and phase schedule
- How MNIST images are binarized and encoded
- Precise classification rule and the claimed advantages
- Any numerical results
