# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Simulate a pairing Hamiltonian (BCS/Richardson-type reduced pairing model) on a solid-state qubit array with nearest-neighbor interactions, and extract its energy spectrum by a measurement scheme. The abstract gives no explicit equations, so only a tiny background instance is reconstructed.

Scope: One smallest construction: a 2-pair-level reduced pairing Hamiltonian mapped to 2 qubits (pair occupied/empty), Trotterized time evolution, and phase-estimation-style spectrum extraction by Fourier transform of a time signal. The paper's specific nearest-neighbor gate decompositions, fidelity studies, complexity comparisons across Hamiltonian types, and its actual measurement scheme remain outside scope.

## Symbols

- $\epsilon_j$: single-particle level energy of pair level j; domain: real
- $G$: pairing coupling strength; domain: real
- $b_j^\dagger,b_j$: pair creation/annihilation operators on level j (hard-core boson, qubit raising/lowering); domain: operators
- $\sigma_j^{\pm},\sigma_j^z$: Pauli raising/lowering and Z operators on qubit j; domain: 2x2 matrices
- $t$: evolution time; domain: real
- $n$: number of Trotter steps; domain: positive integer
- $E_k$: eigenvalue of H; domain: real
- $|\psi_0\rangle$: initial reference state; domain: state in (C^2)^{\otimes 2}

## eq_1: Pairing Hamiltonian

$$
H=\sum_{j}2\epsilon_j\, b_j^\dagger b_j - G\sum_{j,k} b_j^\dagger b_k
$$

Standard reduced pairing (BCS-type) Hamiltonian in pair operators; level energy is doubled for pairs.

Provenance: `standard_background`. Generic form of a pairing Hamiltonian; the abstract names pairing Hamiltonians but gives no form.

Equation assumptions:

- Reduced BCS form with uniform coupling G
- Not claimed to be the paper's exact Hamiltonian

## eq_2: Qubit mapping

$$
b_j^\dagger\mapsto\sigma_j^{+},\quad b_j^\dagger b_j=\tfrac{1}{2}(1-\sigma_j^z)\ \text{(with }\sigma^z|0\rangle=|0\rangle\text{ as empty)}
$$

Hard-core pair occupation encoded as one qubit per level; |0> empty, |1> occupied.

Provenance: `assumption`. Proposed encoding for the tiny instance.

Equation assumptions:

- Pair-level occupation is 0 or 1
- Qubit j corresponds to level j, ordering q_0 then q_1

## eq_3: Two-qubit instance

$$
H=\sum_{j=0}^{1}\epsilon_j(1-Z_j)-\tfrac{G}{2}\left(2\cdot\tfrac{1-Z_0}{2}\cdot 0\right)-\,G\left(\tfrac{1-Z_0}{2}+\tfrac{1-Z_1}{2}\right)-\tfrac{G}{2}(X_0X_1+Y_0Y_1)
$$

Two-level instance: diagonal terms (number terms with j=k) plus an XY exchange term hopping a pair between levels, which is a nearest-neighbor XY-type interaction.

Provenance: `assumption`. Direct substitution of eq_2 into eq_1 for 2 levels, using \sigma^+_0\sigma^-_1+h.c.=(XX+YY)/2.

Equation assumptions:

- Two levels
- The vanishing-coefficient term is a placeholder that equals zero and carries no content

## eq_4: Trotterized evolution

$$
e^{-iHt}\approx\left(\prod_m e^{-iH_m t/n}\right)^n,\quad H=\sum_m H_m
$$

First-order Trotter approximation (approximate, not exact) with error O(t^2/n).

Provenance: `standard_background`. Standard method for simulating Hamiltonians with gates.

Equation assumptions:

- H_m are the diagonal Z terms and the XX+YY term

## eq_5: Spectrum from time signal

$$
S(t)=\langle\psi_0|e^{-iHt}|\psi_0\rangle=\sum_k |c_k|^2 e^{-iE_k t},\quad c_k=\langle E_k|\psi_0\rangle
$$

Time-domain signal whose Fourier transform peaks at eigenvalues E_k.

Provenance: `standard_background`. Common route to energy spectra; the paper's actual scheme is not stated in the abstract.

Equation assumptions:

- Re and Im of S(t) estimated via an ancilla-controlled evolution or Ramsey-type measurement

## Registers

- q: 2 qubits; system qubits encoding pair occupation of levels 0 and 1
- a: 1 qubits; ancilla for Hadamard-test estimation of S(t)

## Initial state

|\psi_0\rangle=|01\rangle (one pair in level 1), ancilla in |+\rangle; assumed choice

## Measurement

Ancilla measured in X and Y bases for a grid of times t.

## Classical postprocessing

Discrete Fourier transform of S(t) over sampled times; peak positions give eigenvalues E_k up to resolution ~2\pi/T_max.

## Algorithm steps

1. Prepare the system in the reference state and the ancilla in |+>. (no equation reference)
2. Apply the controlled Trotterized evolution for time t using the mapped Hamiltonian. (eq_3, eq_4)
3. Measure the ancilla in X and Y bases to estimate Re and Im of S(t) at multiple times. (eq_5)

## Assumptions

- No scope was given; the 2-level instance with Hadamard-test spectroscopy was chosen
- Hamiltonian form and measurement scheme are generic background, not the paper's
- Fidelity analysis, hardware-specific nearest-neighbor decompositions and complexity comparison not reconstructed

## Missing information

- Exact Hamiltonians and interaction types used by the paper
- Gate sequences or phase schedules for each algorithm
- Fidelity definitions and numerical parameters
- The paper's actual spectrum measurement scheme
- Complexity expressions
