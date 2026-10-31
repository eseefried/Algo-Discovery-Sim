# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Exact/near-exact minimization of quantum cost (QC) of 4-bit reversible circuits built from multiple-control Toffoli (MCT) gates, using a tool that finds gate-count (GC) optimal Toffoli networks for any 4-variable reversible function; the abstract reports QC savings of up to 74% over previously published circuits for benchmarks.

Scope: Scoped to the mathematical formulation of the synthesis problem: a 4-bit reversible function as a permutation of {0,1}^4, an MCT-gate circuit model on 4 wires without ancillae, the gate-count and quantum-cost objectives, and the QC-savings metric. One tiny explicit instance is chosen as an assumption (target function = 3-control Toffoli on wires (x1,x2,x3 -> x4), compared under a standard QC table). Outside scope: the internal search algorithm of the GC-optimal synthesis tool, the specific QC cost model used in the paper, the benchmark set, the actual optimized circuits, and the reported 74% result, none of which are specified in the abstract.

## Symbols

- $n$: Number of bits/wires of the reversible circuit; domain: Fixed to n = 4 in this paper
- $x = (x_1,x_2,x_3,x_4)$: Input bit vector on the 4 wires; wire 1 is listed first (leftmost), integer encoding x = \sum_{i=1}^{4} x_i 2^{4-i} used only for labelling truth-table rows; domain: \{0,1\}^4
- $f$: Target 4-variable reversible function to be synthesized; domain: Bijection \{0,1\}^4 \to \{0,1\}^4, i.e. element of the symmetric group S_{16}
- $T(C;t)$: Multiple-control Toffoli gate with control set C and target wire t (|C|=0 is NOT, |C|=1 is CNOT, |C|=2 is Toffoli, |C|=3 is 3-control Toffoli); domain: C \subseteq \{1,2,3,4\}, t \in \{1,2,3,4\} \setminus C
- $G = (g_1,\dots,g_L)$: Reversible circuit (Toffoli network) given as an ordered sequence of MCT gates, g_1 applied first; domain: Finite sequence of gates T(C;t)
- $L = GC(G)$: Gate count of circuit G; domain: Non-negative integer
- $qc(g)$: Quantum cost of a single MCT gate under a chosen cost table; domain: Positive integer
- $QC(G)$: Quantum cost of circuit G (sum of gate costs); domain: Non-negative integer
- $\sigma$: Relative QC savings of a new circuit versus a previously known circuit; domain: Real number in [0,1) when the new circuit is cheaper

## eq_1: Reversible 4-bit function as a permutation

$$
f:\{0,1\}^4 \to \{0,1\}^4,\quad f \text{ bijective}\ \Leftrightarrow\ f \in S_{16}
$$

A 4-variable reversible function is a bijection on the 16 input patterns, equivalently a permutation of 16 elements; the synthesis target is any such f.

Provenance: `abstract_inferred`. 'Reversible circuit' and 'any 4-variable function' imply the standard model in which the target is a bijection on 4-bit strings; the abstract does not spell out the formal definition.

Abstract evidence: optimal gate count Toffoli networks for any 4variable function

Equation assumptions:

- No ancilla or garbage lines; the circuit acts on exactly the 4 function variables.

## eq_2: Multiple-control Toffoli gate action

$$
T(C;t):\ x_t \mapsto x_t \oplus \bigwedge_{c \in C} x_c,\qquad x_j \mapsto x_j\ \ (j \neq t)
$$

An MCT gate flips the target bit exactly when all control bits are 1 (the empty conjunction is 1, giving NOT); all other wires are unchanged. On 4 wires, 0 <= |C| <= 3.

Provenance: `standard_background`. Standard definition of the Toffoli-gate library used in reversible synthesis; the abstract only names 'Toffoli networks'.

Equation assumptions:

- Gate library is the MCT library (positive controls only); negative-control or Fredkin/Peres gates are not included unless the paper says otherwise.

## eq_3: Circuit realization and gate count

$$
f = g_L \circ g_{L-1} \circ \cdots \circ g_1,\qquad GC(G) = L,\qquad GC^{*}(f) = \min\{L : g_L\circ\cdots\circ g_1 = f\}
$$

A circuit realizes f exactly (not approximately) when the composition of its gates equals f as a permutation; the gate count is the number of gates, and the GC-optimal value is the minimum over all realizing circuits. The referenced tool computes GC^*(f) and an optimal circuit for every 4-bit f.

Provenance: `abstract_inferred`. Exact GC minimization means finding a realizing circuit with the minimum number of gates; the formulation is the standard reading of the abstract's claim.

Abstract evidence: exact minimization of gate count (GC) in 4-bit circuits

Equation assumptions:

- Exact equality of permutations is required (no don't-cares).

## eq_4: Quantum cost of a circuit

$$
QC(G) = \sum_{i=1}^{L} qc(g_i),\qquad qc(T(C;t)) = \begin{cases} 1 & |C| \in \{0,1\} \\ 5 & |C| = 2 \\ 13 & |C| = 3 \end{cases}
$$

Quantum cost is additive over gates. The displayed per-gate values (NOT/CNOT = 1, Toffoli = 5, 3-control Toffoli on 4 lines = 13) are a commonly used table from the reversible-logic literature; the specific table used in the paper is not given in the abstract.

Provenance: `standard_background`. Additivity of QC and this cost table are standard in the reversible-synthesis literature (e.g. RevLib conventions); the abstract only names 'quantum cost (QC)'.

Equation assumptions:

- Cost table values are an assumption about the paper's metric; the 3-control value in particular depends on the available free line and decomposition used.

## eq_5: QC minimization objective

$$
QC^{*}(f) = \min\{QC(G) : G \text{ realizes } f\},\qquad QC^{*}(f) \le \min\{QC(G) : G \text{ realizes } f,\ GC(G)=GC^{*}(f)\}
$$

The target is the minimum QC over all realizing circuits. Restricting to GC-optimal circuits only gives an upper bound, since a circuit with more but cheaper gates may have lower QC; the abstract describes applying the GC-optimal tool to QC reduction but not the exact mechanism (e.g. enumerating all GC-optimal circuits, or relaxing GC).

Provenance: `abstract_inferred`. Follows from the abstract's distinction between GC and QC minimization; the inequality is a direct consequence of definitions, the method itself is not specified.

Abstract evidence: presents an application of the above mentioned tool to reducing QC of 4-bit reversible circuits

Equation assumptions:

- How the GC-optimal tool is adapted to QC (search over all GC-optimal networks, or over networks with GC above optimum) is unknown.

## eq_6: Relative quantum-cost savings

$$
\sigma = 1 - \frac{QC(G_{\mathrm{new}})}{QC(G_{\mathrm{prev}})},\qquad \max_{\text{benchmarks}} \sigma \approx 0.74
$$

Savings are measured relative to the previously best-known circuit for the same function; the abstract reports a maximum of about 74% over benchmarks and published designs. The exact formula is the natural reading of 'savings of up to 74%', not stated explicitly.

Provenance: `abstract_inferred`. Standard interpretation of percentage savings relative to the previous cost; the 0.74 figure is the paper's reported number and is not verified here.

Abstract evidence: savings in QC of up to 74% comparing with previously known circuits

Equation assumptions:

- Savings are computed per function against the previously published circuit's QC under the same cost table.

## eq_7: Tiny explicit instance (chosen for a later circuit stage)

$$
f_0 = T(\{1,2,3\};4):\ (x_1,x_2,x_3,x_4) \mapsto (x_1,x_2,x_3,\ x_4 \oplus x_1 x_2 x_3),\qquad GC^{*}(f_0)=1,\quad QC(T(\{1,2,3\};4)) = 13 \text{ under eq\_4}
$$

Smallest nontrivial 4-bit target: the 3-control Toffoli itself. Its GC-optimal circuit is the single gate (QC 13 under the assumed table); whether a multi-gate network with lower QC exists illustrates the GC-vs-QC trade-off that the paper exploits. This instance is a choice, not from the abstract.

Provenance: `assumption`. A minimal concrete 4-bit permutation suitable for a 16-row truth-table check; chosen because no benchmark is specified in the abstract.

Equation assumptions:

- Instance and its GC-optimality follow from eq_2/eq_3 trivially (f_0 is a single library gate, so GC^*(f_0)=1); the stated QC uses the assumed cost table of eq_4.

## Registers

- x (4 wires): 4 qubits; Data lines carrying the 4 function variables x_1..x_4; wire 1 is the top/leftmost line and the most significant bit in the integer labelling of truth-table rows

## Initial state

Computational basis state |x_1 x_2 x_3 x_4\rangle for each of the 16 inputs x in {0,1}^4 (classical reversible evaluation; no superposition is required to specify or verify the circuit).

## Measurement

Computational-basis readout of all 4 wires for each of the 16 basis inputs (or classical simulation) to check that the circuit's truth table equals f; no non-trivial quantum measurement statistics are involved.

## Classical postprocessing

Compare the observed output table with f for exact equality; sum per-gate costs to obtain QC(G); compute savings sigma = 1 - QC_new/QC_prev relative to the previously known circuit.

## Algorithm steps

1. Specify the target 4-bit reversible function f as a permutation of {0,1}^4 (for the scoped instance, f_0 of eq_7). (eq_1, eq_7)
2. Obtain (from the GC-optimal synthesis tool, whose algorithm is not given in the abstract) a Toffoli network G of MCT gates realizing f exactly with minimum gate count. (eq_2, eq_3)
3. Evaluate the quantum cost of candidate realizing networks using the additive per-gate cost table, and select the network with minimum QC (search mechanism unspecified; restriction to GC-optimal networks only yields an upper bound on QC*). (eq_4, eq_5)
4. Apply the selected gate sequence g_1,...,g_L in order to the 4 wires; verify that the resulting permutation equals f on all 16 basis inputs. (eq_2, eq_3)
5. Compare QC of the new network with the previously known circuit for the same function and compute the relative savings. (eq_6)

## Assumptions

- Gate library is positive-control MCT gates on 4 lines with no ancillae.
- Quantum cost table NOT/CNOT = 1, Toffoli = 5, 3-control Toffoli = 13 is assumed; the paper's actual table may differ.
- Exact realization of the target permutation (no don't-care outputs).
- The tiny instance f_0 = T({1,2,3};4) is the author's own choice for a smallest useful construction, not a benchmark named in the abstract.
- Percentage savings are interpreted as 1 - QC_new/QC_prev.

## Missing information

- Identity and search algorithm of the GC-optimal 4-bit synthesis tool (e.g. BFS over permutations, meet-in-the-middle, symmetry reduction) are not described in the abstract.
- The exact quantum-cost model used (per-gate costs, treatment of negative controls, free-line discounts) is not stated.
- How the GC-optimal tool is adapted to QC minimization (enumeration of all GC-optimal networks, allowing GC above the optimum, post-processing/template rewriting) is unspecified.
- The list of benchmark functions and designs from recent publications, and the specific circuits achieving up to 74% savings, are not given.
- Whether the reported QC minimization is exact (provably optimal QC) or heuristic reduction is not stated.
