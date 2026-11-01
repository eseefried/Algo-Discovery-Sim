# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate a disordered 2D discrete-time (split-step) quantum walk on a small periodic lattice with reflecting links cut along a straight A-to-B line, and estimate the arrival probability P_B(T) at B for cut versus uncut walks with identical static disorder.

Scope: One tiny instance: 4x4 periodic lattice (2 qubits per axis), 2 coin qubits (one per axis), 6 qubits total, no ancilla. A=(0,0), B=(2,0) on the x axis; the cut is on the horizontal links of the line y=0. Static random disorder angles come from a fixed seed. T is a few times the A-B distance. Out of scope: the periodically driven Hamiltonian realization, the quasienergy winding invariant computation, the Chern number, and large-lattice scaling.

## Symbols

- $x,y$: position basis labels on each axis; domain: {0,1,2,3}, encoded as 2-bit little-endian integers
- $c_x,c_y$: coin qubits; each sets the hop direction along its axis; domain: {0,1}; 0 means +1, 1 means -1
- $\theta_x(x,y),\theta_y(x,y)$: static random coin rotation angles per site and per coin qubit; domain: [0,2\pi), fixed seed
- $C$: site-dependent coin operator; domain: unitary on position and coin
- $R$: reflection operator at cut links; domain: unitary on position and coin
- $S$: coin-controlled shift; domain: unitary on position and coin
- $U$: one-step walk operator; domain: unitary
- $T$: number of steps; domain: positive integer
- $P_B(T)$: probability of finding the walker at B after T steps; domain: [0,1]

## eq_1: Disordered coin

$$
C=\sum_{x,y}|x,y\rangle\langle x,y|\otimes e^{-i\theta_x(x,y)Y}\otimes e^{-i\theta_y(x,y)Y}
$$

Per-site rotation of each coin qubit, built as multiplexed Ry(2\theta) gates controlled on the position registers.

Provenance: `assumption`. The abstract mentions disorder but gives no coin form; this is the proposed concrete construction.

Equation assumptions:

- Static disorder
- Y-rotation coin per axis
- Uniform random angles from a fixed seed

## eq_2: Shift

$$
S=\sum_{x,y,c_x,c_y}|x+(-1)^{c_x},\,y+(-1)^{c_y}\rangle\langle x,y|\otimes|c_x c_y\rangle\langle c_x c_y|\quad(\mathrm{mod}\ 4)
$$

Coin-controlled increment or decrement on each axis, with periodic boundaries.

Provenance: `assumption`. A standard 2D discrete-time walk shift with this coin encoding is assumed.

Equation assumptions:

- Periodic 4x4 lattice
- Modular arithmetic

## eq_3: Reflecting cut

$$
R=\sum_{(x,y)\in L}|x,y\rangle\langle x,y|\otimes X_{c}\ \text{on the cut-crossing coin value},\quad U=S'\,R\,C
$$

On cut sites with the coin pointing across the cut link, flip the coin and skip the hop (reflection). S' is the shift restricted to non-reflected components. Equivalently, a swap of coin direction takes the place of the hop on cut links.

Provenance: `abstract_inferred`. The abstract says links are cut; reflection rather than loss of amplitude is the sketch's assumption. The exact reflecting-link implementation is not given in the abstract and must be defined unitarily.

Abstract evidence: by cutting some of the links

Equation assumptions:

- Reflection, not absorption
- The cut set L is the horizontal links along y=0 between A and B
- Unitarity requires the reflected component to receive no shift

## eq_4: Walk evolution

$$
|\psi_T\rangle=U^T|A\rangle|c_0\rangle,\quad |A\rangle=|0,0\rangle,\ |c_0\rangle=|00\rangle
$$

T repeated applications of the same step operator with the same disorder realization on the initial state.

Provenance: `assumption`. Fixed initial state at A, prepared with X gates only, or the trivial all-zero state.

Equation assumptions:

- The initial coin state is a fixed choice

## eq_5: Arrival probability

$$
P_B(T)=\sum_{c}\left|\langle B,c|\psi_T\rangle\right|^2,\quad \hat P_B=\frac{N_B}{N_{shots}}
$$

Position-register marginal at B, estimated from counts or read exactly from the statevector.

Provenance: `assumption`. The readout defined by the task sketch. The comparison is P_B(cut) versus P_B(uncut) with identical disorder.

Equation assumptions:

- Measure only the 4 position qubits
- Little-endian: counts bits[::-1][i] is classical bit i

## Registers

- x: 2 qubits; x position, qubits 0-1, little-endian
- y: 2 qubits; y position, qubits 2-3, little-endian
- coin: 2 qubits; c_x on qubit 4, c_y on qubit 5

## Initial state

|x=0,y=0>|c_x=0,c_y=0>, or a fixed coin state set by X gates

## Measurement

Measure the 4 position qubits only into 4 classical bits; the coin is not measured.

## Classical postprocessing

Marginalize counts onto position B, divide by the shot count to get P_B(T), compare cut versus uncut, and locate the arrival time peak versus A-B distance.

## Algorithm steps

1. Prepare the walker at A with X gates only where needed. (eq_4)
2. Apply the disordered coin as multiplexed Ry gates controlled on the position registers. (eq_1)
3. Apply the reflection on the cut line (multi-controlled X on the coin qubit), then the shift for non-reflected components, using increment/decrement from cascaded multi-controlled X gates. Repeat for T steps. Build the uncut baseline by omitting R with the same angles. (eq_2, eq_3)
4. Measure the position qubits only, or read the statevector, and compute P_B(T) for cut and uncut. Scan T for the arrival-time scaling. (eq_5)

## Assumptions

- Concrete 4x4 lattice with A and B on the x axis
- The 2-qubit coin has one qubit per axis
- Reflection, not absorption, on cut links
- Disorder is a fixed seed and the same for cut and uncut circuits
- No black box or oracle query is used

## Missing information

- The paper's exact coin and shift definitions (split-step ordering)
- Exact disorder distribution
- The precise cut geometry and the coin-reflection rule for cut links
- Hamiltonian realization and winding number formula
- Numerical results to compare against
