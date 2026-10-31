# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct a mathematical specification of a fast-signal assisted adiabatic quantum algorithm for the 3-bit exact cover problem (EC3): an interpolating adiabatic Hamiltonian whose final ground state encodes EC3 solutions, supplemented by a sequence of fast (random or regular) signals, implemented via a (randomized) Trotter product formula.

Scope: One smallest useful construction: standard linear-interpolation AQC for a single-clause EC3 instance on n=3 qubits (clause x_1+x_2+x_3=1), with the Hamiltonian evolution discretized by a first-order Trotter product formula into which a generic fast-signal term is interleaved. Out of scope / not reconstructable from the abstract: the specific fast-signal schedule (random or regular), the operator the signals couple to, the paper's randomized Trotter formula and its error analysis, the runtime-reduction and coherence-protection claims, the open-system (system-bath) model, and the trapped-ion implementation.

## Symbols

- $n$: number of qubits (bits of the EC3 instance); domain: positive integer; n=3 in the chosen instance
- $T$: total adiabatic evolution time (runtime); domain: positive real
- $t$: physical time; domain: [0,T]
- $s$: dimensionless adiabatic schedule parameter s=t/T; domain: [0,1]
- $H_B$: initial (beginning) Hamiltonian with easily prepared ground state; domain: Hermitian operator on (\mathbb{C}^2)^{\otimes n}
- $H_P$: problem Hamiltonian whose ground states encode EC3 solutions; domain: diagonal Hermitian operator on (\mathbb{C}^2)^{\otimes n}
- $H(s)$: interpolating adiabatic Hamiltonian; domain: Hermitian operator on (\mathbb{C}^2)^{\otimes n}
- $X_i, Z_i$: Pauli X and Z operators on qubit i; domain: Hermitian unitary operators
- $x_i$: classical bit i, encoded in computational basis state of qubit i with Z_i|x_i\rangle=(-1)^{x_i}|x_i\rangle; domain: \{0,1\}
- $\mathcal{C}$: set of EC3 clauses, each a triple (a,b,c) of distinct bit indices; domain: finite set of triples in \{1,\dots,n\}^3
- $f(t)$: fast random or regular control signal amplitude; domain: real-valued function of t (unspecified in abstract)
- $V$: operator to which the fast signal couples; domain: Hermitian operator (unspecified in abstract)
- $M$: number of Trotter time steps; domain: positive integer
- $\Delta t$: Trotter time step \Delta t = T/M; domain: positive real
- $|\psi(t)\rangle$: system state at time t; domain: unit vector in (\mathbb{C}^2)^{\otimes n}
- $S$: set of satisfying bit strings of the EC3 instance; domain: subset of \{0,1\}^n

## eq_1: Linear-interpolation adiabatic Hamiltonian

$$
H(s) = (1-s)\,H_B + s\,H_P,\qquad s = t/T \in [0,1]
$$

Driving Hamiltonian interpolating from H_B at t=0 to H_P at t=T; by the adiabatic principle the system tracks the instantaneous ground state if T is large enough compared to the inverse squared minimum gap.

Provenance: `standard_background`. Standard AQC construction (Farhi et al.); the abstract only states the adiabatic principle, not the schedule form.

Equation assumptions:

- Linear schedule s=t/T; the paper may use a different schedule.

## eq_2: Initial Hamiltonian and its ground state

$$
H_B = \sum_{i=1}^{n} \frac{1 - X_i}{2},\qquad |\psi(0)\rangle = |+\rangle^{\otimes n} = \frac{1}{\sqrt{2^n}}\sum_{x\in\{0,1\}^n}|x\rangle
$$

Transverse-field initial Hamiltonian whose unique ground state (energy 0) is the uniform superposition.

Provenance: `standard_background`. Conventional choice of beginning Hamiltonian for AQC on satisfiability-type problems.

Equation assumptions:

- Paper's H_B is not given in the abstract; standard transverse-field form assumed.

## eq_3: EC3 problem Hamiltonian

$$
H_P = \sum_{(a,b,c)\in\mathcal{C}} \left(x_a + x_b + x_c - 1\right)^2,\qquad x_i = \frac{1 - Z_i}{2}
$$

Each clause contributes penalty 0 exactly when exactly one of its three bits equals 1, and a positive integer penalty otherwise; the ground-state energy is 0 iff the EC3 instance is satisfiable, and zero-energy computational basis states are exactly the solutions.

Provenance: `abstract_inferred`. The abstract states EC3 is solved adiabatically, implying a problem Hamiltonian whose ground states encode EC3 solutions; the explicit quadratic penalty form is the standard encoding and is not confirmed by the abstract.

Abstract evidence: We apply the algorithm for solving the $3$-bit exact cover problem (EC$3$)

Equation assumptions:

- Standard quadratic clause penalty; the paper's exact penalty normalization may differ.

## eq_4: Fast-signal assisted total Hamiltonian (generic form)

$$
H_{\mathrm{tot}}(t) = H(t/T) + f(t)\,V
$$

The adiabatic driving Hamiltonian is supplemented by a rapidly varying signal f(t) (random or regular) coupled to an operator V. The abstract does not specify f(t), V, or how they achieve runtime reduction.

Provenance: `assumption`. Minimal additive form consistent with the abstract's statement that a sequence of fast random or regular signals is applied during the evolution; the actual construction is not given.

Equation assumptions:

- Additive coupling of the fast signal to the Hamiltonian.
- f(t) and V are unspecified; any choice here is a placeholder, not the paper's.

## eq_5: First-order Trotter product formula for simultaneous implementation (approximation)

$$
U(T) \approx \prod_{k=M}^{1} e^{-i f(t_k) V \Delta t}\, e^{-i H(s_k) \Delta t},\qquad t_k = k\Delta t,\ s_k = t_k/T,\ \Delta t = T/M
$$

Time-ordered product (k=M applied last) approximating the evolution under H_tot(t), implementing the driving Hamiltonian and the fast signals in an interleaved manner; error is O(\Delta t) per step for the standard first-order formula. The paper's randomized Trotter formula is not reconstructable from the abstract.

Provenance: `standard_background`. Standard Lie-Trotter discretization; the abstract claims a randomized Trotter formula allowing simultaneous implementation, but gives no formula.

Equation assumptions:

- Deterministic first-order splitting used as a stand-in; randomization rule (e.g., random ordering or random term sampling) is unknown.

## eq_6: Tiny explicit instance: single-clause EC3 on 3 qubits

$$
n=3,\ \mathcal{C}=\{(1,2,3)\},\quad H_P = (x_1+x_2+x_3-1)^2,\quad S=\{100,010,001\},\quad H_P|x\rangle = E(x)|x\rangle,\ E(000)=1,\ E(x\in S)=0,\ E(110)=E(101)=E(011)=1,\ E(111)=4
$$

Smallest nontrivial EC3 instance; bit string written as x_1x_2x_3 (qubit 1 leftmost). Ground space of H_P is 3-fold degenerate.

Provenance: `assumption`. Chosen as the smallest useful test instance since no experiment scope was provided.

Equation assumptions:

- Instance is a reconstruction choice, not from the paper.

## eq_7: Success probability

$$
P_{\mathrm{succ}} = \sum_{x\in S} |\langle x|\psi(T)\rangle|^2
$$

Probability that a final computational-basis measurement yields a satisfying assignment.

Provenance: `standard_background`. Standard figure of merit for adiabatic optimization.

## Registers

- system: n = 3 qubits; Holds the EC3 bit assignment; qubit i encodes bit x_i with |0\rangle \leftrightarrow x_i=0; ordering x_1 x_2 x_3 left to right.

## Initial state

|\psi(0)\rangle = |+\rangle^{\otimes 3}, the ground state of H_B (eq_2), prepared by Hadamard on each qubit from |000\rangle.

## Measurement

Computational (Z) basis measurement of all n=3 qubits, yielding a bit string x_1x_2x_3; repeat to estimate P_succ.

## Classical postprocessing

Check each sampled bit string against the clause(s): x is a solution iff x_a+x_b+x_c=1 for every clause (equivalently E(x)=0). Estimate P_succ as the fraction of satisfying samples.

## Algorithm steps

1. Prepare the system register in the uniform superposition, the ground state of H_B. (eq_2)
2. Choose total time T and M Trotter steps; for k=1..M apply e^{-i H(s_k)\Delta t} with H(s_k)=(1-s_k)H_B + s_k H_P (for the chosen instance, eq_6), interleaved with the fast-signal pulse e^{-i f(t_k) V \Delta t} (placeholder form, eq_4). (eq_1, eq_3, eq_4, eq_5, eq_6)
3. Measure all qubits in the computational basis to obtain a candidate bit string x. (eq_7)

## Assumptions

- No experiment scope was supplied; the single-clause 3-qubit EC3 instance (eq_6) is a reconstruction choice.
- Linear interpolation schedule and transverse-field H_B are standard choices, not confirmed by the abstract.
- The fast-signal term is modeled generically as f(t)V added to the driving Hamiltonian; the paper's actual signal sequence and coupling are unknown.
- A deterministic first-order Trotter formula is used as a stand-in for the paper's randomized Trotter formula.
- Closed-system (unitary) dynamics are assumed; the abstract's system-bath decoherence discussion is not modeled.

## Missing information

- Explicit form of the fast random or regular signal sequence (amplitudes, timing, statistics) and the operator it couples to.
- The randomized Trotter formula itself, its randomization rule, and its error bounds.
- Mechanism and quantitative statement of the claimed runtime reduction while preserving adiabatic advantages.
- The open-system model (system-bath interaction) and the coherence measure used.
- Specific EC3 instances, schedule, T, and numerical results used in the paper.
- Trapped-ion implementation details (native interactions, pulse sequences, mapping of H_B, H_P, and signals).
