# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Grover search over a small quantum phone book (find index whose number or name equals a programmable query), plus analysis of unambiguous discrimination between Grover states produced for two different database sizes N and N' after the same t iterations.

Scope: Tiny instance: N=4 (k=2 index qubits), M=1, 2-bit names and 2-bit numbers stored by controlled-X gates, one number query; then overlap and IDP success computed from statevectors for two sizes (e.g. N=4 vs N'=8) with the same t. Excluded: general programmable-query database model details of the paper, M>1, multi-entry priors, exact unknown-size parametrization, optimal/non-IDP discrimination.

## Symbols

- $N=2^k$: number of database entries; domain: power of two, small
- $M$: number of marked entries; domain: integer, assumed 1
- $\theta$: Grover angle for true size N; domain: (0,\pi/2), \sin\theta=\sqrt{M/N}
- $\theta'$: Grover angle for alternative size N'; domain: (0,\pi/2)
- $t$: number of Grover iterations; domain: nonnegative integer
- $q$: query value held in query register; domain: m-bit string (number) or n-bit string (name)
- $P_{IDP}$: unambiguous discrimination success probability with equal priors; domain: [0,1]

## eq_1: Database state

$$
|\Phi\rangle=\frac{1}{\sqrt N}\sum_{i=0}^{N-1}|i\rangle|\mathrm{name}_i\rangle|\mathrm{num}_i\rangle
$$

State after index Hadamards and loading of classical entries with controlled-X gates.

Provenance: `assumption`. Sketch construction of the quantum phone book; the abstract only mentions a quantum database with programmable queries.

Equation assumptions:

- Entries are fixed classical constants
- Little-endian index register

## eq_2: Comparison oracle

$$
O_q|i\rangle|\mathrm{num}_i\rangle|-\rangle=(-1)^{[\mathrm{num}_i=q]}|i\rangle|\mathrm{num}_i\rangle|-\rangle
$$

Phase-flip on entries matching the query; for a name search replace num by name.

Provenance: `assumption`. Standard compare-by-CX plus multi-controlled-X onto a |-> ancilla; load and unload data registers around each use.

Equation assumptions:

- Comparison ancillas are uncomputed
- Data registers are unloaded after the phase flip so only the index register is diffused

## eq_3: Grover iteration count

$$
t\approx\frac{\pi}{4}\sqrt{N/M}
$$

Near-optimal number of iterations for the known size.

Provenance: `standard_background`. Standard Grover analysis; for N=4, M=1 this gives t=1 and success probability 1.

Equation assumptions:

- M known

## eq_4: State after t steps

$$
|\psi_t\rangle=\sin((2t+1)\theta)|\mathrm{good}\rangle+\cos((2t+1)\theta)|\mathrm{bad}\rangle,\ \sin\theta=\sqrt{M/N}
$$

Grover state in the 2D span of the good and bad subspaces.

Provenance: `standard_background`. Standard Grover geometry; the abstract only says the question reduces to distinguishability of states during Grover's algorithm.

Equation assumptions:

- Uniform initial superposition
- Same marked set in both runs

## eq_5: Overlap

$$
\langle\psi_t|\psi'_t\rangle=\cos((2t+1)(\theta-\theta'))
$$

Overlap of states for sizes N and N' with the same t, and the same good/bad basis.

Provenance: `abstract_inferred`. Follows from eq_4 when both states are written in a common good/bad basis; this requires identifying the two Hilbert spaces, which is an assumption.

Abstract evidence: This question reduces to analysis of the distinguishability of states occurring during Grover’s algorithm.

Equation assumptions:

- Identification of the good/bad basis across different N, N' (e.g. embed the smaller database)

## eq_6: IDP success

$$
P_{IDP}=1-|\langle\psi_t|\psi'_t\rangle|
$$

Ivanovic-Dieks-Peres unambiguous discrimination success probability for two pure states with equal priors.

Provenance: `standard_background`. Standard IDP bound; the abstract names unambiguous discrimination but gives no formula.

Equation assumptions:

- Equal priors

## Registers

- index: k (2 for N=4) qubits; search index, in uniform superposition, diffused
- name: n (2) qubits; stores name_i
- number: m (2) qubits; stores num_i
- flag: 1 qubits; oracle ancilla in |->
- query: m or n qubits; classical query value; may be encoded by X gates on the comparison register instead of a separate register

## Initial state

All qubits |0>, then X and H on flag to make |->, H on index register.

## Measurement

Search: measure the index register only, then look up the name or number classically. Discrimination: no measurement, read the statevector.

## Classical postprocessing

Map measured index to the (name, number) table; compute |overlap| from statevector inner product and P_IDP=1-|overlap|.

## Algorithm steps

1. Prepare index uniform superposition and flag in |->. (eq_1)
2. Load name and number via controlled-X gates controlled on index values. (eq_1)
3. Apply comparison oracle for the chosen query (number or name register), then unload the data registers. (eq_2)
4. Apply diffusion on the index register (H, X, multi-controlled Z, X, H). (eq_4)
5. Repeat the oracle and diffusion steps t times. (eq_3)
6. For discrimination: build final index states for N and N' with the same t and compute overlap from statevectors, then the IDP success. (eq_5, eq_6)

## Assumptions

- N power of two, small, M=1
- Two candidate sizes with the same t
- Equal priors and IDP bound
- Entries are constants loaded by controlled-X
- Ancilla compute/uncompute keeps qubits under the cap

## Missing information

- Paper's actual quantum database model and programmable query construction
- How the unknown-size parametrization is defined
- Exact states and priors used in the discrimination analysis
- Numerical results
