# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Generate an orthonormal basis of n-qubit Bell-like states, each a uniform-magnitude superposition of 2^m terms with amplitudes +-1/sqrt(2^m), using Hadamards on m control qubits, a CNOT-fan controlled gate (type A) and CZ-style phase gates (type B), then check orthonormality and compute entanglement and monogamy measures classically from the statevector.

Scope: One tiny instance: n=3, m=1 (also n=4, m=2 as an optional extension). Qubit 0 is the control and qubits 1,2 are targets, with X gates on the inputs to set labels. Statevector only, no measurements. The paper's exact two controlled-unitary definitions, the proof that all earlier methods are special cases, the entanglement-measure computations and the qudit extension are outside scope except as noted.

## Symbols

- $n$: total number of qubits; domain: integer, 3 to 5
- $m$: number of control qubits; domain: integer, 1 <= m < n
- $c$: control bit string; domain: {0,1}^m
- $f$: injective GF(2)-linear map from controls to targets, given by the CNOT fan pattern; domain: {0,1}^m -> {0,1}^{n-m}
- $a$: bit-flip label applied by X on the target inputs; domain: {0,1}^{n-m}
- $b$: phase label, set by the X-prepared control inputs before H; domain: {0,1}^m
- $g$: GF(2)-linear sign function for type B gates; domain: {0,1}^m -> {0,1}
- $|\Psi_{a,b}\rangle$: Bell-like basis state; domain: 2^n-dimensional Hilbert space, normalized
- $G$: Gram matrix of the basis statevectors; domain: complex 2^n x 2^n matrix

## eq_1: Multi-term state

$$
|\Psi_{a,b}\rangle=\frac{1}{\sqrt{2^m}}\sum_{c\in\{0,1\}^m}(-1)^{b\cdot c}\,|c\rangle\,|f(c)\oplus a\rangle
$$

Proposed form of the basis states: a type A fan-out of H-prepared controls, a phase label b on the controls and a bit-flip label a on the targets.

Provenance: `assumption`. The abstract only states 2^m terms with amplitudes +-1/sqrt(2^m). This explicit form is my interpretation of the sketch.

Equation assumptions:

- f injective and linear
- Gate order is H on controls, then CNOT fan, then labels as stated

## eq_2: Amplitude magnitude

$$
|\langle c,t|\Psi_{a,b}\rangle|\in\{0,\,2^{-m/2}\},\quad \langle c,t|\Psi_{a,b}\rangle\in\{0,\pm 2^{-m/2}\}
$$

Every nonzero amplitude has magnitude 1/sqrt(2^m) with sign +-1.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: that is, their amplitudes being $\pm 1/\sqrt{2^{m}}$

## eq_3: Orthonormality

$$
G_{(a,b),(a',b')}=\langle\Psi_{a,b}|\Psi_{a',b'}\rangle=\delta_{aa'}\delta_{bb'}
$$

The Gram matrix of all 2^n states should be the identity.

Provenance: `abstract_inferred`. Orthonormality of the basis is claimed. For my eq_1 form, the overlap is nonzero only if f(c)+a = f(c)+a' for some c, i.e. a=a'. Then the sum over c of the characters gives delta_bb'. The count 2^m * 2^(n-m) = 2^n labels requires the a label to range over the full target space.

Abstract evidence: generate multi-term orthonormal entangled Bell-like bases

Equation assumptions:

- eq_1 form
- labels range over all 2^n values

## eq_4: Type B phase gate

$$
U_B|c\rangle|t\rangle=(-1)^{g(c)}|c\rangle|t\rangle,\quad g(c)=\bigoplus_i w_i c_i
$$

A CZ-style gate that attaches linear-character signs. Distinct w give different sign patterns.

Provenance: `assumption`. This is my interpretation of a phase-type gate. The abstract does not define it.

Equation assumptions:

- g linear over GF(2)

## eq_5: Monogamy score

$$
\pi_1=\tau_{1|\text{rest}}-\sum_{j\ne1}\tau_{1j},\quad \tau_{1|\text{rest}}=2(1-\mathrm{Tr}\rho_1^2)
$$

Classical postprocessing on the statevector. The one-vs-rest tangle is computed from the single-qubit purity, and the pairwise tangles are squared concurrences of reduced two-qubit states.

Provenance: `standard_background`. The standard residual-tangle form of monogamy score. The abstract's monogamy score may use another measure such as negativity.

Equation assumptions:

- Concurrence-based tangle is used

## Registers

- ctrl: m qubits; control qubits, H applied, hold the phase label b
- tgt: n-m qubits; target qubits, X-set to label a, fanned out by CNOTs

## Initial state

Computational basis state |b>_ctrl |a>_tgt, set by X gates. In the actual circuit the b-bits are applied by X before the Hadamards, giving the phase character.

## Classical postprocessing

Read the statevector of each label circuit. Build the Gram matrix and compare it with the identity. Check that nonzero amplitudes have magnitude 2^{-m/2}. Compute reduced density matrices, entropies, concurrence/tangle and monogamy score per state.

## Algorithm steps

1. Apply X on the control and target qubits according to the labels b and a. (eq_1)
2. Apply H on each control qubit. (eq_1)
3. Apply the type A CNOT fan: control i flips its prescribed subset of targets, realizing f(c). (eq_1, eq_2)
4. Optionally apply type B CZ gates to attach extra signs (different bases). (eq_4)
5. Repeat for all labels, then compute the Gram matrix and check that the amplitudes are 0 or +-2^{-m/2}. (eq_2, eq_3)
6. Compute reduced-state entropies and the monogamy score for each state. (eq_5)

## Assumptions

- Smallest instance n=3, m=1 chosen by me
- The two gates are read as a bit-flip fan-out and a phase type
- No black-box oracle appears, so no query budget applies
- Qubit cap not stated; instances use at most 5 qubits
- Qudit extension excluded

## Missing information

- Exact definitions of the paper's two multiple qubit controlled-unitary gates
- Exact gate orderings for generating each basis
- Which monogamy and correlation measures are used, and the numerical results
- Why other bases are special cases
