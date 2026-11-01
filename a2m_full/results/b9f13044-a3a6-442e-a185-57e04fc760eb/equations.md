# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Synthesize the 3-qubit Toffoli (CCX) gate on a linear nearest-neighbor chain q0-q1-q2 (q2 target) as a single optimized parameterized block, with parameters found by global optimization (Differential Evolution), up to global phase. The abstract reports a pulse-level 99.9% fidelity construction for three transmons; the circuit-level version here is a proxy.

Scope: Circuit-level proxy only: 3 qubits, no ancillas, L layers of single-qubit u rotations plus entanglers on pairs (0,1) and (1,2) only, parameters optimized offline by DE to maximize |Tr(CCX^dag U)|/8, then hardcoded. Out of scope: transmon Hamiltonian pulse optimization, 3-level truncation, leakage penalty, decoherence, the paper's enhanced non-greedy DE details, and the reported 99.9% fidelity and timing.

## Symbols

- $U(\theta)$: 3-qubit unitary of the parameterized circuit; domain: U(8)
- $\theta$: vector of circuit parameters (u angles); domain: R^{3*3*(L+1)}, angles in [0,2pi)
- $L$: number of entangling layers; domain: positive integer, assumed small (e.g. 3 to 6 layers; at least 6 CX-equivalents is the known exact decomposition count)
- $U_{CCX}$: Toffoli target unitary, flips q2 iff q0=q1=1; domain: permutation matrix in U(8)
- $F$: trace overlap fidelity; domain: [0,1]
- $H(t)$: pulse-level transmon Hamiltonian (background model); domain: Hermitian operators on 3 transmons with 3 levels each

## eq_1: Toffoli action

$$
U_{CCX}|x_0 x_1 x_2\rangle=|x_0\,x_1\,x_2\oplus(x_0 x_1)\rangle
$$

Target gate action on computational basis states, x_0 and x_1 controls, x_2 target.

Provenance: `standard_background`. Definition of the Toffoli gate named in the abstract (controlled-controlled-NOT).

Equation assumptions:

- Qubit labelling: q0,q1 controls, q2 target; Qiskit little-endian index = x0+2x1+4x2

## eq_2: Circuit ansatz

$$
U(\theta)=\prod_{l=L}^{1}\Big[E_{12}E_{01}\,\big(\otimes_{i=0}^{2}u(\theta_{l,i})\big)\Big]\cdot\otimes_{i}u(\theta_{0,i})
$$

Layered ansatz of single-qubit u gates and nearest-neighbor entanglers (cx or cz) only on pairs (0,1) and (1,2).

Provenance: `assumption`. Proposed circuit-level stand-in for the pulse sequence; entangler choice and L are not from the abstract.

Equation assumptions:

- Entanglers E are cx or cz; no 0-2 interaction

## eq_3: Trace fidelity

$$
F(\theta)=\frac{|\mathrm{Tr}(U_{CCX}^\dagger U(\theta))|}{8}
$$

Global-phase-insensitive overlap between synthesized and target unitaries.

Provenance: `standard_background`. Standard gate fidelity measure; the abstract only reports a fidelity of 99.9%, not this formula.

Equation assumptions:

- No leakage in the qubit-only circuit

## eq_4: DE cost

$$
\theta^*=\arg\min_\theta\,[1-F(\theta)]
$$

Optimization objective solved offline by Differential Evolution with restarts.

Provenance: `abstract_inferred`. The abstract says gate parameters come from DE optimal control; the specific cost is inferred.

Abstract evidence: The gate is achieved by a non-greedy quantum control procedure using our enhanced version of the Differential Evolution algorithm.

Equation assumptions:

- Cost is infidelity; the pulse-level version would add a leakage penalty

## eq_5: DE trial update

$$
v=\theta_a+F_s(\theta_b-\theta_c),\quad u_j=\begin{cases}v_j&r_j<CR\\ \theta_{j}&\text{otherwise}\end{cases}
$$

Standard DE/rand/1/bin mutation and crossover. The enhanced version differs by accepting some worse trials, adaptive F_s and CR, and restarts.

Provenance: `standard_background`. Textbook DE; the paper's enhancements are not specified in the abstract.

Equation assumptions:

- F_s is the scale factor

## Registers

- q: 3 qubits; q0 and q1 controls, q2 target, chain 0-1-2, no ancillas

## Initial state

Check on each computational basis input |x0 x1 x2>, or take the full unitary; no measurement for unitary checks.

## Measurement

None for unitary or statevector tasks; if counts are required, measure all 3 qubits on basis inputs and expect x2 xor (x0 and x1).

## Classical postprocessing

Compute F=|Tr(U_CCX^dag U)|/8 and compare statevector outputs to eq_1 up to global phase.

## Algorithm steps

1. Fix L, the entangler type, and the bounds on the parameters. (eq_2)
2. Run DE offline to minimize 1-F and hardcode theta*. (eq_3, eq_4, eq_5)
3. Build the circuit from standard u and cx gates with only 0-1 and 1-2 entanglers. (eq_2)
4. Verify against CCX through the unitary or the statevector on all 8 basis inputs. (eq_1, eq_3)

## Assumptions

- Circuit-level proxy replaces the transmon pulse model
- Decoherence and leakage are ignored
- The DE result is hardcoded
- Small L is enough to reach near-unit fidelity; exact CCX needs a sufficiently expressive ansatz

## Missing information

- Actual DE hyperparameters and enhancement details
- Pulse shapes, number of slices, and device parameters
- Numerical optimal parameters
- Whether a nearest-neighbor 3-qubit ansatz of small depth reaches F=1 exactly
