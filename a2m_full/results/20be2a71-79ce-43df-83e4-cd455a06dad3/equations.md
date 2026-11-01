# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Three-qubit refined Deutsch-Jozsa: apply H^3, a diagonal phase oracle U_f=sum_x (-1)^{f(x)}|x><x| (placeholder, one query), H^3, then read the output distribution |hat F(s)|^2 to identify the function class. Also give a Z/CZ/CCZ decomposition of each of the 35 phase gates (the abstract's protocol contribution).

Scope: Ideal qubit-subspace statevector instance with 3 qubits, no ancilla, 1 oracle query. Out of scope: transmon qutrits, cavity coupling, two-target controlled-phase hardware pulses, numerical circuit QED simulation, and the paper's exact gate sequences for each of the 35 gates.

## Symbols

- $n$: number of qubits; domain: n=3
- $f$: Boolean function on 3 bits; domain: f:{0,1}^3->{0,1}
- $x$: computational basis index; qubit i holds bit x_i, Qiskit little-endian; domain: x in {0,...,7}
- $s$: measured Walsh index (output bitstring); domain: s in {0,1}^3
- $\hat F(s)$: normalized Walsh-Hadamard coefficient of (-1)^f; domain: real in [-1,1]
- $U_f$: diagonal phase oracle; domain: 8x8 diagonal unitary with entries +-1
- $a_S$: ANF coefficients of f; domain: {0,1}

## eq_1: Phase oracle

$$
U_f|x\rangle=(-1)^{f(x)}|x\rangle
$$

f-controlled phase gate acting diagonally on three qubits

Provenance: `abstract_inferred`. The abstract names f-controlled phase gates as the objects constructed; the diagonal +-1 form is the standard interpretation.

Abstract evidence: 35 $f$-controlled phase gates

Equation assumptions:

- Phase kickback convention with no ancilla

## eq_2: Output amplitudes

$$
\langle s|H^{\otimes 3}U_fH^{\otimes 3}|000\rangle=\hat F(s)=\frac{1}{8}\sum_{x}(-1)^{f(x)+s\cdot x}
$$

Final amplitude on outcome s; the probability is |\hat F(s)|^2

Provenance: `standard_background`. Standard Deutsch-Jozsa interference calculation.

Equation assumptions:

- Initial state |000>

## eq_3: Constant vs balanced

$$
P(000)=\hat F(0)^2=\begin{cases}1&f\text{ constant}\\0&f\text{ balanced}\end{cases}
$$

Standard DJ decision rule

Provenance: `standard_background`. Follows from eq_2.

## eq_4: ANF gate decomposition

$$
(-1)^{f(x)}=\prod_{S}\left[(-1)^{\prod_{i\in S}x_i}\right]^{a_S},\quad f(x)=\bigoplus_S a_S\prod_{i\in S}x_i
$$

Phase oracle as product of Z (|S|=1), CZ (|S|=2), CCZ (|S|=3) gates; constant term a_empty is a global phase

Provenance: `assumption`. A standard ANF-based diagonal synthesis, a proposed construction consistent with the abstract's use of Z and controlled-phase gates; not the paper's specific protocol.

Equation assumptions:

- Standard CCZ used in place of two-target controlled-phase gate
- Balanced f has ANF degree at most 2 for 3 variables, so CCZ is not needed

## eq_5: Class readout

$$
\mathrm{supp}(f)=\{s:P(s)>0\},\quad P(s)=\hat F(s)^2,\ \sum_sP(s)=1
$$

Post-processing maps the measured distribution to a Walsh-support class; functions with equal spectra are not separated

Provenance: `assumption`. Defines refined readout from the sketch; the paper's exact refined-DJ criterion is not in the abstract.

Equation assumptions:

- Exact probabilities or enough shots

## Registers

- q: 3 qubits; data qubits q0,q1,q2; no ancilla

## Initial state

|000>

## Measurement

Measure q0,q1,q2 into c0,c1,c2; the counts key reversed gives s_0 s_1 s_2. Omit measurements if the runner reads the statevector.

## Classical postprocessing

Estimate P(s) from counts. Declare constant if only 000 appears. Otherwise declare balanced and report the support of P as the Walsh class.

## Algorithm steps

1. Apply H on all three qubits. (eq_2)
2. Apply the opaque diagonal oracle placeholder U_f on qubits 0,1,2 (one query). (eq_1, eq_4)
3. Apply H on all three qubits. (eq_2)
4. Measure all 3 qubits (only for counts tasks); the string is s with the last character = qubit 0. (eq_3, eq_5)

## Assumptions

- Oracle supplied as a diagonal phase gate with no ancilla
- Qutrit and cavity hardware abstracted to ideal qubits
- Single oracle query
- Qiskit-standard Z, CZ, CCZ available for the local synthesis of test oracles

## Missing information

- Paper's explicit gate sequences for the 35 phase gates
- Exact refined-DJ discrimination criterion among the 35 functions
- Two-target controlled-phase gate definition
- Qutrit encoding and cavity pulse details
