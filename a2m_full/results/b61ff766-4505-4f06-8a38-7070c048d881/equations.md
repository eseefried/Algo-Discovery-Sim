# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Model a discrete-time quantum walk (DTQW) of a spin-1/2 coin on a small cyclic lattice with spin dephasing and spatial dephasing, and read out position distribution, spatial coherence length from rho(x,x'), and a discrete Wigner function. The abstract gives no formulas; this is a phenomenological model reconstruction.

Scope: One instance: n=3 position qubits (8 sites, assumed; n=4 is possible if the cap allows), 1 coin qubit, fresh ancillas per step for T<=3 steps (or averaging over sampled random-phase circuits). Computes P(x,t), a coherence length from the reduced density matrix, and a discrete Wigner function classically. Outside scope: fitting to the neutral-atom experiment, the distinction between short- and long-time dephasing as tied to real experimental noise, and the paper's exact Wigner formalism and decoherence parametrization.

## Symbols

- $x$: lattice site index; domain: Z_N, N=2^n
- $T$: number of walk steps; domain: positive integer
- $p_s$: spin dephasing probability per step; domain: [0,1]
- $q$: spatial dephasing probability per step (damping of |x><x'| coherence); domain: [0,1]
- $\rho(x,x')$: position reduced density matrix (coin traced out); domain: complex NxN, Hermitian, trace 1
- $C(d)$: coherence profile, sum over x of |rho(x,x+d)|; domain: nonnegative reals, d in Z_N
- $W(x,k)$: discrete Wigner function; domain: real, x in Z_N, k in Z_N
- $\theta_0$: fixed Z angle on the spin per run for quasi-stationary dephasing; domain: random real, e.g. Gaussian, constant over steps

## eq_1: Step operator

$$
U=S\,(I_x\otimes H),\quad S=\sum_x |x+1\rangle\langle x|\otimes|0\rangle\langle0|+|x-1\rangle\langle x|\otimes|1\rangle\langle1|
$$

Hadamard coin followed by a spin-conditional shift on a cyclic lattice (increment for spin 0, decrement for spin 1); the lattice index is read as an integer from the position qubits, with the least significant bit as qubit 0.

Provenance: `standard_background`. Standard DTQW definition; the abstract names discrete-time quantum walks only.

Equation assumptions:

- Hadamard coin
- cyclic boundary with N=2^n sites

## eq_2: Initial state

$$
|\psi_0\rangle=|x_0\rangle\otimes\frac{|0\rangle+i|1\rangle}{\sqrt2},\quad x_0=N/2
$$

Walker at the center site with a symmetric spin state, prepared with H then S on the coin and X gates on the position register.

Provenance: `assumption`. Chosen as the smallest instance; not stated in the abstract.

Equation assumptions:

- The center site is N/2

## eq_3: Spin dephasing channel

$$
\mathcal{E}_s(\rho)=(1-p_s)\rho+p_s\,(Z_c\otimes I)\rho(Z_c\otimes I)
$$

Per-step spin dephasing, implemented by an ancilla prepared with Ry(2 asin(sqrt(p_s))) and CZ or CX onto the coin, with the ancilla then discarded (fresh per step).

Provenance: `abstract_inferred`. A phase-flip channel is one plausible realization of spin decoherence; the exact form in the paper is unknown.

Abstract evidence: phenomenological model that distinguishes spin and spatial decoherence

Equation assumptions:

- Dephasing is Z-type and Markovian per step

## eq_4: Spatial dephasing channel

$$
\mathcal{E}_x(\rho)=(1-q)\rho+q\,Z_{x,0}\rho Z_{x,0}
$$

Per-step spatial dephasing using a fresh ancilla Ry(2 asin(sqrt(q))) controlling Z on the least significant position qubit. It damps coherences between sites of opposite parity by (1-2q) per step. Other position-bit choices, or Rz, give different spatial damping patterns.

Provenance: `assumption`. A simple unitary-dilation toy model of spatial decoherence; the paper's form is not given.

Equation assumptions:

- Only parity-resolving dephasing is modeled, a limited model of spatial decoherence

## eq_5: Coherence length profile and Wigner function

$$
C(d)=\sum_x|\rho(x,x+d)|,\quad W(x,k)=\sum_{d}\rho(x+d,x-d)\,e^{-2\pi i\,kd/N}
$$

The coherence length is the width of C(d), for example the d at which C(d)/C(0) drops below 1/e. W is a discrete Wigner-type transform, computed classically. For even N, the half-integer subtlety is not handled.

Provenance: `abstract_inferred`. The abstract introduces a coherence length and a discrete Wigner function without formulas; these definitions are proposed.

Abstract evidence: We introduce the concept of coherence length in the discrete-time quantum walk, which quantifies the range of spatial coherences.

Equation assumptions:

- Cyclic indices modulo N
- Width definition is a choice

## Registers

- pos: n (3 assumed) qubits; walker position, little-endian integer, qubit 0 is the least significant bit
- coin: 1 qubits; spin qubit
- anc: 2 per step (one spin, one spatial) if fresh per step qubits; environment for the dephasing dilation, traced out

## Initial state

pos set to N/2 by X on the top position qubit; coin in (|0>+i|1>)/sqrt2 via H then S.

## Measurement

Measure pos in the computational basis for P(x,T). Coherences come from the statevector or tomography, with no measurement in unitary or statevector tasks.

## Classical postprocessing

Compute P(x,T), its variance, C(d), the coherence length and W(x,k). Fit p_s and q by matching to simulated variance and shape. Average over sampled theta_0 for quasi-stationary dephasing.

## Algorithm steps

1. Prepare the initial state of eq_2. (eq_2)
2. For each step: apply H to the coin, then the conditional increment/decrement (MCX ripple, with the coin as control for increment and an X-conjugated coin for decrement). (eq_1)
3. After each shift, apply the spin dephasing dilation with a fresh ancilla (or for quasi-stationary dephasing a fixed Rz(theta_0) on the coin per run, averaged over runs). (eq_3)
4. Apply the spatial dephasing dilation with a fresh ancilla. (eq_4)
5. Obtain rho(x,x') from the statevector by tracing out the coin and ancillas, then compute C(d) and W(x,k) classically. (eq_5)

## Assumptions

- The abstract's experiment is modeled as a qubit-coin cyclic walk.
- Ancillas are fresh per step, so the qubit count grows by 2T; keep T small to stay under the cap.
- Fitting is limited to simulation.
- The walk length must be short enough to avoid wrap-around artifacts on the cyclic lattice.

## Missing information

- The paper's actual decoherence model and parameterization
- The paper's Wigner function definition
- The coin angle and initial state used experimentally
- The qubit cap and query budget (no black box is involved here)
