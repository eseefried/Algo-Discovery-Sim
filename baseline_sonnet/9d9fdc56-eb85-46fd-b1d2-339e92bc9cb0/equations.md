# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Perfect state transfer (PST) between antipodal nodes of a discrete-time quantum walk (DTQW) on a modified cycle graph, here the tiny case C4 with a generic coin. The abstract's specific modifications, coin choices and graph families are not given.

Scope: Background-only DTQW on the unmodified cycle C4 (N=4) with a Grover coin, testing PST from node 0 to antipodal node 2 via fidelity. Outside scope: the specific modifications of C4/C6/C8, the three coin choices, the three generalised graph families, continuous-time walks, robustness tests (initial state variation, interpolation, decoherence).

## Symbols

- $N$: number of cycle nodes; domain: N=4 in the instance
- $|v,c\rangle$: walker at node v with coin/arc label c; domain: v in Z_N, c in {0,1}
- $C$: coin operator; domain: 2x2 unitary acting on the coin space
- $S$: shift operator; domain: unitary on C^N tensor C^2
- $U$: one-step walk operator; domain: unitary
- $t$: discrete time step; domain: nonnegative integers
- $F_t$: probability of finding the walker at the target node after t steps; domain: [0,1]
- $|\psi_0\rangle$: initial state; domain: unit vector

## eq_1: Walk operator

$$
U=S\,(I_N\otimes C),\quad S|v,c\rangle=|v+(-1)^c \bmod N,\,c\rangle
$$

One step of coined DTQW on the cycle: coin then shift, with c=0 moving forward and c=1 backward.

Provenance: `standard_background`. Standard DTQW definition on a cycle; the abstract's modified graphs are not specified.

Equation assumptions:

- Unmodified C4
- Moving-shift convention chosen here

## eq_2: Grover coin

$$
C=\begin{pmatrix}0&1\\1&0\end{pmatrix}
$$

The 2x2 Grover coin 2|s><s|-I with s uniform, which equals the Pauli X matrix.

Provenance: `assumption`. One example coin chosen as an assumption; the abstract's three coins are not named.

Equation assumptions:

- Grover coin on a degree-2 vertex

## eq_3: State evolution

$$
|\psi_t\rangle=U^t|\psi_0\rangle,\quad |\psi_0\rangle=|0,0\rangle
$$

Evolution from an assumed localized initial state at node 0.

Provenance: `assumption`. Concrete initial condition chosen for the tiny instance; the abstract mentions initial conditions only generally.

Equation assumptions:

- Initial coin state is |0>

## eq_4: Antipodal transfer fidelity

$$
F_t=\sum_{c\in\{0,1\}}|\langle N/2,c|\psi_t\rangle|^2
$$

Probability at the antipodal node 2 for N=4 after t steps.

Provenance: `abstract_inferred`. Inferred: PST between antipodal nodes means F_t=1 at some t; the exact definition used by the paper (e.g. including fixed coin state) is unknown.

Abstract evidence: perfect state transfer between antipodal nodes of discrete time quantum walks

Equation assumptions:

- Coin state ignored at the target

## eq_5: PST criterion

$$
\exists\, t>0:\ F_t=1
$$

Perfect state transfer occurs when the fidelity at the antipode reaches exactly 1.

Provenance: `abstract_inferred`. Inferred from the notion of PST as exact unit transfer probability; numerical tolerance is not in the abstract.

Abstract evidence: Perfect state transfer was found, in general, to be very rare

Equation assumptions:

- Exact equality, not approximation

## Registers

- position: 2 qubits (N=4) qubits; node label v in Z_4, binary encoded with v=2q1+q0
- coin: 1 qubit qubits; arc direction c; ordering: position register first, then coin

## Initial state

|0>_pos|0>_coin (assumed)

## Measurement

Measure the position register in the computational basis after t steps; estimate the probability of node 2.

## Classical postprocessing

Compare the estimated F_t with 1 over a range of t to detect PST or high-fidelity transfer.

## Algorithm steps

1. Prepare the initial state at node 0 with coin |0>. (eq_3)
2. Apply the coin C to the coin register, then the conditional shift S, and repeat t times. (eq_1, eq_2)
3. Compute the antipodal fidelity F_t for each t and check the PST criterion. (eq_4, eq_5)

## Assumptions

- Unmodified C4 used as the smallest instance
- Grover coin (Pauli X) and initial state |0,0> are chosen for illustration, not taken from the abstract
- Shift convention is a choice

## Missing information

- Actual modifications of C4, C6, C8 (added edges, loops, weights)
- The three coin operators
- Definitions of the three graph families
- Exact fidelity and initial-state definitions
- Decoherence model
- Continuous-time walk details
