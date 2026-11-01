# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Implement a single-qubit POVM (trine, SIC or unambiguous state discrimination) as a Naimark dilation by a coined discrete-time quantum walk on 3 qubits (1 polarisation/coin qubit plus 2 position qubits). The scoped instance is the trine POVM, and SIC and USD reuse the same structure with different target elements.

Scope: Smallest useful construction: the trine POVM with 3 outcomes on 3 qubits and no black-box queries. The isometry V is built from the target Kraus operators, completed to a unitary on (position, polarisation), and decomposed into u gates and controlled shifts. Outside scope: the optical implementation, a full gate-level SIC or USD angle solution, loss and noise, and paper-specific coin angles, none of which the abstract gives.

## Symbols

- $|\psi\rangle$: input polarisation state; domain: normalised vector in C^2
- $E_k$: POVM element for outcome k; domain: 2x2 positive semidefinite matrices summing to I
- $K_k$: rank-1 Kraus operator with K_k=\sqrt{w_k}|\phi_k\rangle\langle\phi_k|; domain: 2x2 complex matrices
- $V$: Naimark isometry V|\psi\rangle=\sum_k |k\rangle\otimes K_k|\psi\rangle; domain: C^2 -> C^N (x) C^2
- $|t_k\rangle$: trine states, half angles 0, \pi/3, 2\pi/3; domain: real unit vectors in C^2
- $C_1,C_2$: coin unitaries (wave-plate analogues); domain: U(2)
- $S,S_2$: polarisation-conditioned position shifts (beam-displacer analogues); domain: permutations on the position register
- $x,p$: final position label (2 bits) and polarisation bit; domain: x in {0..3}, p in {0,1}
- $a$: USD element weight 1/(1+|\langle\psi_1|\psi_2\rangle|); domain: (1/2,1]

## eq_1: POVM completeness and Born rule

$$
\sum_k E_k=I,\quad E_k=K_k^\dagger K_k,\quad P(k)=\langle\psi|E_k|\psi\rangle
$$

Defines the POVM and outcome probabilities.

Provenance: `standard_background`. Standard POVM definition; the abstract names POVMs but states no equation.

Equation assumptions:

- Rank-1 elements

## eq_2: Trine POVM

$$
E_k=\tfrac{2}{3}|t_k\rangle\langle t_k|,\ |t_k\rangle=\cos(k\pi/3)|0\rangle+\sin(k\pi/3)|1\rangle,\ k=0,1,2
$$

Three elements uniformly distributed on an equatorial great circle of the Bloch sphere.

Provenance: `abstract_inferred`. Uniform spacing on an equatorial circle gives 120-degree Bloch spacing. The weight 2/3 follows from completeness. The real-state basis choice is an assumption.

Abstract evidence: the POVM elements uniformly distributed on an equatorial plane of the Bloch sphere

Equation assumptions:

- Equator is the x-z plane, with real amplitudes

## eq_3: Naimark dilation by the walk

$$
|\Psi_{out}\rangle=S_2(I\otimes C_2)S(I\otimes C_1)\,|0\rangle_{pos}|\psi\rangle,\quad P(x,p)=|\langle x,p|\Psi_{out}\rangle|^2
$$

Two-step coined walk. Labels (x,p) map to outcomes k, with some grouped, so that P(k)=\sum_{(x,p)\in k}P(x,p)=\langle\psi|E_k|\psi\rangle.

Provenance: `assumption`. Proposed construction from the sketch; the coin angles are not given in the abstract.

Equation assumptions:

- Two steps suffice
- Angles solved numerically offline

## eq_4: Isometry condition

$$
V^\dagger V=\sum_k K_k^\dagger K_k=I
$$

The walk's first columns form an isometry. Complete V to a 3-qubit unitary and decompose it into u gates and controlled shifts.

Provenance: `standard_background`. Standard Naimark/Stinespring construction.

## eq_5: SIC and USD elements

$$
E_k=\tfrac12|s_k\rangle\langle s_k|\ (k=1..4);\ E_1=a|\psi_2^\perp\rangle\langle\psi_2^\perp|,\ E_2=a|\psi_1^\perp\rangle\langle\psi_1^\perp|,\ E_{inc}=I-E_1-E_2,\ a=\frac{1}{1+|\langle\psi_1|\psi_2\rangle|}
$$

Targets for the other two POVMs: tetrahedral SIC elements and equal-prior USD, whose success probability is 1-|<psi1|psi2>|.

Provenance: `standard_background`. Standard SIC and USD (Ivanovic-Dieks-Peres) results; the abstract only names them.

Equation assumptions:

- Equal priors
- Tetrahedral Bloch vectors

## Registers

- pol: 1 qubits; polarisation/coin qubit, qubit 0, input state |psi>
- pos: 2 qubits; walker position (qubits 1,2), starts at |00>

## Initial state

|0>_pos (x) |psi>_pol, with |psi> prepared by standard u/ry/rz gates

## Measurement

Measure position qubits and polarisation qubit. Little-endian: the counts key is pos bits then pol bit, with pol as the last character, classical bit 0.

## Classical postprocessing

Group the (x,p) counts into outcome labels, normalise to get P(k), and compare with <psi|E_k|psi> for several inputs. For USD, report the conclusive and inconclusive probabilities.

## Algorithm steps

1. Fix the target POVM (trine) and its Kraus operators, and prepare the input state |psi> on the polarisation qubit by u gates. (eq_1, eq_2)
2. Apply coin C1 followed by the conditional shift S (increment position if pol=1). (eq_3)
3. Apply coin C2 followed by the shift S2. Angles are solved numerically offline so the outcome channels realise the target K_k and the isometry condition holds. (eq_3, eq_4)
4. Measure all 3 qubits and map the (x,p) labels to POVM outcomes. Compare with the Born-rule targets, and with the SIC/USD targets if those variants are run. (eq_1, eq_2, eq_5)

## Assumptions

- 2 position qubits suffice for up to 4 outcomes
- Equal priors for the USD
- Shifts emulated by controlled increments
- Two to three steps suffice
- Total of 3 qubits and no black-box queries

## Missing information

- Actual coin angles and shift schedule from the paper
- Exact mapping of (x,p) labels to outcomes
- Orientation of the trine/SIC frames relative to the computational basis
- USD state pair
