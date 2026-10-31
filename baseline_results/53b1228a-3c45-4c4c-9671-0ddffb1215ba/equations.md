# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Model a one-dimensional discrete-time (coined) quantum walk subject to per-step decoherence, with a phenomenological distinction between spin (coin) decoherence and spatial (position) decoherence, and extract the position distribution from which the decoherence per step can be inferred.

Scope: One smallest useful construction: a 1D coined quantum walk on a cyclic lattice of N=2^n sites (n=3, N=8) with a single coin qubit, a Hadamard coin, a conditional shift, and a phenomenological per-step channel composed of coin (spin) dephasing with probability p_s and position dephasing with probability p_x. Tiny instance: initial state |x=0>|up>, T=3 steps (no wrap-around), measure position. Outside scope: the atom-in-optical-lattice experimental mechanisms, the short-time versus long-time (quasi-stationary) spin-dephasing distinction, the coherence-length definition, the discrete Wigner-function formalism and momentum-space analysis, and all measured numerical values.

## Symbols

- $n$: number of position qubits; lattice has N=2^n sites; domain: positive integer (instance: n=3)
- $x$: lattice site index, encoded as the integer x mod N in the position register (binary, qubit 0 least significant); domain: \{0,\dots,N-1\} with site -k identified with N-k
- $c$: coin (spin) state; domain: \{\uparrow,\downarrow\} \equiv \{0,1\}
- $C$: coin operator acting on the coin qubit; domain: 2x2 unitary
- $S$: spin-dependent shift operator; domain: unitary on \mathbb{C}^{N}\otimes\mathbb{C}^{2}
- $W$: one unitary walk step; domain: unitary on \mathbb{C}^{N}\otimes\mathbb{C}^{2}
- $p_s$: spin (coin) decoherence probability per step; domain: [0,1]
- $p_x$: spatial (position) decoherence probability per step; domain: [0,1]
- $\rho_t$: density operator of the walker after t steps; domain: positive unit-trace operator on \mathbb{C}^{N}\otimes\mathbb{C}^{2}
- $P(x,t)$: probability of finding the walker at site x after t steps; domain: [0,1], sums to 1 over x
- $T$: total number of walk steps; domain: non-negative integer (instance: T=3)
- $\sigma_z$: Pauli Z on the coin qubit; domain: 2x2 Hermitian unitary

## eq_1: Coin operator (Hadamard coin)

$$
C = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
$$

Balanced coin applied to the spin qubit before each shift.

Provenance: `assumption`. The abstract does not specify the coin; the Hadamard coin is the simplest balanced choice for a minimal instance.

Equation assumptions:

- Hadamard coin chosen; the experiment's actual coin (e.g. a microwave pi/2 pulse with some phase) may differ.

## eq_2: Spin-dependent shift

$$
S = \sum_{x=0}^{N-1} \big( |x+1 \bmod N\rangle\langle x| \otimes |\uparrow\rangle\langle\uparrow| + |x-1 \bmod N\rangle\langle x| \otimes |\downarrow\rangle\langle\downarrow| \big)
$$

Moves the walker one site right if the coin is up and one site left if down; arithmetic is modulo N on the cyclic register.

Provenance: `standard_background`. Standard definition of the conditional shift in a discrete-time coined quantum walk; cyclic boundary is an encoding convenience.

Equation assumptions:

- Cyclic lattice of N=2^n sites; for T < N/2 starting from x=0 no wrap-around occurs.

## eq_3: Unitary walk step

$$
W = S\,(\mathbb{1}_N \otimes C)
$$

One coherent step of the discrete-time quantum walk.

Provenance: `standard_background`. Standard coined-walk step; the abstract names discrete-time quantum walks without giving this relation explicitly.

## eq_4: Spin decoherence channel (per step)

$$
\mathcal{E}_s(\rho) = (1-p_s)\,\rho + p_s\,(\mathbb{1}_N\otimes\sigma_z)\,\rho\,(\mathbb{1}_N\otimes\sigma_z)
$$

Phenomenological dephasing of the coin with probability p_s per step; it destroys coin coherences while leaving populations and position unchanged.

Provenance: `abstract_inferred`. The abstract states a phenomenological per-step model separating spin decoherence; a coin dephasing channel is the simplest such model, but its exact form in the paper is not given in the abstract.

Abstract evidence: a phenomenological model that distinguishes spin and spatial decoherence

Equation assumptions:

- Dephasing (not depolarizing or amplitude damping) form assumed; memoryless (Markovian) per-step application assumed, which does not capture the quasi-stationary dephasing discussed in the abstract.

## eq_5: Spatial decoherence channel (per step)

$$
\mathcal{E}_x(\rho) = (1-p_x)\,\rho + p_x \sum_{x=0}^{N-1} (|x\rangle\langle x|\otimes\mathbb{1}_2)\,\rho\,(|x\rangle\langle x|\otimes\mathbb{1}_2)
$$

Phenomenological position dephasing with probability p_x per step; it destroys spatial coherences between different sites while preserving the position distribution.

Provenance: `abstract_inferred`. The abstract introduces spatial decoherence as a distinct mechanism; position dephasing is the minimal model, but the paper's precise form is not available here.

Abstract evidence: a phenomenological model that distinguishes spin and spatial decoherence

Equation assumptions:

- Pure position dephasing assumed; alternative spatial mechanisms (e.g. random site hopping) are not modelled.

## eq_6: Full decoherent step and position distribution

$$
\rho_{t+1} = \mathcal{E}_x\big(\mathcal{E}_s(W\rho_t W^\dagger)\big), \qquad P(x,t) = \mathrm{Tr}\big[(|x\rangle\langle x|\otimes\mathbb{1}_2)\,\rho_t\big]
$$

Iterated open-system map for the walk and the measured spatial distribution from which the decoherence per step is estimated.

Provenance: `abstract_inferred`. The abstract states that decoherence per step is extracted from measured spatial distributions, implying a per-step channel composed with the unitary step and a position-probability observable.

Abstract evidence: From the measured spatial distributions, we determine with good precision the amount of decoherence per step

Equation assumptions:

- Order of channels within a step (unitary, then spin, then spatial dephasing) is a choice; the two dephasing channels commute with each other but not with W.

## eq_7: Ballistic versus diffusive spreading (background diagnostic)

$$
\sigma^2(t) = \sum_x x^2 P(x,t) - \Big(\sum_x x P(x,t)\Big)^2, \qquad \sigma^2(t) \propto t^2 \ (\text{ballistic}),\quad \sigma^2(t) \propto t \ (\text{diffusive})
$$

Variance of the position distribution and its asymptotic scaling; the abstract warns this alone does not indicate the coherence range.

Provenance: `standard_background`. Standard characterization of quantum-walk spreading; included because the abstract discusses ballistic versus diffusive expansion. Scalings are asymptotic proportionalities, not exact equalities, and x is interpreted as a signed integer (sites x>N/2 mapped to x-N).

Equation assumptions:

- Signed-integer reinterpretation of the modular position register is required for the variance to be meaningful.

## Registers

- position: n = 3 qubits qubits; Encodes the lattice site x mod 8 in binary (qubit 0 least significant); shift is increment/decrement mod 8 conditioned on the coin.
- coin: 1 qubit qubits; Spin (internal) degree of freedom; |0> = up moves right, |1> = down moves left.

## Initial state

|x=0>_{position} ⊗ |up>_{coin} = |000>|0> (pure state, rho_0 = |psi_0><psi_0|). Assumption: localized start with a definite coin state.

## Measurement

Computational-basis measurement of the n position qubits after T steps; repeated shots estimate P(x,T). The coin qubit may be traced out (not measured).

## Classical postprocessing

Reinterpret measured bitstrings as signed sites (x > N/2 -> x - N), build the histogram P(x,T), compute the variance per eq_7, and fit the simulated model (eq_6) with free parameters p_s and p_x to the measured distribution to estimate decoherence per step. The paper's specific fitting procedure is not available from the abstract.

## Algorithm steps

1. Prepare the position register in |000> and the coin in |0>. (no equation reference)
2. Repeat for t = 1..T (T=3): apply the coin operator C to the coin qubit. (eq_1)
3. Apply the conditional shift S: controlled increment mod N on the position register if coin is |0>, controlled decrement mod N if coin is |1>. (eq_2, eq_3)
4. Apply the phenomenological spin dephasing channel with probability p_s (e.g. by a classically randomized Z gate on the coin, or an ancilla-based Kraus implementation). (eq_4)
5. Apply the phenomenological spatial dephasing channel with probability p_x (e.g. randomized phase kicks diagonal in the position basis, or an ancilla-based implementation). (eq_5, eq_6)
6. After T steps measure the position register in the computational basis to sample P(x,T). (eq_6)

## Assumptions

- No experiment scope supplied; a minimal 1D coined walk on 8 cyclic sites with 3 steps was chosen as the instance.
- Hadamard coin and localized initial state are choices, not taken from the abstract.
- Spin and spatial decoherence are modelled as memoryless per-step dephasing channels; this is the simplest phenomenological model consistent with the abstract's description, not a verified reproduction of the paper's model.
- Channel ordering within a step (W, then spin, then spatial dephasing) is a choice.

## Missing information

- Exact form of the paper's phenomenological spin and spatial decoherence model and its parametrization.
- The actual coin operation and lattice/shift implementation used in the neutral-atom experiment.
- Definition of the coherence length for the discrete-time quantum walk.
- Model distinguishing short-time from long-time (quasi-stationary) spin dephasing and how it affects spatial coherences.
- Definition of the discrete analogue of the Wigner function and the momentum-space analysis.
- Measured decoherence-per-step values and the fitting procedure used to extract them.
