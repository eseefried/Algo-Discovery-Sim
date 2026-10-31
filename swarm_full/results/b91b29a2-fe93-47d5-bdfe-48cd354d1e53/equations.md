# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Decompose a diagonal Hermitian quantum gate on n qubits into multiple-controlled Z gates by mapping the gate to a binary representation and expressing it in the basis given by the binary representations of multiple-controlled Z gates. CZ is proposed as the two-qubit library gate in place of CNOT.

Scope: Small finite instance: an n-qubit diagonal Hermitian gate with entries +1 or -1, decomposed over GF(2). The abstract does not give the exact binary encoding, cost model or experimental benchmarks, so these are not reconstructed.

## Symbols

- $D$: diagonal Hermitian gate, D=diag((-1)^{f(x)}); domain: 2^n x 2^n unitary
- $f(x)$: binary vector representing D, f(x) in {0,1}; domain: x in {0,1}^n
- $c_S$: coefficient selecting the multiple-controlled Z gate on qubit subset S; domain: GF(2)
- $Z_S$: multiple-controlled Z gate acting on qubit subset S; domain: S subset of {1..n}, nonempty

## eq_1: Diagonal Hermitian form

$$
D=\sum_x (-1)^{f(x)}|x\rangle\langle x|
$$

A diagonal gate that is Hermitian and unitary has entries +1 or -1, so it is fixed by a binary vector f.

Provenance: `abstract_inferred`. Unitarity plus Hermiticity forces entries of +1 or -1. The truth-table vector f is a plausible form of the representation, not the paper's confirmed definition.

Abstract evidence: a binary representation for the diagonal Hermitian gates is introduced

Equation assumptions:

- The binary representation is the vector f over the computational basis.

## eq_2: MCZ decomposition

$$
D=\prod_{S}Z_S^{c_S},\quad f(x)=\bigoplus_S c_S\prod_{i\in S}x_i
$$

The decomposition is a GF(2) linear combination of the MCZ binary vectors, i.e. an algebraic normal form.

Provenance: `abstract_inferred`. The basis claim implies a unique GF(2) expansion. The monomial form is the standard background realization of that basis.

Abstract evidence: the binary representations of multiple-controlled $Z$ gates form a basis for the vector space

Equation assumptions:

- The vector space is over GF(2).
- MCZ on S has binary vector equal to the monomial product of x_i for i in S.

## Registers

- q: n qubits; data qubits on which the diagonal Hermitian gate D acts

## Initial state

Arbitrary n-qubit input state; the decomposed circuit is diagonal, so no special preparation is required.

## Measurement

None: this is a unitary decomposition task. Correctness is checked by comparing the circuit's diagonal with D, not by measurement.

## Classical postprocessing

Classical GF(2) computation of c_S from f (Moebius/ANF transform), then listing the subsets with c_S=1 as the gate list.

## Algorithm steps

1. Form the binary vector f from the diagonal entries of D (entry -1 maps to 1, +1 maps to 0). (eq_1)
2. Solve for the GF(2) coefficients c_S by expanding f in the MCZ monomial basis (algebraic normal form, e.g. Moebius transform). (eq_2)
3. For each S with c_S=1, apply a multiple-controlled Z on the qubits in S; singletons are Z gates and pairs are CZ. The gates commute, so order is free. (eq_2)

## Assumptions

- The binary representation is the truth-table vector over GF(2).
- The basis is the set of monomials indexed by nonempty subsets S.
- MCZ gates commute, so application order does not matter.
- The step order is an inferred reconstruction.
- The measurement and postprocessing entries are inferred, not from the abstract.
- Measurement and postprocessing entries are inferred reconstructions.

## Missing information

- Exact binary representation definition used in the paper
- Cost metric and benchmark details
- The paper's algorithm for the basis change, and any gate-ordering optimization, are not given in the abstract.
- Whether the global phase or the identity (empty S) term is handled is unspecified.
- Handling of the empty-subset (global phase) term is not specified.
