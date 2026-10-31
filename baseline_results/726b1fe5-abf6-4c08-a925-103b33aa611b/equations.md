# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Quantum pattern classification: given a training set of N binary patterns x^k in {0,1}^n with class labels y^k, and an unlabelled input x in {0,1}^n, assign a class to x using a quantum routine in which (a) training patterns are held in superposition, (b) Hamming distances to the input are computed into relative phases following Trugenberger's distance-measurement proposal, and (c) measurement yields class probabilities weighted by closeness to x.

Scope: One smallest useful construction (assumption, no scope supplied): a Trugenberger-style Hamming-distance classifier with a binary class label, specified for a tiny explicit instance n=2 bits, N=2 training patterns (x^1=00,y^1=0), (x^2=01,y^2=1), input x=00. The superposition of training patterns is treated as given (prepared by an unspecified storage routine). Outside scope: the paper's MNIST handwritten-digit experiment, binarisation/encoding of grey-scale images, multi-class label registers, the training-set storage algorithm, discussion of advantages, and any paper-specific modifications of Trugenberger's circuit.

## Symbols

- $n$: number of bits (qubits) per pattern; domain: positive integer; instance n=2
- $N$: number of training patterns; domain: positive integer; instance N=2
- $x$: input pattern to classify, bits x_1..x_n; domain: {0,1}^n
- $x^k$: k-th training pattern, bits x^k_1..x^k_n; domain: {0,1}^n, k=1..N
- $y^k$: class label of k-th training pattern; domain: {0,1} (binary class, assumption)
- $d_k$: Hamming distance between x and x^k; domain: integer in [0,n]
- $\oplus$: bitwise XOR; domain: {0,1}^n x {0,1}^n -> {0,1}^n
- $Z_j, Z_c$: Pauli-Z on memory qubit j / ancilla c; domain: 2x2 Hermitian unitaries
- $\theta_k$: phase angle pi d_k/(2n); domain: real in [0, pi/2]

## eq_1: Initial superposition of training data with input and ancilla

$$
|\psi_0\rangle = \frac{1}{\sqrt{N}} \sum_{k=1}^{N} |x\rangle_I \, |x^k\rangle_M \, |y^k\rangle_Y \otimes \frac{1}{\sqrt{2}}\left(|0\rangle_c + |1\rangle_c\right)
$$

Register order: input I (n qubits), memory M (n qubits), class Y (1 qubit), ancilla c (1 qubit). Bit j of a pattern is stored in qubit j of the corresponding register (j=1..n).

Provenance: `abstract_inferred`. Trugenberger's distance measurement acts on a uniform superposition of stored patterns next to the input, with a control ancilla in |+>; attaching a class label register is the natural extension for classification implied by the abstract. The preparation of this state (a storage algorithm) is not reconstructed here.

Abstract evidence: draws on Trugenberger’s proposal for measuring the Hamming distance on a quantum computer

Equation assumptions:

- Uniform amplitudes 1/sqrt(N) over training patterns
- Binary class label stored in one qubit
- State preparation treated as a given oracle/subroutine

## eq_2: Hamming-distance bits via CNOTs

$$
\prod_{j=1}^{n} \mathrm{CNOT}_{I_j \to M_j}: \; |x\rangle_I |x^k\rangle_M \mapsto |x\rangle_I |x \oplus x^k\rangle_M, \qquad d_k = \sum_{j=1}^{n} (x_j \oplus x^k_j)
$$

After the CNOTs, memory qubit j holds 1 exactly where input and training bit differ; the Hamming weight of the memory register equals the exact Hamming distance d_k.

Provenance: `standard_background`. Standard first step of Trugenberger's 2001 Hamming-distance routine (recalled from knowledge, not from the paper text). Equality is exact, no approximation.

Equation assumptions:

- Memory register is overwritten with XOR bits; input register is left unchanged

## eq_3: Ancilla-controlled phase encoding of Hamming distance

$$
U = \exp\!\left(-i\,\frac{\pi}{2n}\, Z_c \otimes \sum_{j=1}^{n} \frac{I - Z_j}{2}\right), \qquad U|\psi_1\rangle = \frac{1}{\sqrt{2N}} \sum_{k=1}^{N} \left(e^{-i\theta_k}|0\rangle_c + e^{i\theta_k}|1\rangle_c\right)|x\rangle_I |x\oplus x^k\rangle_M |y^k\rangle_Y, \quad \theta_k = \frac{\pi d_k}{2n}
$$

(I-Z_j)/2 projects memory qubit j onto |1>, so the sum counts d_k; Z_c gives opposite-sign phases for the two ancilla branches. Exact unitary evolution.

Provenance: `standard_background`. Trugenberger's Hamiltonian-evolution step writing the Hamming distance into a relative phase between ancilla branches (recalled background). Sign conventions are a choice; probabilities below are convention-independent.

Equation assumptions:

- Phase scale pi/(2n) so that d_k = n maps to zero amplitude for ancilla outcome 0

## eq_4: Hadamard on ancilla and ancilla measurement probability

$$
H_c U|\psi_1\rangle = \frac{1}{\sqrt{N}} \sum_{k=1}^{N} \left(\cos\theta_k |0\rangle_c - i \sin\theta_k |1\rangle_c\right)|x\rangle_I |x\oplus x^k\rangle_M |y^k\rangle_Y, \qquad P(c=0) = \frac{1}{N}\sum_{k=1}^{N} \cos^2\!\left(\frac{\pi d_k}{2n}\right)
$$

The ancilla outcome 0 is more likely when training patterns are close to the input; outcome 1 flags failure and the run is discarded (postselection).

Provenance: `standard_background`. Direct consequence of eq_3 followed by H_c; this is the measurement step of Trugenberger's proposal (recalled background).

Equation assumptions:

- Postselection on ancilla outcome 0; runs with outcome 1 are repeated

## eq_5: Class probability after postselection (classification rule)

$$
P(y \mid c=0) = \frac{\sum_{k: y^k = y} \cos^2\!\left(\frac{\pi d_k}{2n}\right)}{\sum_{k=1}^{N} \cos^2\!\left(\frac{\pi d_k}{2n}\right)}, \qquad \hat{y}(x) = \arg\max_{y \in \{0,1\}} P(y \mid c=0)
$$

Measuring the class register conditioned on ancilla outcome 0 gives a Hamming-distance-weighted vote of the training set; the predicted class is the most probable outcome, estimated from repeated runs.

Provenance: `abstract_inferred`. Inferred: a classifier built on Trugenberger's routine must read out a class from the distance-weighted state; measuring an attached class register conditioned on the successful ancilla outcome is the minimal such rule. The paper's exact decision rule is not known from the abstract.

Abstract evidence: We introduce a quantum pattern classification algorithm that draws on Trugenberger’s proposal for measuring the Hamming distance

Equation assumptions:

- Class decided by majority of class-register outcomes over repeated postselected runs
- Binary classes

## eq_6: Tiny explicit instance

$$
n=2,\; N=2,\; (x^1,y^1)=(00,0),\; (x^2,y^2)=(01,1),\; x=00 \;\Rightarrow\; d_1=0,\; d_2=1,\; P(c=0)=\tfrac{1}{2}\left(1+\tfrac{1}{2}\right)=\tfrac{3}{4},\; P(y=0\mid c=0)=\tfrac{1}{1+1/2}=\tfrac{2}{3},\; \hat{y}=0
$$

Concrete 6-qubit instance (2 input + 2 memory + 1 class + 1 ancilla) with exact target probabilities derived from eq_4 and eq_5.

Provenance: `assumption`. Chosen as the smallest non-trivial instance; values follow exactly from the equations above, not from the paper.

Equation assumptions:

- Instance chosen by the reconstruction agent, not from the paper

## Registers

- I (input): n (instance: 2) qubits; holds the pattern x to be classified; unchanged by the circuit
- M (memory/training): n (instance: 2) qubits; holds superposed training patterns x^k; overwritten with x XOR x^k
- Y (class): 1 qubits; holds class label y^k entangled with the corresponding training pattern; measured at the end
- c (ancilla): 1 qubits; control qubit in |+> whose relative phase encodes the Hamming distance; measured and postselected on 0

## Initial state

|psi_0> as in eq_1: (1/sqrt N) sum_k |x>_I |x^k>_M |y^k>_Y (|0>+|1>)_c/sqrt2, with register order I, M, Y, c and pattern bit j in qubit j. Preparation of the training superposition is assumed available.

## Measurement

Computational-basis measurement of ancilla c (postselect outcome 0, probability eq_4), then computational-basis measurement of the class register Y (distribution eq_5). Input and memory registers need not be measured.

## Classical postprocessing

Discard runs with ancilla outcome 1; over kept runs estimate the frequency of each class-register outcome and assign x the class with the highest estimated frequency (eq_5). For the instance in eq_6 the expected frequencies are 2/3 for class 0 and 1/3 for class 1.

## Algorithm steps

1. Prepare the training superposition with the input pattern and the ancilla in |+> (storage routine assumed). (eq_1)
2. Apply CNOT from each input qubit j to memory qubit j, so the memory register holds x XOR x^k and its Hamming weight is d_k. (eq_2)
3. Apply the ancilla-controlled phase unitary U, writing phases exp(-/+ i pi d_k/(2n)) on the two ancilla branches. (eq_3)
4. Apply a Hadamard to the ancilla and measure it; keep the run only if the outcome is 0. (eq_4)
5. Measure the class register on kept runs; repeat to estimate class probabilities and output the most probable class. (eq_5, eq_6)

## Assumptions

- No experiment scope was supplied; a single minimal binary-class Trugenberger-style classifier with the instance n=2, N=2 in eq_6 was chosen
- The paper's algorithm follows Trugenberger's 2001 routine as recalled from background knowledge; paper-specific modifications are unknown
- Training patterns are stored with uniform amplitudes and the preparation of this superposition is treated as an available subroutine
- Class label is a single qubit (binary classification); multi-class digit recognition would need a larger class register
- Runs with ancilla outcome 1 are discarded and repeated; the number of repetitions for probability estimation is unspecified

## Missing information

- The paper's exact circuit and any deviations from Trugenberger's original proposal (phase scale, ancilla handling, decision rule)
- Storage algorithm used to prepare the superposition of training patterns
- Encoding of MNIST grey-scale images into n-bit binary patterns and the choice of n, N and digit classes
- Numerical results, accuracy, and the specific advantages discussed for handwritten digit recognition
- Whether classification uses a single-shot measurement, repeated sampling, or a different readout strategy
