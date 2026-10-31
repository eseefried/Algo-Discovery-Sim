# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct, as a mathematical specification, the three-qubit refined Deutsch-Jozsa (DJ) algorithm in which the oracle for a constant-or-balanced Boolean function f on 3 bits is an 'f-controlled phase gate' U_f|x> = (-1)^{f(x)}|x>, and express each such oracle (35 inequivalent balanced cases up to global phase) as a product of single-qubit sigma_z gates, two-qubit controlled-phase (CZ) gates, and one-control/two-target controlled-phase gates, as claimed in the abstract.

Scope: Scope chosen (no experiment_scope supplied): the abstract-level gate algebra only. (i) The refined DJ circuit for n=3 qubits with a phase oracle; (ii) the algebraic normal form (ANF) of 3-bit balanced functions and the resulting decomposition of U_f into Z, CZ and two-target-CZ gates; (iii) one tiny explicit instance f(x1,x2,x3) = x1 XOR x2 x3, for which U_f = Z_1 CZ_{23}, with the DJ output distribution. Outside scope (not reconstructable from the abstract): the physical realization with superconducting transmon qutrits resonantly coupled to a single cavity (Hamiltonian, pulse sequences, use of the third level), the specific operation sequence the paper uses for the two-target controlled-phase gate, the exact list/ordering of the 35 gates in the paper, and all numerical feasibility (fidelity/decoherence) results. Register ordering: qubit 1 is leftmost, |x> = |x_1 x_2 x_3>, integer label x = 4x_1 + 2x_2 + x_3.

## Symbols

- $n$: number of input qubits; fixed to n = 3; domain: positive integer, here 3
- $x = (x_1, x_2, x_3)$: 3-bit computational basis label, qubit 1 leftmost, integer value 4x_1+2x_2+x_3; domain: \{0,1\}^3
- $f$: Boolean function promised to be constant or balanced (balanced: f(x)=1 for exactly 4 of the 8 inputs); domain: f:\{0,1\}^3 \to \{0,1\}
- $U_f$: f-controlled phase gate (phase oracle) acting on the 3 qubits; domain: diagonal unitary on (\mathbb{C}^2)^{\otimes 3} with entries \pm 1
- $a_0, a_i, a_{ij}, a_{123}$: algebraic-normal-form (ANF) coefficients of f over GF(2); domain: \{0,1\}
- $Z_i$: single-qubit \sigma_z gate on qubit i; domain: unitary on qubit i
- $CZ_{ij}$: two-qubit controlled-phase gate between qubits i and j (phase -1 on |11>); domain: unitary on qubits i,j
- $CZ_{c;t_1 t_2}$: two-target controlled-phase gate: control c, targets t_1 and t_2; domain: unitary on 3 qubits
- $H$: Hadamard gate; domain: single-qubit unitary
- $\oplus$: addition modulo 2 (XOR); domain: GF(2) operation

## eq_1: f-controlled phase gate (phase oracle)

$$
U_f \lvert x \rangle = (-1)^{f(x)} \lvert x \rangle, \qquad U_f = \sum_{x \in \{0,1\}^3} (-1)^{f(x)} \lvert x \rangle\langle x \rvert
$$

The oracle of the refined DJ algorithm is a diagonal +/-1 phase gate on the three input qubits; no auxiliary qubit is used.

Provenance: `abstract_inferred`. The refined DJ algorithm (Collins-Kim-Holton form) encodes f as a phase (-1)^{f(x)} without an ancilla; the abstract's 'f-controlled phase gate' is read as this diagonal oracle. The count 35 matches the number of balanced 3-bit functions modulo complementation (70/2), since f and 1+f give the same gate up to global phase.

Abstract evidence: the 35 $f$-controlled phase gates of a three-qubit refined Deutsch-Jozsa (DJ) algorithm

Equation assumptions:

- 'f-controlled phase gate' means the ancilla-free phase oracle (-1)^{f(x)}
- Constant f gives U_f = +/- I and is treated as trivial, so the 35 nontrivial gates are the balanced functions up to global phase

## eq_2: Refined DJ circuit and decision rule

$$
\lvert \psi_{\mathrm{out}} \rangle = H^{\otimes 3} U_f H^{\otimes 3} \lvert 000 \rangle, \qquad P(000) = \left| \tfrac{1}{8} \sum_{x \in \{0,1\}^3} (-1)^{f(x)} \right|^2 = \begin{cases} 1, & f \text{ constant} \\ 0, & f \text{ balanced} \end{cases}
$$

Hadamards on all three qubits, one oracle call, Hadamards again, then measurement in the computational basis; outcome 000 occurs with certainty iff f is constant and never if f is balanced.

Provenance: `standard_background`. Standard refined (ancilla-free) Deutsch-Jozsa algorithm; the amplitude of |000> is the normalized sum of the oracle phases, which is +/-1 for constant f and exactly 0 for balanced f (equal numbers of +1 and -1).

Equation assumptions:

- Ideal gates and noiseless measurement

## eq_3: Algebraic normal form; balanced 3-bit functions have degree at most 2

$$
f(x) = a_0 \oplus a_1 x_1 \oplus a_2 x_2 \oplus a_3 x_3 \oplus a_{12} x_1 x_2 \oplus a_{13} x_1 x_3 \oplus a_{23} x_2 x_3 \oplus a_{123} x_1 x_2 x_3, \qquad a_{123} = \bigoplus_{x \in \{0,1\}^3} f(x) = 0 \ \text{if } f \text{ is balanced}
$$

Every 3-bit Boolean function has a unique ANF over GF(2). The cubic coefficient equals the parity of the number of ones in the truth table, which is even (4) for balanced f, so every balanced f is at most quadratic.

Provenance: `standard_background`. Standard Moebius-inversion property of the ANF: the top-degree coefficient is the XOR of all function values. This is why no three-qubit CCZ gate is needed and Z, CZ and two-target CZ gates suffice.

## eq_4: Decomposition of U_f into sigma_z and controlled-phase gates

$$
U_f = (-1)^{a_0} \, Z_1^{a_1} Z_2^{a_2} Z_3^{a_3} \, CZ_{12}^{a_{12}} CZ_{13}^{a_{13}} CZ_{23}^{a_{23}}, \qquad Z_i \lvert x \rangle = (-1)^{x_i} \lvert x \rangle, \quad CZ_{ij} \lvert x \rangle = (-1)^{x_i x_j} \lvert x \rangle
$$

Since (-1)^{u XOR v} = (-1)^u (-1)^v, each ANF monomial of degree 1 or 2 contributes one commuting diagonal gate; the constant term is a global phase. All factors are diagonal and mutually commute, so their order is irrelevant.

Provenance: `abstract_inferred`. Combining eq_1 and eq_3: for balanced f (degree <= 2) the phase (-1)^{f(x)} factorizes exactly into single-qubit Z and two-qubit CZ phases. This matches the abstract's gate set; the two-target gate (eq_5) merges two CZs sharing a control.

Abstract evidence: by using single-qubit $\sigma_{z}$ gates, two-qubit controlled phase gates, and two-target-qubit controlled phase gates

Equation assumptions:

- Global phase (-1)^{a_0} is physically irrelevant and dropped
- The paper's specific grouping of CZs into two-target gates is not known; any pair CZ_{ci}CZ_{cj} may be merged

## eq_5: Two-target-qubit controlled-phase gate

$$
CZ_{c;t_1 t_2} = \lvert 0 \rangle\langle 0 \rvert_c \otimes I_{t_1} \otimes I_{t_2} + \lvert 1 \rangle\langle 1 \rvert_c \otimes Z_{t_1} \otimes Z_{t_2} = CZ_{c t_1} \, CZ_{c t_2}
$$

A single control qubit applies sigma_z simultaneously to two target qubits; algebraically equal to the product of two CZ gates sharing the control.

Provenance: `assumption`. The abstract names the gate but does not define it; this is the natural definition (phase (-1)^{x_c(x_{t_1} XOR x_{t_2})}) consistent with the term 'two-target-qubit controlled phase gate'. It allows ANF terms x_c x_{t_1} XOR x_c x_{t_2} to be realized with one native gate.

Equation assumptions:

- The paper's two-target gate acts as Z on each target when the control is |1>; a different phase convention would change the identity

## eq_6: Tiny explicit instance

$$
f(x) = x_1 \oplus x_2 x_3 \ (\text{balanced}), \qquad U_f = Z_1 \, CZ_{23} = \mathrm{diag}(1,1,1,-1,-1,-1,-1,1), \qquad P(000) = 0
$$

One of the 35 balanced oracles: a_1 = a_{23} = 1, all other ANF coefficients zero. Diagonal entries listed in order x = 0,...,7 with x = 4x_1+2x_2+x_3. Running eq_2 yields outcome 000 with probability exactly 0 (the output state is H^{\otimes 3} U_f |+++> = a superposition of basis states with x_1 = 1).

Provenance: `assumption`. Chosen as the smallest nontrivial instance exercising both a single-qubit Z and a CZ; f is balanced because x_1 XOR x_2x_3 equals 1 for exactly 4 inputs (x = 1,2,3,4 in decimal... precisely: (0,1,1),(1,0,0),(1,0,1),(1,1,0)).

Equation assumptions:

- Instance choice is ours, not from the paper

## Registers

- q: 3 qubits; Input/query register of the refined DJ algorithm; qubit 1 leftmost, |x> = |x_1 x_2 x_3>, integer x = 4x_1+2x_2+x_3. No ancilla (refined DJ). The physical transmon qutrit third level used in the paper's implementation is outside scope.

## Initial state

\lvert 000 \rangle on register q (all three qubits in the computational ground state).

## Measurement

Measure all three qubits in the computational basis (single shot suffices ideally). Record the outcome string x_1 x_2 x_3.

## Classical postprocessing

Decide 'f constant' if the outcome is 000, otherwise 'f balanced' (eq_2). For the instance f = x_1 XOR x_2 x_3 the outcome 000 never occurs, so the answer 'balanced' is returned deterministically in the ideal case.

## Algorithm steps

1. Apply H to each of the three qubits, producing the uniform superposition (1/\sqrt{8}) \sum_x |x>. (eq_2)
2. Apply the f-controlled phase gate U_f, realized as the product of Z_i, CZ_{ij} (and optionally merged two-target CZ) gates given by the ANF coefficients of f; for the instance, apply Z_1 and CZ_{23}. (eq_1, eq_3, eq_4, eq_5, eq_6)
3. Apply H to each of the three qubits again. (eq_2)

## Assumptions

- The refined DJ algorithm is the ancilla-free version with phase oracle (-1)^{f(x)}; constant functions give trivial oracles (identity up to global phase), and the 35 nontrivial gates correspond to the 70 balanced 3-bit functions modulo complementation f -> 1 XOR f
- Two-target controlled-phase gate is defined as in eq_5 (Z on both targets conditioned on the control)
- Qubit ordering: qubit 1 leftmost, integer label x = 4x_1 + 2x_2 + x_3
- Gates are ideal; no noise model, qutrit leakage or cavity dynamics is included
- The explicit instance f = x_1 XOR x_2 x_3 is our choice for a minimal test, not taken from the paper

## Missing information

- The paper's explicit enumeration and chosen gate sequences for each of the 35 f-controlled phase gates (which pairs of CZs are merged into two-target gates)
- Definition and phase convention of the paper's two-target-qubit controlled phase gate
- Physical model: transmon qutrit level structure, cavity-coupling Hamiltonian, resonant pulse sequences, and how the third level is used to realize the gates
- All numerical feasibility results (gate/algorithm fidelity, decoherence parameters, operation times)
- Whether the paper counts constant functions among the 35 gates or treats them separately
