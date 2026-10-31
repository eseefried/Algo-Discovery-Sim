# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Reduce quantum cost (QC) of 4-bit reversible circuits by applying an existing tool that finds gate-count-optimal Toffoli networks for any 4-variable function, and compare QC against previously known circuits for benchmarks and published designs.

Scope: Classical reversible circuit synthesis/optimization on 4 bits; no quantum algorithm with measurement. Abstract gives no details of the tool or the QC procedure, so only the optimization objectives and the reported savings are reconstructed.

## Symbols

- $GC$: Gate count of a reversible circuit; domain: non-negative integers
- $QC$: Quantum cost of a reversible circuit; domain: non-negative integers
- $f$: 4-variable reversible function (permutation of 16 states); domain: permutations of {0,1}^4
- $S$: Relative QC saving versus previously known circuit; domain: [0,1]

## eq_1: GC minimization

$$
\min_{C:\,C\equiv f} \mathrm{GC}(C)
$$

Exact minimization of gate count of a Toffoli network C realizing f; the tool solves this for 4 variables.

Provenance: `abstract_inferred`. Abstract states the tool finds optimal GC Toffoli networks for any 4-variable function.

Abstract evidence: finding optimal gate count Toffoli networks for any 4variable function

Equation assumptions:

- Toffoli gate library

## eq_2: QC minimization goal

$$
\min_{C:\,C\equiv f} \mathrm{QC}(C)
$$

Target objective: reduce quantum cost of circuits realizing f.

Provenance: `abstract_inferred`. Abstract names QC minimization in 4-bit circuits as the goal.

Abstract evidence: exact minimization of quantum cost (QC) in 4-bit circuits

## eq_3: Relative saving

$$
S=\frac{\mathrm{QC}_{\mathrm{prev}}-\mathrm{QC}_{\mathrm{new}}}{\mathrm{QC}_{\mathrm{prev}}}\le 0.74
$$

Relative QC saving versus previously known circuits; reported maximum about 74%.

Provenance: `abstract_inferred`. Formalizes the stated percentage saving; the formula is the standard definition.

Abstract evidence: savings in QC of up to 74% comparing with previously known circuits

Equation assumptions:

- Saving defined as relative reduction

## Registers

- x: 4 qubits; Four-bit reversible data lines carrying the input/output of f (classical bits)

## Initial state

Classical 4-bit input x in {0,1}^4; the circuit realizes the permutation f on all 16 basis states (no quantum superposition required).

## Measurement

No quantum measurement. Evaluation is classical: verify the synthesized network reproduces f on all 16 input states, and compute GC and QC of the result.

## Classical postprocessing

Compute QC of each candidate network under a QC model, select the minimum, and compute the relative saving S against the previously known circuit's QC for each benchmark/design; report the maximum (up to 74%).

## Algorithm steps

1. Take a 4-bit reversible function f from a benchmark or published design, with its previously known circuit and QC. (eq_2, eq_3)
2. Apply the GC-optimal Toffoli network synthesis tool to f (or to 4-bit sub-blocks) to get a minimal-gate-count network. (eq_1)
3. Evaluate QC of the resulting network (and alternatives) under a QC model; keep the lowest-QC realization. The exact procedure is not given in the abstract. (eq_2)
4. Compare new QC with previously known QC to compute the saving. (eq_3)

## Assumptions

- Savings are the standard relative reduction in QC.
- Step 3 assumes QC is evaluated per candidate network; the abstract does not specify how.
- Circuit plan is a generic classical synthesis workflow, not a quantum circuit.
- Functional verification on all 16 inputs is assumed as the check; the abstract does not state it.
- Functional equivalence is checked by exhaustive evaluation on 16 inputs.

## Missing information

- Quantum cost model per gate
- How GC-optimal networks are converted or used to reduce QC
- Specific benchmarks and QC values
- Tool algorithm details
