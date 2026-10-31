# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Reconstruct, from the abstract alone, the discrete-time lazy quantum walk on the integer line with a three-dimensional coin acted on by the 3x3 Discrete Fourier Transform (DFT) coin operator, its position probability distribution P_t(x), the n-th moment M_n(t) claimed to scale as O(t^n), and a measurable proxy for the paper's 'occupancy number' and 'occupancy rate' statistics.

Scope: Smallest useful construction (chosen here as an assumption, since no experiment_scope was supplied): a lazy quantum walk on a finite line segment of 8 positions (3 position qubits, integer encoding x -> x+4 so that x in {-4,...,3}), coin register of 2 qubits embedding the 3 coin states {L,S,R} = {|00>,|01>,|10>} with |11> unused, DFT_3 coin embedded as F_3 (+) 1, t = 3 steps starting at x = 0 so that no boundary wrap-around occurs. Target quantities: P_t(x), M_n(t) for n = 1,2, and an occupancy number/rate computed with an assumed threshold rule. Outside scope: the proof that moments are O(t^n) in general, the continuous-time-limit construction of Childs, the comparison of concentration intervals with the Hadamard walk, the paper's exact definition of occupancy number/rate, and comparisons with classical and lazy classical walks.

## Symbols

- $x$: walker position on the integer line; domain: \mathbb{Z} (truncated to \{-4,\dots,3\} in the scoped instance)
- $c$: coin state index: 0 = move left, 1 = stay (lazy), 2 = move right; domain: \{0,1,2\}
- $t$: number of walk steps; domain: \mathbb{N}_0 (t = 3 in the scoped instance)
- $\psi_{x,c}(t)$: amplitude of the walker at position x with coin state c after t steps; domain: \mathbb{C}
- $F_3$: 3x3 Discrete Fourier Transform coin operator; domain: U(3)
- $\omega$: primitive cube root of unity e^{2\pi i/3}; domain: \mathbb{C}
- $S$: coin-conditioned shift operator (left / stay / right); domain: unitary on position (x) coin space
- $U$: single-step lazy quantum walk unitary; domain: unitary on position (x) coin space
- $P_t(x)$: probability of finding the walker at position x after t steps; domain: [0,1]
- $M_n(t)$: n-th moment of the position distribution after t steps; domain: \mathbb{R}
- $R_t$: range of the walk after t steps (positions reachable with nonzero probability); domain: finite subset of \mathbb{Z}
- $\theta_t$: threshold defining a 'relatively high' probability (assumed definition); domain: (0,1]
- $N_{occ}(t)$: occupancy number: count of positions in the range with probability at least the threshold (assumed definition); domain: \mathbb{N}_0
- $\rho_{occ}(t)$: occupancy rate: occupancy number divided by size of the range (assumed definition); domain: [0,1]

## eq_1: Walker state and DFT coin operator

$$
|\psi(t)\rangle=\sum_{x\in\mathbb{Z}}\sum_{c=0}^{2}\psi_{x,c}(t)\,|x\rangle\otimes|c\rangle,\qquad F_3=\frac{1}{\sqrt{3}}\begin{pmatrix}1&1&1\\1&\omega&\omega^{2}\\1&\omega^{2}&\omega\end{pmatrix},\quad \omega=e^{2\pi i/3}
$$

The lazy walk uses a three-dimensional coin (left, stay, right); the coin operator is the 3x3 unitary DFT matrix.

Provenance: `abstract_inferred`. The abstract names the DFT coin; a lazy walk on the line has three coin outcomes, so the coin is the 3x3 DFT. The specific matrix (ordering of rows/columns, sign of the exponent) is the standard DFT and is not confirmed by the abstract.

Abstract evidence: the lazy quantum walk with DFT (Discrete Fourier Transform) coin operator

Equation assumptions:

- Coin dimension is 3 (left/stay/right) as in Childs' lazy walk on the line
- Standard DFT sign convention \omega=e^{+2\pi i/3}

## eq_2: Lazy shift operator and one-step unitary

$$
S=\sum_{x}\Big(|x-1\rangle\langle x|\otimes|0\rangle\langle 0|+|x\rangle\langle x|\otimes|1\rangle\langle 1|+|x+1\rangle\langle x|\otimes|2\rangle\langle 2|\Big),\qquad U=S\,(I\otimes F_3)
$$

Coin state 0 moves the walker left, state 1 leaves it in place (the 'lazy' option), state 2 moves it right; one step is coin followed by shift.

Provenance: `standard_background`. Standard definition of a three-state (lazy) discrete-time quantum walk on the line; the abstract only names lazy quantum walks and does not display this operator.

Equation assumptions:

- Assignment of coin indices to directions is a convention
- Coin is applied before the shift

## eq_3: Evolution and position distribution

$$
|\psi(t)\rangle=U^{t}|\psi(0)\rangle,\qquad P_t(x)=\sum_{c=0}^{2}\big|\psi_{x,c}(t)\big|^{2},\qquad \sum_{x}P_t(x)=1
$$

Repeated application of the step unitary; the probability distribution over positions is obtained by tracing out the coin.

Provenance: `standard_background`. Standard discrete-time quantum walk evolution; required to define the distribution whose moments and occupancy the abstract discusses.

## eq_4: n-th moment scaling

$$
M_n(t)=\sum_{x}x^{n}P_t(x)=O(t^{n})
$$

The n-th moment of the lazy-walk position distribution grows at most as t^n, matching the ballistic scaling of ordinary (non-lazy) quantum walks.

Provenance: `abstract_explicit`. Stated directly in the abstract; the definition of M_n(t) as the raw moment about x=0 is the standard one and is an interpretation.

Abstract evidence: lazy quantum walks have $O(t^{n})$ order of the n-th moment of the corresponding probability distribution, which is the same as that for normal quantum walks

Equation assumptions:

- Moment taken about the origin (raw moment) rather than a central moment; the abstract does not specify
- Asymptotic statement; not verifiable from the t=3 scoped instance

## eq_5: Assumed occupancy number and occupancy rate

$$
R_t=\{x: P_t(x)>0\},\qquad N_{occ}(t)=\big|\{x\in R_t: P_t(x)\ge\theta_t\}\big|,\qquad \rho_{occ}(t)=\frac{N_{occ}(t)}{|R_t|},\qquad \theta_t=\frac{1}{|R_t|}\ (\text{assumed})
$$

A proposed operational definition: positions in the range whose probability is at least a 'relatively high' threshold are counted; the rate normalises by the range size. The threshold 1/|R_t| (the uniform-distribution value) is an assumption.

Provenance: `assumption`. The abstract introduces occupancy number and occupancy rate as measures of 'the extent to which the walk has a (relatively) high probability at every position in its range' but gives no formula; this is a plausible proxy, explicitly not the paper's definition.

Equation assumptions:

- Threshold choice \theta_t = 1/|R_t| is invented here for concreteness and may differ from the paper
- Range defined as support of P_t; the paper may use the kinematic range \{-t,\dots,t\}

## eq_6: Scoped instance: encoding and initial state

$$
|x\rangle_{pos}\equiv|x+4 \bmod 8\rangle_{3\ \text{qubits}},\quad |c\rangle_{coin}\in\{|00\rangle,|01\rangle,|10\rangle\},\quad \tilde F=F_3\oplus 1,\qquad |\psi(0)\rangle=|x=0\rangle\otimes|c=1\rangle,\quad t=3
$$

Position stored as an unsigned 3-bit integer with offset 4; the 3-state coin is embedded in 2 qubits with |11> inert under the coin; walker starts at the origin in the 'stay' coin state and takes 3 steps (|x| <= 3, so no wrap-around occurs and the modular shift equals the integer shift).

Provenance: `assumption`. Smallest explicit instance chosen for a later circuit stage; the abstract specifies no sizes, initial state, or encoding.

Equation assumptions:

- Initial coin state |1> (stay) is a choice; symmetric superpositions are equally plausible
- Shift implemented as modular increment/decrement on 3 qubits; exact for t <= 3 from x = 0
- Coin state |11> never becomes populated because \tilde F and S act trivially on it and the initial state has no |11> component

## Registers

- pos: 3 qubits; Position register storing x+4 as an unsigned integer (x in {-4,...,3}); qubit 0 is the least significant bit.
- coin: 2 qubits; Coin register embedding the three lazy-walk coin states: |00> = left, |01> = stay, |10> = right; |11> unused.

## Initial state

|pos = 4> (i.e. x = 0, bitstring 100) tensor |coin = 01> (stay), per eq_6.

## Measurement

Computational-basis measurement of the 3 pos qubits (coin register may be discarded or measured and marginalised). Decode x = (measured integer) - 4. Repeat shots to estimate P_t(x) for t = 3.

## Classical postprocessing

From the estimated P_t(x): compute M_1(t) and M_2(t) via eq_4; determine the range R_t as the set of positions with (statistically) nonzero probability, and compute the assumed occupancy number N_occ(t) and occupancy rate rho_occ(t) via eq_5 with threshold theta_t = 1/|R_t|. Optionally compare with a classical lazy random walk (probabilities 1/3 left/stay/right) computed exactly.

## Algorithm steps

1. Prepare the initial state: set pos to the encoding of x = 0 and coin to |01>. (eq_6)
2. Apply the embedded DFT coin \tilde F = F_3 (+) 1 to the coin register. (eq_1, eq_6)
3. Apply the coin-conditioned shift: controlled on coin = |00> apply a modular decrement to pos, controlled on coin = |10> apply a modular increment to pos, do nothing for coin = |01>. (eq_2, eq_6)
4. Repeat the coin and shift steps for a total of t = 3 iterations, realising U^t. (eq_3)
5. Measure the position register in the computational basis; repeat the whole circuit to estimate P_t(x). (eq_3)

## Assumptions

- No experiment_scope was provided, so a single smallest instance (8 positions, 3 steps, origin start, 'stay' initial coin) was chosen as an assumption.
- The coin is the 3x3 DFT with the standard phase convention; coin applied before shift; coin index-to-direction assignment is conventional.
- Occupancy number/rate definitions in eq_5 are a proposed proxy, not the paper's definitions.
- Moments are raw moments about the origin.
- Finite register with modular arithmetic is exact for the chosen t because the walker never reaches the boundary.

## Missing information

- The paper's precise definitions of occupancy number and occupancy rate (threshold rule, definition of 'range').
- The initial state (position and coin) used in the paper's analysis and comparisons.
- Whether the 'lazy quantum walk' uses exactly the DFT_3 coin or Childs' parameterised lazy coin, and any laziness parameter.
- Exact statement and proof of the O(t^n) moment result and the 'concentrated interval' comparison with the Hadamard walk.
- Any numerical values (occupancy rates, step counts) reported in the paper for quantum, classical and lazy classical walks.
