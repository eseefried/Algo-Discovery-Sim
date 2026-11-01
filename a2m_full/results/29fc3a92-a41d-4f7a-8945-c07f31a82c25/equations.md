# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate the reduced BCS/Richardson pairing Hamiltonian on N pair-level qubits (hard-core bosons / pseudospins) via Trotterization, optionally prepare the ground state adiabatically, and read out eigenenergies by Trotterized quantum phase estimation.

Scope: One tiny instance: N=3 pair levels (assumed eps_j = j, G=0.5 rescaled), first-order Trotter, QPE with t=4 ancillas, reference state with one pair (one qubit flipped). The paper's other algorithms for different native Hamiltonians (Ising/XY/other), fidelity studies, and complexity comparisons are outside scope beyond a gate-count note. The exact paper algorithms are not specified in the abstract.

## Symbols

- $N$: number of pair levels = system qubits; domain: integer, 3 or 4
- $t$: number of QPE ancilla qubits; domain: integer, 4 or 5
- $\epsilon_j$: single-particle level energy; domain: real
- $G$: pairing strength; domain: real, G>0
- $P_j^+$: pair creation at level j, hard-core boson (sigma^+_j); domain: operator
- $\delta t$: Trotter step / QPE base time after rescaling; domain: real > 0
- $r$: number of Trotter steps per U; domain: integer >= 1
- $\phi$: measured phase fraction; domain: [0,1)
- $s$: adiabatic schedule parameter; domain: [0,1]

## eq_1: Pairing Hamiltonian

$$
H=\sum_j \epsilon_j n_j - G\sum_{j,k}P_j^+P_k
$$

Reduced pairing Hamiltonian with pair levels as hard-core bosons.

Provenance: `abstract_inferred`. The abstract names pairing Hamiltonians; the explicit BCS form is background and from the sketch, not the abstract.

Abstract evidence: we propose a complete set of algorithms for simulating pairing Hamiltonians

Equation assumptions:

- Standard reduced BCS form
- Blocked levels removed

## eq_2: Qubit form

$$
H=\sum_j \frac{\epsilon_j}{2}(1-Z_j)-\frac{G}{2}\sum_{j<k}(X_jX_k+Y_jY_k)-\frac{G}{2}\cdot\frac{N}{2}\cdot 2\cdot 0
$$

Jordan-Wigner-free spin mapping with |1>=occupied pair, n_j=(1-Z_j)/2, P_j^+=sigma^+_j; the diagonal j=k terms give -G sum_j n_j which is absorbed into eps_j -> eps_j - G. Last term is zero and just notational.

Provenance: `standard_background`. sigma^+_j sigma^-_k + h.c. = (X_jX_k+Y_jY_k)/2; the sketch's Z/2 convention differs from this one only by a constant and sign convention for |1>=occupied.

Equation assumptions:

- Convention |1> = pair occupied
- Constant energy shifts dropped or tracked classically

## eq_3: Trotter step

$$
U(\delta t)\approx\Big[\prod_j e^{-i\delta t\,\epsilon_j (1-Z_j)/2/r}\prod_{j<k}e^{i\frac{G\delta t}{2r}(X_jX_k+Y_jY_k)}\Big]^r
$$

First-order Trotter product. XX and YY terms commute for the same pair, so each pair factor is exactly RXX*RYY with angle -G dt/r (Qiskit RXX(theta)=exp(-i theta XX/2)).

Provenance: `assumption`. Standard product formula applied to the sketch's Hamiltonian; the abstract gives no schedule.

Equation assumptions:

- Small dt
- Non-adjacent pairs via SWAP chains if linear connectivity is required

## eq_4: Adiabatic path

$$
H(s)=(1-s)H_0+sH,\; H_0=\sum_j\epsilon_j n_j,\; F=|\langle E_0|\psi_{final}\rangle|^2
$$

Linear-schedule adiabatic preparation from the reference state, and fidelity with the exact ground state by statevector overlap.

Provenance: `assumption`. Abstract states that the fidelity of target states is numerically studied; the linear schedule is an assumed choice.

Equation assumptions:

- Linear schedule
- Ground state in the fixed pair-number sector

## eq_5: QPE eigenphase

$$
U|E\rangle=e^{-iE\delta t}|E\rangle,\;\phi=\mathrm{frac}\!\left(-\frac{E\delta t}{2\pi}\right),\;E=-\frac{2\pi\phi}{\delta t}\ (\text{after unfolding})
$$

Phase-estimation readout of energy: controlled-U^(2^k) on ancilla k, then inverse QFT.

Provenance: `abstract_inferred`. The abstract only says a spectrum measurement scheme exists; the QPE details are from the sketch and background.

Abstract evidence: we design a measurement scheme to extract energy spectra from the simulators

Equation assumptions:

- Spectrum rescaled to fit one 2pi window of the phase
- Resolution 2pi/(2^t dt)

## eq_6: Counts to phase

$$
\phi=\frac{\mathrm{int}(\text{bits},2)}{2^t}
$$

Convert ancilla counts string (Qiskit little-endian, ancilla k = rightmost bit k) to phase if ancilla register measured into classical bits 0..t-1 in order.

Provenance: `standard_background`. Qiskit bit ordering convention with the standard inverse QFT including swaps.

Equation assumptions:

- Inverse QFT includes bit-reversal swaps

## Registers

- sys: N (3) qubits; pair-level qubits, qubit j = level j, |1> occupied
- anc: t (4) qubits; QPE energy readout; ancilla k controls U^(2^k)

## Initial state

sys: reference product state with lowest-level pairs filled by X gates (e.g. |001> for one pair on level 0); anc: H on all giving |+>^t. For multiple peaks use a superposition or the adiabatic state.

## Measurement

Measure the t ancilla qubits into classical bits 0..t-1 (ancilla k to bit k); system qubits unmeasured.

## Classical postprocessing

phi=int(bitstring,2)/2^t, E=-2*pi*phi/dt with unfolding by 2pi/dt multiples, undoing any rescaling and constant shifts.

## Algorithm steps

1. Choose rescaled eps_j, G, dt so the spectrum fits one 2pi window; prepare the reference state with X gates. (eq_2)
2. Optionally run the adiabatic Trotterized evolution and compute the statevector fidelity (no measurements). (eq_3, eq_4)
3. Apply H to ancillas and controlled-U^(2^k) built from controlled RZ, RXX, RYY (or CX-RZ-CX) Trotter steps. (eq_3, eq_5)
4. Apply inverse QFT to ancillas and measure only ancillas. (eq_5)
5. Convert counts to phases and energies. (eq_5, eq_6)

## Assumptions

- Tiny instance N=3, t=4 chosen by me
- Hard-core boson spin mapping, blocked levels ignored
- First-order Trotter with small step
- Controlled evolution built from standard gates; controlled-U^(2^k) is implemented by repeating controlled steps
- Fidelity from statevector
- Sign/shift conventions between eq_1 and eq_2 need fixing in implementation

## Missing information

- Actual paper algorithms for each native Hamiltonian type
- Paper's exact gate sequences, schedules and parameters
- Numerical fidelity and complexity results
- Exact measurement-scheme details of the paper
