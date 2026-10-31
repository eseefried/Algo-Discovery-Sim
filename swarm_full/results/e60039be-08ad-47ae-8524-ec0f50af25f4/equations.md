# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Approximately decompose an n-qubit diagonal unitary with k distinct phases over the Clifford+T basis, minimizing the number of phase-rotation gates, with equivalent T-count bounded by k C_0 log2(1/eps) + E(n,k), where E(n,k) is the total entanglement cost in T gates.

Scope: Abstract-level specification of the T-count bound and the cost comparison against prior methods. The circuit construction, entanglement-cost formula and decision boundary are not given in the abstract and are not reconstructed.

## Symbols

- $n$: number of qubits of the diagonal unitary; domain: positive integer
- $k$: number of distinct phases in the diagonal unitary; domain: integer, 1 <= k <= 2^n
- $\varepsilon$: desired approximation precision; domain: (0,1)
- $C_0$: quality factor of the single-rotation synthesis method; domain: real, 1 < C_0 < 4
- $E(n,k)$: total entanglement cost in T gates; domain: nonnegative integer

## eq_1: T-count bound

$$
T_{\mathrm{eq}} \le k C_0 \log_2(1/\varepsilon) + E(n,k)
$$

Upper bound on the equivalent T-count of the synthesized circuit

Provenance: `abstract_inferred`. Stated in the abstract; the symbol T_eq is introduced for the equivalent T-count.

Abstract evidence: bounded by $kC_{0}\log_{2}(1/\varepsilon)+E(n,k)$

## eq_2: Quality factor range

$$
1 < C_0 < 4
$$

Range of the rotation-synthesis quality factor

Provenance: `abstract_explicit`. Stated in the abstract.

Abstract evidence: ($1<C_{0}<4$)

## eq_3: Diagonal unitary

$$
U=\sum_{x=0}^{2^n-1} e^{i\theta_x}|x\rangle\langle x|,\ |\{\theta_x\}|=k
$$

Diagonal n-qubit unitary with k distinct phases

Provenance: `standard_background`. Standard definition of a diagonal unitary with k distinct phase values.

## Registers

- q: n qubits; data qubits on which the diagonal unitary acts (assumed; any ancillas unspecified)

## Initial state

Arbitrary n-qubit input state; the diagonal unitary is applied as a gate, so no specific state preparation is given.

## Measurement

None specified in the abstract. The task is unitary synthesis; the circuit is a diagonal gate, so any evaluation would be by computational-basis measurement of an input state (phases invisible there) or by process/operator-norm comparison to the target, not by a measurement prescribed by the paper.

## Classical postprocessing

Classical compilation only: group diagonal entries into k distinct phases, choose parity/entanglement structure, run single-rotation Clifford+T synthesis to precision eps per phase, tally T-count against the bound, and compare cost with baselines over (n,k,eps) to find the decision boundary. Details are not in the abstract.

## Algorithm steps

1. Identify the k distinct phase values among the 2^n diagonal entries of U. (eq_3)
2. Build the entangling (Clifford/CNOT-type) structure that generates the needed phase-polynomial parities; its cost is E(n,k). Details are not given in the abstract. (eq_1)
3. Synthesize each of the k distinct phase rotations to precision eps over Clifford+T, using about C_0 log2(1/eps) T gates each. (eq_1, eq_2)
4. Sum the rotation and entanglement T-costs to obtain the total equivalent T-count bound. (eq_1)

## Assumptions

- T_eq denotes the equivalent T-count including the entanglement cost.
- Circuit steps are an assumed generic outline consistent with the abstract's cost structure, not the paper's actual construction.
- Measurement and postprocessing are inferred as a generic compilation workflow, not stated in the abstract.

## Missing information

- Explicit form of E(n,k)
- Circuit construction and registers
- Decision boundary in (n,k,eps) space
- Baseline methods compared against
- Actual circuit construction and ancilla registers
- How entanglement cost is realized concretely in the circuit
- Error metric defining precision eps and how errors accumulate over k rotations
