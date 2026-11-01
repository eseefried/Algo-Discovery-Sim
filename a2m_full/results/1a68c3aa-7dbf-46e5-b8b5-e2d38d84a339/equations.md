# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate MaxCut on small unweighted regular graphs G=(V,E), n=|V|, m=|E|, using p-layer QAOA with parameters (gamma,beta) and Z-basis readout.

Scope: Build the p-layer QAOA circuit (p=1..3) on n qubits for a tiny explicit instance (for example the 3-regular K4 graph or a 2-regular ring), with no ancillas. Compute <C> from the statevector or counts, and take the best sampled cut. Out of scope: the proof of the 0.6924 bound, the closed-form p=1 edge expectation for 3-regular graphs, the large-p strategy, and the explicit classical preprocessing based on local subgraphs for large graphs.

## Symbols

- $G=(V,E)$: unweighted graph, vertex i maps to qubit i; domain: n=|V| small, m=|E|
- $p$: number of QAOA layers; domain: integer >=1
- $\gamma_l,\beta_l$: phase-separator and mixer angles of layer l; domain: real numbers
- $C$: MaxCut objective operator, diagonal in the Z basis; domain: Hermitian operator on n qubits
- $B$: mixer Hamiltonian, the sum of X_i; domain: Hermitian operator on n qubits
- $z$: bitstring, with z_i the bit of vertex i; domain: {0,1}^n

## eq_1: MaxCut objective

$$
C=\sum_{(i,j)\in E}\frac{1-Z_iZ_j}{2},\quad C(z)=\sum_{(i,j)\in E}[z_i\ne z_j]
$$

C counts the cut edges. Each term acts on 2 qubits.

Provenance: `standard_background`. Standard MaxCut Hamiltonian. The abstract only says the gate locality is at most that of the objective.

Equation assumptions:

- unweighted graph

## eq_2: QAOA state

$$
|\gamma,\beta\rangle=\prod_{l=p}^{1}e^{-i\beta_l B}e^{-i\gamma_l C}\,H^{\otimes n}|0\rangle^{\otimes n}
$$

Start from |+>^n. Layer l applies the phase separator and then the mixer, with layer 1 applied first.

Provenance: `standard_background`. Standard QAOA ansatz, consistent with the abstract's integer p and its circuit of local unitaries.

Equation assumptions:

- B=\sum_i X_i

## eq_3: Gate decomposition

$$
e^{-i\gamma(1-Z_iZ_j)/2}\simeq \mathrm{RZZ}(\gamma)_{ij}=CX_{ij}\,RZ_j(\gamma)\,CX_{ij}\ (\text{up to global phase});\quad e^{-i\beta X_i}=RX_i(2\beta)
$$

Qiskit gates for each edge term and each mixer term. RZZ(theta)=exp(-i theta ZZ/2), so the e^{-i gamma C} edge term gives RZZ(-gamma) up to a global phase. The sign of the angle depends on the convention, so the angle sign must be checked in the builder.

Provenance: `standard_background`. The gate count is O(p*m), which matches the abstract's claim that depth is linear in p times the number of constraints.

Equation assumptions:

- The sign convention is fixed so that maximizing <C> gives the largest cut

## eq_4: Expected cut and readout

$$
F_p(\gamma,\beta)=\langle\gamma,\beta|C|\gamma,\beta\rangle=\sum_{(i,j)\in E}\frac{1-\langle Z_iZ_j\rangle}{2},\quad \text{best}=\max_{z\in\text{samples}}C(z)
$$

Estimate <C> from the statevector or from counts, or keep the best sampled cut. In a Qiskit counts key, vertex i is bits[::-1][i].

Provenance: `abstract_inferred`. The abstract implies an approximation quality measured by the objective. The estimator itself is the standard one.

Abstract evidence: The algorithm depends on an integer $p\geq 1$ and the quality of the approximation improves as $p$ is increased.

Equation assumptions:

- Z-basis measurement

## eq_5: 2-regular ring ratio

$$
\frac{\langle C\rangle}{m}=\frac{2p+1}{2p+2}
$$

Known result for rings of large girth, recalled from background. It is not stated in the abstract and can serve as a sanity check for a large ring.

Provenance: `standard_background`. Recalled from the QAOA literature, not verified. It holds for rings with n>2p+1.

Equation assumptions:

- ring length n>2p+1

## Registers

- q: n qubits; one qubit per vertex, no ancillas

## Initial state

|0>^n, then H on every qubit, giving |+>^n

## Measurement

Measure all n qubits in the Z basis only if counts are required. Otherwise read the statevector without measurements. Qiskit little-endian order applies, so vertex i is bits[::-1][i].

## Classical postprocessing

Evaluate the cut of each sampled bitstring and keep the maximum, or compute F_p. Optimize (gamma, beta) by a classical grid search, using the full small-graph simulation as a stand-in for the local-subgraph evaluation.

## Algorithm steps

1. Apply H to every qubit. (eq_2)
2. For l=1..p, apply RZZ-type phase gates on every edge using gamma_l. (eq_1, eq_3)
3. For l=1..p, apply RX(2*beta_l) on every qubit after the phase layer. (eq_2, eq_3)
4. Read the statevector or measure all qubits. Compute <C> or the best sampled cut. The angles come from a classical grid search or optimization on F_p. (eq_4)

## Assumptions

- The instance is a tiny unweighted regular graph, chosen by the builder.
- p is between 1 and 3.
- The angle sign and RZZ convention are fixed by the builder so that maximizing <C> gives the largest cut.
- n is within the qubit cap.

## Missing information

- The explicit p=1 closed-form edge expectation for 3-regular graphs is not given.
- The optimal angles are not given.
- The large-p strategy is not specified.
- The detailed classical preprocessing method is not specified.
