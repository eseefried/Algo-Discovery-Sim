# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a 4-bit reversible function as a permutation pi of {0..15}, find a cascade of NOT/CNOT/Toffoli (optionally Peres, Fredkin) gates on 4 wires realizing pi with minimum quantum cost QC (sum of gate costs), then realize it as a 4-qubit circuit and verify it reproduces pi.

Scope: One tiny explicit instance: 4 wires, NCT library with optional Peres/Fredkin, exact minimum-QC synthesis by meet-in-the-middle over permutations, then Qiskit realization and basis-state verification of all 16 inputs. Not covered: the paper's actual gate-count-optimal tool internals, equivalence-class symmetry reduction details, benchmark list, and the reported savings of up to 74%.

## Symbols

- $\pi$: target reversible function as a permutation; domain: S_{16}, bijection on {0,...,15}
- $g_i$: i-th gate of the network, as a permutation of {0..15}; domain: gate library L
- $c(g)$: quantum cost of gate g; domain: positive integers
- $QC$: total quantum cost of a network; domain: nonnegative integers
- $k$: cost bound in the search; domain: nonnegative integer
- $H_j$: hash table of permutations reachable with cost at most j; domain: subset of S_{16}
- $x$: basis input on wires (a,b,c,d); in Qiskit, a is qubit 0 (little-endian integer x=a+2b+4c+8d); domain: {0..15}

## eq_1: Network realizes target

$$
\pi = g_m\circ\cdots\circ g_2\circ g_1
$$

A cascade of gates composes to the target permutation.

Provenance: `assumption`. Standard model of reversible circuits as permutations; chosen for the specification.

Equation assumptions:

- No ancilla lines
- Gate order g_1 applied first

## eq_2: Quantum cost as sum of gate costs

$$
QC=\sum_{i=1}^m c(g_i),\quad c(\mathrm{NOT})=c(\mathrm{CNOT})=1,\ c(\mathrm{Toffoli})=5,\ c(\mathrm{Peres})=4,\ c(\mathrm{Fredkin})=7
$$

Additive NCV-based cost metric.

Provenance: `standard_background`. Standard quantum cost values recalled from the literature; the abstract only names quantum cost.

Equation assumptions:

- Standard NCV cost values

## eq_3: Optimal cost objective

$$
QC^*(\pi)=\min\{\sum_i c(g_i):\ g_m\circ\cdots\circ g_1=\pi,\ g_i\in L\}
$$

Exact minimization of quantum cost over networks in library L.

Provenance: `abstract_inferred`. The abstract states the goal of exact QC minimization; the formula is the natural formalization.

Abstract evidence: exact minimization of quantum cost (QC) in 4-bit circuits

Equation assumptions:

- L = NCT, optionally with Peres and Fredkin

## eq_4: Meet-in-the-middle match

$$
QC^*(\pi)=\min_{\sigma\in H_{\lceil k/2\rceil},\ \tau\in H_{\lfloor k/2\rfloor},\ \tau\circ\sigma=\pi}\big(QC(\sigma)+QC(\tau)\big),\quad \text{equivalently } \tau^{-1}\circ\pi=\sigma\ \text{is looked up in }H
$$

For each stored tau, test whether tau^{-1} composed with pi lies in the hash table; the minimum over k gives the exact optimum.

Provenance: `assumption`. The meet-in-the-middle search comes from the sketch, not the abstract. Splitting by cost across gate boundaries needs care, since a gate's cost may straddle the midpoint.

Equation assumptions:

- Gate set closed under inversion (true for NCT, Peres inverse may need to be added)
- Search over increasing k

## eq_5: Relative saving

$$
\text{saving}=100\cdot\frac{QC_{\text{prev}}-QC^*}{QC_{\text{prev}}}\ \%
$$

Percentage saving relative to a previously known circuit.

Provenance: `abstract_inferred`. The abstract reports percent savings; the formula is the usual definition.

Abstract evidence: savings in QC of up to 74% comparing with previously known circuits

Equation assumptions:

- QC_prev given for each benchmark

## Registers

- q[0..3]: 4 qubits; data wires a,b,c,d; qubit 0 = a (least significant bit); no ancillas

## Initial state

Computational basis state |x> for each x in {0..15}, run one at a time, or the unitary is read directly.

## Measurement

None for unitary check; alternatively read the statevector for each basis input and compare the output index to pi(x).

## Classical postprocessing

Compute QC of the found network, compare with the known circuit's QC, and report the percent saving.

## Algorithm steps

1. Define the gate library with costs and each gate as a permutation of 16 values. (eq_2)
2. BFS over cost levels (Dijkstra by cost) to build hash tables of permutations reachable at cost up to k/2, optionally reduced by wire-permutation and inversion symmetry. (eq_4)
3. For increasing k, match the target against products with stored permutations to find the minimal-cost decomposition. (eq_3, eq_4)
4. Build the network in Qiskit using x, cx, ccx; Peres as ccx then cx; verify that the unitary or basis mapping equals pi. (eq_1)
5. Compute QC as the sum of costs and the percent saving versus the reference circuit. (eq_2, eq_5)

## Assumptions

- Standard NCV costs NOT/CNOT=1, Toffoli=5, Peres=4, Fredkin=7
- Exact gate-count-optimal 4-variable synthesizer can be reused or extended for QC
- No ancilla lines
- Gate library is NCT, possibly with Peres and Fredkin
- Targets are 16-entry permutations
- Qiskit realization uses ccx; the 5-primitive NCV decomposition is for costing only

## Missing information

- Exact search algorithm and symmetry reduction of the original tool
- Specific benchmark functions and their previous QC values
- Costs for larger controlled gates
- Handling of cost straddling in the meet-in-the-middle split
- Whether a SAT or BFS method was used
