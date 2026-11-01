# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Quantum-walk-based search for a marked node on an n-node graph, with the walk and marking implemented by explicit circuits rather than a black-box oracle. The abstract gives no graph definitions, walk operators or circuits.

Scope: Generic discrete-time (coined) quantum walk search on a tiny assumed instance, the 4-cycle (n=4, a 2-qubit position register). Only standard background equations are given. The paper's graph families, the twisted toroid construction, the explicit circuits and the numerical analysis are outside this scope.

## Symbols

- $n$: number of graph nodes; domain: positive integer
- $d$: node degree (regular graph assumed); domain: positive integer
- $m$: marked node; domain: {0,...,n-1}
- $S$: shift operator; domain: unitary on position and coin space
- $C$: coin operator, Grover diffusion; domain: unitary on C^d
- $C'$: coin operator with marking; domain: unitary on C^d
- $U$: one walk-plus-search step; domain: unitary
- $T$: number of walk steps; domain: nonnegative integer

## eq_1: Gate-count claim

$$
G(n)=O\left(\sqrt{n}\,\log n\right)
$$

Elementary 2-qubit gate count for finding a marked node on the twisted toroid family

Provenance: `abstract_explicit`. Stated asymptotic cost in the abstract. The gate construction is not given.

Abstract evidence: requires O($\sqrt{n}$ log($n$)) elementary 2-qubit quantum gate operations to find a marked node

## eq_2: Grover coin

$$
C=2|s_d\rangle\langle s_d|-I_d,\quad |s_d\rangle=\frac{1}{\sqrt d}\sum_{j=0}^{d-1}|j\rangle
$$

Standard Grover diffusion coin on the d-dimensional coin space

Provenance: `standard_background`. Common coin choice in quantum walk search. The paper's coin is not stated.

Equation assumptions:

- Grover coin is used

## eq_3: Walk step with marking

$$
U=S\,\left(\left(I-|m\rangle\langle m|\right)\otimes C+|m\rangle\langle m|\otimes(-I_d)\right)
$$

The marked node gets coin -I instead of C, and the shift S then moves the walker

Provenance: `standard_background`. Standard coined-walk search construction. It is not the paper's explicit oracle-free circuit.

Equation assumptions:

- Marking is realized by a coin modification

## eq_4: Initial state

$$
|\psi_0\rangle=\frac{1}{\sqrt{nd}}\sum_{x=0}^{n-1}\sum_{j=0}^{d-1}|x\rangle|j\rangle
$$

Uniform superposition over positions and coins

Provenance: `standard_background`. Usual start state for walk search.

Equation assumptions:

- Uniform initial state

## eq_5: Evolution and success probability

$$
|\psi_T\rangle=U^T|\psi_0\rangle,\quad p_T=\sum_{j}\left|\left(\langle m|\otimes\langle j|\right)|\psi_T\rangle\right|^2
$$

State after T steps and the probability of measuring the marked node

Provenance: `standard_background`. Defines the figure of merit for choosing T.

Equation assumptions:

- T is chosen near the first maximum of p_T

## Registers

- pos: ceil(log2 n) qubits (2 for the assumed 4-cycle) qubits; node index x in binary
- coin: ceil(log2 d) qubits (1 for the 4-cycle) qubits; edge or direction label

## Initial state

Uniform superposition over pos and coin registers (eq_4), assumed.

## Measurement

Computational-basis measurement of the position register, assumed.

## Classical postprocessing

Read the measured node as the candidate marked node, and verify it classically if needed.

## Algorithm steps

1. Prepare the uniform superposition with Hadamards. (eq_4)
2. Repeat T times: apply the marked coin, then the shift. (eq_2, eq_3)
3. Measure the position register and estimate p_T. (eq_5)

## Assumptions

- The 4-cycle with a Grover coin is an illustrative choice and is not from the abstract.
- Equations 2 to 5 are generic background and not the paper's construction.

## Missing information

- Definitions of the graph families and the twisted toroid
- The explicit circuits for the shift, coin and marking
- The paper's walk model, coin and search algorithm
- The number of steps and the numerical analysis details
- The derivation of the O(sqrt(n) log n) gate count
