# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Solve Simon's Problem for a logical two-qubit black-box function f:{0,1}^2->{0,1}^2 with hidden period s (f(x)=f(y) iff y=x or y=x XOR s), using a one-way (measurement-based) implementation on a five-qubit photonic cluster state, with single-qubit measurement bases adapted to query representative functions.

Scope: Small finite instance: n=2 logical qubits Simon algorithm on a five-qubit cluster state; the abstract does not give the cluster geometry, measurement angles, or the specific functions. The n-qubit resource analysis is out of scope.

## Symbols

- $f$: Black-box function promised to be two-to-one with hidden period s; domain: f:{0,1}^n->{0,1}^n, n=2
- $s$: Hidden period (bit string); domain: s in {0,1}^n
- $y$: Measured output string of the input register; domain: y in {0,1}^n

## eq_1: Simon promise

$$
f(x)=f(x\oplus s)\ \ \forall x
$$

Defines the hidden period of the black-box function.

Provenance: `standard_background`. Standard definition of Simon's Problem; the abstract only names a period-finding black-box problem.

Equation assumptions:

- Two-to-one promise with s nonzero, or one-to-one for s=0

## eq_2: Orthogonality condition

$$
y\cdot s=0 \pmod 2
$$

Each measured string y is orthogonal to s; collecting independent y's determines s.

Provenance: `standard_background`. Standard Simon's algorithm output property, not stated in the abstract.

Equation assumptions:

- Ideal noiseless operation

## Registers

- cluster_input: 2 qubits (assumed logical input register) qubits; Logical input register x, ends up measured to give y
- cluster_output: 2 qubits (assumed logical output register) qubits; Holds f(x) values; measured/discarded
- cluster_aux: 1 qubit (assumed) qubits; Fifth cluster qubit; role not specified in abstract

## Initial state

Five-qubit photonic cluster state (graph geometry not given in abstract); logical registers assumed initialised in |+> via the cluster.

## Measurement

Single-qubit projective measurements of the photonic cluster qubits, with bases set per function (angles not given in the abstract). Outcomes of the qubits carrying the logical input register give the string y; the other qubits' outcomes are byproduct or output information (assumed).

## Classical postprocessing

Repeat runs to collect independent y strings satisfying y.s=0 mod 2 and solve the linear system over GF(2) for s. For n=2, a nonzero y fixes s, and y=00 gives no information. Compare outcome distributions with the theoretical model (assumed).

## Algorithm steps

1. Prepare the five-qubit cluster state. (no equation reference)
2. Choose single-qubit measurement bases on the cluster qubits to implement the black-box oracle for a representative function f (the Simon promise). (eq_1)
3. Measure remaining qubits in bases that realise the final Hadamard-type step, yielding output string y satisfying the orthogonality condition. (eq_2)

## Assumptions

- Standard Simon's algorithm relations are used as background
- Register sizes and roles are assumed, as the abstract only states five qubits and two logical qubits
- Register split 2 input + 2 output + 1 auxiliary is assumed
- Measurement readout and postprocessing follow the standard Simon algorithm
- Measurement outcomes of the input-register qubits yield y; postprocessing is the standard GF(2) solve

## Missing information

- Cluster state graph and qubit roles
- Measurement angles for each function
- Specific functions tested
- Feed-forward details
- Exact postprocessing details
- Actual mapping of the five physical qubits to logical registers
- Which physical qubits are read out for y and how byproduct corrections are applied
