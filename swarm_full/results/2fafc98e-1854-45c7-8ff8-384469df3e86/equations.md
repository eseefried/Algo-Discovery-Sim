# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Decompose an arbitrary n-qubit unitary (n<=2) with entries in Z[i,1/sqrt2], of the form (a+b sqrt2+i(c+d sqrt2))/sqrt2^k, exactly into a Clifford+T circuit with O(k) gates using at most one ancilla, via decomposition into 1- and 2-level matrices (Giles-Selinger approach).

Scope: Abstract-level problem statement and gate-count claim only; the detailed decomposition algorithm is not in the abstract and is not reconstructed.

## Symbols

- $a,b,c,d$: integer coefficients of a matrix entry; domain: integers
- $k$: denominator exponent (sqrt2 power) of the operator; domain: nonnegative integer
- $n$: number of qubits; domain: n<=2

## eq_1: Entry form

$$
\frac{a+b\sqrt{2}+i(c+d\sqrt{2})}{\sqrt{2}^{k}}
$$

Form of each matrix entry in Z[i,1/sqrt2].

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: \frac{a+b\sqrt{2}+i(c+d\sqrt{2})}{\sqrt{2}^{k}}

## eq_2: Gate bound

$$
\text{gate count}=O(k)
$$

Claimed Clifford+T gate count with at most one ancilla.

Provenance: `abstract_inferred`. Stated bound in abstract.

Abstract evidence: achieves a bound of $O(k)$ gates

Equation assumptions:

- n<=2

## Registers

- data: n (n<=2) qubits; qubits on which the target operator acts
- ancilla: at most 1 qubits; optional helper qubit for Clifford+T synthesis of 2-level matrices

## Initial state

Data register in an arbitrary input state; ancilla (if used) in |0>.

## Measurement

None specified: this is a unitary synthesis task. For verification one could measure all data qubits (and the ancilla) in the computational basis after applying the circuit; the ancilla should return to |0> if used as a clean ancilla. This is an assumption, not from the abstract.

## Classical postprocessing

Classical work is the compilation: computing the 1-/2-level decomposition and gate sequences from the matrix entries (a,b,c,d,k). No measurement-outcome postprocessing is described.

## Algorithm steps

1. Take the unitary U with entries of the stated form (eq_1) and reduce it to a product of 1- and 2-level matrices over Z[i,1/sqrt2], following Giles-Selinger (details not given in abstract). (eq_1)
2. Implement each 1- and 2-level factor as a Clifford+T gate sequence, using at most one ancilla, so total gate count is O(k). (eq_2)

## Assumptions

- The operator is assumed unitary, as is needed for a circuit.
- Plan is a high-level outline following the cited Giles-Selinger approach.
- Measurement is only an optional verification choice; the abstract specifies none.
- Ancilla is assumed to be returned to |0>.

## Missing information

- Explicit decomposition algorithm
- Circuit details
- Ancilla usage details
- Explicit gate sequences for each 2-level factor
- Whether ancilla is clean/borrowed and how it is restored
