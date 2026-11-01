# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Characterize the time-averaged position distribution of a recycled-coin discrete-time quantum walk on the cycle graph C_N as a function of a real memory parameter in [0,8], the initial state, and N mod 4. The abstract does not give the recycled-coin coin operator, so only generic walk and time-averaging background can be written.

Scope: Smallest useful construction: a generic coined discrete-time quantum walk on C_N with a placeholder parameter-dependent coin C(m), plus the time-averaged distribution. Tiny instance assumed: N=4 (N mod 4 = 0) with a single coin qubit. The recycled-coin update rule, the specific coin form, the claimed non-uniform parameter values, and the proved relationship to the other memory-based walk are outside scope.

## Symbols

- $N$: number of vertices of the cycle graph; domain: integer, N>=3
- $m$: memory parameter affecting the coin flip operator; domain: real, 0<=m<=8
- $x$: position on the cycle; domain: {0,...,N-1}
- $c$: coin basis value; domain: {0,1}
- $U(m)$: one-step walk operator, shift times coin; domain: unitary on C^N tensor C^2 (assumed form)
- $C(m)$: parameter-dependent coin operator (unspecified); domain: unitary on C^2 in the simple model; recycled coin may need extra memory
- $S$: conditional shift operator; domain: unitary on C^N tensor C^2
- $\psi_0$: initial state; domain: normalized vector in C^N tensor C^2
- $\bar{P}_T(x)$: time-averaged probability at position x over T steps; domain: [0,1]

## eq_1: Conditional shift on cycle

$$
S\,|x,c\rangle=|x+(-1)^c \bmod N,\;c\rangle
$$

Coin-conditioned move on the cycle, with position arithmetic modulo N.

Provenance: `standard_background`. Standard coined walk on a cycle; the shift convention is an assumption, not from the abstract.

Equation assumptions:

- Coin value 0 moves right and 1 moves left
- Single coin qubit

## eq_2: Walk evolution

$$
|\psi_t\rangle=U(m)^t|\psi_0\rangle,\quad U(m)=S\,(I_N\otimes C(m))
$$

Placeholder evolution with a parameter-dependent coin.

Provenance: `assumption`. The abstract says that the memory parameter affects the coin flip operator but gives no form for it; the recycled-coin dynamics may not be a fixed coin.

Equation assumptions:

- C(m) is a placeholder, not the recycled-coin rule

## eq_3: Position distribution

$$
P_t(x)=\sum_{c\in\{0,1\}}\left|\langle x,c|\psi_t\rangle\right|^2
$$

Probability of finding the walker at x after t steps.

Provenance: `standard_background`. Born rule on the position register.

## eq_4: Time-averaged distribution

$$
\bar{P}_T(x)=\frac{1}{T}\sum_{t=0}^{T-1}P_t(x),\quad \bar{P}(x)=\lim_{T\to\infty}\bar{P}_T(x)
$$

Time-averaged distribution studied in the abstract. The uniform case corresponds to 1/N for every x.

Provenance: `abstract_inferred`. The abstract names the time-averaged distribution as the object of study; the explicit formula is the standard definition.

Abstract evidence: we will consider its time averaged distribution

Equation assumptions:

- Uniform means \bar{P}(x)=1/N

## eq_5: Tiny instance initial state

$$
N=4,\quad |\psi_0\rangle=|0\rangle_{pos}\otimes\frac{|0\rangle+i|1\rangle}{\sqrt2}
$$

Concrete instance chosen for later circuit generation.

Provenance: `assumption`. The abstract says the initial state and N mod 4 matter, so a concrete instance is needed; this one is an arbitrary choice.

Equation assumptions:

- Symmetric coin initial state chosen arbitrarily

## Registers

- pos: 2 qubits for N=4 (ceil(log2 N) in general) qubits; walker position, integer-encoded x in {0,...,N-1}
- coin: 1 qubit qubits; coin; the recycled-coin memory may require extra qubits

## Initial state

|0>_pos tensor (|0>+i|1>)/sqrt2 for the N=4 instance (assumed).

## Measurement

Measure the position register in the computational basis after t steps, with t chosen at random from 0..T-1, to estimate the time-averaged distribution.

## Classical postprocessing

Histogram the outcomes, compare with 1/N, and scan m in [0,8], the initial state and N mod 4.

## Algorithm steps

1. Prepare the initial position and coin state. (eq_5)
2. Apply the placeholder coin C(m) and the conditional shift S repeatedly for t steps. (eq_1, eq_2)
3. Obtain the position distribution at each t and average over t to get the time-averaged distribution, then compare with uniform 1/N. (eq_3, eq_4)

## Assumptions

- The recycled-coin rule is not specified, so a standard coined walk with a parameter-dependent coin is a placeholder
- N=4 and a single coin qubit are chosen as the instance
- Shift convention is arbitrary

## Missing information

- Definition of the recycled-coin model and how the coin is reused
- Explicit form of C(m) and why m lies in [0,8]
- Which parameter values give non-uniform behavior
- Details of the related memory-based quantum walk and the proved relationship
- Results on the effect of the initial state and N mod 4
