# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Sparse Hamiltonian simulation: approximate e^{-iHt} for a d-sparse Hamiltonian H with max entry magnitude ||H||_max to error epsilon, by combining quantum-walk steps with Bessel-function coefficients (Jacobi-Anger expansion), giving query complexity near-linear in tau = d t ||H||_max and logarithmic in 1/epsilon.

Scope: Background-level reconstruction of the Bessel-function linear-combination idea: a quantum walk operator W whose eigenphases are arcsin(lambda/(d||H||_max)) for eigenvalues lambda of H, and the Jacobi-Anger truncated expansion of e^{-i tau sin(theta)}. Excluded: the explicit walk construction, the LCU/oblivious amplitude amplification circuit, error analysis, gate-count accounting, and the lower-bound proof. No tiny circuit instance is given.

## Symbols

- $H$: d-sparse Hamiltonian; domain: Hermitian matrix on N-dimensional space
- $d$: sparsity (max nonzero entries per row); domain: positive integer
- $\|H\|_{\max}$: magnitude of largest entry of H; domain: nonnegative real
- $t$: evolution time; domain: real
- $\tau$: product of evolution time, sparsity and max entry magnitude; domain: nonnegative real
- $\epsilon$: target error; domain: (0,1)
- $J_n$: Bessel function of the first kind of order n; domain: real-valued function
- $W$: quantum walk operator (assumed form); domain: unitary
- $\lambda$: eigenvalue of H; domain: real, |\lambda| \le d\|H\|_{\max}
- $K$: truncation order of the Bessel series; domain: positive integer

## eq_1: Parameter definition

$$
\tau = d\,\|H\|_{\max}\, t
$$

Product of evolution time, sparsity and largest entry magnitude, as described in the abstract.

Provenance: `abstract_inferred`. Directly describes tau as a product of three named quantities; the symbolic form is the inference.

Abstract evidence: the product $\tau$ of the evolution time, the sparsity, and the magnitude of the largest entry of the Hamiltonian

Equation assumptions:

- d denotes sparsity and ||H||_max the largest entry magnitude

## eq_2: Jacobi-Anger expansion

$$
e^{-i\tau\sin\theta}=\sum_{n=-\infty}^{\infty}J_n(\tau)\,e^{-in\theta}
$$

Expansion of a phase in a Bessel series; with sin(theta)=lambda/(d||H||_max)-type walk eigenphases it yields e^{-iHt} as a linear combination of walk powers.

Provenance: `standard_background`. Standard identity; the abstract only mentions coefficients given by Bessel functions, not this exact form.

Equation assumptions:

- Used as the likely mechanism, not verified against the paper

## eq_3: Walk eigenphase relation (assumed)

$$
W\,|\mu_\pm\rangle = \pm e^{\pm i\arcsin(\lambda/(d\|H\|_{\max}))}|\mu_\pm\rangle
$$

Typical Szegedy-style quantum walk spectrum for a Hamiltonian with normalization d||H||_max, with sin(theta)=lambda/(d||H||_max).

Provenance: `assumption`. Standard form for Hamiltonian-simulation quantum walks; the paper's exact construction is not given in the abstract.

Equation assumptions:

- Walk built from a sparse-access oracle with normalization d||H||_max
- Eigenvectors mu_pm are in the invariant subspace

## eq_4: Truncated linear combination of walk powers

$$
e^{-iHt}\approx\sum_{n=-K}^{K}J_n(\tau)\,W^{n}\ \text{(up to sign/phase conventions)},\quad K=O\!\left(\tau+\frac{\log(1/\epsilon)}{\log\log(1/\epsilon)}\right)
$$

Approximation of the evolution by a Bessel-weighted combination of walk steps, which is an approximation and not an exact equality; the truncation order K is a typical scaling not stated in the abstract.

Provenance: `assumption`. Proposed from the Bessel-coefficient description; sign and phase corrections for the +/- branches are omitted.

Equation assumptions:

- Sign and phase handling between branches omitted
- Truncation scaling taken from general knowledge of Bessel decay

## eq_5: Claimed complexity form

$$
\text{Cost}=\tilde O\!\left(\tau\right)\cdot\mathrm{polylog}(1/\epsilon),\qquad \text{lower bound: }\Omega(\tau)
$$

Near-linear in tau, logarithmic in 1/epsilon, with a claimed lower bound showing no sublinear dependence on tau.

Provenance: `abstract_inferred`. Qualitative scaling is stated; the precise polylog factors are not.

Abstract evidence: is logarithmic in the inverse error, and nearly linear in the product $\tau$

Equation assumptions:

- Exact polylog factors unspecified

## Registers

- system: n = log2 N qubits (assumed) qubits; Register holding the state acted on by H
- walk/ancilla: unknown qubits; Ancilla for quantum walk steps and sparse-oracle queries
- LCU control: unknown, about log K qubits (assumed) qubits; Index register selecting the walk power n with amplitude proportional to J_n(tau)

## Initial state

Arbitrary system state |psi> with ancillas in |0>; the specific state is not given.

## Classical postprocessing

Classical computation of Bessel coefficients and choice of K; details are not given in the abstract.

## Algorithm steps

1. Define tau and choose truncation order K to meet error epsilon. (eq_1, eq_4)
2. Build the quantum walk W whose spectrum encodes arcsin of the scaled eigenvalues of H using sparse-access queries. (eq_3)
3. Prepare control amplitudes proportional to the Bessel coefficients J_n(tau) and apply the controlled powers of W as a linear combination (LCU). (eq_2, eq_4)
4. Boost success probability, for example via amplitude amplification, and compare cost scaling with the claimed result. (eq_5)

## Assumptions

- The method is assumed to be the Jacobi-Anger Bessel expansion over a quantum walk, which is background rather than paper-sourced
- No explicit small instance is chosen
- Normalization and sign conventions are not verified

## Missing information

- Exact quantum walk construction and its spectrum
- Exact LCU and amplitude amplification procedure
- Rigorous truncation and error bounds
- Explicit gate and query counts and the polylog factors
- Lower-bound proof
- Concrete tiny instance
