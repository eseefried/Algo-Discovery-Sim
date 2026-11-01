# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate the single-qubit Markovian semigroup T_t = exp(tL) applied to a density matrix rho, using a second-order product formula over a decomposition of L, with each factor realized as a single-qubit channel via a unitary on system plus one ancilla (ancilla reset to |0> between segments).

Scope: One tiny instance: a qubit generator L = L_H + L_deph + L_damp (Hamiltonian rotation, pure dephasing, amplitude damping) with symmetric second-order Trotter with r segments, each segment channel dilated on 1 system + 1 ancilla qubit (2 qubits total). Readout via the system reduced density matrix (statevector, trace out ancilla). Out of scope: the paper's specific decomposition and recombination technique, the specific arbitrary single-qubit channel approximation method and its gate counts, and the proof of the O((||L|| t)^{3/2}/eps^{1/2}) bound.

## Symbols

- $\mathcal{L}$: Lindblad generator of the qubit semigroup; domain: linear superoperator on 2x2 matrices
- $T_t$: semigroup of single-qubit channels e^{t L}; domain: CPTP maps, t>=0
- $\mathcal{L}_j$: j-th simple generator piece (Hamiltonian, dephasing, damping); domain: superoperators, j=1..m
- $r$: number of Trotter segments; domain: positive integer
- $\epsilon$: target accuracy; domain: (0,1)
- $\|\mathcal{L}\|_{(1\to1)}$: induced trace-norm superoperator norm of L; domain: nonnegative real
- $U_j$: 2-qubit unitary dilating the channel e^{(t/(2r))L_j}; domain: U(4)
- $\gamma, \Gamma, \omega$: dephasing rate, damping rate, Hamiltonian frequency in the instance; domain: nonnegative reals

## eq_1: Semigroup

$$
T_t=e^{t\mathcal{L}},\quad \mathcal{L}=\sum_{j=1}^m\mathcal{L}_j
$$

Target channel and generator decomposition into simple pieces.

Provenance: `abstract_inferred`. The channel form is stated; the decomposition into simple terms is inferred from 'decomposition and recombination technique'.

Abstract evidence: approximates the channel $T_{t}=e^{t\mathcal{L}}$ up to chosen accuracy $\epsilon$

Equation assumptions:

- The specific decomposition used in the paper is unknown; this one is assumed.

## eq_2: Second-order product formula

$$
S_2(s)=e^{\frac{s}{2}\mathcal{L}_1}\cdots e^{\frac{s}{2}\mathcal{L}_m}e^{\frac{s}{2}\mathcal{L}_m}\cdots e^{\frac{s}{2}\mathcal{L}_1},\quad T_t\approx S_2(t/r)^r
$$

Symmetric Suzuki formula with r segments.

Provenance: `standard_background`. Inspired by Hamiltonian simulation; second-order choice follows the 3/2 exponent but is assumed.

Equation assumptions:

- Second-order formula used; the paper may use other orders.

## eq_3: Trotter error and segment count

$$
\|T_t-S_2(t/r)^r\|=O\!\left(\frac{(\|\mathcal{L}\|t)^3}{r^2}\right),\quad r=O\!\left(\frac{(\|\mathcal{L}\|t)^{3/2}}{\epsilon^{1/2}}\right)
$$

Error scaling gives segment count consistent with the claimed gate count when each segment costs O(1) gates.

Provenance: `abstract_inferred`. Inverting the standard second-order error gives this r; matches the stated scaling.

Abstract evidence: $\mathcal{O}\big((||\mathcal{L}||_{(1\rightarrow 1)}t)^{3/2}/\epsilon^{1/2}\big)$ single qubit and CNOT gates

Equation assumptions:

- Constant gates per segment
- Norm of terms bounded by a constant times ||L||

## eq_4: Dilation of each factor

$$
\mathcal{E}_j(\rho)=\mathrm{Tr}_{A}\!\left[U_j(\rho\otimes|0\rangle\langle0|)U_j^\dagger\right]=\sum_k K_k\rho K_k^\dagger,\quad K_k=(\mathbb{1}\otimes\langle k|)U_j(\mathbb{1}\otimes|0\rangle)
$$

Each single-qubit channel is realized with one ancilla in |0>, then ancilla discarded/reset.

Provenance: `abstract_inferred`. Single ancilla dilation is stated; Stinespring form with a 2-dim environment is background (Kraus rank <=2 needed here).

Abstract evidence: the algorithm requires only a single ancilla qubit, the minimal possible dilation for a non-unitary single-qubit quantum channel

Equation assumptions:

- Each e^{sL_j} in the instance has Kraus rank <=2 (true for dephasing, damping, unitary pieces).

## eq_5: Instance channels

$$
K_0=\begin{pmatrix}1&0\\0&\sqrt{1-p}\end{pmatrix},\ K_1=\begin{pmatrix}0&\sqrt p\\0&0\end{pmatrix},\ p=1-e^{-\Gamma s};\quad \text{dephasing: }\rho_{01}\to e^{-\gamma s}\rho_{01};\quad \text{Hamiltonian: }\rho\to e^{-i\omega s Z/2}\rho e^{i\omega sZ/2}
$$

Analytic exponentials of the assumed pieces; amplitude damping realized by controlled rotation by angle 2 arcsin sqrt p plus CNOT.

Provenance: `assumption`. Concrete tiny instance chosen for implementation; standard channels.

Equation assumptions:

- Pieces commute poorly enough to produce nonzero Trotter error only if the Hamiltonian axis differs, e.g. use H=omega X/2 with damping.

## Registers

- sys: 1 qubits; system qubit holding rho
- anc: 1 qubits; dilation ancilla, starts and is reset to |0> after each factor

## Initial state

sys in a chosen pure state (e.g. |+> or |0>), anc in |0>

## Measurement

If counts are required: measure the system in X, Y, Z bases for Bloch vector; otherwise no measurement and use statevector with partial trace. Mid-circuit ancilla reset is assumed allowed.

## Classical postprocessing

Reconstruct rho=(I+xX+yY+zZ)/2 from expectations, or take the partial trace; compute exp(tL) via the 4x4 matrix exponential of the Liouvillian and compare in trace distance.

## Algorithm steps

1. Choose the instance (rates, t, r) and the decomposition L_1=Hamiltonian, L_2=dephasing, L_3=amplitude damping. (eq_1, eq_5)
2. Pick r from the target eps via the error scaling; use second-order symmetric ordering. (eq_2, eq_3)
3. For each factor in each segment, apply the dilating unitary on sys+anc with anc in |0>, compiled to standard gates (ry, cx, rz); reset anc to |0>. Unitary pieces need no ancilla. (eq_4, eq_5)
4. After r segments, read the reduced density matrix of sys (statevector with ancilla traced out, or Pauli expectation measurements) and compare with exp(tL) rho. (eq_1)

## Assumptions

- Lindblad L with few terms each having analytic exponential
- Ancilla reset between segments is allowed
- Second-order Suzuki
- Per-factor channel synthesis is exact or error much smaller than Trotter error
- Paper's general channel approximation method replaced by exact dilations for Kraus rank <=2 pieces

## Missing information

- Paper's actual decomposition and recombination technique
- Details of the approximation method for arbitrary single-qubit channels
- Exact gate-level circuits and constants
- Rank-3/4 Kraus channels not handled
