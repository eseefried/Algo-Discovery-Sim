# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Quantum pattern classification using a Trugenberger-style quantum measurement of Hamming distance between an input pattern and stored training patterns, illustrated on handwritten digit recognition from MNIST.

Scope: Abstract-level reconstruction only: the problem statement and a minimal finite-instance Hamming-distance encoding. Circuit details, measurement protocol and MNIST encoding are not given in the abstract; the circuit, measurement and postprocessing are assumed templates.

## Symbols

- $d_H(x,p)$: Hamming distance between input pattern x and stored pattern p; domain: integers 0..n
- $n$: number of bits per binary pattern; domain: positive integer
- $p_k$: k-th stored training pattern; domain: binary strings of length n, k=1..N
- $N$: number of stored training patterns; domain: positive integer

## eq_1: Hamming distance

$$
d_H(x,p)=\sum_{i=1}^{n}(x_i\oplus p_i)
$$

Number of differing bits between the input and a stored pattern.

Provenance: `abstract_inferred`. Hamming distance is the quantity named in the abstract; the formula is the standard definition.

Abstract evidence: measuring the Hamming distance on a quantum computer

Equation assumptions:

- Patterns are binary strings of fixed length n

## eq_2: Memory superposition

$$
|M\rangle=\frac{1}{\sqrt{N}}\sum_{k=1}^{N}|p_k\rangle
$$

Uniform superposition of stored training patterns, as in Trugenberger's associative memory.

Provenance: `standard_background`. Standard background for Trugenberger-type schemes; the abstract does not state it.

Equation assumptions:

- Uniform amplitudes
- Training patterns are encoded as basis states

## Registers

- input: n qubits; holds the binary input pattern x
- memory: n qubits; holds superposition of stored training patterns p_k
- control: 1 qubits; ancilla for Hadamard-based interference encoding Hamming distance into its amplitude (assumed Trugenberger-style)

## Initial state

Assumed: input register in |x>, memory register in |M> (uniform superposition of training patterns), control qubit in |0>.

## Measurement

Assumed: measure the control qubit in the computational basis, post-selecting on the outcome favoring small d_H; then measure the memory register (and its class label) to read out a stored pattern, with probability weighted toward patterns near x. Repeat over many shots.

## Classical postprocessing

Assumed: tally the class labels of the retrieved patterns over repeated runs and assign the input the majority (most frequent) class label. Exact decision rule not in the abstract.

## Algorithm steps

1. Prepare memory register in uniform superposition of the N stored binary training patterns, and load the input pattern x into the input register. (eq_2)
2. Apply Hadamard to the control qubit, then compute bitwise differences between input and memory registers (XOR-type operations) so each branch carries the Hamming distance (assumed Trugenberger-style; details not in abstract). (eq_1)
3. Apply a distance-dependent phase on the control qubit branch, then a final Hadamard on the control qubit so that the control-qubit outcome probability depends on d_H (assumed). (eq_1, eq_2)

## Assumptions

- Binary-encoded patterns of fixed length
- Uniform superposition memory
- Circuit steps follow a generic Trugenberger-style control-qubit interference template as an assumption; the abstract does not specify gates
- Measurement with control-qubit post-selection and majority-vote postprocessing are assumed, not stated in the abstract
- Only eq_1 is abstract-supported (by inference); eq_2 is background

## Missing information

- Exact circuit and gates
- Exact phase angle, number of repetitions and post-selection details
- MNIST binarization and encoding
- Class label storage and assignment details
- Exact measurement and decision rule, and shot count
- The authors' specific modifications to Trugenberger's algorithm and the claimed advantages
- The authors' specific modifications to Trugenberger's algorithm and the claimed advantages are not in the abstract
