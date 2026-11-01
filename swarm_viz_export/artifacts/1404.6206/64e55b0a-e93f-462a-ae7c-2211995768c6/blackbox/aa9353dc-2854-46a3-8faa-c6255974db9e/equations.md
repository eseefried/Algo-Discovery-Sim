# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Construct a 2^m-term equal-magnitude (amplitudes ±1/sqrt(2^m)) orthonormal entangled Bell-like basis on n qubits using H, CNOT parity maps and Pauli gates, realised as a unitary mapping computational basis |s,t> to |psi_{s,t}>. Here t ranges over coset representatives, so the number of labels is 2^m * 2^(n-m) = 2^n only when A is handled carefully (see assumptions).

Scope: One tiny instance: n=3, m=1, A=[1] (n-m=2 target qubits, A is a 2x1 column (1,1)^T). Qubit order: q0 = superposition qubit, q1,q2 = target qubits. Label register is the same physical register: input |s>|t1 t2>, with the t label restricted so that t1 = 0 (t on q2 only has meaningful degrees of freedom beyond the column space), i.e. a full 2^n basis is obtained by using the full register as defined below. Not covered: the paper's two multi-qubit controlled-unitary gates, the claim that prior algorithms are special cases, monogamy-score and correlation analyses, and the qudit extension.

## Symbols

- $n$: total number of qubits; domain: integer >= m+1
- $m$: number of superposition qubits; domain: integer >= 1
- $x$: computational string on the superposition register; domain: {0,1}^m
- $s$: sign-pattern label; domain: {0,1}^m
- $t$: target shift label; domain: {0,1}^{n-m}
- $A$: binary (n-m) x m matrix, arithmetic mod 2; domain: GF(2)^{(n-m) x m}

## eq_1: Basis states

$$
|\psi_{s,t}\rangle=\frac{1}{\sqrt{2^m}}\sum_{x\in\{0,1\}^m}(-1)^{s\cdot x}|x\rangle|Ax\oplus t\rangle
$$

Bell-like state with 2^m terms and amplitudes ±1/sqrt(2^m).

Provenance: `abstract_inferred`. The amplitude structure is stated in the abstract; the explicit CNOT-parity form is a proposed construction, not the paper's controlled-unitary method.

Abstract evidence: The Bell-like states in any basis is superposition of $2^{m}$-terms with equal probabilities (that is, their amplitudes being $\pm 1/\sqrt{2^{m}}$).

Equation assumptions:

- CNOT parity map used instead of multi-qubit controlled unitaries

## eq_2: Orthonormality

$$
\langle\psi_{s,t}|\psi_{s',t'}\rangle=\delta_{ss'}\,\frac{1}{2^m}\sum_x(-1)^{(s\oplus s')\cdot x}[A x\oplus t=Ax\oplus t']
$$

For t=t' it equals delta_{ss'} by character orthogonality. For t≠t' the inner product is zero since Ax⊕t differs from Ax⊕t' for every x. States are orthonormal as a family over (s,t) because the x-register is shared and the target strings differ pointwise whenever t≠t'.

Provenance: `standard_background`. Hadamard character orthogonality, plus pointwise-different target strings for t≠t'. Count is 2^m*2^(n-m)=2^n, so the set is a complete basis.

Equation assumptions:

- Correction to the earlier spec: for the same x, the target strings differ for t≠t', but the x-register is also compared, so orthogonality holds for all t≠t' without needing coset restrictions

## eq_3: Preparation circuit

$$
V=\mathrm{CNOT}_A\,\big(H^{\otimes m}\otimes I\big)\ \text{with input}\ |s\rangle|t\rangle\ \text{encoded as}\ |\psi_{s,t}\rangle=\mathrm{CNOT}_A\,(I\otimes X^t)\,(H^{\otimes m}Z^{?}\otimes I)|0\rangle
$$

Unitary mapping |s>|t> to |psi_{s,t}>: apply H^{⊗m} to the sup register holding |s> (giving 2^{-m/2} sum_x (-1)^{s·x}|x>), leave |t> on the target register, then CNOT_A XORs Ax into the target giving |x>|t⊕Ax>.

Provenance: `assumption`. H on a computational |s> yields the sign pattern (-1)^{s·x} directly, so no separate Z gates are needed. CNOT_A is a reversible linear map, so V is unitary and maps the 2^n computational states onto the 2^n states psi_{s,t}.

Equation assumptions:

- The label register is the physical register itself
- Correction: the earlier spec's separate Z^s/X^t gates are replaced by this simpler input-encoding

## eq_4: Rejected prediction (controlled-X projector form)

$$
\mathcal{U}_{C^mX}=\left[I-P_A\right]\otimes\cdots\otimes\left[I-P_M\right]+P_A\otimes\cdots\otimes P_M\,X
$$

Predicted multi-qubit controlled-X form with a product-of-projectors expansion; recalled as standard background and not used in the circuit.

Provenance: `standard_background`. The projector form is a standard way of writing a multi-controlled X, but the paper's exact gate definitions are unverified. As printed, the tensor ordering is ambiguous (the first term lacks an identity on the target). The prediction is not used in the circuit.

Equation assumptions:

- P_k=|1><1| projects the k-th control; the X acts on the target qubit

## Registers

- sup: m (instance: 1) qubits; holds the label s on input, then x after H; qubit 0
- tgt: n-m (instance: 2) qubits; holds the label t on input, then Ax⊕t after CNOT_A; qubits 1,2

## Initial state

Computational basis |s>_sup|t>_tgt, with the bits of s and t prepared externally (e.g. by X gates on |0...0>). The all-zero input gives |psi_{0,0}>.

## Measurement

Not part of the unitary. To decode the label, apply the inverse circuit V^dagger (CNOT_A then H^{⊗m}) and measure all qubits in the computational basis to read out (s,t) exactly.

## Classical postprocessing

None needed: the measured bit string is directly (s,t). The monogamy-score and other correlation analyses are not computed.

## Algorithm steps

1. Apply H to each qubit of sup, which holds |s>, giving the sign pattern (-1)^{s.x}. (eq_3, eq_1)
2. For each (i,j) with A_ij=1, apply CNOT from sup qubit j to tgt qubit i, mapping |x>|t> to |x>|Ax⊕t>. (eq_3, eq_1)
3. The output is |psi_{s,t}>; orthonormality and completeness follow from the bijective unitary V on 2^n states. (eq_2)

## Assumptions

- Chosen tiny instance n=3, m=1, A=(1,1)^T (full column rank)
- Labels s,t are compiled as explicit input bits
- Correction to the earlier spec: the instance was changed from m=2 to m=1 so that A is full column rank and the construction is unambiguous; the CNOT-parity family is a generic special case, not the paper's controlled-unitary method

## Missing information

- The paper's two multi-qubit controlled-unitary gates and their exact definitions
- The paper's specific algorithms and families of bases
- Entanglement measures and monogamy score computations
- Exact qudit generalisation
