# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Show how a classically controlled (adaptive) circuit on a kD nearest-neighbor grid can simulate an abstract-depth-d circuit with arbitrary pairwise gates in O(d) depth. The tiny scoped instance is a nonlocal CNOT between two logical qubits that sit at distant sites on a 1D line segment of the grid. The line is used as a stand-in routing path, which is the smallest case of the grid path routing. The gate is implemented by constant-depth entanglement swapping, gate teleportation and classical Pauli feed-forward.

Scope: Only the following is reconstructed: (a) a constant-depth Bell pair between the endpoints of a path of m+1 qubits via parallel Bell measurements and an XOR Pauli correction; (b) a nonlocal CNOT via that Bell pair, as local CNOTs, measurements and Pauli fixes; (c) the non-adaptive fanout lightcone bound as a counting statement. Outside this scope: full layer-by-layer routing and congestion resolution in k>=2 dimensions, Pauli-frame absorption by Clifford conjugation, the constant-depth Shor circuit, GHZ/fanout in constant depth, and the optimal Theta(n^(1/k)) non-adaptive construction in full.

## Symbols

- $k$: grid dimension; domain: integer, k>=2 in the paper; k=1 line used for the tiny instance
- $n$: number of logical qubits or fanout targets; domain: positive integer
- $m$: number of Bell-pair links along a routing path; domain: positive integer
- $t$: circuit depth; domain: positive integer
- $s_j$: outcome bit of the j-th Bell measurement (X-parity bit x_j, Z-parity bit z_j); domain: {0,1}
- $|\Phi^+\rangle$: Bell state (|00>+|11>)/\sqrt{2}; domain: two-qubit state
- $x_j,z_j$: swap measurement outcomes at the j-th intermediate site; domain: {0,1}

## eq_1: Bell pair

$$
|\Phi^+\rangle=\tfrac{1}{\sqrt2}(|00\rangle+|11\rangle)=\mathrm{CNOT}_{01}(H\otimes I)|00\rangle
$$

Short-range Bell pair preparation in constant depth, used for each link of the path.

Provenance: `standard_background`. Standard Bell state preparation.

Equation assumptions:

- Neighboring sites can interact via CNOT

## eq_2: Entanglement swapping correction

$$
\bigotimes_{j=1}^{m-1}(\text{Bell meas. on pair }j)\;:\;|\Phi^+\rangle^{\otimes m}\to (X^{\oplus_j x_j}Z^{\oplus_j z_j}\otimes I)|\Phi^+\rangle_{\text{ends}}
$$

All intermediate Bell measurements run in parallel; the end pair is Bell up to a Pauli whose exponents are the XOR of outcomes, computed classically. Depth is constant independent of m.

Provenance: `abstract_inferred`. Standard entanglement swapping combined with the sketch's parallel-path claim; the abstract only claims constant-depth simulation with classical control.

Abstract evidence: classical controller determines which local interactions to apply

Equation assumptions:

- Mid-circuit measurement and feed-forward cost zero depth
- Classical XOR is free

## eq_3: Nonlocal CNOT via Bell pair

$$
\mathrm{CNOT}_{a\to b}:\ \text{CNOT}_{a\to e_a},\ \text{measure }e_a\to u;\ X^{u}\text{ on }e_b;\ \text{CNOT}_{e_b\to b};\ H\text{ on }e_b,\text{ measure}\to v;\ Z^{v}\text{ on }a
$$

Standard gate teleportation of a CNOT using Bell pair halves e_a, e_b (a is the control, b is the target). Outcomes u,v drive the fixes. The ends e_a, e_b are first Pauli-corrected from eq_2.

Provenance: `standard_background`. Textbook nonlocal CNOT with one ebit; the paper's exact protocol is not given.

Equation assumptions:

- Bell pair is exact after correction

## eq_4: Fanout lightcone bound

$$
t^{k}\cdot c\ge n\ \Rightarrow\ t=\Omega(n^{1/k})
$$

A non-adaptive fanout from one control to n targets needs depth at least about n^(1/k) because the number of grid sites in the lightcone grows as O(t^k).

Provenance: `abstract_inferred`. Reading the abstract's k-th root of n as n^(1/k) and the lightcone argument from the sketch.

Abstract evidence: These circuits have depth Θ( k√n), size Θ(n) and width Θ(n).

Equation assumptions:

- Depth read as n^(1/k)
- c is a constant depending on k

## eq_5: Fanout action

$$
\mathrm{FAN}_n|c\rangle|x_1\ldots x_n\rangle=|c\rangle|x_1\oplus c,\ldots,x_n\oplus c\rangle
$$

Fanout is one control with n CNOT targets, so size Theta(n) with one CNOT per target.

Provenance: `standard_background`. Definition of fanout.

Equation assumptions:

- Bits computational basis

## Registers

- logical: 2 (control a and target b for the tiny instance) qubits; data qubits at distant sites
- path: 2m (m links, 2 qubits each; the endpoints e_a and e_b are among them) qubits; Bell-pair routing ancillas
- classical: 2(m-1)+2 qubits; swap outcomes plus gate-teleportation outcomes u,v

## Initial state

Logical qubits in an arbitrary test state (e.g. |+>|0> to give a Bell pair after the CNOT); all ancillas in |0>.

## Measurement

Mid-circuit Bell measurements on the intermediate qubits and the gate-teleportation measurements. Final check: the statevector or counts of the logical register after the corrections. Qiskit is little-endian: bit i is set by measure(i,i) and is the last character in counts keys.

## Classical postprocessing

XOR the swap outcomes to get the Pauli on the end pair, then compute the u,v fixes. The Pauli frame can be applied by classically conditioned gates or tracked.

## Algorithm steps

1. Prepare m Bell pairs on adjacent ancilla pairs along the path, in constant depth. (eq_1)
2. Perform parallel Bell measurements on the adjacent middle qubits, XOR the outcomes classically, and apply the resulting Pauli to one end (or track it in the frame). (eq_2)
3. Apply the teleported CNOT from a to b using the end qubits, with measurements and feed-forward fixes. (eq_3)
4. Verify that the output equals the ideal CNOT; for fanout, compare with the ideal action and check the n^(1/k) depth scaling. (eq_5, eq_4)

## Assumptions

- Tiny instance chosen: nonlocal CNOT over a 1D path with m=2 or 3, as an illustration
- Mid-circuit measurement and feed-forward are free in depth
- The controller computes the routing and corrections for free
- Ancillas start in |0>
- Depth is counted over quantum layers only
- Fanout depth read as n^(1/k)

## Missing information

- The exact routing and congestion resolution in k>=2
- How Pauli frames are absorbed by Clifford conjugation
- The constant-depth Shor and GHZ fanout construction details
- The optimal non-adaptive grid circuit layout
- Whether the simulator supports classically conditioned gates in this task
