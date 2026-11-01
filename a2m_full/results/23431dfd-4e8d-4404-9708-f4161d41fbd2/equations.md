# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Prepare the ground state of a diagonal EC3 (exact cover, 3-bit) problem Hamiltonian H_P on n=3 data qubits by a digitized adiabatic evolution from H_B=-sum X_i, with optional ancilla-controlled phase-kick filter steps, then read the solution by computational-basis measurement of the data qubits.

Scope: One tiny instance: n=3 variables, a few EC3 clauses (each clause penalizes all bit triples except those with exactly one 1), unique satisfying assignment; M about 10-50 first-order Trotter slices; noiseless statevector simulation. Outside scope: the paper's fast random or regular signal sequences, the randomized Trotter formula, decoherence or system-bath effects, and the trapped-ion implementation. The phase-kick filter is a sketch-level proposal, not the paper's method.

## Symbols

- $n$: number of data qubits (variables); domain: n=3
- $H_B$: driver Hamiltonian -sum_i X_i; domain: operator on n qubits
- $H_P$: diagonal problem Hamiltonian; zero energy exactly on satisfying assignments; domain: operator on n qubits
- $s_k$: schedule value at step k; domain: [0,1]
- $M$: number of Trotter slices; domain: positive integer, about 10-50
- $dt$: time step length; domain: positive real
- $T$: total evolution time; domain: positive real
- $g(s)$: spectral gap of H(s) between ground and first excited state; domain: nonnegative real
- $H(s)$: interpolating Hamiltonian (1-s)H_B + s H_P; domain: operator
- $\tau$: phase-kick duration for the filter; domain: small positive real

## eq_1: Interpolating Hamiltonian

$$
H(s)=(1-s)H_B+sH_P,\quad H_B=-\sum_{i=0}^{n-1}X_i
$$

Standard AQC interpolation between driver and problem Hamiltonian.

Provenance: `standard_background`. The abstract describes AQC generically with a final Hamiltonian encoding the solution; the linear interpolation and H_B are standard choices.

Equation assumptions:

- Linear interpolation in s
- Driver is the transverse field

## eq_2: EC3 problem Hamiltonian

$$
H_P=\sum_{c}\sum_{b\notin A_c}|b\rangle\langle b|_{c},\quad A_c=\{100,010,001\}
$$

Each clause c on three variables adds a penalty projector onto the 5 forbidden triples (all except exactly-one-1). It is diagonal and expands into Z, ZZ terms. For a clause, the penalty is (1/2)(1-(1-z_a... ) ) form; equivalently the clause cost is (s-1)^2 with s=sum of the three bits, giving Z and ZZ terms only.

Provenance: `assumption`. The abstract names EC3 but not its Hamiltonian; this is the usual EC3 definition, and the concrete clauses must be chosen for the instance.

Equation assumptions:

- Penalty per violated clause is 1 (or the squared-sum form (x_a+x_b+x_c-1)^2)
- Clause set chosen to have a unique solution

## eq_3: First-order Trotter slice

$$
U_k=e^{-i(1-s_k)H_B\,dt}\,e^{-i s_k H_P\,dt},\quad U\approx\prod_{k=M}^{1}U_k
$$

Digitized adiabatic evolution; exact only as dt goes to 0 and approximate otherwise. The H_P factor is exactly a product of commuting Z-rotations (RZ, CX-RZ-CX); the H_B factor is a product of RX(-2(1-s_k)dt).

Provenance: `assumption`. The abstract proposes a randomized Trotter formula, but the details are absent; the ordinary first-order formula is used as a stand-in.

Equation assumptions:

- First-order Trotter
- dt=T/M

## eq_4: Local adiabatic schedule

$$
\frac{ds}{dt}=c\,g(s)^2,\quad T=\frac{1}{c}\int_0^1\frac{ds}{g(s)^2}
$$

Local adiabatic rule giving a slow sweep near the minimum gap; g(s) is computed classically by exact diagonalization for this tiny instance, and s_k is obtained by discretizing the integral.

Provenance: `standard_background`. Roland-Cerf local adiabatic rule, recalled from background; the sketch requests it.

Equation assumptions:

- g(s) known classically for the 8-dimensional instance
- c sets the total time T

## eq_5: Ancilla phase-kick filter (sketch)

$$
K_k=C\text{-}e^{-iH(s_k)\tau}\,(\text{ancilla}\to\text{data}),\quad F_k=K_k^{-1}\cdot K_k\text{ with ancilla in }|0\rangle
$$

Controlled short evolution from an ancilla in |+>/|0>, followed by the inverse kick to return the ancilla to |0>. With ancilla returned to |0> and the data unchanged, the net data effect is the identity unless the kicks differ; as written it is not a verified filter.

Provenance: `assumption`. Proposed in the sketch as a stand-in for the paper's fast signals; applying a kick and its exact inverse is the identity, so a nontrivial filter needs a different construction, which is unspecified.

Equation assumptions:

- Standard gates only
- May need to be dropped

## eq_6: Readout and success probability

$$
p_{succ}=\left|\langle x^*|\psi_M\rangle\right|^2,\quad x^*=\arg\max_x \mathrm{count}(x),\ \langle x^*|H_P|x^*\rangle=0
$$

The final state is measured on the data qubits and the most frequent bitstring is checked against the clauses. For a unique solution, success probability equals the squared overlap with the ground state.

Provenance: `standard_background`. Follows from the diagonal H_P with a zero-energy ground space; the abstract says only that the final Hamiltonian state encodes the solution.

Equation assumptions:

- Unique satisfying assignment

## Registers

- data: 3 qubits; EC3 variable qubits; qubit i corresponds to counts string bits[::-1][i]
- anc: 1 qubits; optional ancilla for phase-kick filter, returned to |0>, not measured

## Initial state

|+>^{\otimes 3} on data (ground state of H_B), ancilla |0>

## Measurement

Measure the 3 data qubits in the computational basis; do not measure the ancilla. Counts key bits[::-1][i] gives data qubit i.

## Classical postprocessing

Histogram counts, take the most frequent bitstring, reverse it to map to variable order, and verify that every clause has exactly one 1.

## Algorithm steps

1. Apply H to each data qubit to prepare the ground state of H_B. (eq_1)
2. Choose the EC3 clauses and expand H_P into Z, ZZ terms; compute the schedule s_k classically from the gap rule. (eq_2, eq_4)
3. For k=1..M, apply the Trotter slice: RZ/CX-RZ-CX for H_P with angle proportional to s_k dt, then RX on every data qubit for H_B. (eq_3)
4. Optionally, every few steps apply the ancilla phase-kick filter and its inverse; skip it if it reduces to the identity. (eq_5)
5. Measure only the 3 data qubits in the computational basis, histogram, take the argmax, verify against the clauses. (eq_6)

## Assumptions

- Instance: 3 variables with a few clauses and a unique satisfying assignment, chosen by us
- Noiseless simulation, so decoherence robustness is not tested
- M about 10-50, first-order Trotter
- Phase-kick filter built from standard gates; no black box
- Total qubits 4 or fewer

## Missing information

- The paper's fast-signal form (random or regular) and how it assists the evolution
- The randomized Trotter formula
- The concrete EC3 instance and schedule used in the paper
- Any nontrivial filter construction
- The trapped-ion implementation
