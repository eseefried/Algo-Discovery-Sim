# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Grover search on a 4-spin nuclear spin chain with Ising-type nearest and next-nearest neighbour couplings, with fidelity studied versus time and Rabi frequency. The abstract gives no explicit equations, so only background and assumed constructions are reconstructed.

Scope: Smallest useful construction: ideal 2-qubit Grover search (N=4, one marked item) as a reference, plus a generic 4-spin Ising-coupled Hamiltonian and fidelity definition. Pulse-level implementation, actual coupling values, pulse sequences and the paper's 2πk-method condition derivation are outside scope.

## Symbols

- $n$: number of spins in the chain; domain: n=4 (from abstract)
- $J_{i,i+1}, J_{i,i+2}$: Ising coupling constants for nearest and second nearest neighbours; domain: real, values unspecified
- $\sigma_z^{(i)}$: Pauli Z on spin i; domain: operator
- $\Omega$: Rabi frequency of driving pulses; domain: positive real
- $w$: marked item; domain: {0,1,2,3} (assumed instance)
- $F(t)$: fidelity between simulated and ideal state; domain: [0,1]
- $k$: integer in 2πk condition; domain: positive integer
- $\tau$: pulse duration; domain: positive real

## eq_1: Ising chain Hamiltonian

$$
H_0=\sum_{i=1}^{3}J_{i,i+1}\,\tfrac{1}{2}\sigma_z^{(i)}\tfrac{1}{2}\sigma_z^{(i+1)}\cdot 4/4+\sum_{i=1}^{2}J_{i,i+2}\,\tfrac{1}{2}\sigma_z^{(i)}\tfrac{1}{2}\sigma_z^{(i+2)}\cdot 4/4
$$

Generic Ising-type interactions between nearest and second nearest neighbours for four spins (Zeeman terms omitted).

Provenance: `assumption`. Abstract names Ising-type nearest and second-nearest interactions but gives no form or normalization.

Equation assumptions:

- Zeeman terms omitted
- normalization of J chosen arbitrarily

## eq_2: Grover iteration

$$
G=(2|s\rangle\langle s|-I)\,(I-2|w\rangle\langle w|),\quad |s\rangle=\tfrac{1}{2}\sum_{x=0}^{3}|x\rangle
$$

Standard Grover iterate for N=4 on 2 data qubits.

Provenance: `standard_background`. Standard Grover algorithm; the abstract only names it.

Equation assumptions:

- single marked item
- 2 qubits as the reduced instance

## eq_3: Ideal result for N=4

$$
G|s\rangle=|w\rangle
$$

One iteration finds the marked item with certainty when N=4.

Provenance: `standard_background`. Since sin(3θ)=1 with sinθ=1/2.

Equation assumptions:

- one marked item

## eq_4: Fidelity

$$
F(t)=\left|\langle\psi_{\rm ideal}(t)|\psi_{\rm sim}(t)\rangle\right|^{2}
$$

Fidelity between ideal and simulated states during the algorithm; final fidelity is evaluated at the end time as a function of Omega.

Provenance: `abstract_inferred`. Fidelity is named, but its definition is not given. Pure-state overlap squared is assumed.

Abstract evidence: We determine the temporal behaviour of the fidelity during the algorithm, and we compute the final fidelity as a function of the Rabi frequency.

Equation assumptions:

- pure-state fidelity definition
- ideal reference state is the target state

## eq_5: Generic 2πk condition

$$
\Omega_{\rm eff}\,\tau=2\pi k,\quad k\in\mathbb{N}
$$

Generic form of a 2πk-type condition under which a coupling-induced error is expected to cancel after a pulse. Its exact form for second-nearest-neighbour couplings is not given.

Provenance: `assumption`. Abstract mentions a 2πk-method condition on Rabi frequencies, but the actual condition (e.g. its dependence on J) is not given.

Equation assumptions:

- Omega_eff is a placeholder for the paper's actual frequency combination involving Omega and J_{i,i+2}

## Registers

- spins: 4 qubits; Nuclear spin qubits in a chain; ordering s1..s4 along chain, computational basis |x> with s1 as most significant bit (assumed)

## Initial state

Assumed: all spins in |0000>, with Hadamard-like preparation to the uniform superposition on the search qubits (assumed).

## Measurement

Computational-basis measurement of the search register to read the marked item (assumed).

## Classical postprocessing

Scan Omega and identify maxima of final fidelity (inferred from abstract).

## Algorithm steps

1. Prepare the initial state and the uniform superposition on the search qubits. (eq_2)
2. Apply the Grover iteration (oracle then diffusion), implemented by resonant pulses with Rabi frequency Omega while the Ising couplings act during evolution. (eq_1, eq_2, eq_3)
3. Compute the fidelity versus time, and the final fidelity versus Omega, and look for maxima at values satisfying the 2πk condition. (eq_4, eq_5)

## Assumptions

- Reduced to an N=4 search with one marked item
- How the four spins map to data and ancilla qubits is not specified
- Hamiltonian form and pulse implementation are assumed

## Missing information

- Coupling constants and their distance dependence
- Pulse sequences for gates and oracle
- Exact form of the 2πk condition
- Exact fidelity definition
- Mapping of the search problem onto the 4 spins
