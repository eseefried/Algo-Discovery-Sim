# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Implement a two-outcome qubit generalized measurement with Kraus operators M0=U0 diag(a,b) V and M1=U1 diag(sqrt(1-a^2),sqrt(1-b^2)) V as a Naimark dilation on one system qubit and one probe qubit, using a Z⊗Y-type interaction (controlled-RY), and check outcome probabilities and post-measurement states against the target.

Scope: Single-shot dilation (N=1) on 2 qubits for a tiny explicit instance (e.g. a=0.9, b=0.5, chosen U0, U1, V). An optional N-step version with N fresh probes uses N+1 qubits. The proof that only two singular values arise, and the full decomposition of an arbitrary qubit measurement into a sequence of such steps, are outside scope.

## Symbols

- $a,b$: singular values of M0; domain: 0<=a,b<=1, a!=b for a nontrivial measurement
- $U_0,U_1,V$: single-qubit unitaries (feedback corrections and pre-rotation); domain: U(2)
- $\theta_0,\theta_1$: probe RY angles conditioned on system Z-basis state 0 or 1; domain: [0,pi]
- $M_0,M_1$: Kraus operators; domain: 2x2 complex matrices with M0†M0+M1†M1=I
- $\psi$: input system state; domain: normalized vector in C^2

## eq_1: Kraus operators

$$
M_0=U_0\,\mathrm{diag}(a,b)\,V,\quad M_1=U_1\,\mathrm{diag}(\sqrt{1-a^2},\sqrt{1-b^2})\,V
$$

Target two-outcome measurement from the sketch, with polar/singular value decomposition.

Provenance: `assumption`. Taken from the method sketch; the abstract only mentions generalized measurements with two distinct singular values.

Equation assumptions:

- Both operators share the right unitary V
- Completeness M0†M0+M1†M1=I holds by construction

## eq_2: Angle choice

$$
\cos(\theta_0/2)=a,\quad \cos(\theta_1/2)=b
$$

Controlled RY angles so that the probe's |0> amplitude equals the singular value for each Z-basis state of s.

Provenance: `assumption`. Direct from the construction: RY(theta)|0>=cos(theta/2)|0>+sin(theta/2)|1>.

Equation assumptions:

- RY convention of Qiskit

## eq_3: Interaction

$$
W=\exp(-i\,g t\,Z\otimes Y)=\sum_{z}|z\rangle\langle z|\otimes R_Y((-1)^z 2gt)
$$

Constant Z⊗Y coupling yields a controlled rotation of the probe, with opposite signs for z=0,1. Local pulses (e.g. an X on the probe or a system Z-basis flip) give the general (theta0,theta1).

Provenance: `standard_background`. Since Z is diagonal, the exponential splits into Z-conditioned Y rotations.

Equation assumptions:

- Sign convention exp(-i phi Y/2)=RY(phi)
- Reaching theta0!=±theta1 needs extra pulses, which are not specified here

## eq_4: Dilated circuit

$$
|\Psi\rangle=\sum_{k\in\{0,1\}}(U_k\otimes|k\rangle\langle k|)\,C\,(V|\psi\rangle\otimes|0\rangle)=\sum_k (M_k|\psi\rangle)\otimes|k\rangle,\quad C=\sum_z|z\rangle\langle z|\otimes R_Y(\theta_z)
$$

Net effect of V, controlled-RY on p, then probe-controlled U_k on s (U_0 when p=0, U_1 when p=1), implemented as controlled gates.

Provenance: `assumption`. Direct computation: the p=0 amplitude is diag(cos(theta_z/2)) V psi, and the p=1 amplitude is diag(sin(theta_z/2)) V psi, up to sign conventions.

Equation assumptions:

- U_1 absorbs sign conventions
- Only the control of U_k from p=k is used, so the controls are CU1 after an X on p

## eq_5: Outcome probability

$$
p_k=\langle\psi|M_k^\dagger M_k|\psi\rangle,\quad |\psi_k\rangle=M_k|\psi\rangle/\sqrt{p_k}
$$

Readout comparison with the target: probe statistics and conditional system state.

Provenance: `standard_background`. Born rule for Kraus measurements.

Equation assumptions:

- Statevector used in place of tomography

## Registers

- s: 1 qubits; system qubit (qubit 0)
- p: 1 qubits; probe/ancilla qubit (qubit 1), starts in |0>, read into one classical bit

## Initial state

|psi>_s ⊗ |0>_p, with psi a chosen test state prepared with standard gates

## Measurement

Measure p into classical bit 0 (Qiskit little-endian: the last character of the counts key is bit 0). Skip the measurement for statevector checks.

## Classical postprocessing

Compute p_k from counts or the statevector and compare with <psi|M_k†M_k|psi>. Compare the conditional s state via the reduced statevector given p=k.

## Algorithm steps

1. Apply V on s. (eq_1)
2. Apply CRY(theta0) on p controlled on s=0 (X on s, CRY, X on s) and CRY(theta1) on p controlled on s=1. (eq_2, eq_3)
3. Apply U0 on s controlled on p=0 and U1 on s controlled on p=1 (X on p around the controlled gate for k=0); then measure p only if counts are requested, otherwise read the statevector. (eq_4)
4. Compare probe probabilities and the conditional s state with the target Kraus predictions. (eq_5)

## Assumptions

- The choice of a, b, U0, U1, V and psi is an illustrative tiny instance
- N=1 only; the continuous N-step splitting is not constructed
- No black box or query is used
- Qubit count 2, within a typical cap

## Missing information

- The proof that the composition of constant-H interactions with arbitrary unitaries yields only two singular values
- The paper's exact pulse sequence and Hamiltonian normalization
- The decomposition of a general qubit POVM into a sequence of such steps
- The N-step small-rotation scheme with fresh probes
