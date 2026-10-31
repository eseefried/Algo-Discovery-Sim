# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Perfect state transfer (PST) of an arbitrary unknown qubit state between two sites of a lattice using a discrete-time quantum walk (DTQW) whose coin operation may vary with time step and position ('various settings of coin flippings'). The abstract claims PST of an arbitrary unknown two-qubit state, extension to multi-qubit entangled-state distribution on a multi-dimensional network, and quantum routing; it gives no equations, encodings, or coin schedules.

Scope: Smallest useful construction chosen here (an assumption, not the paper's protocol): a single DTQW walker on a one-dimensional line with a two-dimensional coin, transferring ONE unknown coin qubit from site 0 to site d using a position- and time-dependent coin schedule drawn from {I, X}. Tiny explicit instance: d = 2, T = d + 2 = 4 steps, positions in [-1, 3] (encoded as y = x + 1 in 3 qubits) plus one coin qubit. Outside scope: the paper's two-qubit (coin + position or two-walker) encoding, its specific coin-flipping settings, the multi-dimensional network and multi-qubit entangled-state distribution between every pair of sites, and the routing architecture.

## Symbols

- $x$: walker position (site index) on the one-dimensional line; domain: \mathbb{Z}; in the instance x \in \{-1,0,1,2,3\}
- $c$: coin (internal) state label; c=0 moves right, c=1 moves left; domain: \{0,1\}
- $\psi_{x,c}$: amplitude of the walker at site x with coin value c; domain: \mathbb{C}, \sum_{x,c}|\psi_{x,c}|^2 = 1
- $S$: coin-conditioned shift operator; domain: unitary on \mathcal{H}_P \otimes \mathcal{H}_C
- $C_t(x)$: coin operator applied at time step t to a walker located at site x; domain: \{I, X\} \subset U(2)
- $U_t$: one full walk step (position-dependent coin followed by shift) at time t; domain: unitary on \mathcal{H}_P \otimes \mathcal{H}_C
- $|\phi\rangle = a|0\rangle + b|1\rangle$: arbitrary unknown single-qubit state to be transferred, initially carried by the coin; domain: a,b \in \mathbb{C}, |a|^2+|b|^2=1
- $d$: target site (transfer distance from site 0); domain: \mathbb{Z}, d \geq 1; instance d = 2
- $T$: total number of walk steps; domain: \mathbb{Z}, T = d + 2; instance T = 4
- $V$: known, state-independent unitary correction on the transferred qubit; domain: U(2); in the proposed schedule V = X
- $y$: shifted non-negative position label for register encoding, y = x + 1; domain: \{0,\dots,d+2\}, stored as an n_P-bit unsigned integer

## eq_1: DTQW state space

$$
|\Psi\rangle = \sum_{x\in\mathbb{Z}} \sum_{c\in\{0,1\}} \psi_{x,c}\, |x\rangle_P \otimes |c\rangle_C
$$

The walker lives on a position register tensored with a two-level coin register.

Provenance: `standard_background`. Standard definition of a coined discrete-time quantum walk on a line.

Equation assumptions:

- One walker, two-dimensional coin, one-dimensional line (the paper's network is multi-dimensional).

## eq_2: Coin-conditioned shift

$$
S = \sum_{x\in\mathbb{Z}} \Big( |x+1\rangle\langle x| \otimes |0\rangle\langle 0| + |x-1\rangle\langle x| \otimes |1\rangle\langle 1| \Big)
$$

Coin value 0 moves the walker one site to the right, coin value 1 one site to the left.

Provenance: `standard_background`. Standard flip-flop-free shift of the coined DTQW; direction convention chosen here.

Equation assumptions:

- Direction convention c=0 -> +1, c=1 -> -1.

## eq_3: Walk step with position- and time-dependent coin flippings

$$
U_t = S \Big( \sum_{x\in\mathbb{Z}} |x\rangle\langle x| \otimes C_t(x) \Big), \qquad C_t(x) \in \{I, X\}
$$

Each step applies a coin operator that may depend on the site and the step, then shifts. The restriction to {I, X} ('flipping' vs 'no flipping') is an interpretation.

Provenance: `abstract_inferred`. The abstract says PST is achieved by varying the coin flippings; the natural formalisation is a site- and step-dependent coin inside the standard DTQW step. The exact coin set used in the paper is not stated.

Abstract evidence: via a discrete-time quantum walk with various settings of coin flippings

Equation assumptions:

- Coin set restricted to {I, X}; the paper may use other coins (e.g. Hadamard) in some settings.

## eq_4: Perfect state transfer condition

$$
U_T U_{T-1} \cdots U_1 \big( |0\rangle_P \otimes |\phi\rangle_C \big) = |d\rangle_P \otimes V|\phi\rangle_C \quad \forall\, |\phi\rangle \in \mathbb{C}^2, \; V \text{ fixed, independent of } |\phi\rangle
$$

After T steps the walker is found at site d with certainty and the unknown qubit is recovered up to a known unitary V (exact equality, not approximate).

Provenance: `abstract_inferred`. 'Perfect' and 'arbitrary unknown' imply unit-fidelity, input-independent (hence linear/unitary) transfer; here specialised from the paper's two-qubit claim to a single coin qubit.

Abstract evidence: a perfect state transfer of an arbitrary unknown two-qubit state can be achieved

Equation assumptions:

- Specialisation to one qubit; the paper's two-qubit encoding is unknown.

## eq_5: Proposed coin schedule (assumption)

$$
C_1(x) = I;\quad C_2(x) = \begin{cases} X & x=-1 \\ I & \text{else}\end{cases};\quad C_t(x) = I \;(3 \le t \le T-1);\quad C_T(x) = \begin{cases} X & x = T-2 \\ I & \text{else}\end{cases};\quad T = d+2
$$

Step 1 splits the two coin components to x=\pm1; step 2 flips the left component so both travel right with separation 2; the final step flips the leading component so both components meet at x = T-2 = d.

Provenance: `assumption`. A minimal explicit schedule constructed here that satisfies eq_4 using only {I,X} coins; it is not taken from the paper.

Equation assumptions:

- Not the paper's schedule; chosen as the smallest construction consistent with eq_3 and eq_4.

## eq_6: Resulting transfer for the proposed schedule

$$
U_T\cdots U_1\big(|0\rangle \otimes (a|0\rangle + b|1\rangle)\big) = |d\rangle \otimes (a|1\rangle + b|0\rangle) = |d\rangle \otimes X|\phi\rangle, \qquad d = T-2
$$

Trajectory: after step 1: a|1,0\rangle + b|-1,1\rangle; after step 2: a|2,0\rangle + b|0,0\rangle; after step t (3 \le t \le T-1): a|t,0\rangle + b|t-2,0\rangle; after step T: a|T-2,1\rangle + b|T-2,0\rangle. Hence V = X in eq_4. For d=2, T=4.

Provenance: `assumption`. Direct application of eq_2, eq_3 and eq_5 to the initial state; derived here, not verified against the paper.

Equation assumptions:

- Infinite line or a register large enough that positions in [-1, d+1] do not wrap; d \ge 1.

## Registers

- P (position): n_P = \lceil \log_2(d+3) \rceil qubits (3 qubits for d=2), storing y = x+1 \in \{0,\dots,d+2\} as an unsigned big-endian integer qubits; Walker position on the line; site 0 is the sender, site d the receiver.
- C (coin): 1 qubits; Coin register; initially carries the unknown qubit |\phi\rangle and delivers X|\phi\rangle at the end.

## Initial state

|\Psi_0\rangle = |x=0\rangle_P \otimes (a|0\rangle + b|1\rangle)_C, i.e. position register in |y=1\rangle (binary 001 for n_P=3) and coin in the unknown state |\phi\rangle.

## Measurement

Verification only (the protocol itself is unitary): measure the position register in the computational basis; outcome y = d+1 (x=d) should occur with probability 1. The coin register, after the X correction, should equal |\phi\rangle; verify by state tomography or by measuring in the basis that distinguishes |\phi\rangle for several known test inputs (e.g. |0\rangle, |1\rangle, |+\rangle, |+i\rangle) and estimating fidelity.

## Classical postprocessing

Check that all position outcomes equal x=d; estimate transfer fidelity F = |\langle\phi| X \rho_C X |\phi\rangle| from tomography of the coin register over the test inputs; F should be exactly 1 in a noiseless simulation.

## Algorithm steps

1. Prepare the position register in |x=0\rangle (y=1) and load the unknown qubit |\phi\rangle into the coin register. (eq_1)
2. Step t=1: apply coin I everywhere, then the shift S; the two coin components separate to x=+1 and x=-1. (eq_2, eq_3, eq_5)
3. Step t=2: apply X on the coin controlled on position x=-1 (y=0), I elsewhere, then S; both components now have coin 0 and sit at x=2 and x=0. (eq_3, eq_5)
4. Steps t=3,...,T-1: coin I everywhere followed by S; both components move right in parallel, at x=t and x=t-2. (eq_3, eq_5)
5. Step t=T=d+2: apply X on the coin controlled on position x=T-2 (the leading component), I elsewhere, then S; the components recombine at x=d with the coin in X|\phi\rangle. (eq_3, eq_5, eq_6)
6. Apply the known correction V^\dagger = X to the coin register (or absorb it into the receiver's basis relabelling) to recover |\phi\rangle at site d. (eq_4, eq_6)

## Assumptions

- No experiment_scope was supplied; the single-qubit line transfer with d=2, T=4 was chosen as the smallest useful instance and is not claimed to be the paper's protocol.
- Coin operators restricted to {I, X} as an interpretation of 'coin flippings'.
- Shift convention c=0 -> x+1, c=1 -> x-1; position register large enough to avoid wrap-around (positions -1..d+1).
- The known final correction V=X is allowed in the definition of perfect state transfer (transfer up to a fixed, input-independent unitary).

## Missing information

- How the paper encodes a two-qubit state in the walk (e.g. coin plus a position degree of freedom, or two walkers/coins) and the corresponding coin-flipping settings.
- The specific coin operators and their time/position schedule used in the paper for PST.
- The structure of the multi-dimensional network and the protocol for distributing an arbitrary multi-qubit entangled state between every pair of sites.
- The routing scheme (how paths/targets are selected by coin settings) and any resource counts (number of steps vs. distance/dimension).
- Any statements about robustness, measurement scheme, or physical implementation.
