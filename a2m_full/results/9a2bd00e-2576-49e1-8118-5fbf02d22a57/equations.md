# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Discrete-time coined quantum walk on the cycle C_N (N=4 as the smallest instance, optionally N=6 or 8) with coin in {Hadamard, Grover, DFT}. Test perfect state transfer (PST) from node 0 to the antipodal node N/2 by computing the antipodal probability P(t) over t=1..T. Modified graphs, decoherence and the continuous-time comparison are out of scope.

Scope: Smallest instance: C4 with a 2-qubit position register and a 1-qubit coin, with the Hadamard coin and the moving-shift convention. Read out P(t) from the statevector for t=1..T with T small (e.g. 8). Out of scope: the specific modified graphs, the Grover/DFT coins on degree>2 graphs, the enumeration of modifications, the interpolation ancilla, decoherence, the continuous-time walk, and the three families of graphs. The abstract does not specify these.

## Symbols

- $N$: number of cycle nodes; domain: even integer, 4 here (2^n)
- $n$: number of position qubits; domain: integer, log2 N = 2
- $C$: coin unitary on the 1-qubit coin; domain: 2x2 unitary, Hadamard H
- $S$: conditional shift on position and coin; domain: permutation unitary on C^N tensor C^2
- $U$: one-step walk operator; domain: unitary on C^N tensor C^2
- $|\psi_0\rangle$: initial state, node 0 with coin state |c_0\rangle; domain: unit vector
- $P(t)$: probability of being at antipodal node N/2 at step t, summed over coin states; domain: [0,1]
- $T$: maximum number of steps scanned; domain: positive integer

## eq_1: Shift operator

$$
S=\sum_{x=0}^{N-1}\left(|x+1 \bmod N\rangle\langle x|\otimes|0\rangle\langle 0|+|x-1 \bmod N\rangle\langle x|\otimes|1\rangle\langle 1|\right)
$$

Coin 0 increments position, coin 1 decrements it, mod N. This is the moving shift on the plain cycle, implemented with an incrementer/decrementer ladder.

Provenance: `assumption`. The sketch proposes this convention. The abstract does not give the shift. The sketch states a flip-flop assumption, but this is the simple moving shift for the degree-2 cycle, so the convention is unresolved.

Equation assumptions:

- Moving shift used for the cycle
- Flip-flop convention for higher-degree graphs not specified

## eq_2: Walk step

$$
U=S\,(I_N\otimes C),\quad |\psi_t\rangle=U^t|\psi_0\rangle
$$

One step applies the coin to the coin qubit and then the shift. The state at step t is U^t applied to the initial state.

Provenance: `standard_background`. Standard coined discrete-time quantum walk definition.

Equation assumptions:

- No measurement between steps

## eq_3: Initial state

$$
|\psi_0\rangle=|0\rangle_{pos}\otimes(\cos\tfrac{\theta}{2}|0\rangle+e^{i\phi}\sin\tfrac{\theta}{2}|1\rangle)_{coin}
$$

Walker at node 0 with a coin state set by Bloch angles. It is prepared with Ry(theta) and Rz(phi) or X/H/S gates.

Provenance: `assumption`. The abstract mentions varying the initial state. The specific parametrization comes from the sketch.

Equation assumptions:

- Start at node 0
- Default coin state is |0> or (|0>+i|1>)/sqrt2

## eq_4: Antipodal transfer probability

$$
P(t)=\sum_{c\in\{0,1\}}\left|\langle N/2,c|\psi_t\rangle\right|^2
$$

Probability at the antipodal node, summed over coin states. PST occurs at t if P(t)=1 within 1e-9. Otherwise it is high fidelity if P(t) is close to 1.

Provenance: `abstract_inferred`. The abstract defines PST between antipodal nodes. The sum over coin states follows the sketch's assumption.

Abstract evidence: perfect state transfer between antipodal nodes of discrete time quantum walks

Equation assumptions:

- The coin state at arrival is ignored

## eq_5: Periodicity test

$$
|\langle\psi_0|U^t|\psi_0\rangle|=1
$$

The walk is periodic at t when the return amplitude has unit modulus.

Provenance: `abstract_inferred`. The abstract names periodicity as one of the dynamics. The test is the standard definition.

Abstract evidence: either periodicity, perfect state transfer, or very high fidelity state transfer

Equation assumptions:

- Tolerance about 1e-9

## Registers

- pos: 2 (n=log2 N, 3 for C8) qubits; node index, little-endian integer encoding, qubit 0 is the least significant bit
- coin: 1 qubits; coin qubit, 0=forward, 1=backward

## Initial state

Node 0 with a chosen coin state (default |0>), prepared with X/H/S gates or Ry/Rz.

## Measurement

None for statevector reading. If counts are needed, measure only the position qubits. With little-endian bits, the last character of the key is pos bit 0.

## Classical postprocessing

Compute P(t) for each t from the statevector. Declare PST if max_t P(t) >= 1-1e-9, and compute |<psi0|U^t|psi0>| for periodicity.

## Algorithm steps

1. Prepare the initial state on pos=0 and the coin. (eq_3)
2. Apply the coin gate to the coin qubit. (eq_2)
3. Apply the conditional shift S, with increment when coin=0 and decrement when coin=1, using CX and multi-controlled X gates. (eq_1)
4. Repeat for t=1..T, with a separate circuit per t and no measurements. Read the statevector and compute P(t) and the return amplitude. (eq_2, eq_4, eq_5)

## Assumptions

- Smallest instance is C4 with the Hadamard coin
- Coin and shift conventions are as in eq_1
- Antipodal node is N/2, starting at node 0
- The three coins are Hadamard, Grover and DFT. Grover and DFT coins are not applicable to a 1-qubit coin on the plain cycle, since Grover on 2 dimensions equals a Pauli-like reflection and DFT on 2 dimensions equals H.
- Qubit count: 3 for C4 and 4 for C8, within the cap

## Missing information

- The specific modified graphs that give PST
- The exact coin definitions and arc conventions in the paper
- The weights used to interpolate between structures
- The decoherence model details
- The three graph families
