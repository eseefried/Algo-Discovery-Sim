# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Quantum state tomography of n qubits using a complete set of mutually unbiased bases (MUBs) generated cyclically by a generator built from Hadamard and controlled-phase gates.

Scope: Smallest useful instance: 2-qubit (d=4) tomography with MUB-defining conditions and a cyclic-generator structure. The specific 3- and 4-qubit generators, entanglement classes and circuits from the abstract are outside this scope.

## Symbols

- $n$: number of qubits; domain: positive integer
- $d$: Hilbert space dimension, 2^n; domain: positive integer
- $\{|\psi_k^{(a)}\rangle\}$: vectors of the a-th orthonormal basis; domain: k=0..d-1, a=0..d
- $U$: cyclic generator unitary built from Hadamard and controlled-phase gates (specific form not given); domain: unitary on (C^2)^{\otimes n}
- $\rho$: unknown n-qubit density matrix; domain: d x d positive semidefinite, trace 1
- $p_k^{(a)}$: probability of outcome k in basis a; domain: [0,1]

## eq_1: Mutual unbiasedness

$$
|\langle\psi_k^{(a)}|\psi_l^{(b)}\rangle|^2=\frac{1}{d},\quad a\neq b
$$

Defining condition for two orthonormal bases to be mutually unbiased.

Provenance: `standard_background`. Standard definition of MUBs; the abstract names the concept only.

## eq_2: Complete MUB set size

$$
N_{\mathrm{MUB}}=d+1=2^n+1
$$

A complete set has d+1 bases, which exists for prime-power d such as 2^n.

Provenance: `standard_background`. Known result for prime-power dimensions; the abstract mentions complete sets for three and four qubits.

## eq_3: Cyclic generation (schematic)

$$
|\psi_k^{(a+1)}\rangle=U|\psi_k^{(a)}\rangle
$$

Bases obtained by repeated application of a generator U (schematic; the actual cycle structure and any permutation or relabeling are not specified).

Provenance: `abstract_inferred`. Inferred from 'cyclic generation'; the exact form of the cycle is not given.

Abstract evidence: cyclic generation of mutually unbiased bases

Equation assumptions:

- U^m acts as identity or permutes bases after a cycle of some length
- Whether one cycle covers all bases is unspecified

## eq_4: Generator gate content (schematic)

$$
U=\Big(\prod_{i<j}CZ_{ij}^{\,c_{ij}}\Big)H^{\otimes n}\ \text{(assumed form)}
$$

Hypothetical form using Hadamards and controlled-phase gates with binary coupling pattern c_ij; the paper's actual generator is unknown.

Provenance: `assumption`. The abstract says only that the generator needs Hadamard and controlled-phase gates.

Equation assumptions:

- c_ij in {0,1} chosen per entanglement class
- Order of gates is assumed

## eq_5: Linear inversion reconstruction

$$
\rho=\sum_{a=0}^{d}\sum_{k=0}^{d-1}p_k^{(a)}|\psi_k^{(a)}\rangle\langle\psi_k^{(a)}|-\mathbb{I}
$$

State reconstruction from the outcome probabilities of a complete MUB set.

Provenance: `standard_background`. Standard identity for complete MUBs using d+1 bases, with Tr(rho)=1.

Equation assumptions:

- Complete set of d+1 MUBs
- Ideal probabilities

## Registers

- q: n (tiny instance n=2 assumed) qubits; system qubits being measured in each MUB

## Initial state

Unknown state rho on the n qubits to be reconstructed.

## Measurement

Computational-basis measurement of all n qubits after the basis-change circuit, for each of the d+1 MUBs.

## Classical postprocessing

Linear inversion using estimated probabilities (eq_5); finite-statistics corrections such as positivity projection are not specified.

## Algorithm steps

1. For each basis index a, apply the circuit implementing the basis change, i.e. a power of the generator U built from H and CZ gates (exact form unspecified). (eq_3, eq_4)
2. Measure all qubits in the computational basis to get outcome statistics p_k^(a) for each of the d+1 bases. (eq_1, eq_2)
3. Reconstruct rho from the frequencies. (eq_5)

## Assumptions

- Chosen scope is a tiny n=2 instance with standard MUB theory
- The explicit generator form is a placeholder, not from the abstract

## Missing information

- Explicit generator U and the gate order and phase pattern
- Cycle structure and how complete sets are covered
- Entanglement classes of the bases for 3 and 4 qubits
- Circuit details and gate counts
- Measurement-count or error analysis
