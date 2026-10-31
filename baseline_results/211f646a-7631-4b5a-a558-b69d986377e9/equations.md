# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Construct, by a quantum circuit, an orthonormal basis of n-qubit 'Bell-like' entangled states in which every basis state is an equal-weight superposition of exactly 2^m computational-basis terms with amplitudes ±1/sqrt(2^m), generalizing the standard Bell basis (n=2, m=1).

Scope: One smallest useful construction chosen by the reconstruction agent (not taken from the abstract): an n-qubit basis with 2^m-term states produced by Hadamards on m control qubits followed by a classical-reversible controlled map C_f onto the remaining n-m target qubits, with the explicit tiny instance n=3, m=2, f(k)=k_1 XOR k_2. Outside scope: the paper's two specific multi-qubit controlled-unitary gates and their 'working principles', the proof that all previously known entangled-basis constructions are special cases, the entanglement/quantum-correlation comparison, the monogamy-score analysis, and the qudit extension.

## Symbols

- $n$: total number of qubits in the system; domain: positive integer, n >= 2
- $m$: number of control qubits; each basis state has 2^m terms; domain: integer, 1 <= m <= n-1
- $a$: m-bit label of the control-register input (determines the sign pattern); domain: \{0,1\}^m
- $b$: (n-m)-bit label of the target-register input (determines the target offset); domain: \{0,1\}^{n-m}
- $k$: summation index over control-register computational basis states; domain: \{0,1\}^m
- $a \cdot k$: bitwise inner product a_1 k_1 + ... + a_m k_m taken mod 2; domain: \{0,1\}
- $f$: Boolean map from control strings to target strings implemented by the controlled gate C_f; domain: f:\{0,1\}^m \to \{0,1\}^{n-m}
- $\oplus$: bitwise XOR (addition mod 2) on bit strings; domain: \{0,1\}^{n-m} \times \{0,1\}^{n-m} \to \{0,1\}^{n-m}
- $s_j$: sign of the j-th term of a Bell-like state; domain: \{+1,-1\}
- $|B_{a,b}\rangle$: Bell-like basis state labelled by (a,b); the n-bit string ab (a leftmost) is read as an integer in [0, 2^n-1] with qubit 1 most significant; domain: unit vector in (\mathbb{C}^2)^{\otimes n}
- $H$: single-qubit Hadamard gate; domain: 2x2 unitary
- $C_f$: multi-qubit controlled-XOR gate writing f(k) into the target register; domain: 2^n x 2^n permutation unitary

## eq_1: Bell-like state form

$$
|B\rangle = \frac{1}{\sqrt{2^{m}}}\sum_{j=1}^{2^{m}} s_j\,|t_j\rangle,\quad s_j\in\{+1,-1\},\ t_j\in\{0,1\}^n\ \text{pairwise distinct}
$$

Every basis state is an equal-probability superposition of exactly 2^m distinct computational-basis terms with real amplitudes ±1/sqrt(2^m).

Provenance: `abstract_explicit`. Direct transcription of the amplitude/term-count statement in the abstract.

Abstract evidence: The Bell-like states in any basis is superposition of $2^{m}$-terms with equal probabilities (that is, their amplitudes being $\pm 1/\sqrt{2^{m}}$)

Equation assumptions:

- Terms t_j are distinct computational-basis states so that the squared amplitudes sum to 1.

## eq_2: Orthonormality of the basis

$$
\langle B_{a,b}|B_{a',b'}\rangle = \delta_{a a'}\,\delta_{b b'},\qquad (a,b)\in\{0,1\}^m\times\{0,1\}^{n-m},\ \ 2^n\ \text{states in total}
$$

The 2^n Bell-like states form an orthonormal basis of the n-qubit Hilbert space.

Provenance: `abstract_inferred`. Inferred from the word 'orthonormal bases'; a basis of n qubits must contain 2^n mutually orthogonal unit vectors. Labelling by (a,b) is the agent's choice.

Abstract evidence: generate multi-term orthonormal entangled Bell-like bases

Equation assumptions:

- Labelling of basis states by the computational-basis input (a,b) of the generating circuit.

## eq_3: Hadamard layer on the control register

$$
H^{\otimes m}|a\rangle = \frac{1}{\sqrt{2^{m}}}\sum_{k\in\{0,1\}^m} (-1)^{a\cdot k}\,|k\rangle
$$

m Hadamards create the 2^m-term equal-weight superposition with ±1 signs fixed by the input label a.

Provenance: `standard_background`. Standard identity for the m-fold tensor power of the Hadamard gate.

## eq_4: Controlled-XOR gate and generating unitary (chosen construction)

$$
C_f\,|k\rangle|b\rangle = |k\rangle\,|b\oplus f(k)\rangle,\qquad U = C_f\,\bigl(H^{\otimes m}\otimes I^{\otimes (n-m)}\bigr)
$$

A multi-qubit controlled gate that XORs a Boolean function of the control string into the target register; composed with the Hadamard layer it defines the generating circuit U.

Provenance: `assumption`. The abstract names 'multiple qubit controlled-unitary gates' but does not define them; C_f is a generic reversible stand-in chosen by the agent so that a concrete construction exists. It is NOT claimed to be either of the paper's two gates.

Equation assumptions:

- f is an arbitrary Boolean map; for the output to be entangled f must be non-constant.
- The paper's gates may act differently (e.g., non-permutation unitaries); this choice is a placeholder.

## eq_5: Generated Bell-like basis state

$$
|B_{a,b}\rangle = U|a\rangle|b\rangle = \frac{1}{\sqrt{2^{m}}}\sum_{k\in\{0,1\}^m} (-1)^{a\cdot k}\,|k\rangle\,|b\oplus f(k)\rangle
$$

Output of the chosen circuit on computational input (a,b). Since U is unitary and inputs are orthonormal, the 2^n outputs are orthonormal (eq_2); each has exactly 2^m distinct terms (distinct k) with amplitudes ±1/sqrt(2^m), matching eq_1.

Provenance: `assumption`. Follows exactly (no approximation) from eq_3 and eq_4 by linearity; equality is exact.

Equation assumptions:

- Construction of eq_4.

## eq_6: Tiny explicit instance n=3, m=2, f(k)=k_1 XOR k_2

$$
|B_{00,0}\rangle = \tfrac{1}{2}\bigl(|000\rangle+|011\rangle+|101\rangle+|110\rangle\bigr),\quad |B_{10,1}\rangle = \tfrac{1}{2}\bigl(|001\rangle+|010\rangle-|100\rangle-|111\rangle\bigr)
$$

Two of the eight orthonormal 4-term states (qubit 1 leftmost = most significant; label string ab read as integer, e.g. 00,0 -> 0 and 10,1 -> 5).

Provenance: `assumption`. Direct evaluation of eq_5 for the chosen instance; third qubit equals parity of first two XORed with b.

Equation assumptions:

- Instance parameters chosen by the agent for minimality.

## Registers

- control: m qubits; receives H^{⊗m}; its 2^m basis strings k index the terms of the Bell-like state; qubit 1 is the leftmost/most significant
- target: n-m qubits; receives b ⊕ f(k) via the multi-qubit controlled gate C_f; written to the right of the control register in kets

## Initial state

Computational basis state |a⟩|b⟩ with a ∈ {0,1}^m, b ∈ {0,1}^{n-m} (all 2^n inputs enumerate the whole basis); for the tiny instance, e.g. |000⟩.

## Measurement

None is required for state generation. Optional verification: measure all n qubits in the computational basis; for a correct |B_{a,b}⟩ the 2^m strings (k, b⊕f(k)) each appear with probability 2^{-m} and no other strings appear.

## Classical postprocessing

Optional: estimate outcome frequencies and compare with the uniform distribution over the 2^m predicted strings; sign (phase) information is not accessible from computational-basis statistics alone.

## Algorithm steps

1. Prepare the control and target registers in the computational basis state |a⟩|b⟩ labelling the desired basis element. (eq_2)
2. Apply H to each of the m control qubits to create the equal-weight 2^m-term superposition with sign pattern (-1)^{a·k}. (eq_3)
3. Apply the multi-qubit controlled gate C_f (controls: control register; targets: target register), XORing f(k) into the target register. (eq_4)
4. The output is the Bell-like basis state |B_{a,b}⟩ with exactly 2^m terms and amplitudes ±1/sqrt(2^m); running over all (a,b) yields the full orthonormal basis. (eq_5, eq_1, eq_2, eq_6)

## Assumptions

- No experiment_scope was supplied; the agent chose the single construction of eq_4 and the tiny instance n=3, m=2, f(k)=k_1⊕k_2.
- Register ordering: control register (qubit 1 most significant) is written left of the target register; the label string ab is read as a big-endian integer.
- The generic controlled-XOR gate C_f is a placeholder standing in for the paper's undefined controlled-unitary gates and is not claimed to reproduce their specific working principles or entanglement properties.

## Missing information

- Definitions and 'working principles' of the two multiple-qubit controlled-unitary gates introduced in the paper.
- The exact algorithms (gate sequences) proposed, and how previously known entangled-basis constructions arise as special cases.
- Which quantum-correlation measures (entanglement content, monogamy score) are used and their definitions/results for the different bases.
- The statement/proof that orthogonality forbids arbitrary amplitudes beyond the ±1/sqrt(2^m) pattern.
- The qudit generalization.
