# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Quantized density classification of a 5-bit input x: decide majority 0 vs majority 1 using a single quantum particle (QPA) whose position basis has 32 states indexed by x. A unitary U (parameter theta plus others, found offline by a genetic algorithm) is applied T times, then position is measured and the mass in a boundary partition P decides the output.

Scope: One tiny explicit instance: n=5, one particle on a 32-site ring (5 position qubits) with one optional coin qubit (6 qubits total). The input is loaded as the initial basis state |x>. U = S*(I tensor Ry(2 theta)) is applied T times, then the position register is measured and the P-mass is thresholded at 1/2. Classical GA search is described only as an objective. Outside scope: the actual GA-found unitaries, partitions, theta values, the paper's exact QPA Hamiltonian/operator form, and generalization to arbitrary n.

## Symbols

- $n$: input length; domain: n=5
- $x$: binary input string, also the integer index of the initial position; domain: x in {0,...,31}, bit i of x on qubit i (little-endian)
- $|x\rangle$: initial particle position basis state; domain: 32-dim position Hilbert space
- $\theta$: coin/mass rotation angle; small gives light, fast particle, large gives heavy, slow particle; domain: real, [0,\pi]
- $T$: number of evolution steps; domain: positive integer, fixed (assumed)
- $S$: coin-controlled shift: +1 mod 32 if coin=0, -1 mod 32 if coin=1; domain: unitary on coin and position registers
- $C(\theta)$: coin rotation Ry(2 theta); domain: single-qubit unitary
- $P$: boundary partition: set of position basis states labelled majority-1; domain: subset of {0,...,31}, encoded as a 32-bit mask
- $p_x(j)$: probability of measuring position j for input x after T steps; domain: [0,1]
- $w(x)$: Hamming weight of x; domain: 0..5
- $F$: GA fitness: mean correct-side probability over all inputs; domain: [0,1]

## eq_1: Initial state

$$
|\psi_0(x)\rangle=|c=0\rangle\otimes|x\rangle,\quad |x\rangle=\bigotimes_{i=0}^{4}|x_i\rangle_{q_i}
$$

Input encoded as starting position by X gates on qubits with x_i=1; coin starts in |0> (assumed).

Provenance: `assumption`. Sketch places the particle at |x>; the coin initial state is a choice.

Equation assumptions:

- Coin starts in |0>
- Qubit i holds bit i

## eq_2: One-step evolution

$$
U=S\,(C(\theta)\otimes I),\quad C(\theta)=R_y(2\theta),\quad S=|0\rangle\langle0|\otimes V+|1\rangle\langle1|\otimes V^{\dagger},\ V|j\rangle=|j+1 \bmod 32\rangle
$$

Dirac-like discrete walk with coin; theta sets the effective mass.

Provenance: `assumption`. The abstract says a unitary operator with parameter theta drives evolution, with small theta giving small mass and fast evolution; the specific coin-shift form is a proposed construction, and the paper's operator may differ.

Equation assumptions:

- Coin-shift form is a stand-in for the paper's operator
- GA may add extra Ry/Rz/CX layers

## eq_3: State after T steps and output probabilities

$$
|\psi_T(x)\rangle=U^T|\psi_0(x)\rangle,\quad p_x(j)=\sum_{c\in\{0,1\}}|\langle c,j|\psi_T(x)\rangle|^2
$$

Measuring only position qubits marginalizes over the coin.

Provenance: `abstract_inferred`. Measurement probabilities of the evolved state determine the correct-side likelihood.

Abstract evidence: when the particle was measured, it was more likely to collapse to the basis states that were on the correct side of the boundary partition

Equation assumptions:

- Fixed T

## eq_4: Decision rule

$$
M_x=\sum_{j\in P}p_x(j),\quad \text{output}=\begin{cases}1&M_x>1/2\\0&\text{otherwise}\end{cases}
$$

Majority 1 if the measured mass in P exceeds 1/2; no ties since n=5 is odd.

Provenance: `abstract_inferred`. Abstract states a boundary partition makes the classification decision; the 1/2 threshold is the natural choice.

Abstract evidence: the QPA to decide if the binary input had majority density 0 or majority density 1

Equation assumptions:

- Threshold 1/2

## eq_5: GA fitness

$$
F(\theta,\vec\phi,P)=\frac{1}{32}\sum_{x=0}^{31}\Big[\mathbb{1}[w(x)\ge3]\,M_x+\mathbb{1}[w(x)\le2]\,(1-M_x)\Big]
$$

Mean probability on the correct side of P over all 32 inputs; the chromosome is (theta, other angles, 32-bit mask).

Provenance: `assumption`. Proposed formalization of the GA objective; the abstract only says the GA searched for unitaries and partitions.

Equation assumptions:

- Fitness is exactly this mean
- Fitness is evaluated offline

## Registers

- pos: 5 qubits; particle position, index x, little-endian
- coin: 1 (optional) qubits; coin for the Dirac-like walk
- c: 5 qubits; classical bits for the position measurement

## Initial state

Coin |0>, position |x> via X gates on qubits where x_i=1.

## Measurement

Measure the 5 position qubits into 5 classical bits; the coin is not measured.

## Classical postprocessing

Reverse the Qiskit key to get j, sum probability over P, output 1 if above 1/2 else 0.

## Algorithm steps

1. Load x by X gates on position qubit i where x_i=1. (eq_1)
2. Apply U T times: Ry(2 theta) on coin, then coin-controlled increment/decrement on the position register built from MCX/standard gates; the GA-found angles are inserted as fixed constants. (eq_2, eq_3)
3. Measure the position qubits only; reverse the counts key to read the index j (last char = bit 0). (eq_3)
4. Sum counts over j in P and compare to half the shots. (eq_4)
5. Offline: GA tunes theta, other angles, and P by maximizing F. (eq_5)

## Assumptions

- n=5 with the input indexing one of 32 basis states
- Coin-shift walk form is an assumption
- T, theta, and P are not given in the abstract and must be supplied by a GA run
- No black-box queries

## Missing information

- Exact QPA unitary form and parameterization
- Values of theta, T, and P found by the GA
- GA hyperparameters
- Whether the paper uses a coin or a different internal degree of freedom
- Quantitative success rates
