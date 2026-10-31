# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Evaluate a binary NAND formula on N input bits using a discrete-query quantum algorithm, with query complexity O(sqrt(N)) for balanced formulas and O(N^{1/2+O(1/sqrt(log N))}) for arbitrary formulas.

Scope: Only the query-complexity claims in the abstract are reconstructed; no circuit, algorithm construction, or measurement details are given, so the scope is limited to the problem statement and complexity bounds.

## Symbols

- $N$: Number of input variables (leaves) of the NAND formula; domain: positive integers
- $Q_{bal}(N)$: Discrete query complexity for balanced binary NAND formulas; domain: nonnegative integers
- $Q_{arb}(N)$: Discrete query complexity for arbitrary binary NAND formulas; domain: nonnegative integers

## eq_1: Balanced formula query bound

$$
Q_{bal}(N)=O(\sqrt{N})
$$

Query complexity of evaluating balanced binary NAND formulas.

Provenance: `abstract_inferred`. Stated in abstract as an O(sqrt N) query bound; the notation Q_bal is introduced here.

Abstract evidence: O(√N) discrete query quantum algorithm for evaluating balanced binary NAND formulas

## eq_2: Arbitrary formula query bound

$$
Q_{arb}(N)=O\left(N^{\frac12+O\left(\frac{1}{\sqrt{\log N}}\right)}\right)
$$

Query complexity of evaluating arbitrary binary NAND formulas.

Provenance: `abstract_inferred`. The abstract gives an exponent of 1/2+O(1/sqrt(log N)); the text is garbled, so the exponent is read from its form.

Abstract evidence: discrete query quantum algorithm for evaluating arbitrary binary NAND formulas

Equation assumptions:

- Garbled exponent in abstract read as N^{1/2+O(1/sqrt(log N))}.

## Registers

- X: N classical input bits accessed via oracle qubits; Black-box input string queried through a discrete (standard) oracle; not a quantum register
- query: ceil(log2 N) qubits (assumed) qubits; Index register selecting which leaf to query
- work: unknown qubits; Workspace for the formula-evaluation procedure, for example a walk on the formula tree

## Initial state

Assumed: all registers in a fixed basis state, then a uniform or tree-root-based starting state set up by the unspecified algorithm.

## Measurement

Assumed: after the final query step, measure the designated output (root) qubit in the computational basis; the outcome is taken as the formula value. The abstract does not specify the measurement.

## Classical postprocessing

Assumed: output the measured bit as the formula value; optionally repeat a constant number of times and take the majority to reduce error. The abstract states no error probability.

## Algorithm steps

1. Assumed: prepare the initial state on the index and work registers, encoding the formula tree structure. (no equation reference)
2. Apply an unspecified sequence of discrete oracle queries interleaved with formula-dependent unitaries. The total number of queries is Q_bal(N)=O(sqrt N) for balanced formulas. (eq_1)
3. For arbitrary formulas, use the same kind of procedure with total queries bounded by Q_arb(N). (eq_2)

## Assumptions

- Exponent in the abstract read as 1/2+O(1/sqrt(log N)).
- Register sizes and the step structure are generic assumptions, not taken from the abstract.
- Generic oracle-based circuit skeleton assumed; it is not drawn from the abstract.
- Measurement of a root or output qubit with optional majority vote is assumed, not from the abstract.

## Missing information

- Algorithm construction (for example a quantum walk or span program) is not described.
- Registers, initial state, and measurement are not specified.
- Error probability is not stated.
- Exact unitaries between queries are unknown.
- Actual measurement procedure and postprocessing are not given in the abstract.
