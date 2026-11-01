# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Exact or near-exact minimization of gate count and quantum cost (QC) of 4-bit reversible circuits built from Toffoli-type (NCT) gates. The abstract only states that an existing optimal-gate-count tool is applied to reduce QC; no algorithm details are given.

Scope: Tiny instance: a 4-bit reversible function as a permutation of {0..15}, a Toffoli-gate network realizing it, and a quantum cost sum over gates. The tool's internal search, the benchmarks, and the 74% savings result are outside scope and not reconstructed.

## Symbols

- $f$: 4-variable reversible function, a permutation; domain: bijection on {0,1}^4 (S_16)
- $G_i$: i-th gate in the cascade; domain: NOT, CNOT, Toffoli (assumed gate library)
- $n$: number of gates (gate count GC); domain: nonnegative integer
- $c(G)$: quantum cost of a gate; domain: positive integer
- $QC$: total quantum cost of a circuit; domain: positive integer
- $x$: 4-bit input vector; domain: {0,1}^4

## eq_1: Circuit realization

$$
f = G_n \circ \cdots \circ G_2 \circ G_1
$$

A cascade of reversible gates implements f.

Provenance: `standard_background`. Standard definition of reversible circuit synthesis; the abstract does not state it.

Equation assumptions:

- Gates applied in order G_1 first

## eq_2: Gate count minimization

$$
\mathrm{GC}(f)=\min\{ n : f = G_n\circ\cdots\circ G_1,\ G_i\in\mathcal{L}\}
$$

Optimal gate count over library L of Toffoli-type gates.

Provenance: `abstract_inferred`. The abstract says the tool finds optimal-gate-count Toffoli networks; the formula is a formalization.

Abstract evidence: finding optimal gate count Toffoli networks for any 4variable function

Equation assumptions:

- L is the NCT-style library of NOT, CNOT, Toffoli

## eq_3: Quantum cost of a circuit

$$
\mathrm{QC}=\sum_{i=1}^{n} c(G_i)
$$

Total quantum cost as additive sum of per-gate costs.

Provenance: `standard_background`. Common cost model in reversible synthesis; the abstract does not give the cost values.

Equation assumptions:

- Additive cost model
- Commonly used values c(NOT)=1, c(CNOT)=1, c(Toffoli)=5 (recalled, not from abstract)

## eq_4: QC minimization objective

$$
\mathrm{QC}^*(f)=\min_{(G_1,\dots,G_n):\,G_n\circ\cdots\circ G_1=f}\ \sum_{i=1}^{n} c(G_i)
$$

Goal of reducing QC; the minimum may need more gates than GC(f).

Provenance: `abstract_inferred`. The abstract names QC minimization as the target; the formal objective is inferred.

Abstract evidence: exact minimization of quantum cost (QC) in 4-bit circuits

Equation assumptions:

- Search is over the same gate library
- How the tool is used to reach QC-optimal circuits is not specified

## eq_5: Relative saving

$$
s = \frac{\mathrm{QC}_{\mathrm{old}}-\mathrm{QC}_{\mathrm{new}}}{\mathrm{QC}_{\mathrm{old}}}\times 100\%
$$

Percentage QC saving versus a previously known circuit.

Provenance: `abstract_inferred`. The percentage definition is the natural reading of the claim; the abstract states no formula.

Abstract evidence: savings in QC of up to 74% comparing with previously known circuits

Equation assumptions:

- Saving defined relative to the old QC

## Registers

- x: 4 qubits; Four reversible lines carrying the bit vector, encoded as integer 0..15 (assumed x_0 least significant)

## Classical postprocessing

Compute QC for candidate circuits and compare with previously published circuits to get percentage savings.

## Algorithm steps

1. Specify target 4-bit permutation f and gate library with per-gate costs. (eq_1, eq_3)
2. Use an optimal-GC synthesis tool to obtain minimal-gate Toffoli networks (details not given). (eq_2)
3. Select or search for the circuit that minimizes QC (mechanism unspecified) and compute saving versus known circuits. (eq_4, eq_5)

## Assumptions

- The gate library is NOT, CNOT, Toffoli with the usual costs; the abstract does not specify them
- Instance is a generic 4-bit permutation, not a specific benchmark

## Missing information

- How the optimal-GC tool is adapted to minimize QC
- The exact gate library and QC cost table
- The benchmarks and circuits compared
- Algorithm and data-structure details of the tool
- Any quantum circuit state preparation or measurement (this is classical synthesis)
