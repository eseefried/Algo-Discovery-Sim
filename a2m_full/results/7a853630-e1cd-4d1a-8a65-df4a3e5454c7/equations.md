# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Perfect transfer of an unknown two-qubit state across a small qubit chain by a mirror-symmetric XX+YY (Christandl/Krawtchouk) evolution, used as a stand-in for the abstract's discrete-time quantum walk with coin flips. Verified by an undo-preparation fidelity check. No black box, so zero queries.

Scope: One instance: chain of N=4 site qubits (optionally up to 6), two-qubit state on sites 0,1 transferred to sites N-1,N-2, no ancillas. Outside scope: the actual coined-walk construction, multi-dimensional hypercube distribution to every pair, multi-qubit entangled state distribution, and routing by stopping times. These are sketched only as extensions.

## Symbols

- $N$: number of site qubits in the chain; domain: integer, 4 to 8 (instance N=4)
- $J_j$: coupling on bond (j,j+1); domain: positive reals, j=1..N-1
- $H$: XX+YY chain Hamiltonian; domain: operator on (C^2)^{\otimes N}
- $t$: total evolution time; domain: real, t=\pi/2 in units where J_j=\sqrt{j(N-j)}
- $U_{prep}$: standard-gate circuit preparing the test two-qubit state from |00>; domain: unitary on 2 qubits
- $F$: transfer fidelity; domain: [0,1]

## eq_1: Chain Hamiltonian

$$
H=\frac{1}{2}\sum_{j=1}^{N-1}J_j\,(X_jX_{j+1}+Y_jY_{j+1}),\quad J_j=\sqrt{j(N-j)}
$$

Engineered-coupling XX chain with Krawtchouk profile, sites indexed 1..N here. Bond terms XX and YY commute on one bond, so each bond is exactly RXX*RYY. Different bonds do not commute, so a full evolution needs Trotter steps or the exact spin-J rotation property.

Provenance: `standard_background`. Christandl et al. perfect-state-transfer chain, recalled from background. It is not stated in the abstract.

Equation assumptions:

- Nearest-neighbor XX+YY coupling
- Single-excitation subspace acts as a spin-(N-1)/2 J_x rotation

## eq_2: Mirror transfer

$$
e^{-iHt}\big|_{t=\pi/2}\,|j\rangle=e^{i\phi_j}|N+1-j\rangle,\quad \phi_j=\phi_0+j\pi/2
$$

In the one-excitation sector, the evolution maps site j to site N+1-j up to phases. Phases are corrected locally by Z rotations. Sector phases are consistent for multi-excitation sectors by free-fermion structure (Jordan-Wigner).

Provenance: `standard_background`. Known PST property. Sign and phase conventions must be verified numerically. The phase is linear in j, so it is correctable by S-type gates on the output sites.

Equation assumptions:

- Time unit matches eq_1 so that the Hamiltonian rotation angle at time t is pi over the spin-J rotation
- Jordan-Wigner string signs are handled by checking numerically

## eq_3: Bond gate

$$
B_j(\tau)=\mathrm{RXX}(\theta_j)\,\mathrm{RYY}(\theta_j)=e^{-i\theta_j(XX+YY)/2},\quad \theta_j=J_j\,\tau
$$

Circuit gate for each bond for a Trotter step of duration tau. With r steps, tau=t/r, applied in a bond-layer order. Qiskit RXX(theta)=exp(-i theta XX/2).

Provenance: `assumption`. Concrete gate realization from the sketch. Trotter error is nonzero unless r is large. For N=4, instead use a free-fermion/numerical decomposition or large r, since the circuit is only small.

Equation assumptions:

- Trotter error is tolerated, or the evolution is compiled exactly by other means

## eq_4: Overall transfer with relabeling

$$
|\psi\rangle_{0,1}\otimes|0\rangle^{N-2}\;\mapsto\;(Z\text{-phase corr.})\,|\psi\rangle_{N-1,N-2}\otimes|0\rangle^{N-2}
$$

The output on sites N-1,N-2 holds the input state with qubit order reversed. Reading the output with the order swapped gives the original state.

Provenance: `abstract_inferred`. The abstract claims two-qubit state transfer. The mirror order reversal is inferred from the chain sketch, not from the abstract.

Abstract evidence: perfect state transfer of an arbitrary unknown two-qubit state

Equation assumptions:

- Mirror-symmetric chain
- Initial state on the remaining sites is all-zero

## eq_5: Fidelity readout

$$
F=\big|\langle 00|U_{prep}^{\dagger}\,\langle\text{tr. out}|\ldots\big|^2=P(\text{out sites}=00)
$$

After evolution, apply U_prep^dagger on the output sites with the order swapped and phase corrections. Measure those two sites. P(00) equals F, which should be near 1. Other sites should be 0 and need not be measured.

Provenance: `assumption`. Standard undo-preparation test from the sketch.

Equation assumptions:

- Input state is pure, prepared by U_prep from |00>
- Measure only output bits, mapping Qiskit little-endian bit i to the qubit measured into bit i

## Registers

- site: N (4 for the instance) qubits; chain qubits. Sites 0,1 at the input end hold the state, sites N-2,N-1 are the output.

## Initial state

U_prep on sites 0,1 from |00>, all other sites |0>.

## Measurement

Measure only the two output site qubits N-2 and N-1 after U_prep^dagger. The all-zero probability is the fidelity. Check bit order in the little-endian counts key.

## Classical postprocessing

Estimate F as the fraction of 00 outcomes. If a statevector is read, compute the overlap directly.

## Algorithm steps

1. Prepare a random two-qubit state on sites 0,1 with a standard gate circuit U_prep. (eq_5)
2. Apply r Trotter steps of the bond gates with couplings J_j over total time pi/2. Use brickwork ordering of odd and even bonds. (eq_1, eq_3, eq_2)
3. Apply local Z/S phase corrections on the output sites and relabel the order (the mirror reverses it). (eq_2, eq_4)
4. Apply U_prep^dagger on the output sites with the swapped order, then measure those two qubits. (eq_5)

## Assumptions

- Chosen construction: spin-chain PST replaces the coined walk, which is not given in the abstract.
- N=4 as the smallest instance.
- Phase corrections are found numerically by a calibration, not given in the abstract.
- Zero queries because there is no black box.

## Missing information

- Actual coin-flip walk operators and their settings
- Hypercube/grid distribution to all pairs and multi-qubit entangled state distribution
- Routing stopping times
- Exact phase-correction schedule and exact time units
