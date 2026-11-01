# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Coined discrete-time quantum walk search for a single known marked node on a degree-4 twisted-toroid graph with n=2^(2m) nodes, implemented as an explicit circuit with the marking compiled in (no black box).

Scope: One tiny instance, m=1 or m=2 (n=4 or 16), with Grover coin, flip-flop shift, a twist on x-wraparound, a compiled marked node, and a numerically chosen iteration count T. Statevector simulation, then position-register readout. Excludes the other graph families in the abstract, the exact twist definition from the paper, the O(sqrt(n) log n) gate-count proof, and large-n numerics.

## Symbols

- $m$: qubits per coordinate; domain: positive integer
- $n=2^{2m}$: number of nodes; domain: integer
- $x,y$: lattice coordinates (little-endian, x in the low m bits, y in the high m bits); domain: {0,...,2^m-1}
- $c$: coin direction (0:+x, 1:-x, 2:+y, 3:-y); domain: {0,1,2,3}
- $w$: marked node (x_w,y_w); domain: {0,...,n-1}
- $s$: twist offset applied to y when x wraps; domain: integer, assumed 1
- $T$: number of search iterations; domain: positive integer, chosen numerically
- $U$: one-step operator S C O; domain: unitary

## eq_1: Initial state

$$
|\psi_0\rangle=\frac{1}{\sqrt{4n}}\sum_{c,x,y}|c\rangle|x,y\rangle
$$

Uniform superposition over coin and position, made by Hadamards.

Provenance: `assumption`. The sketch specifies Hadamards on the position and coin registers. The abstract does not state this.

Equation assumptions:

- Hadamards on all 2m+2 qubits

## eq_2: Marking and coin

$$
O=I-2\,I_c\otimes|w\rangle\langle w|,\quad C=\left(2|s_c\rangle\langle s_c|-I\right)\otimes I,\ |s_c\rangle=\tfrac12\sum_c|c\rangle
$$

Phase flip on the marked position, compiled as a multi-controlled Z (X gates on the zero bits of w), followed by the Grover coin on the 2 coin qubits.

Provenance: `assumption`. The sketch gives a coin phase flip at a fixed marked address and a Grover coin. The sign conventions are a choice. A full-coin flip is used here, and the sketch's phrase 'flipping the coin phase' is ambiguous.

Equation assumptions:

- Marked-node phase applies to all coin values
- Grover coin on all nodes

## eq_3: Twisted shift

$$
S|c,x,y\rangle=|\bar c,\ x\pm1\bmod 2^m,\ y+s\,[\text{wrap}]\rangle\ (c\in\{0,1\});\ |\bar c,x,y\pm1\rangle\ (c\in\{2,3\})
$$

Flip-flop shift: move in the direction c and reverse the coin. Modular increments or decrements come from MCX cascades. When x wraps (x=2^m-1 going +x, or x=0 going -x), y also shifts by s, with the sign following the direction.

Provenance: `assumption`. The sketch describes a conditional increment of the other coordinate on wraparound. The exact twist in the paper is unknown, so this is one plausible choice.

Equation assumptions:

- twist s=1 on x-wrap only
- flip-flop coin reversal c XOR 1

## eq_4: Search evolution and success probability

$$
|\psi_T\rangle=U^T|\psi_0\rangle,\ U=S\,C\,O,\quad P(T)=\sum_c\left|\langle c,w|\psi_T\rangle\right|^2
$$

T iterations, where T maximizes P(T) in a numerical scan over T for small instances.

Provenance: `abstract_inferred`. A numerical analysis implies scanning the marked-node probability. The sketch's T~sqrt(n) with a 1/log n peak is not stated in the abstract.

Abstract evidence: We also provide a numerical analysis of a quantum walk based search along a twisted toroid family of graphs

Equation assumptions:

- the optimal T is found by classical simulation of the same circuit

## eq_5: Gate scaling claim

$$
N_{2q}=O\!\left(\sqrt n\,\log n\right)
$$

Claimed total two-qubit gate count for finding a marked node.

Provenance: `abstract_explicit`. Stated directly in the abstract. It is a claim, not a derivation, and is used here as a target only.

Abstract evidence: requires O($\sqrt{n}$ log($n$)) elementary 2-qubit quantum gate operations to find a marked node

## Registers

- coin: 2 qubits; direction qubits (little-endian)
- pos: 2m qubits; x in the low m bits, y in the high m bits
- anc: 1 qubits; ancilla for multi-controlled gates, returned to |0>

## Initial state

All qubits |0>, then H on coin and pos, giving the uniform state; the ancilla stays |0>.

## Measurement

Measure the 2m position qubits only. Qiskit little-endian: the last character of the counts key is bit 0, which is x bit 0. Do not measure the coin or the ancilla.

## Classical postprocessing

Take the most frequent position outcome as the marked node, and decode x = low m bits and y = high m bits.

## Algorithm steps

1. Prepare the uniform superposition with Hadamards. (eq_1)
2. Repeat T times: apply the marking phase flip at w, then the Grover coin. (eq_2)
3. Apply the coin-controlled twisted shift, with wrap detection and the y increment. (eq_3)
4. Choose T by simulating and maximizing P(T). Read out the position register. (eq_4)

## Assumptions

- Choose m=1 or 2 as the instance
- Coin-based walk with Grover coin and flip-flop shift
- Single known marked node compiled in, no black-box queries
- Twist is y+1 when x wraps (a guess)
- Qubit count 2m+3 or fewer
- Success probability may be only about 1/log n and is boosted by repetition

## Missing information

- Exact twisted-toroid graph definition (twist size and direction)
- Paper's exact oracle and coin conventions
- Gate-level decomposition and exact iteration counts
- Other graph families in the abstract
- Numerical results
