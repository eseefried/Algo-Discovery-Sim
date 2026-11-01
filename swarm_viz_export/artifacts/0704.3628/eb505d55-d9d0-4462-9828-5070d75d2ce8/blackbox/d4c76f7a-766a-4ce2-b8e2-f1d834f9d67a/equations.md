# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Evaluate the balanced depth-2 NAND formula f(x)=NAND(NAND(x1,x2),NAND(x3,x4)) for explicit classical x in {0,1}^4 via a discrete-time coined quantum walk on a tree with tail, x compiled into gates. The abstract's O(sqrt N) balanced-formula bound is the motivating goal; the general O(N^(1/2+O(1/sqrt(log N)))) bound is out of scope.

Scope: Only the N=4 balanced instance. The circuit is the unitary U_x^T on a fixed 8-vertex graph. It is a walk-dynamics demonstration whose output is not shown to decode f(x). The decode statistic and threshold are NOT validated; the paper's actual construction is not reconstructed, and no black-box query claim is made.

## Symbols

- $x$: input bits, compiled into gates; domain: {0,1}^4
- $f(x)$: formula value; domain: {0,1}
- $|v,s\rangle$: walker at vertex v in edge slot s; domain: v in 0..7 (0 tail, 1 root, 2 and 3 internal, 4..7 leaves), s in 0..3 (slot 3 unused)
- $S_x$: flip-flop shift swapping |u,s_u> with |v,s_v> across each present edge (u,v); domain: permutation unitary
- $C_v$: Grover coin on the used slots of v, with degree computed from the x-dependent edge set; phase -1 on a degree-1 vertex slot; domain: unitary
- $T$: number of walk steps; domain: positive integer; heuristic T~ceil(pi*sqrt(N)/2)=4 for N=4, uncalibrated
- $p$: return probability to |t,0>; domain: [0,1]

## eq_1: Formula

$$
f(x)=\neg\big(\neg(x_1\wedge x_2)\wedge\neg(x_3\wedge x_4)\big)=(x_1\wedge x_2)\vee(x_3\wedge x_4)
$$

Depth-2 balanced NAND tree, with NAND(a,b)=not(a and b). The NAND of two NANDs equals the OR of the two ANDs.

Provenance: `standard_background`. Boolean identity for the chosen smallest instance.

Equation assumptions:

- N=4

## eq_2: Walk step

$$
U_x=S_x\,C_x,\quad C_x=\bigoplus_{v}C_v(x),\quad C_v=2|s_v\rangle\langle s_v|-I\ \text{on used slots},\ |s_v\rangle=\tfrac{1}{\sqrt{\deg v}}\sum_{s\ \text{used}}|s\rangle
$$

Coin at each vertex over its used slots, then flip-flop shift. Absent-leaf convention: a leaf with x_i=0 is disconnected, so its parent's slot for it is UNUSED (degree reduced) and the leaf vertex acts as identity on its isolated state; the leaf is never reached. This removes the earlier inconsistency.

Provenance: `assumption`. Standard coined-walk form adapted from the sketch; not the paper's exact walk. Used slots are derived from x consistently for both parent and leaf.

Equation assumptions:

- x-dependent edge set compiled classically
- A leaf is present iff x_i=1
- Unused slots untouched
- Degree-1 vertices get coin -1
- Tail is a single edge, too short for a real scattering analysis

## eq_3: Initial state

$$
|\psi_0\rangle=|t,0\rangle=|v=0,s=0\rangle
$$

The walker starts at the tail vertex in its only used slot, pointing to the root. This is the all-zero computational basis state.

Provenance: `assumption`. Start must be a used slot.

Equation assumptions:

- Little-endian: slot occupies low 2 qubits, vertex the high 3 qubits

## eq_4: Evolution

$$
|\psi_T\rangle=U_x^{T}|\psi_0\rangle,\quad T=O(\sqrt N)
$$

State after T walk steps.

Provenance: `abstract_inferred`. The sqrt(N) bound suggests T=O(sqrt N) steps, each using one x-dependent operation.

Abstract evidence: O(√N) discrete query quantum algorithm for evaluating balanced binary NAND formulas

Equation assumptions:

- One x-dependent operation per step

## eq_5: Decode statistic

$$
p=|\langle t,0|\psi_T\rangle|^2,\quad \hat f=\mathbb{1}[p>\theta]\ \text{(sign convention unverified)}
$$

Return probability compared with a threshold; the sketch associates reflection with f=1. No validated theta exists. Decoding is offline classical postprocessing, not part of the unitary.

Provenance: `assumption`. From the sketch only. If no theta and T separate all 16 inputs, the circuit is only a dynamics demo.

Equation assumptions:

- theta and T must be found by simulation over all 16 inputs
- Near-zero energy is not guaranteed by this finite construction

## Registers

- vertex: 3 qubits qubits; vertex index 0..7: 0 tail, 1 root, 2 and 3 internal, 4..7 leaves
- slot: 2 qubits qubits; edge slot at the vertex: 0 parent/tail direction, 1 and 2 child directions, 3 unused

## Initial state

|t,0> = all-zero state of 5 qubits (vertex=0, slot=0); little-endian with slot in the low qubits.

## Measurement

None inside the unitary. For analysis, the probability of basis state |t,0> is computed from the final state.

## Classical postprocessing

Threshold p at a theta calibrated by simulation over all 16 inputs. No calibration is supplied here. If no theta separates the inputs, the circuit is only a walk-dynamics demo and does not demonstrably compute f(x).

## Algorithm steps

1. Take the all-zero state as |t,0>. (eq_3)
2. Apply the coin C_x, using degrees derived from x (absent leaves reduce parent degree, and the leaf is isolated), then the flip-flop shift S_x over present edges. (eq_2)
3. Repeat for T steps. (eq_4)
4. Offline, compute p and compare it to a calibrated theta to give a candidate f(x). This is unvalidated, and f(x) is the reference value. (eq_5, eq_1)

## Assumptions

- Scope limited to depth-2 balanced N=4
- x is compiled into gates, so no black-box query claim
- Absent-leaf handling: leaf disconnected and parent slot unused
- T and theta are uncalibrated free choices

## Missing information

- The paper's exact walk, weights and phase-estimation or scattering procedure
- Validated T and threshold
- A longer tail and the energy-near-zero analysis
- Rebalancing for arbitrary formulas
