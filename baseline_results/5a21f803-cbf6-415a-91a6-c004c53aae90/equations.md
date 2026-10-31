# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Quantum-walk-based spatial search on structured graph families (including a twisted toroid family) implemented as explicit quantum circuits in which the marked node is encoded directly in the circuit rather than through a black-box oracle; the abstract reports O(sqrt(n) log n) elementary 2-qubit gates to find a marked node on the twisted toroid family.

Scope: One smallest useful construction chosen as an assumption (no experiment_scope was supplied): a discrete-time coined quantum walk search on a single tiny 4-regular circulant graph taken as a stand-in for a member of the twisted toroid family, with n = 8 vertices (3 position qubits), degree d = 4 (2 coin qubits), one marked vertex w = 0, a Grover coin on unmarked vertices and a -I coin on the marked vertex, a modular-shift operator built from controlled modular increment/decrement circuits, t walk steps, and a final measurement of the position register. Outside scope: the exact definition of the paper's twisted toroid family and the other graph families, the paper's specific circuit decompositions and gate counts, its numerical analysis, and any choice of t or coin that the paper actually used.

## Symbols

- $n$: number of graph vertices (instance: n = 8); domain: positive integer, power of 2 in the chosen instance
- $d$: vertex degree of the regular graph (instance: d = 4); domain: positive integer
- $m$: second circulant offset defining the twisted connections (instance: m = 3); domain: integer with 1 < m < n/2
- $x$: vertex label, encoded as a binary integer in the position register; domain: \{0,\dots,n-1\}
- $c$: coin label selecting one of the d outgoing directions; domain: \{0,1,2,3\}
- $\delta_c$: vertex displacement associated with coin value c; domain: \{+1,-1,+m,-m\}
- $w$: marked vertex to be found (instance: w = 0); domain: \{0,\dots,n-1\}
- $t$: number of walk steps applied before measurement; domain: non-negative integer
- $U$: one step of the quantum-walk search operator; domain: unitary on \mathbb{C}^{d}\otimes\mathbb{C}^{n}
- $S$: shift operator moving the walker along the edge selected by the coin; domain: unitary on \mathbb{C}^{d}\otimes\mathbb{C}^{n}
- $C_0, C_1$: coin operators on unmarked and marked vertices respectively; domain: unitaries on \mathbb{C}^{d}
- $P_w(t)$: probability of measuring the marked vertex after t steps; domain: [0,1]

## eq_1: Circulant stand-in for a twisted toroid instance

$$
V=\mathbb{Z}_n,\quad E=\{\{x,\,x\pm 1 \bmod n\},\ \{x,\,x\pm m \bmod n\} : x\in\mathbb{Z}_n\},\quad n=8,\ m=3
$$

A 4-regular circulant graph on n vertices with nearest-neighbour and offset-m connections, used as a tiny concrete instance; all arithmetic on vertex labels is modular reduction mod n.

Provenance: `assumption`. The abstract names a twisted toroid family but does not define it; a circulant graph with two offsets is a plausible minimal degree-4 graph with a torus-like twisted wrap-around whose shift is implementable by modular adders, but this specific definition is a choice, not paper evidence.

Equation assumptions:

- The paper's twisted toroid family may be defined differently; this instance is a stand-in only.
- n is a power of 2 so that vertex labels fill the position register exactly.

## eq_2: Initial state (uniform superposition over coin and position)

$$
|\psi_0\rangle=\frac{1}{\sqrt{d}}\sum_{c=0}^{d-1}|c\rangle\otimes\frac{1}{\sqrt{n}}\sum_{x=0}^{n-1}|x\rangle,\qquad d=4,\ n=8
$$

Equal superposition over all directions and vertices; with d and n powers of 2 this is H^{\otimes 5} applied to |0\rangle^{\otimes 5} on the coin and position registers.

Provenance: `standard_background`. Standard starting state for coined quantum-walk search algorithms (e.g. SKW/AKR-type); the abstract does not state the initial state.

Equation assumptions:

- Register ordering is coin register then position register, |c\rangle\otimes|x\rangle.

## eq_3: Modular shift operator

$$
S\,|c\rangle\otimes|x\rangle=|c\rangle\otimes|(x+\delta_c)\bmod n\rangle,\qquad (\delta_0,\delta_1,\delta_2,\delta_3)=(+1,-1,+m,-m)
$$

Coin-controlled modular increment/decrement of the position register; implementable as four coin-controlled adders modulo n (each O(log n) elementary gates up to multi-controlled gate decomposition). Equality is exact; addition is reduced mod n.

Provenance: `abstract_inferred`. An efficient walk implementation on a circulant/toroidal graph is naturally realised by coin-controlled modular adders; this is an inference from the efficiency claim, and the specific 'moving' (coin-preserving) shift convention is a choice.

Abstract evidence: allow both efficient quantum walk implementations

Equation assumptions:

- Moving shift (coin unchanged) rather than flip-flop shift.
- Position x is encoded in binary on the position register.

## eq_4: Marked-vertex-dependent coin (oracle-free marking)

$$
C=C_0\otimes(I_n-|w\rangle\langle w|)+C_1\otimes|w\rangle\langle w|,\quad C_0=2|s\rangle\langle s|-I_d,\ |s\rangle=\tfrac{1}{\sqrt d}\sum_c|c\rangle,\quad C_1=-I_d
$$

Grover diffusion coin on unmarked vertices and a sign-flip coin on the marked vertex. Because w is a fixed classical integer, C_1 is applied via a position-controlled operation (X gates mapping |w\rangle to |1\cdots1\rangle, a multi-controlled Z, and the inverse X gates), so no black-box oracle is needed.

Provenance: `abstract_inferred`. The abstract states the marking is implemented explicitly without an oracle; a position-controlled coin conditioned on the classical value w is the standard way to do so. The particular coin choices (Grover coin, -I) are standard SKW-type assumptions, not stated in the abstract.

Abstract evidence: explicitly implement the full quantum walk search algorithm, without reference to a ‘black box’ oracle

Equation assumptions:

- Single marked vertex w.
- Coin choices C_0 = Grover coin and C_1 = -I are assumed; the paper may use other coins.

## eq_5: One step of the walk search and the final state

$$
U=S\,C,\qquad |\psi_t\rangle=U^{t}|\psi_0\rangle
$$

Each step applies the marked-dependent coin then the shift; t steps are applied before measurement.

Provenance: `standard_background`. Standard discrete-time coined quantum-walk search iteration; the abstract does not specify the operator ordering or t.

Equation assumptions:

- Coin applied before shift within each step.

## eq_6: Marked-vertex success probability and gate-count scaling

$$
P_w(t)=\sum_{c=0}^{d-1}\left|\langle c,w|\,U^{t}|\psi_0\rangle\right|^{2},\qquad t=O(\sqrt{n}),\quad \text{total 2-qubit gates}=O(\sqrt{n}\,\log n)
$$

Probability of observing the marked vertex when the position register is measured; the abstract's total gate count is consistent with O(sqrt(n)) steps each costing O(log n) elementary gates (this split is an inference). The optimal t for the tiny instance is not known from the abstract and would need to be scanned numerically.

Provenance: `abstract_explicit`. The total O(sqrt(n) log n) gate count is stated in the abstract; the success-probability definition is standard and the decomposition into O(sqrt(n)) steps times O(log n) gates per step is inferred rather than stated.

Abstract evidence: requires O($\sqrt{n}$ log($n$)) elementary 2-qubit quantum gate operations to find a marked node

Equation assumptions:

- The scaling applies to the paper's twisted toroid family; it is not verified for the stand-in instance.
- Asymptotic statement only; constants and the exact t are unknown.

## Registers

- coin: 2 qubits; Encodes the direction c in {0,1,2,3} (d = 4); first register in the tensor product |c>|x>.
- position: 3 qubits; Encodes the vertex label x in {0,...,7} in binary (n = 8); second register, target of the modular shift and control for the marked coin.

## Initial state

|psi_0> = H^{\otimes 2}|00>_coin ⊗ H^{\otimes 3}|000>_pos, i.e. the uniform superposition of eq_2 over all 32 coin-position basis states.

## Measurement

Computational-basis measurement of the 3-qubit position register (coin register discarded or traced out); outcome x in {0,...,7}. Success event: x = w = 0, with probability P_w(t) from eq_6.

## Classical postprocessing

Verify classically that the measured x is adjacent to the intended marked structure (here trivially x = w); if not, repeat the whole procedure. To choose t for the tiny instance, scan t over a small range (e.g. 0..10) and pick the t maximising P_w(t), since the abstract gives only the asymptotic O(sqrt(n)) scaling.

## Algorithm steps

1. Prepare the uniform superposition over coin and position registers with Hadamards on all 5 qubits. (eq_2)
2. Repeat t times: apply the marked-dependent coin C (Grover coin on the coin register for x ≠ w, implemented by the Grover coin followed by a correction, or equivalently a position-controlled selection; -I on x = w realised by X^{⊗3} ... multi-controlled Z ... X^{⊗3} on the position register, no oracle), then apply the shift S as four coin-controlled modular ±1 and ±m adders on the position register. (eq_4, eq_3, eq_5)
3. Measure the position register in the computational basis and record the outcome x; the walk is successful if x = w. (eq_6)

## Assumptions

- No experiment_scope was provided, so a single tiny instance (n = 8 circulant graph with offsets ±1, ±3, one marked vertex w = 0) was chosen as the reconstruction target.
- The paper's twisted toroid family is modelled by a degree-4 circulant graph; the true definition may differ.
- Discrete-time coined walk with Grover coin on unmarked vertices and -I coin on the marked vertex (SKW-style) is assumed; the paper's actual coin and walk model (coined vs. Szegedy vs. continuous-time) is not stated in the abstract.
- Register ordering coin ⊗ position with binary integer encoding of vertex labels; moving (coin-preserving) shift.
- The decomposition of the stated O(sqrt(n) log n) gate count into O(sqrt(n)) steps of O(log n) gates each is an inference.

## Missing information

- Exact definition of the twisted toroid graph family and of the other graph families treated in the paper.
- The specific quantum-walk model, coin operators, and shift convention used by the paper.
- The paper's explicit circuit decompositions, gate counts, and how multi-controlled gates are counted as elementary 2-qubit operations.
- The number of walk steps t and the resulting success probabilities from the paper's numerical analysis.
- Whether multiple marked nodes or amplitude amplification/repetition are used to boost success probability.
