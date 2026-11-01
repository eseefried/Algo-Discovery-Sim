# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Compute the time-averaged position distribution of a discrete-time coined quantum walk on the N-cycle with a one-qubit memory register coupled to the coin (an assumed model of the recycled-coin walk), and compare it with the uniform distribution via total variation distance, for small N and a grid of memory parameter p in [0,8].

Scope: Single smallest instance: N=4 (2 position qubits, 1 coin, 1 memory = 4 qubits), initial state |x=0>|coin=0>|mem=0>, an assumed coin unitary C(p) built from ry(pi p/8) and cx, T steps simulated exactly by statevector, probabilities averaged classically over t=0..T-1. Extensions to N=5..8, other initial states and the Fourier block analysis are listed but not required. The exact recycled-coin operator of the paper and the equivalence proof with the other memory walk are outside scope.

## Symbols

- $N$: cycle size; domain: integer, 4<=N<=8
- $p$: memory parameter; domain: real in [0,8]
- $\theta$: rotation angle derived from p (assumed linear map); domain: [0,\pi]
- $C(p)$: assumed 4x4 unitary on (coin,memory); domain: U(4)
- $S$: coin-controlled shift on position: |x,c> -> |x+(-1)^c mod N, c>; domain: unitary on N*2 dim
- $U$: one-step operator S(I_pos⊗C(p)) on position,coin,memory; domain: unitary on 4N dim
- $T$: number of averaged time steps; domain: positive integer, e.g. 64
- $P_t(x)$: position marginal probability after t steps; domain: [0,1]
- $\bar P(x)$: time-averaged position distribution; domain: [0,1]
- $TV$: total variation distance from uniform; domain: [0,1]
- $U(k)$: 4x4 Fourier-momentum block of U; domain: U(4)

## eq_1: Assumed angle map

$$
\theta=\pi p/8
$$

Maps the memory parameter p in [0,8] to a rotation angle used by ry in C(p).

Provenance: `assumption`. Abstract only says p is a real number between zero and eight affecting the coin operator; the linear map is a proposed choice.

Equation assumptions:

- Linear map; the true paper's coin dependence on p may differ

## eq_2: Assumed coin-memory step

$$
C(p)=\mathrm{SWAP}_{c,m}\,\mathrm{CX}_{m\to c}\,(R_y(\theta)\otimes I)
$$

Illustrative coin unitary: rotate the coin, couple to memory by CX, then swap to recycle the coin into memory.

Provenance: `assumption`. Sketch suggests ry, cx and a swap-like recycling; exact form is not given by the abstract.

Equation assumptions:

- Gate order and placement of rotation are a guess

## eq_3: Walk step and evolution

$$
U=S\,(I_x\otimes C(p)),\quad |\psi_t\rangle=U^t|\psi_0\rangle,\quad |\psi_0\rangle=|0\rangle_x|0\rangle_c|0\rangle_m
$$

Coined walk with the shift conditioned on the coin qubit.

Provenance: `standard_background`. Standard coined discrete-time walk structure on a cycle.

Equation assumptions:

- Shift +1 for coin 0, -1 for coin 1, modulo N
- Initial state localized at position 0

## eq_4: Time-averaged distribution

$$
P_t(x)=\sum_{c,m}|\langle x,c,m|\psi_t\rangle|^2,\quad \bar P(x)=\frac1T\sum_{t=0}^{T-1}P_t(x)
$$

Position marginal and its classical average over steps.

Provenance: `abstract_inferred`. The abstract names the time-averaged distribution as the studied quantity; the finite-T average is an implementation choice.

Abstract evidence: we will consider its time averaged distribution

Equation assumptions:

- Finite T approximates the infinite-time limit

## eq_5: Deviation from uniform

$$
TV=\tfrac12\sum_{x=0}^{N-1}\left|\bar P(x)-1/N\right|
$$

Scalar measure of non-uniform behavior to scan over p, N and initial states.

Provenance: `abstract_inferred`. Needs a quantitative non-uniformity metric; TV is the chosen one.

Abstract evidence: only a few produce non-uniform behavior

Equation assumptions:

- TV distance is the metric

## eq_6: Fourier block decomposition

$$
U\cong\bigoplus_{k=0}^{N-1}U(k),\quad U(k)=D(k)\,C(p),\quad D(k)=\mathrm{diag}(e^{2\pi i k/N},e^{-2\pi i k/N})_c\otimes I_m
$$

Translation invariance gives 4x4 blocks in momentum space; eigenphase degeneracies across k explain lack of dephasing.

Provenance: `standard_background`. Standard Fourier analysis of translation-invariant walks; applies to the assumed C(p).

Equation assumptions:

- Shift sign convention matches eq_3

## Registers

- pos: ceil(log2 N) (2 for N=4, 3 for N=8) qubits; walker position, little-endian integer x
- coin: 1 qubits; direction qubit
- mem: 1 qubits; memory qubit holding recycled coin

## Initial state

|0>_pos|0>_coin|0>_mem (product state at position 0); other coin/memory product states are variations

## Measurement

No measurement in the exact simulation: statevector probabilities are marginalized over coin and memory. If counts are required, measure only pos qubits (bit i of the key from the right is pos qubit i).

## Classical postprocessing

Average P_t over t, compute TV from uniform, scan p, N and initial state, and identify the few p values with non-vanishing TV.

## Algorithm steps

1. Prepare initial state; for each t from 0 to T-1 compute P_t(x) from the statevector, then apply one step U (C(p) on coin,mem followed by coin-controlled increment/decrement on pos, e.g. QFT adder or modular incrementer; for N=4 use a mod-4 incrementer from standard gates). (eq_1, eq_2, eq_3)
2. Average the marginals over t classically and compute TV against uniform; scan p grid in [0,8], initial states, and N=4..8. (eq_4, eq_5)
3. Optionally diagonalize U(k) for each k to check eigenphase degeneracy at special p. (eq_6)

## Assumptions

- Memory is one qubit and C(p) is the guessed form of eq_2
- Linear map of p to angle
- Only N<=8 for the qubit cap; N non-power-of-two needs a modular incrementer on a larger register with unused states left invariant
- Time average taken over finite T using exact simulation instead of a phase-estimation time register
- Initial state localized at position 0

## Missing information

- Actual recycled-coin coin operator and its dependence on p
- Exact definition of the memory parameter range 0 to 8
- Definition of the other memory-based walk and the proven relation
- Which p values give non-uniform behavior
- Initial states studied
