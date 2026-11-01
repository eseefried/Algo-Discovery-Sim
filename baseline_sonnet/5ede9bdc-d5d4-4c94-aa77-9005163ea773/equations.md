# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Phenomenological modelling of spin and spatial decoherence in a 1D discrete-time quantum walk (neutral atoms in an optical lattice), with decoherence per step inferred from position distributions.

Scope: Smallest useful construction: a 1D Hadamard-coin discrete-time quantum walk with a generic per-step spin dephasing channel (probability p) and spatial dephasing channel (probability q) acting on the density matrix. Excluded: the paper's specific decoherence model, fitting procedure, quasi-stationary vs. short-time dephasing distinctions, coherence length definition, discrete Wigner function formalism, and experimental parameters.

## Symbols

- $x$: lattice site position; domain: integers
- $s$: spin (coin) basis state; domain: {\uparrow,\downarrow}
- $\rho_t$: density matrix of walker after t steps; domain: positive semidefinite, trace 1, on H_spin ⊗ H_pos
- $C$: coin operator (Hadamard assumed); domain: 2x2 unitary
- $S$: spin-dependent shift operator; domain: unitary on H_spin ⊗ H_pos
- $p$: spin dephasing probability per step; domain: [0,1]
- $q$: spatial dephasing probability per step; domain: [0,1]
- $P_t(x)$: position distribution after t steps; domain: [0,1], sums to 1 over x

## eq_1: Unitary step

$$
U=S\,(C\otimes \mathbb{1}),\quad S=\sum_{x}\left(|\uparrow\rangle\langle\uparrow|\otimes|x+1\rangle\langle x|+|\downarrow\rangle\langle\downarrow|\otimes|x-1\rangle\langle x|\right),\quad C=\tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}
$$

Standard coin-then-shift discrete-time quantum walk step with an assumed Hadamard coin.

Provenance: `standard_background`. Textbook definition of a discrete-time quantum walk; the abstract does not give the coin or shift.

Equation assumptions:

- Hadamard coin
- 1D lattice

## eq_2: Spin dephasing channel

$$
\mathcal{E}_s(\rho)=(1-p)\rho+p\,(\sigma_z\otimes\mathbb{1})\rho(\sigma_z\otimes\mathbb{1})
$$

Phenomenological spin dephasing applied each step with probability p.

Provenance: `assumption`. The abstract mentions a phenomenological spin-decoherence model but not its form; the phase-flip channel is a proposed stand-in.

Equation assumptions:

- Phase-flip (σ_z) channel is a stand-in for the paper's model

## eq_3: Spatial dephasing channel

$$
\mathcal{E}_x(\rho)=(1-q)\rho+q\,(\mathbb{1}\otimes Z_x)\rho(\mathbb{1}\otimes Z_x),\quad Z_x=\sum_x (-1)^x|x\rangle\langle x|
$$

Phenomenological spatial dephasing, which damps coherences between neighbouring sites.

Provenance: `assumption`. The abstract distinguishes spatial decoherence but does not specify its form; this is a proposed simple instance.

Equation assumptions:

- Parity-dependent phase flip as a stand-in for spatial decoherence

## eq_4: Decohered evolution

$$
\rho_{t+1}=\mathcal{E}_x\!\left(\mathcal{E}_s\!\left(U\rho_t U^\dagger\right)\right)
$$

One step of the walk with decoherence after the unitary.

Provenance: `assumption`. Combines the unitary step and the assumed channels; ordering is a choice.

Equation assumptions:

- Channel ordering as written
- Same p, q at every step

## eq_5: Position distribution

$$
P_t(x)=\sum_{s\in\{\uparrow,\downarrow\}}\langle s,x|\rho_t|s,x\rangle
$$

Measured spatial distribution, from which decoherence per step would be determined by fitting p and q.

Provenance: `abstract_inferred`. The abstract says the decoherence per step is determined from the measured spatial distributions; this is the observable such a fit would use.

Abstract evidence: From the measured spatial distributions, we determine with good precision the amount of decoherence per step

Equation assumptions:

- Spin is traced out in the position measurement

## Registers

- spin: 1 qubit qubits; coin degree of freedom
- position: unknown (symbolic, ~log2 of the number of lattice sites) qubits; walker position on the lattice

## Initial state

Assumed |\uparrow\rangle\otimes|x=0\rangle (density matrix \rho_0=|\uparrow,0\rangle\langle\uparrow,0|).

## Measurement

Position-resolved measurement (spin traced out), giving P_t(x).

## Classical postprocessing

Fit p and q to the measured P_t(x). The fitting method is not specified in the abstract.

## Algorithm steps

1. Prepare the walker at the origin with a fixed spin state. (no equation reference)
2. Apply the unitary coin and shift step. (eq_1)
3. Apply the spin and spatial dephasing channels. (eq_2, eq_3, eq_4)
4. Repeat for t steps, then read out the position distribution. (eq_4, eq_5)

## Assumptions

- No experiment scope was given, so a minimal Hadamard walk with phase-flip channels was chosen.
- The channel forms and parameters are illustrative, not the paper's.

## Missing information

- The paper's actual decoherence model and parameters
- Definitions of coherence length and the discrete Wigner function
- Distinction between short- and long-time (quasi-stationary) dephasing
- Experimental coin and shift implementation and initial state
- Fitting procedure for decoherence per step
