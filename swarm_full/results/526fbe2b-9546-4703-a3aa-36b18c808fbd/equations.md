# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Decompose an arbitrary isometry from m to n qubits into single-qubit gates and C-not gates, minimizing the C-not count. Derive a lower bound on the C-not count, give three explicit decompositions that meet it up to a factor of about two at leading order, and extend to quantum operations and POVMs via Stinespring's theorem.

Scope: Abstract-level problem statement and generic counting bound only. The explicit decomposition circuits, the exact C-not counts, and the small-case optimizations are not in the abstract and are not reconstructed.

## Symbols

- $m$: number of input qubits of the isometry; domain: positive integer, m <= n
- $n$: number of output qubits of the isometry; domain: positive integer
- $V$: isometry from m to n qubits, V^\dagger V = I; domain: 2^n x 2^m complex matrix

## eq_1: Isometry condition

$$
V^\dagger V = I_{2^m},\quad V:\mathbb{C}^{2^m}\to\mathbb{C}^{2^n}
$$

Defines an isometry from m to n qubits.

Provenance: `standard_background`. Standard definition of an isometry; the abstract only names isometries from m to n qubits.

Equation assumptions:

- Isometry means a norm-preserving linear map

## eq_2: Stinespring dilation

$$
\mathcal{E}(\rho)=\mathrm{Tr}_E\left[V\rho V^\dagger\right]
$$

A quantum operation is realized by an isometry V followed by tracing out an environment E.

Provenance: `standard_background`. Standard form of Stinespring's theorem, which the abstract invokes for quantum operations and POVMs. The exact form used in the paper is not given.

Equation assumptions:

- Finite-dimensional systems

## Registers

- input: m qubits; qubits carrying the input state, ancillas in |0> added to reach n qubits
- ancilla: n-m qubits; qubits initialized to |0> so that the unitary extension acts on n qubits
- E: unknown qubits; environment qubits traced out or measured when implementing operations or POVMs via Stinespring

## Initial state

Input state on m qubits tensored with |0>^{n-m} on the remaining qubits (generic assumption; the paper's construction is not given).

## Measurement

Isometry synthesis itself needs no measurement; correctness is checked by comparing the circuit unitary to V on inputs with ancillas in |0>. For POVMs via Stinespring, measure the output/environment qubits in the computational basis, with outcomes labeling POVM elements (generic assumption; the paper's scheme is not given).

## Classical postprocessing

Count C-not gates in the compiled circuit and compare with the lower bound. For POVMs or operations, map computational-basis outcomes of the dilated register to POVM outcomes or Kraus branches. Exact mapping not specified in the abstract.

## Algorithm steps

1. Prepare the m-qubit input and append n-m ancillas in |0>. (eq_1)
2. Apply a generic placeholder circuit of single-qubit gates and C-nots implementing V. The three explicit decompositions are not given in the abstract. (eq_1)
3. For quantum operations or POVMs, treat the isometry as a Stinespring dilation and discard or measure the environment qubits. (eq_2)

## Assumptions

- Only the generic isometry definition and Stinespring form are supplied as background.
- Circuit plan is a generic ancilla-based outline, not the paper's specific decompositions.
- Measurement is a computational-basis assumption for POVM implementation.

## Missing information

- Exact C-not lower bound formula
- Explicit decomposition circuits and their gate counts
- Small-case optimizations
- Register sizes for the environment are unspecified.
- Paper's specific measurement and outcome mapping for POVMs
