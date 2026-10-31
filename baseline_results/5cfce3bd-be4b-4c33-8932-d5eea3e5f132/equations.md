# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Given black-box (oracle) access to a function F on a finite domain of N points, approximate its mean value \mu = (1/N)\sum_x F(x) to additive error \epsilon using as few oracle queries as possible; the abstract also mentions a related algorithm for approximating the median of a set of points under an arbitrary distance, which is left outside this reconstruction.

Scope: Only the first task (mean estimation of a black-box function) is reconstructed, and only as a generic amplitude-estimation-based mean estimator, because the abstract gives no mathematical detail of the paper's novel algorithm. Scope: F:{0,...,N-1}\to[0,1] encoded as a controlled rotation on one ancilla, uniform superposition over indices, Brassard-Hoyer-Mosca-Tapp amplitude estimation with m precision qubits. Tiny explicit instance (assumption): N=4 (n=2 index qubits), F=(0,1/2,1/2,1) so \mu=1/2, m=3 precision qubits (M=8), giving an exact estimate. Outside scope: the paper's specific novel optimal algorithm, the Aharonov-type variant, success-probability amplification, and the median-approximation algorithm over an arbitrary distance.

## Symbols

- $N$: size of the domain of the black-box function; N = 2^n; domain: positive integer, power of two
- $n$: number of index qubits; domain: positive integer
- $F$: black-box function whose mean is sought (rescaled to [0,1]); domain: F:\{0,\dots,N-1\}\to[0,1]
- $\mu$: exact mean value of F over the domain; domain: [0,1]
- $\tilde{\mu}$: estimate of the mean returned by the algorithm; domain: [0,1]
- $\epsilon$: target additive error; domain: (0,1)
- $\theta$: amplitude angle with \sin^2\theta = \mu; domain: [0,\pi/2]
- $m$: number of precision (phase) qubits in amplitude estimation; M = 2^m; domain: positive integer
- $y$: integer measured on the precision register (big-endian, y = \sum_j y_j 2^{m-1-j}); domain: \{0,\dots,M-1\}
- $U_F$: oracle unitary encoding F(x) as an ancilla rotation amplitude; domain: unitary on n+1 qubits
- $\mathcal{A}$: state-preparation unitary \mathcal{A} = U_F (H^{\otimes n}\otimes I); domain: unitary on n+1 qubits
- $Q$: Grover/amplitude-amplification operator built from \mathcal{A}; domain: unitary on n+1 qubits

## eq_1: Mean of the black-box function

$$
\mu = \frac{1}{N}\sum_{x=0}^{N-1} F(x), \qquad F(x)\in[0,1]
$$

Quantity to be approximated; the range restriction to [0,1] is a normalization assumption (a bounded F can be affinely rescaled).

Provenance: `abstract_inferred`. The abstract names the mean of a black-box function as the target; the explicit formula and the [0,1] normalization are inferred/assumed, not stated.

Abstract evidence: approximate the mean value of a black-box function

Equation assumptions:

- F is bounded and rescaled to [0,1]
- domain size N is a power of two

## eq_2: Oracle encoding of F as ancilla amplitude

$$
U_F\,|x\rangle|0\rangle = |x\rangle\left(\sqrt{1-F(x)}\,|0\rangle + \sqrt{F(x)}\,|1\rangle\right)
$$

The black box is assumed available as a unitary that rotates a single ancilla qubit by an angle determined by F(x). Any oracle returning F(x) in a register can be converted to this form by a controlled rotation.

Provenance: `assumption`. The abstract does not specify the oracle model; this is the standard encoding used for amplitude-estimation-based mean estimation and is chosen as the smallest useful construction.

Equation assumptions:

- oracle access to F is available as a unitary U_F or as a digital oracle convertible to U_F

## eq_3: Prepared state and amplitude-angle relation

$$
\mathcal{A}|0^n\rangle|0\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle\left(\sqrt{1-F(x)}|0\rangle+\sqrt{F(x)}|1\rangle\right) = \cos\theta\,|\Psi_0\rangle + \sin\theta\,|\Psi_1\rangle, \qquad \sin^2\theta = \mu
$$

With \mathcal{A}=U_F(H^{\otimes n}\otimes I), the probability of measuring the ancilla in |1\rangle equals exactly the mean \mu. |\Psi_1\rangle (resp. |\Psi_0\rangle) is the normalized component with ancilla 1 (resp. 0).

Provenance: `standard_background`. Direct computation: the squared norm of the ancilla-1 component is (1/N)\sum_x F(x) = \mu.

Equation assumptions:

- eq_1 normalization
- eq_2 oracle model

## eq_4: Amplitude-amplification operator and its eigenvalues

$$
Q = -\mathcal{A}\,S_0\,\mathcal{A}^{\dagger}\,S_\chi, \qquad S_\chi = I\otimes Z_{\text{anc}}, \quad S_0 = I - 2|0^{n+1}\rangle\langle 0^{n+1}|, \qquad Q|\Psi_\pm\rangle = e^{\pm 2i\theta}|\Psi_\pm\rangle
$$

S_\chi flips the sign of basis states whose ancilla is 1 (a Z gate on the ancilla, up to global convention); S_0 reflects about the all-zero state. Q acts as a rotation by 2\theta on span{|\Psi_0\rangle,|\Psi_1\rangle}, and \mathcal{A}|0\rangle is an equal superposition of the eigenvectors |\Psi_\pm\rangle.

Provenance: `standard_background`. Standard Brassard-Hoyer-Mosca-Tapp amplitude amplification/estimation construction.

Equation assumptions:

- eq_3

## eq_5: Amplitude estimation output and error bound

$$
\tilde{\mu} = \sin^2\!\left(\frac{\pi y}{M}\right),\ M=2^m, \qquad \Pr\left[\,|\tilde{\mu}-\mu| \le \frac{2\pi\sqrt{\mu(1-\mu)}}{M} + \frac{\pi^2}{M^2}\right] \ge \frac{8}{\pi^2}
$$

After phase estimation of Q with m precision qubits (controlled Q^{2^j} followed by inverse QFT) and measurement outcome y, the estimate is \tilde{\mu}. The bound is an approximation guarantee, not an exact equality; it becomes exact equality when 2\theta M/(2\pi) is an integer (as in the chosen instance).

Provenance: `standard_background`. Standard amplitude estimation theorem (BHMT 2002, Theorem 12) applied to the amplitude \mu of eq_3.

Equation assumptions:

- eq_3
- eq_4
- no additional success-probability amplification (e.g., median of repetitions) is included

## eq_6: Query complexity for additive error \epsilon

$$
\text{queries to } U_F \text{ (and } U_F^{\dagger}\text{)} = O(M) = O(1/\epsilon), \qquad \text{matching the lower bound } \Omega(1/\epsilon)
$$

Choosing M = \Theta(1/\epsilon) gives additive error \epsilon with constant probability using O(1/\epsilon) oracle calls; the matching lower bound is standard background (Nayak-Wu), which is what 'asymptotically optimal' is taken to mean.

Provenance: `abstract_inferred`. The abstract claims the first algorithm is asymptotically optimal; the inference is that its query complexity meets the known \Omega(1/\epsilon) lower bound for mean estimation. The specific algorithm achieving this in the paper is not described in the abstract; the reconstructed amplitude-estimation route is a standard way to attain O(1/\epsilon).

Abstract evidence: asymptotically optimal

Equation assumptions:

- the optimality claim refers to oracle-query complexity as a function of \epsilon
- the paper's actual algorithm may differ from the generic amplitude-estimation reconstruction

## Registers

- index: n = 2 (instance); general n = \log_2 N qubits; holds x in binary (big-endian); put in uniform superposition and queried by U_F
- value ancilla: 1 qubits; target of the F-dependent rotation; marked subspace is ancilla = |1\rangle
- precision: m = 3 (instance); general m = \lceil \log_2(1/\epsilon)\rceil + O(1) qubits; phase-estimation register controlling powers of Q; measured to obtain y

## Initial state

|0\rangle^{\otimes m}_{\text{prec}} \otimes |0\rangle^{\otimes n}_{\text{index}} \otimes |0\rangle_{\text{anc}}; for the instance N=4, F=(0,1/2,1/2,1), so \mu = 1/2 and \theta = \pi/4 (eq_1, eq_3).

## Measurement

Measure all m precision qubits in the computational basis to obtain integer y \in \{0,\dots,M-1\}; index and ancilla registers are discarded.

## Classical postprocessing

Compute \tilde{\mu} = \sin^2(\pi y / M) (eq_5). Optionally repeat O(\log(1/\delta)) times and take the median of the estimates to boost success probability to 1-\delta (not part of the scoped construction). If F was rescaled from [a,b] to [0,1], map back via a + (b-a)\tilde{\mu}.

## Algorithm steps

1. Prepare the amplitude-encoded state: apply H^{\otimes n} to the index register, then the oracle U_F, giving \mathcal{A}|0^n\rangle|0\rangle with ancilla-1 probability exactly \mu. (eq_2, eq_3)
2. Apply H^{\otimes m} to the precision register, then for j = 0,\dots,m-1 apply Q^{2^j} controlled on precision qubit j (big-endian ordering so that qubit j contributes 2^{m-1-j}... with controlled powers arranged accordingly), where Q is the amplitude-amplification operator. (eq_4)
3. Apply the inverse quantum Fourier transform on the precision register so that it holds an approximation to M\theta/\pi (mod M) or M - M\theta/\pi. (eq_4, eq_5)
4. Measure the precision register, obtain y, and output \tilde{\mu} = \sin^2(\pi y/M). For the instance (\theta=\pi/4, M=8) the outcomes y\in\{2,6\} occur with certainty and give \tilde{\mu} = 1/2 exactly. (eq_5, eq_6)

## Assumptions

- The paper's first (novel, optimal) algorithm is reconstructed only generically as amplitude-estimation-based mean estimation; its actual construction is not given in the abstract and may differ.
- F is bounded and normalized to [0,1]; N is a power of two.
- Oracle access is available as the amplitude-encoding unitary U_F (eq_2) or convertible to it.
- Tiny instance chosen: N=4, F=(0,1/2,1/2,1), m=3, giving \mu=1/2 exactly recoverable.
- Big-endian integer encoding for both index and precision registers.
- Success probability is left at the single-shot amplitude-estimation level (\ge 8/\pi^2); no amplification included.

## Missing information

- Mathematical description of the paper's novel asymptotically optimal mean-estimation algorithm (abstract gives no equations).
- Description of the second algorithm (variation on Aharonov's) and its specific strengths/caveats.
- Definition and algorithm for approximating the median of a set of points over an arbitrary distance function, including the oracle model for the distance and how mean estimation is used as a subroutine.
- Precise oracle model, range/normalization assumptions on F, error model (additive vs. relative), and success-probability targets assumed by the paper.
- Exact query-complexity constants and the precise sense of 'asymptotically optimal' (which parameters, which lower bound).
