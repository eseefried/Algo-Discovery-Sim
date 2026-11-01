# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Construct f-controlled phase gates for a three-qubit refined Deutsch-Jozsa algorithm from sigma_z, two-qubit controlled-phase and two-target controlled-phase gates. The abstract does not give the explicit decomposition or the circuit QED implementation details.

Scope: Smallest useful construction: the generic phase-oracle form of the refined DJ algorithm on 3 qubits, and the diagonal phase gate for one example function f, decomposed into Z, CZ and CCZ-type gates. Outside scope: the paper's specific decomposition of all 35 gates, the transmon-qutrit/cavity Hamiltonian, pulse sequences, and numerical feasibility simulations.

## Symbols

- $n$: number of qubits; domain: n=3
- $x$: computational basis string x_1x_2x_3; domain: {0,1}^3
- $f$: Boolean function of the oracle; domain: {0,1}^3 -> {0,1}
- $U_f$: f-controlled phase gate; domain: diagonal 8x8 unitary
- $H$: Hadamard gate; domain: single-qubit unitary
- $\mathrm{CZ}_{jk}$: two-qubit controlled phase gate; domain: diagonal unitary on qubits j,k
- $\mathrm{CCZ}_{123}$: controlled-controlled phase gate, here taken as an example of a multi-qubit phase gate; domain: diagonal unitary on 3 qubits

## eq_1: f-controlled phase gate

$$
U_f|x\rangle=(-1)^{f(x)}|x\rangle
$$

Diagonal phase oracle for a Boolean function f.

Provenance: `abstract_inferred`. The name f-controlled phase gate suggests a phase determined by f(x); the sign convention is assumed.

Abstract evidence: f$-controlled phase gates of a three-qubit refined Deutsch-Jozsa (DJ) algorithm

Equation assumptions:

- Phase is (-1)^{f(x)}, the standard DJ phase-oracle convention

## eq_2: DJ circuit amplitude

$$
|\psi_{\rm out}\rangle=H^{\otimes 3}U_fH^{\otimes 3}|000\rangle,\quad \langle 000|\psi_{\rm out}\rangle=\frac{1}{8}\sum_{x}(-1)^{f(x)}
$$

Standard DJ output amplitude on the all-zero state: magnitude 1 for constant f and 0 for balanced f.

Provenance: `standard_background`. Textbook DJ algorithm. The paper's refined variant may differ in details not given in the abstract.

Equation assumptions:

- Standard single-query phase-oracle DJ circuit used as a proxy for the refined version

## eq_3: Phase gate as polynomial in x

$$
(-1)^{f(x)}=\prod_{S\subseteq\{1,2,3\}}\left[(-1)^{c_S\prod_{j\in S}x_j}\right],\quad f(x)=\bigoplus_S c_S\prod_{j\in S}x_j,\ c_S\in\{0,1\}
$$

The algebraic normal form of f makes U_f a product of Z (|S|=1), CZ (|S|=2) and CCZ (|S|=3) gates, with a global sign for S empty.

Provenance: `standard_background`. Every Boolean function has a unique ANF. This is a generic decomposition, not necessarily the paper's protocol, which uses two-target controlled phase gates.

Equation assumptions:

- Generic decomposition; the paper's two-target gates are not reproduced

## eq_4: Example instance

$$
f(x)=x_1\oplus x_2x_3,\quad U_f=Z_1\,\mathrm{CZ}_{23}
$$

A tiny balanced example function with its decomposition into one single-qubit Z and one two-qubit CZ.

Provenance: `assumption`. Chosen as an illustrative instance; it is not claimed to be from the paper.

Equation assumptions:

- Example f chosen by the reconstruction
- f is balanced, so the all-zero amplitude is 0

## Registers

- q: 3 qubits; Three computational qubits, ordered q1q2q3, with x=4x_1+2x_2+x_3

## Initial state

|000> on the three qubits

## Measurement

Measure all three qubits in the computational basis. Under the standard DJ assumption, outcome 000 indicates constant f and any other outcome indicates balanced f.

## Classical postprocessing

Declare f constant if the result is 000, otherwise balanced.

## Algorithm steps

1. Apply Hadamard to each qubit to prepare the uniform superposition. (eq_2)
2. Apply the f-controlled phase gate U_f, decomposed into Z, CZ and CCZ gates according to the ANF of f (example: Z_1 CZ_23). (eq_1, eq_3, eq_4)
3. Apply Hadamard to each qubit again. (eq_2)

## Assumptions

- No scope was supplied, so a single oracle instance was chosen
- Standard DJ phase-oracle convention used in place of the paper's refined algorithm
- The paper's decomposition into 35 gates is not reconstructed

## Missing information

- Definition of the refined DJ algorithm and the set of 35 functions
- The explicit gate decomposition and the two-target controlled-phase construction
- Transmon qutrit/cavity Hamiltonian, pulse timings, and decoherence parameters
- Numerical fidelity results
