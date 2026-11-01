# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Decide whether two n-qubit circuits U and V (or their output states) are equivalent up to global phase using a swap test, for a tiny explicit instance. This is a generic dense-simulation realisation; the paper's scalable algorithms are not recovered.

Scope: n=2 instance with U = H on qubit 0 then CNOT(0,1) (Bell preparation), and V either identical to U or a variant with a relative phase (e.g. U followed by Z on qubit 0). State-equivalence swap test on |0^n> inputs, built as a measurement-free unitary. The Choi-state variant and the controlled-U/V† exact-phase variant are described but not the primary built circuit. Excluded: the paper's scalable algorithms for hundreds of qubits, its equivalence taxonomy, and the teleportation and Grover benchmarks.

## Symbols

- $n$: number of qubits per circuit; domain: positive integer, n=2 in the instance
- $U, V$: unitaries on n qubits, compiled explicitly into gates; domain: U(2^n)
- $|\psi_U\rangle, |\psi_V\rangle$: U|0^n> and V|0^n>; domain: unit vectors in C^{2^n}
- $p_0$: probability of ancilla outcome 0 after the swap test; domain: [1/2,1]
- $\theta$: global phase; domain: [0,2\pi)
- $\epsilon$: numerical tolerance for decoding; domain: small positive real

## eq_1: Equivalence up to global phase

$$
|\psi_U\rangle = e^{i\theta}|\psi_V\rangle \ \text{for some}\ \theta \iff |\langle\psi_U|\psi_V\rangle|^2=1
$$

Equality up to global phase is equivalent to unit overlap. This is the Cauchy-Schwarz equality condition for unit vectors.

Provenance: `standard_background`. Cauchy-Schwarz equality case. The abstract only says that several notions of equivalence exist.

Equation assumptions:

- Both states are normalised

## eq_2: Swap test probability

$$
P(a=0)=\frac{1+|\langle\psi_U|\psi_V\rangle|^2}{2}
$$

Probability of the ancilla being 0 after H, controlled-SWAP(A,B), H, with A and B holding |psi_U> and |psi_V>.

Provenance: `standard_background`. Standard swap test identity.

Equation assumptions:

- Ancilla, A and B start in |0>
- U acts on A and V acts on B

## eq_3: Swap test unitary

$$
W=(H_a\otimes I)\,\mathrm{CSWAP}_{a;A,B}\,(H_a\otimes I)\,(I_a\otimes U_A\otimes V_B)
$$

Measurement-free unitary on 1+2n qubits. Applied to |0>, it yields p_0 from eq_2.

Provenance: `assumption`. Proposed construction from the method plan, not stated in the abstract.

Equation assumptions:

- Standard gates only
- Ancilla is qubit 0, then A, then B

## eq_4: Choi-state version

$$
|\Phi_U\rangle=(U_A\otimes I_{R_A})\,2^{-n/2}\sum_{x}|x\rangle_A|x\rangle_{R_A},\quad |\langle\Phi_U|\Phi_V\rangle|=\frac{|\mathrm{tr}(U^\dagger V)|}{2^n}
$$

Applying the swap test to the Choi states of U and V tests circuit equivalence up to global phase, since the overlap equals 1 iff V = e^{i theta} U.

Provenance: `standard_background`. Choi-Jamiolkowski overlap identity. This is an extension, not the primary built circuit.

Equation assumptions:

- Reference registers R_A and R_B are swapped alongside A and B

## eq_5: Exact equality with global phase

$$
P(a=0)=\frac{1+\mathrm{Re}\langle\psi_U|\psi_V\rangle}{2}
$$

Hadamard test on the ancilla, with controlled-U and controlled-V† on A. It equals 1 iff U|0>=V|0> exactly, including global phase.

Provenance: `standard_background`. Standard Hadamard-test form for the variant described in the plan. It is not built in the primary scope.

Equation assumptions:

- Controlled-U and controlled-V† applied between the two Hadamards

## Registers

- a: 1 qubits; swap-test ancilla, qubit 0
- A: n=2 qubits; holds U|0^n>
- B: n=2 qubits; holds V|0^n>
- R_A,R_B: n each (Choi variant only) qubits; reference registers for the Choi construction, not in the primary build

## Initial state

|0>_a|0^n>_A|0^n>_B, qubit order a,A,B, little-endian integer encoding as in Qiskit

## Measurement

No in-circuit measurement. The simulator reads the ancilla-0 probability from the statevector.

## Classical postprocessing

Declare equivalence up to global phase if p_0 is within epsilon of 1; otherwise declare non-equivalence.

## Algorithm steps

1. Apply U to A and V to B, where U = H(q0) then CNOT(q0,q1), and V = U or U followed by Z on q0. (eq_3)
2. Apply H on the ancilla, then CSWAP controlled by the ancilla for each qubit pair of A and B, then H on the ancilla. (eq_2, eq_3)
3. Decode in the simulator: compute P(a=0) from the statevector. Declare equivalent up to global phase if P(a=0) >= 1-epsilon. (eq_1, eq_2)

## Assumptions

- The tiny instance with n=2 and the gate choices for U and V are assumptions.
- U and V are compiled explicitly, so no black-box query claim is made.
- Only the global-phase-insensitive state-equivalence test is the primary build.

## Missing information

- The paper's actual algorithms, such as decision-diagram or stabilizer-style methods.
- The paper's taxonomy of equivalence notions.
- Benchmark circuit definitions (teleportation, Grover).
