# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Decide whether two n-qubit unitary circuits U and V, given as gate lists, are equivalent in one of three senses: exact equality including global phase, equality up to global phase, or equality on a given input state. The decision uses overlap estimators read from exact statevector probabilities: compute-uncompute, swap test, Hadamard test, and a Bell-pair (Choi) test.

Scope: Tiny instance with n=1 or 2, for example U=H and V=HZZ (exactly equal), or V=e^{i*phi}H (equal up to phase only), or V=X (inequivalent). Implement (a) compute-uncompute, (b) swap test, (c) Hadamard test for Re and Im of <0|V^dagger U|0>, and (d) a Bell-pair Tr(V^dagger U) test. Outside this scope: the paper's tableau, decision-diagram and stabilizer algorithms, scaling to hundreds of qubits, and random-input sampling strategies. The abstract names these only generically, and their details are not reconstructed.

## Symbols

- $n$: number of data qubits; domain: positive integer
- $U, V$: unitary circuits to be compared; domain: U(2^n)
- $|\psi\rangle,|\phi\rangle$: U|0^n> and V|0^n>; domain: unit vectors in C^{2^n}
- $W$: V^\dagger U, the compute-uncompute circuit; domain: U(2^n)
- $P_0$: probability of ancilla outcome 0; domain: [0,1]
- $\epsilon$: numerical tolerance for deciding equality; domain: small positive real, e.g. 1e-9
- $\Phi^+$: n Bell pairs across data register A and reference register B; domain: state on 2n qubits

## eq_1: Swap test statistic

$$
P_0=\frac{1+|\langle\psi|\phi\rangle|^2}{2}
$$

Probability of the ancilla reading 0 after H, controlled-SWAP between the two n-qubit registers, then H. P_0=1 iff the states are equal up to global phase.

Provenance: `standard_background`. Standard swap-test identity. The abstract mentions only that several notions of equivalence exist, not this formula.

Equation assumptions:

- Registers hold U|0^n> and V|0^n> on 2n+1 qubits in total

## eq_2: Compute-uncompute fidelity

$$
P(0^n)=|\langle 0^n|V^\dagger U|0^n\rangle|^2=|\langle\phi|\psi\rangle|^2
$$

Apply U then V^dagger to |0^n> and measure all data qubits. P=1 iff equality up to global phase on this input. It needs only n qubits.

Provenance: `standard_background`. Standard identity. The abstract does not say that the paper uses this circuit.

Equation assumptions:

- V^dagger is built by reversing the gate list and inverting each gate

## eq_3: Hadamard test readout

$$
P_0^{(X)}-P_1^{(X)}=\mathrm{Re}\langle 0^n|V^\dagger U|0^n\rangle,\quad P_0^{(Y)}-P_1^{(Y)}=\mathrm{Im}\langle 0^n|V^\dagger U|0^n\rangle
$$

The ancilla is prepared in |+>, controlled-W is applied, and the ancilla is measured in the X basis for Re. For Im, apply S^dagger before the final H (equivalently, measure in the Y basis). Exact equality on the input |0^n> means the value is 1, so Re=1 and Im=0.

Provenance: `standard_background`. Standard Hadamard test. It makes global phase observable as a relative phase on the ancilla.

Equation assumptions:

- Controlled-U and controlled-V^dagger are built from controlled standard gates
- Sign convention: Im uses S^dagger before H on the ancilla
- The relative phase of controlled-W on the |0^n> input is exactly the phase of <0|W|0> only when the test is applied to that input; for full-unitary phase use the Bell register

## eq_4: Bell-pair full-unitary overlap

$$
P(\text{all zero})=\left|\langle\Phi^+|(I\otimes V^\dagger U)|\Phi^+\rangle\right|^2=\left|\frac{\mathrm{Tr}(V^\dagger U)}{2^n}\right|^2
$$

Apply V^dagger U to the A half of n Bell pairs, then undo the Bell preparation (CNOT then H on each pair) and measure all 2n qubits. The all-zero probability equals 1 iff U=V up to global phase.

Provenance: `standard_background`. Standard Choi-state fidelity identity. It checks all inputs, which an input-specific test does not.

Equation assumptions:

- Uses 2n qubits, plus 1 for the Hadamard-test variant

## eq_5: Equality decision rules

$$
\text{phase-equal: } P\ge 1-\epsilon;\quad \text{exact: } \left|\langle W\rangle-1\right|<\epsilon,\ \langle W\rangle=\mathrm{Re}+i\,\mathrm{Im}
$$

Threshold decisions applied to statevector probabilities. The up-to-phase check uses P from eq_2, eq_1 or eq_4. The exact check uses the Hadamard-test value, either on |0^n> for input-specific equality or on the Bell register for full unitary equality, where <W> is Tr(V^dagger U)/2^n.

Provenance: `assumption`. The abstract only says that several notions of equivalence exist (exact, up to phase, state-specific). The thresholding is an engineering choice.

Equation assumptions:

- Exact simulation, so epsilon=1e-9 suffices

## Registers

- data_A: n qubits; holds U|0^n> or V^dagger U|0^n>, or the A half of the Bell pairs
- data_B: n qubits; holds V|0^n> in the swap test, or the reference half of the Bell pairs
- anc: 1 qubits; ancilla for the swap test or Hadamard test

## Initial state

All qubits |0>. Compute-uncompute uses only data_A, swap test uses data_A, data_B and anc (2n+1 qubits), Bell test uses data_A and data_B (2n qubits, plus anc for the phase variant).

## Measurement

Compute-uncompute: all data qubits, with the all-zero string meaning equal. Swap test: ancilla only, with 0 meaning equal. Hadamard test: ancilla in X and Y bases. Bell test: all 2n qubits, with the all-zero string meaning equal. In Qiskit the counts key is little-endian, so bit i is the character at position [::-1][i]. For statevector tasks, omit measurements and compute probabilities directly.

## Classical postprocessing

Compute probabilities from counts or the statevector, then Re and Im as P0-P1 per basis, then compare with 1-epsilon as in eq_5. Report which notion holds: exact, phase-only, or none.

## Algorithm steps

1. Build V^dagger by reversing the gate list of V and inverting each gate. Build the composite circuit W = V^dagger U. (eq_2)
2. Up-to-phase test on |0^n> using compute-uncompute: apply U then V^dagger on data_A and measure data_A. Swap-test alternative: prepare U|0> on A and V|0> on B, then H on anc, controlled-SWAP of each qubit pair, H on anc, and measure anc. (eq_1, eq_2)
3. Exact test with phase on |0^n>: H on anc, controlled-U then controlled-V^dagger on data_A, then H on anc for the X readout, or S^dagger then H for the Y readout. Read the ancilla in each basis to get Re and Im. (eq_3)
4. Full-circuit test: create n Bell pairs between data_A and data_B (H then CNOT), apply W on data_A, undo the Bell preparation (CNOT then H), and measure all qubits. For phase, add an ancilla-controlled W and read Re and Im as in step 3. (eq_4, eq_3)
5. Classify using the thresholds. (eq_5)

## Assumptions

- Chosen instance: n=1 or 2 with small test circuits; this is not specified by the abstract
- Circuits are gate lists with invertible standard gates
- Statevector probabilities are exact with epsilon around 1e-9
- The qubit cap allows 2n+1 qubits
- The input-state-specific notion is checked on |0^n> only; other inputs would need a different state-preparation prefix
- All formulas are standard background, not extracted from the paper

## Missing information

- The paper's actual algorithms for equivalence checking (likely stabilizer or decision-diagram based) are not specified in the abstract
- The paper's precise definitions of the several equivalence notions
- The specific benchmark circuits (teleportation and Grover instance details)
- Any robustness or sampling schemes
