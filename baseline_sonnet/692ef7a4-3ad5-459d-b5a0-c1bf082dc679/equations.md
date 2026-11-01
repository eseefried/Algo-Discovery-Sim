# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Adiabatic quantum computing with an added sequence of fast (random or regular) signals to shorten runtime, applied to a tiny instance of the 3-bit exact cover (EC3) problem. Only the generic adiabatic interpolation and a generic randomized product-formula picture can be reconstructed from the abstract.

Scope: Smallest useful construction: standard AQC interpolation H(s)=(1-s)H_B+sH_P on n=3 qubits, with an assumed fast-signal term and an assumed generic randomized Trotter step. Out of scope: the paper's specific signal sequences, the actual randomized Trotter formula and its error analysis, the open-system/decoherence modeling, the specific EC3 clause instance, and the trapped-ion implementation.

## Symbols

- $n$: number of qubits (bits of the EC3 instance); domain: positive integer; n=3 in the assumed tiny instance
- $H_B$: initial driver Hamiltonian; domain: Hermitian operator on (C^2)^{\otimes n}
- $H_P$: problem Hamiltonian whose ground state encodes the solution; domain: diagonal Hermitian operator on (C^2)^{\otimes n}
- $s=t/T$: normalized time; domain: [0,1]
- $T$: total evolution time; domain: positive real
- $H_f(t)$: fast-signal term (assumed form); domain: Hermitian operator, time-dependent
- $\xi_k$: random signal sign/amplitude in step k (assumed); domain: real or {±1}
- $\delta t$: Trotter step duration; domain: positive real
- $N$: number of Trotter steps; domain: positive integer, N=T/\delta t

## eq_1: Adiabatic interpolation

$$
H(s)=(1-s)H_B+sH_P,\quad s=t/T
$$

Standard AQC driving Hamiltonian; the final ground state encodes the solution.

Provenance: `standard_background`. Standard AQC form consistent with the abstract's description of a driving Hamiltonian whose final state encodes the solution; the paper's schedule is not given.

Equation assumptions:

- Linear schedule assumed

## eq_2: Fast-signal-assisted Hamiltonian

$$
H_{\rm tot}(t)=H(t/T)+H_f(t),\quad H_f(t)=\sum_{j}\xi_j(t)\,\sigma_j
$$

Driving Hamiltonian plus a rapidly varying random or regular signal term.

Provenance: `assumption`. The abstract only says fast random or regular signals are applied during evolution; the operator form is a placeholder.

Equation assumptions:

- Signal operators σ_j and time dependence ξ_j(t) are unspecified in the abstract

## eq_3: Randomized product step

$$
U\approx\prod_{k=1}^{N} e^{-i\,\delta t\,[H(s_k)+\xi_k\sigma_{j_k}]},\quad s_k=k\,\delta t/T
$$

Generic randomized Trotter-like discretization in which driving and signal are applied together in each step.

Provenance: `assumption`. The abstract says a randomized Trotter formula allows simultaneous implementation; the actual formula is not stated, so this is a generic stand-in. It is an approximation, not exact equality.

Equation assumptions:

- Each step exponentiates the combined Hamiltonian, or its split terms
- Sampling distribution of ξ_k and j_k unspecified

## eq_4: Adiabatic condition (background)

$$
T\gg\max_{s}\frac{|\langle e_1(s)|\partial_s H(s)|e_0(s)\rangle|}{g(s)^2},\quad g(s)=E_1(s)-E_0(s)
$$

Standard sufficient condition for adiabatic following, setting the long runtime that the fast signals aim to reduce.

Provenance: `standard_background`. Well-known textbook condition, not taken from the abstract.

Equation assumptions:

- Nondegenerate ground state along the path

## eq_5: EC3 problem Hamiltonian (generic form)

$$
H_P=\sum_{c\in C}\left(z_{c_1}+z_{c_2}+z_{c_3}-1\right)^2,\quad z_i=(1-\sigma^z_i)/2
$$

Generic exact cover 3 penalty Hamiltonian: each clause is satisfied iff exactly one of its three bits equals 1; zero energy means a solution.

Provenance: `standard_background`. Common EC3 encoding in the AQC literature; the paper's instance and form may differ.

Equation assumptions:

- Clause set C is not given in the abstract and must be chosen

## Registers

- q: 3 (assumed) qubits; Qubits encoding the EC3 bits, computational basis bit string z_1z_2z_3 with q_1 as most significant

## Initial state

Assumed ground state of H_B, e.g. H_B=-\sum_i\sigma^x_i gives the uniform superposition |+\rangle^{\otimes n}.

## Measurement

Computational-basis measurement of all qubits at the end; a low-energy outcome under H_P indicates an EC3 solution.

## Classical postprocessing

Check the measured bit string against the EC3 clauses and repeat on failure.

## Algorithm steps

1. Choose a tiny EC3 instance (clause set C) and build H_P and a driver H_B. (eq_5, eq_1)
2. Prepare the ground state of H_B. (eq_1)
3. Evolve under H(s) plus the assumed fast-signal term over total time T, with T shorter than the adiabatic-condition estimate. (eq_2, eq_4)
4. Discretize with a randomized Trotter-like product so driving and signals act in the same step. (eq_3)

## Assumptions

- No experiment_scope was given, so a 3-qubit EC3 instance with generic AQC was chosen as the smallest construction
- Signal form, schedule and randomized Trotter formula are placeholders, not the paper's
- No system-bath dynamics modeled

## Missing information

- Exact form and statistics of the fast signals
- The paper's randomized Trotter formula and its error bounds
- The specific EC3 instance and driver Hamiltonian
- Quantitative runtime reduction and decoherence model
- Trapped-ion implementation details
