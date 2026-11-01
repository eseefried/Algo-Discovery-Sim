# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Tulsi-type quantum search on N=2^n items with one marked item w and one control (auxiliary) qubit, modified by projective Z-basis measurement of the control every tau iterations; study success probability P(w), control-search correlations, and the scaling of the optimal iteration count k* with N.

Scope: Smallest useful instance: n=3 search qubits (N=8) plus 1 control qubit (4 qubits total), marked item w fixed, a free fixed angle theta, tau in {1,2,3,none}. Density-matrix (outcome-averaged) or trajectory simulation of k iterations; the n=3..8 scaling fit, MI and CCM computation are described but the exact paper definitions and angle choice are outside the scope.

## Symbols

- $n$: number of search qubits; domain: integer >=1
- $N$: search space size 2^n; domain: integer
- $w$: marked item; domain: {0,...,N-1}
- $\theta$: angular parameter of the control rotation (free, replaces the standard N-dependent choice); domain: real in (0,\pi)
- $\tau$: number of iterations between control measurements; domain: positive integer, or infinity for no measurement
- $k$: total number of iterations; domain: nonnegative integer
- $P_k(w)$: probability of measuring w on the search register after k iterations; domain: [0,1]
- $k^*$: iteration count maximizing P_k(w); domain: positive integer
- $\alpha$: fitted exponent in k^* ~ N^alpha; domain: real
- $I(S:C)$: mutual information between search register S and control C; domain: nonnegative real

## eq_1: Initial state

$$
|\psi_0\rangle=H^{\otimes n}|0\rangle_S\otimes|+\rangle_C=|s\rangle|+\rangle,\quad |s\rangle=N^{-1/2}\sum_x|x\rangle
$$

Uniform superposition on search register; control starts in |+> (|0> is the alternative).

Provenance: `assumption`. Sketch suggests |+> or |0>; the choice is not given in the abstract.

Equation assumptions:

- Control initial state |+> chosen for the smallest instance

## eq_2: Controlled iterate (proposed form)

$$
G_\theta=\big(D\otimes I_C\big)\,\big(R_y^{(C)}(\theta)\,\cdot\,\Lambda_C(O_w)\big),\quad O_w=I-2|w\rangle\langle w|,\quad D=2|s\rangle\langle s|-I
$$

One step: oracle phase flip on w applied only when control is |1> (a single query per step), a control rotation Ry(theta), then Grover diffusion on the search register. This is a simplified stand-in for Tulsi's exact construction.

Provenance: `assumption`. The abstract only says Tulsi's algorithm is modified with a different angular parameter; the precise Tulsi operators are not given, so this is a proposed construction.

Equation assumptions:

- Oracle controlled on c=1
- Diffusion acts on the search register only
- Gate order and the exact role of theta are guesses

## eq_3: Measured evolution

$$
\rho_{k+1}=G_\theta\rho_kG_\theta^\dagger\ \text{if }\tau\nmid(k+1);\quad \rho_{k+1}=\sum_{m\in\{0,1\}}(I\otimes|m\rangle\langle m|)\,G_\theta\rho_kG_\theta^\dagger\,(I\otimes|m\rangle\langle m|)\ \text{if }\tau\mid(k+1)
$$

Control dephasing in the Z basis every tau steps without reset; outcome-averaged state.

Provenance: `abstract_inferred`. Intermediate control measurements with time lapse tau are stated; the no-reset, outcome-averaged form is an assumed implementation.

Abstract evidence: intermediate measurements of the control

Equation assumptions:

- No reset after measurement
- Averaging over outcomes

## eq_4: Success probability

$$
P_k(w)=\mathrm{Tr}\big[(|w\rangle\langle w|_S\otimes I_C)\rho_k\big]
$$

Probability of reading the marked item from the search register.

Provenance: `standard_background`. Standard definition of success probability.

## eq_5: Mutual information

$$
I(S:C)=S_{vN}(\rho_S)+S_{vN}(\rho_C)-S_{vN}(\rho_{SC}),\quad S_{vN}(\rho)=-\mathrm{Tr}\,\rho\log_2\rho
$$

Correlation between search and control registers, computed from reduced density matrices.

Provenance: `standard_background`. The abstract names Mutual Information; this is the standard definition. The Cumulative Correlation Measure definition is not given and is not reproduced here.

Equation assumptions:

- Base-2 logarithm

## eq_6: Order estimate

$$
k^*(N)=\arg\max_k P_k(w),\qquad \log k^*\approx\alpha\log N+c
$$

Empirical order: linear fit of log k* against log N over n=3..8. Expected alpha near 1/2 without measurement and near 1 for tau=1.

Provenance: `abstract_inferred`. The abstract states O(N) when measuring every step; the fit procedure is an assumed way to estimate the order.

Abstract evidence: became of order $O(N)$ (classical brute force search) when the measurement is taken in every step

Equation assumptions:

- Single marked item
- Fit over n=3..8 only

## Registers

- S: n qubits; search register, qubit i holds bit i of x (little-endian), x=sum_i x_i 2^i
- C: 1 qubits; control/auxiliary qubit, measured in Z every tau steps

## Initial state

|s>_S|+>_C

## Measurement

Final Z measurement of the n search qubits (counts, bits reversed per Qiskit little-endian) to estimate P(w); the control is measured mid-circuit only at multiples of tau. For statevector or density-matrix analysis, use the averaged state instead of counts.

## Classical postprocessing

Histogram frequency of w gives P(w); argmax over k gives k*; least-squares fit of log k* vs log N gives alpha; MI from the reduced density matrices.

## Algorithm steps

1. Prepare H on all S qubits and the control in |+>. (eq_1)
2. Repeat for k=1..K: apply G_theta (one oracle query per iteration); after every tau-th iteration measure C in Z (dephase or sample a trajectory, no reset). (eq_2, eq_3)
3. Record P_k(w) at each k for each tau and the no-measurement case; compute I(S:C) from the reduced states. (eq_4, eq_5)
4. For n=3..8 find k* per tau and fit alpha. (eq_6)

## Assumptions

- Single marked item
- Control is the auxiliary qubit, Z-measured, not reset
- Phase oracle controlled on control qubit
- theta is a fixed free parameter, value not given
- Small instance n=3 as the smallest construction

## Missing information

- Exact Tulsi operators and the standard angular parameter
- The paper's specific alternative choice of theta
- Definition of Cumulative Correlation Measure
- Tested values of tau and the range of k
- Whether the measurement outcome is reset or kept
