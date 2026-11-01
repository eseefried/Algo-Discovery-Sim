# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a black box U_sigma|x>=|sigma(x)> for a permutation sigma of {0,1,2,3} on 2 qubits, output the parity (even/odd) of sigma using one query. Reconstructed as a 3-qubit Hadamard test with a fixed ququart probe state |phi>, then a classical lookup/threshold on P(0).

Scope: One tiny instance: 4-element permutations, a single controlled-U_sigma query, 3 qubits. The probe |phi> is a fixed state with phases found by an offline classical search over the 24 permutations. Out of scope: the photonic polarization x path implementation, the experimental fidelity analysis, the antisymmetric two-ququart variant, and any claim that this matches the paper's actual protocol.

## Symbols

- $\sigma$: hidden permutation of {0,1,2,3}; domain: S_4, 24 elements
- $U_\sigma$: permutation unitary on 2 qubits, U|x>=|sigma(x)>; domain: 4x4 permutation matrices
- $\mathrm{sgn}(\sigma)$: parity sign, +1 even and -1 odd; domain: {+1,-1}
- $|\phi\rangle$: fixed probe state on the ququart register, sum_x phi_x |x>; domain: unit vector in C^4
- $P_0(\sigma)$: probability of control outcome 0; domain: [0,1]
- $c(\sigma)$: Re<phi|U_sigma|phi>; domain: [-1,1]
- $x$: ququart integer, x = b_1*2 + b_0 with b_0 the least-significant qubit; domain: {0,1,2,3}

## eq_1: Parity as determinant

$$
\mathrm{sgn}(\sigma)=\det U_\sigma=\prod_k \lambda_k
$$

The parity of a permutation equals the determinant of its permutation matrix, i.e. the product of its eigenvalues.

Provenance: `standard_background`. Standard fact; the abstract only says the algorithm determines the parity of the permutation.

Equation assumptions:

- U_sigma is the permutation matrix on computational basis states

## eq_2: Hadamard-test outcome

$$
P_0(\sigma)=\tfrac12\left(1+\mathrm{Re}\langle\phi|U_\sigma|\phi\rangle\right)=\tfrac12(1+c(\sigma))
$$

Control in |+>, controlled-U_sigma on |phi>, H on control, then measure. P(0) is set by the real overlap.

Provenance: `standard_background`. Standard Hadamard test, used as a proposed single-query readout route. The abstract does not state it.

Equation assumptions:

- Controlled-U_sigma is available as exactly one query
- No extra phase is applied to the control

## eq_3: Overlap in amplitudes

$$
c(\sigma)=\mathrm{Re}\sum_{x}\overline{\phi_{\sigma(x)}}\,\phi_x
$$

The overlap computed classically from the probe amplitudes, used to tabulate expected P_0 for all 24 permutations.

Provenance: `standard_background`. Direct expansion of <phi|U|phi> for a permutation matrix.

Equation assumptions:

- phi_x are the amplitudes of |phi> in the computational basis

## eq_4: Separation requirement on the probe

$$
\{c(\sigma):\mathrm{sgn}(\sigma)=+1\}\cap\{c(\sigma):\mathrm{sgn}(\sigma)=-1\}=\emptyset
$$

The probe must give disjoint overlap values for even and odd permutations. The decision then uses a lookup table or threshold: parity is even if c lies in the even set, odd otherwise.

Provenance: `assumption`. Proposed design criterion. Existence of such a phi is not established here. A simple example phi_x=i^x/2 fails, because the even (01)(23) and the odd (02) both give c=0. A numerical search over generic complex phases is needed.

Equation assumptions:

- A single phi exists that separates all 24 permutations
- Otherwise use two probe states or a two-copy antisymmetric variant

## eq_5: Decision rule

$$
\hat c=2P_0-1,\quad \text{parity}=\begin{cases}\text{even}&\hat c\in C_{+}\\\text{odd}&\hat c\in C_{-}\end{cases},\quad C_\pm=\{c(\sigma):\mathrm{sgn}(\sigma)=\pm1\}
$$

Classical post-processing of the exact P_0 from the statevector: match c-hat to the precomputed sets, with tolerance ~1e-6.

Provenance: `assumption`. Follows from eq_2 and eq_4. A pure threshold only works if the sets are separated by an interval; otherwise use the table.

Equation assumptions:

- Exact probabilities from simulation
- Table built with the same phi

## Registers

- ctrl: 1 qubit qubits; Hadamard-test control, qubit 0, measured into classical bit 0
- sys: 2 qubits qubits; ququart register, qubits 1 and 2, with x = b_1*2 + b_0 (qubit 1 is least significant); holds |phi> and the black box target

## Initial state

|0>_ctrl |00>_sys

## Measurement

Measure ctrl only, into classical bit 0. The decision uses P(0) from the counts, or from exact probabilities in the simulator.

## Classical postprocessing

Offline: enumerate the 24 permutations, compute c(sigma), and verify eq_4 for the chosen phi. Online: c-hat=2P0-1, then look up the parity.

## Algorithm steps

1. Apply H to ctrl. (eq_2)
2. Prepare |phi> on sys from |00> with standard gates (Ry, CX, P/RZ), using the phases found by offline search. (eq_3, eq_4)
3. Place one controlled-U_sigma placeholder (control ctrl, targets the 2 sys qubits). This is the only query. (eq_2)
4. Apply H to ctrl and measure it into classical bit 0 (counts key last character). Do not measure sys. (eq_2)
5. Classically compute c-hat = 2 P(0) - 1 and decide parity by comparison with the precomputed sets. (eq_5)

## Assumptions

- The 4-element permutation acts on the computational basis of 2 qubits
- A controlled version of the black box is available at the cost of one query
- A single probe phi separating even from odd by overlap exists and is found by classical search; this is unverified here
- Statevector simulation gives exact P(0)
- The qubit count is 3 (the 5-qubit two-copy variant is not specified)
- The control and ququart ordering is as given in registers

## Missing information

- The paper's actual state-preparation and permutation encoding, and how it reads the parity in one step
- An explicit phi with verified separation
- Whether the paper uses a controlled oracle or an uncontrolled one
- Details of the antisymmetric or two-copy variant
