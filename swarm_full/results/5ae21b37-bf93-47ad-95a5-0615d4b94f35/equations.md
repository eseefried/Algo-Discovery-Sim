# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Fast-signal assisted adiabatic quantum algorithm: apply a sequence of fast random or regular signals during adiabatic evolution to shorten runtime (limiting decoherence) while keeping adiabatic advantages. A randomized Trotter formula lets the driving Hamiltonian and the fast signals be implemented simultaneously. Applied to the 3-bit exact cover problem (EC3), with a proposed trapped-ion implementation.

Scope: Abstract-level reconstruction only: generic adiabatic evolution with a driving Hamiltonian, a fast-signal term, and a randomized Trotter decomposition, plus an EC3 final Hamiltonian as a finite instance. Specific signal forms, couplings, schedules, and ion-trap pulse details are not given in the abstract.

## Symbols

- $H_0$: initial driving Hamiltonian; domain: Hermitian operator on n qubits
- $H_P$: problem Hamiltonian encoding the EC3 solution in its ground state; domain: Hermitian operator on n qubits
- $s(t)$: adiabatic schedule, s(0)=0 and s(T)=1; domain: [0,1]
- $H_{sig}(t)$: fast random or regular signal Hamiltonian (form assumed); domain: time-dependent Hermitian operator
- $T$: total evolution time (runtime); domain: positive reals

## eq_1: Adiabatic interpolation

$$
H_{AQC}(t)=(1-s(t))H_0+s(t)H_P
$$

Standard AQC driving Hamiltonian interpolating to the problem Hamiltonian.

Provenance: `standard_background`. The abstract mentions a driving Hamiltonian whose final state encodes the solution; this specific linear form is a standard textbook choice.

Equation assumptions:

- Linear interpolation form assumed

## eq_2: Fast-signal assisted Hamiltonian

$$
H(t)=H_{AQC}(t)+H_{sig}(t)
$$

Driving Hamiltonian plus a sequence of fast signals applied during evolution.

Provenance: `abstract_inferred`. Additive combination is an assumed model of the stated signal application.

Abstract evidence: applying a sequence of fast random or regular signals during the evolution process

Equation assumptions:

- Additive coupling; signal form unspecified

## eq_3: Randomized Trotter step

$$
U(\delta t)\approx\prod_{k}e^{-i\,p_k\,h_k\,\delta t/p_k}
$$

Schematic randomized Trotter decomposition in which terms h_k are sampled randomly so the driving and signal parts are implemented together; exact formula not given.

Provenance: `assumption`. Abstract states a randomized Trotter formula exists but not its form; this is a placeholder.

Equation assumptions:

- Schematic only; sampling probabilities p_k unspecified

## Registers

- q: n (EC3 instance; unknown from abstract) qubits; system qubits encoding the bit string of the EC3 problem

## Initial state

Uniform superposition |+>^{\otimes n}, the ground state of H_0=-\sum_i X_i (assumed standard choice)

## Measurement

At t=T measure all n system qubits in the computational (Z) basis, repeated over many runs (and random signal realizations); the outcome bit strings sample the approximate ground state of H_P.

## Classical postprocessing

Take the most frequent outcome (or lowest H_P energy among outcomes) as the candidate solution, and classically check it against the EC3 clauses (exactly one true bit per clause). Success probability is estimated from the outcome frequencies.

## Algorithm steps

1. Prepare the system qubits in the ground state of H_0. (eq_1)
2. Discretize [0,T] into short steps; define the total Hamiltonian as the adiabatic interpolation plus fast signals. (eq_1, eq_2)
3. In each step apply a randomly sampled Trotter term so driving and signal parts are implemented simultaneously. (eq_3)
4. Continue until s=1 so the state approximates the ground state of H_P. (eq_1, eq_2, eq_3)

## Assumptions

- Linear schedule and additive signal model assumed
- Transverse-field initial Hamiltonian and |+>^n initial state assumed
- Register size is a placeholder for the EC3 instance
- Computational-basis readout assumed, not stated in the abstract
- Computational-basis readout and majority/lowest-energy selection assumed

## Missing information

- Explicit signal form and amplitudes
- Exact randomized Trotter formula
- EC3 Hamiltonian clauses and qubit count
- Trapped-ion pulse details
- Abstract does not specify the measurement protocol or postprocessing
- Abstract gives no readout details or success criterion
