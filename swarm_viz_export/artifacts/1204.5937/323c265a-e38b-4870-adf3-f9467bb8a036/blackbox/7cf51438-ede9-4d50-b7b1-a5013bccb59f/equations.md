# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Discrete-time Grover-coined flip-flop quantum walk on the plain 4-cycle C4, built as a unitary U = S C on a 2-qubit position register and a 2-qubit coin register. The goal is to check whether the antipodal node 2 is reached with probability 1 from the arc state at node 0. This is the smallest building block of the abstract's study of antipodal perfect state transfer (PST) on modified C4/C6/C8 graphs.

Scope: Only the plain unmodified C4 with the Grover coin G_2 and the flip-flop shift, with initial arc state |0,0> and t = 1..4. The abstract's modified graphs (chords, extra nodes) are not specified in the abstract and are not constructed. Also outside scope: C6, C8, the other coin choices, the three generalised graph families, continuous-time walks, initial-state robustness, interpolation, and decoherence. The circuit yields only the unitary; evaluating P_t is external analysis. No black-box query claims are made.

## Symbols

- $v$: node index of C4; domain: {0,1,2,3}
- $c$: coin/arc label at a node; c=0 is the arc to v+1 mod 4, c=1 is the arc to v-1 mod 4; c=2,3 are unused padding; domain: {0,1,2,3}
- $U$: one-step walk unitary U = S C; domain: 16x16 unitary
- $C$: Grover coin applied at each node on the used arc subspace; domain: unitary, identity on padding coin states
- $S$: flip-flop shift, arc (v,w) to arc (w,v); domain: permutation on 16 basis states
- $P_t$: probability of being at the antipodal node 2 after t steps; domain: [0,1]
- $d$: node degree; d=2 on plain C4; domain: positive integer

## eq_1: Initial arc state

$$
|\psi_0\rangle=|v{=}0\rangle_P\otimes|c{=}0\rangle_C=|0,0\rangle
$$

Arc at node 0 pointing to neighbour 1, prepared from |0000> with no gates since the binary encoding of 0,0 is all zeros.

Provenance: `assumption`. Chosen as the tiny instance; the abstract does not give the initial state. The sketch's X gates are unnecessary under this labelling.

Equation assumptions:

- Basis ordering |v,c> with position qubits first, integer encoding of v and c in binary

## eq_2: Grover coin

$$
G_d=2|s_d\rangle\langle s_d|-I_d,\quad |s_d\rangle=\tfrac{1}{\sqrt d}\sum_{c<d}|c\rangle,\quad G_2=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad C=\sum_v |v\rangle\langle v|\otimes (G_2\oplus I_2)
$$

Grover coin on each node's d-dimensional arc space; for C4, d=2 so it is X on c in {0,1}, with padding states c=2,3 left unchanged.

Provenance: `standard_background`. Standard Grover coin. The abstract mentions three coin choices but does not name them; Grover is taken from the method plan.

Equation assumptions:

- Grover coin is one of the paper's three coins (unverified)

## eq_3: Flip-flop shift on C4

$$
S|v,0\rangle=|v{+}1 \bmod 4,\,1\rangle,\quad S|v,1\rangle=|v{-}1 \bmod 4,\,0\rangle,\quad S|v,c\rangle=|v,c\rangle\ (c=2,3)
$$

Flip-flop shift mapping arc (v,w) to the reversed arc (w,v), expressed in the label convention.

Provenance: `assumption`. Derived from the stated label convention (c=0 to v+1, c=1 to v-1); the reverse of the arc v to v+1 is the arc v+1 to v, which has label 1 there.

Equation assumptions:

- Padding states fixed by identity so S is a permutation of all 16 states

## eq_4: Step and evolution

$$
U=SC,\quad U|v,0\rangle=|v{-}1,0\rangle,\quad U|v,1\rangle=|v{+}1,1\rangle,\quad |\psi_t\rangle=U^t|\psi_0\rangle
$$

On C4 the Grover flip-flop walk reduces to ballistic motion with a fixed coin label, so U^4 = I on the used subspace. From |0,0>, U^2|0,0>=|2,0>.

Provenance: `assumption`. Direct computation from eq_2 and eq_3: C maps c=0 to c=1, then S moves v to v-1 with label 0.

Equation assumptions:

- Plain C4 with no modification

## eq_5: Antipodal probability

$$
P_t=\sum_{c}\left|\langle 2,c|U^t|\psi_0\rangle\right|^2,\quad \text{PST at } t \iff P_t=1
$$

Probability at the antipodal node 2; PST is declared when P_t equals 1 exactly. For plain C4 from |0,0>, P_2=1.

Provenance: `abstract_inferred`. The abstract studies antipodal PST; the probability form is the standard way to test it. The strict form (transfer to a specific arc state) is a stricter variant that is not used here.

Abstract evidence: perfect state transfer between antipodal nodes of discrete time quantum walks

Equation assumptions:

- PST defined as unit probability at node 2 for some t

## Registers

- pos: 2 qubits qubits; node index v in {0,1,2,3}, binary integer encoding, qubits 0-1
- coin: 2 qubits qubits; arc label c in {0..3}, binary integer encoding, qubits 2-3; only c=0,1 used on C4

## Initial state

|v=0>|c=0> = |0000>, the arc from node 0 toward node 1.

## Measurement

No measurement in the circuit. The simulated final state is analysed externally for the probability on node 2, i.e. the position register equals 10 (binary).

## Classical postprocessing

Compute P_t = sum over coin values of |amplitude at (v=2,c)|^2 for each t and flag PST when P_t = 1 within numerical tolerance.

## Algorithm steps

1. Prepare |0,0>, which is the all-zero state (no gates). (eq_1)
2. Build U = S C as an explicit 16x16 unitary from classical adjacency data: first the block-diagonal Grover coin (X on the coin LSB acting only on c in {0,1}, identity for c=2,3), then the flip-flop permutation. Compile the permutation and coin into standard gates, and repeat U for t steps (t=1..4). (eq_2, eq_3, eq_4)
3. External analysis: compute P_t from the simulated statevector and check P_t=1 (expected at t=2 for plain C4). (eq_5)

## Assumptions

- Chosen smallest instance: plain C4, Grover coin, flip-flop shift, initial arc state |0,0>.
- Modified graphs (chords, extra nodes) are not constructed because the abstract does not specify them.
- The coin used is assumed to match one of the paper's three coins; this is unverified.
- The walk on plain C4 is trivially ballistic, so this instance demonstrates PST mechanics but not the paper's nontrivial modified-graph results.

## Missing information

- The specific modifications of C4/C6/C8 that preserve PST
- The three coin operators used in the paper
- The exact definition of the shift used in the paper
- Definitions of the three generalised graph families
- Initial states, decoherence model, and interpolation scheme
