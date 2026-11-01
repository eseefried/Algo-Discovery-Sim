# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Construct families of graphs admitting efficient quantum walk implementations and quantum-walk-based search, with explicit quantum circuits implementing the full search algorithm (no black-box oracle), and numerically analyze search on a twisted toroid graph family needing O(sqrt(n) log(n)) two-qubit gates to find a marked node.

Scope: Abstract-level reconstruction: problem statement and the stated gate-complexity scaling only; graph definitions, coin/shift operators, circuit details and numerical data are not given in the abstract.

## Symbols

- $n$: number of nodes in the graph (search space size); domain: positive integer
- $G$: graph on which the quantum walk is performed; domain: graph with n nodes
- $T_{\mathrm{gates}}$: number of elementary 2-qubit gates needed to find a marked node; domain: positive integer

## eq_1: Gate complexity

$$
T_{\mathrm{gates}}=O\!\left(\sqrt{n}\,\log n\right)
$$

Elementary 2-qubit gate count for quantum walk search on the twisted toroid family to find a marked node.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: requires O($\sqrt{n}$ log($n$)) elementary 2-qubit quantum gate operations to find a marked node

## Registers

- position: ceil(log2 n) qubits (assumed) qubits; Encodes the graph node label for the walk
- coin: unknown (graph-degree dependent) qubits; Encodes the edge direction/coin state for the walk (assumed coined walk)

## Initial state

Assumed uniform superposition over all n nodes in the position register, with coin register in a uniform or fixed state.

## Measurement

Assumed: after the roughly sqrt(n) search iterations, measure the position register in the computational basis to obtain a node label; the marked node is expected to be found with high probability (the abstract gives no explicit success probability).

## Classical postprocessing

Assumed: check whether the measured node is the marked one; if not, repeat the run. The abstract does not specify this procedure.

## Algorithm steps

1. Prepare the initial state: uniform superposition over nodes (assumed). (no equation reference)
2. Repeatedly apply a circuit-implemented search step: marking operation (flip coin on marked node, implemented without a black-box oracle) followed by the coin and shift walk operator on the graph, for a number of iterations on the order of sqrt(n) (assumed). (eq_1)
3. Decompose each walk step into elementary 1- and 2-qubit gates; total cost is stated as O(sqrt(n) log n) 2-qubit gates for the twisted toroid family. (eq_1)

## Assumptions

- Coined discrete-time walk structure, register layout, and sqrt(n) iteration count are assumed, not stated in the abstract.
- Coined discrete-time walk with position and coin registers assumed.
- Measurement of the position register and a repeat-until-success check are assumed, not stated in the abstract.
- Measurement of the position register in the computational basis, with repeat-until-success verification, is assumed.

## Missing information

- Explicit definition of the twisted toroid graphs and other graph families
- Walk operator (coin/shift) and marking/search operator definitions
- Circuit decomposition, register sizes, iteration count
- Measurement and success-probability details
- Actual register sizes and gate-level decomposition per walk step
- Numerical data and the optimal stopping time from the twisted toroid analysis
- Success probability and optimal stopping time of the search are not given in the abstract.
