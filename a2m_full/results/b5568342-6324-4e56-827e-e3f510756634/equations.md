# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Ideal Grover search over N=16 items on 4 qubits with one hidden marked basis state w, using one black-box phase-oracle query per iteration, 3 iterations, and readout of w from measurement counts.

Scope: Ideal (noise-free, coupling-free) 4-qubit Grover search with H, X, and multi-controlled Z diffusion. The nuclear-spin-chain physics (Rabi-driven pulses, nearest and next-nearest Ising couplings, 2πk pulse-timing condition, fidelity vs Rabi frequency) is outside this scope.

## Symbols

- $n$: number of data qubits (spins); domain: n=4
- $N$: search space size 2^n; domain: N=16
- $w$: hidden marked item, as a 4-bit integer; domain: {0,...,15}
- $|s\rangle$: uniform superposition over all basis states; domain: state in (C^2)^{\otimes 4}
- $O_w$: black-box phase oracle, one query per use; domain: unitary on 4 qubits
- $D$: diffusion operator; domain: unitary on 4 qubits
- $\theta$: Grover angle, sin theta = 1/sqrt(N); domain: (0,\pi/2), about 0.2527 rad
- $k$: Grover iteration index; domain: integer, 0..3
- $F_k$: fidelity with the marked state after k iterations; domain: [0,1]

## eq_1: Oracle and diffusion

$$
O_w=I-2|w\rangle\langle w|,\qquad D=2|s\rangle\langle s|-I=H^{\otimes4}X^{\otimes4}\,(\mathrm{MCZ})\,X^{\otimes4}H^{\otimes4}\ \text{up to global phase}
$$

Phase flip on the marked state, and inversion about the mean. MCZ is a Z on the 4-qubit all-ones state, built as H on the target, a 3-control mcx, then H on the target.

Provenance: `standard_background`. Standard Grover construction. The abstract only names Grover search and does not state these equations.

Equation assumptions:

- Single marked state
- Oracle supplied as an opaque placeholder gate on 4 qubits
- Diffusion equals 2|s><s|-I up to a global phase of -1

## eq_2: Iteration count

$$
k^*=\lfloor \tfrac{\pi}{4}\sqrt{N}\rfloor=\lfloor \pi\rfloor=3
$$

Number of Grover iterations for N=16.

Provenance: `assumption`. Chosen as the standard near-optimal count. The abstract does not give the iteration number.

Equation assumptions:

- N=16

## eq_3: Final state

$$
|\psi_k\rangle=(D\,O_w)^k H^{\otimes4}|0000\rangle
$$

State after k Grover iterations starting from the uniform superposition.

Provenance: `standard_background`. Standard Grover algorithm structure.

Equation assumptions:

- Ideal gates

## eq_4: Fidelity vs iteration

$$
F_k=|\langle w|\psi_k\rangle|^2=\sin^2\!\big((2k+1)\theta\big),\quad \sin\theta=\tfrac14
$$

Ideal success probability. Values: k=0: 0.0625, k=1: 0.5078, k=2: 0.9084, k=3: 0.9613, k=4: 0.5897.

Provenance: `abstract_inferred`. The abstract says that fidelity is tracked during the algorithm. The ideal-case closed form is standard background recalled by me and is not stated in the abstract.

Abstract evidence: We determine the temporal behaviour of the fidelity during the algorithm

Equation assumptions:

- No Ising coupling or pulse errors
- Single marked item

## eq_5: Bit-order readout

$$
w=\sum_{i=0}^{3}b_i2^i,\quad \text{key string}=b_3b_2b_1b_0,\quad b_i=\text{measurement of qubit }i\text{ stored in classical bit }i
$$

Qiskit little-endian readout. The answer is the most frequent key.

Provenance: `assumption`. Fixes the encoding convention for the simulator readout.

Equation assumptions:

- Measure qubit i into classical bit i
- Qiskit little-endian counts keys

## Registers

- q: 4 qubits; data qubits (spins), qubit i is bit i of w; no ancillas
- c: 4 qubits; classical bits, c[i] receives qubit i

## Initial state

|0000>

## Measurement

Measure all 4 qubits, qubit i into classical bit i. Expected success probability is about 0.961.

## Classical postprocessing

Take the most frequent counts key. Its string is b3b2b1b0 (last character is bit 0), and w is its integer value in base 2.

## Algorithm steps

1. Apply H to all 4 qubits to prepare the uniform superposition. (eq_3)
2. Repeat 3 times: place the black-box oracle once on qubits 0..3, then apply the diffusion operator (H^4, X^4, H on qubit 3, mcx with controls 0,1,2 and target 3, H on qubit 3, X^4, H^4). Total 3 oracle queries. (eq_1, eq_2, eq_3)
3. Measure qubits 0..3 into classical bits 0..3 and read the most frequent key as w. (eq_4, eq_5)

## Assumptions

- Ideal Grover only, with no spin-chain physics
- Single marked basis state
- 3 iterations
- Standard Qiskit gates h, x, mcx are used, with no initialize or dense unitary
- The oracle is an opaque placeholder gate and is not inspected
- Optional rx/rz/cx decomposition for depth counting is not specified

## Missing information

- Pulse-level Hamiltonian, coupling strengths, and the Rabi frequency values
- The explicit 2πk condition for the next-nearest-neighbour coupling
- How the paper decomposes the oracle and diffusion into pulses
- Fidelity definition used in the paper for noisy simulation
- The paper's choice of marked state
