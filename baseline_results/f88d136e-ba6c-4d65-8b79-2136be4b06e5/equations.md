# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

All pairs shortest paths (APSP): given a weighted graph G=(V,E,w) with |V|=n and no negative cycles, compute the distance matrix d(i,j) for all vertex pairs. The abstract claims the first quantum algorithms running in O(n^{2.5-\varepsilon}) time for structured variants (geometrically weighted graphs, small integer weights, few distinct weights per vertex, all pairs earliest arrivals), improving on the trivial Grover-based \tilde{O}(n^{2.5}) algorithm.

Scope: The abstract gives no construction details for the paper's O(n^{2.5-\varepsilon}) algorithms. Scope is therefore restricted to the baseline the abstract explicitly references: the trivial \tilde{O}(n^{2.5}) quantum APSP algorithm, reconstructed as repeated (min,+) matrix squaring where each entry minimum is computed with Dürr–Høyer quantum minimum finding (Grover search with a threshold oracle). The circuit-level unit is a single Grover-marked threshold search over the summation index k for one fixed entry (i,j) and threshold t. Tiny instance: an undirected 4-vertex graph with weights w(0,1)=1, w(1,2)=1, w(0,2)=3, w(2,3)=1, w(1,3)=5 (non-edges = INF), so that two squarings are needed to obtain d(0,3)=3. OUTSIDE SCOPE (paper contributions not reconstructable from the abstract): the actual subcubic-improving quantum algorithms for geometric weights, small integer weights, bounded weights per vertex, and earliest arrivals, and the values of \varepsilon achieved.

## Symbols

- $G=(V,E,w)$: Input graph with vertex set V, edge set E and edge weights w; domain: |V|=n, w:E\to\mathbb{R}_{\ge 0}\cup\{\infty\} (nonnegative weights assumed; INF for non-edges)
- $n$: Number of vertices; domain: positive integer; n=4 in the tiny instance
- $d(i,j)$: Shortest path distance from vertex i to vertex j; domain: \mathbb{R}_{\ge 0}\cup\{\infty\}
- $D^{(\ell)}$: Matrix of shortest distances using paths with at most \ell edges; domain: n\times n matrix over \mathbb{R}_{\ge 0}\cup\{\infty\}; D^{(1)} is the weight matrix with zero diagonal
- $\star$: (min,+) matrix product; domain: binary operation on n\times n matrices
- $k$: Summation/search index over intermediate vertices; domain: \{0,\dots,n-1\}, encoded in \lceil\log_2 n\rceil qubits, big-endian binary
- $t$: Current threshold in quantum minimum finding; domain: \mathbb{R}\cup\{\infty\}
- $f_{t}(k)$: Threshold predicate marking indices whose candidate value is below t; domain: \{0,1\}
- $\varepsilon$: Constant by which the paper improves the exponent 2.5; domain: constant >0, value unspecified in abstract
- $\tilde{O}(\cdot)$: Big-O suppressing polylogarithmic factors; domain: asymptotic notation

## eq_1: APSP distance definition

$$
d(i,j)=\min_{P:\,i\to j}\ \sum_{(u,v)\in P} w(u,v)
$$

Shortest path distance as the minimum total weight over all i-to-j paths; d(i,i)=0 and d(i,j)=\infty if no path exists.

Provenance: `standard_background`. Standard definition of the APSP problem named in the abstract.

Equation assumptions:

- No negative cycles (nonnegative weights assumed in the tiny instance)

## eq_2: (min,+) product and repeated squaring

$$
(A\star B)_{ij}=\min_{k\in\{0,\dots,n-1\}}\big(A_{ik}+B_{kj}\big),\qquad D^{(2\ell)}=D^{(\ell)}\star D^{(\ell)},\qquad d(i,j)=D^{(2^{s})}_{ij}\ \text{for}\ s=\lceil\log_2(n-1)\rceil
$$

Exact equality: \lceil\log_2(n-1)\rceil successive (min,+) squarings of the weight matrix yield the distance matrix, since shortest paths use at most n-1 edges. For n=4, s=2.

Provenance: `standard_background`. Classical textbook reduction of APSP to O(\log n) (min,+) products; chosen here as the structure of the trivial baseline.

Equation assumptions:

- Nonnegative weights so shortest paths are simple
- INF arithmetic: INF + x = INF

## eq_3: Threshold oracle for one entry (i,j)

$$
O_{t}^{(i,j)}\,|k\rangle|b\rangle=|k\rangle\,|b\oplus f_{t}(k)\rangle,\qquad f_{t}(k)=\begin{cases}1,& D^{(\ell)}_{ik}+D^{(\ell)}_{kj}<t\\ 0,&\text{otherwise}\end{cases}
$$

Boolean oracle marking intermediate vertices k that improve the current threshold t for entry (i,j). With the flag qubit prepared in |-\rangle this acts as a phase oracle (-1)^{f_t(k)}. The matrix entries are classical data; the oracle is assumed implementable in \tilde{O}(1) time (QRAM-type access).

Provenance: `standard_background`. Standard marking oracle used by Dürr–Høyer minimum finding; the quantities compared come from eq_2.

Equation assumptions:

- Classical data accessible in superposition in polylog time (QRAM model)
- Comparator ancillas uncomputed

## eq_4: Grover iterate and iteration count

$$
|\psi\rangle=\frac{1}{\sqrt{n}}\sum_{k=0}^{n-1}|k\rangle,\qquad G_{t}=\big(2|\psi\rangle\langle\psi|-I\big)\,O_{t}^{(i,j)},\qquad r\approx\left\lfloor\frac{\pi}{4}\sqrt{\frac{n}{M_t}}\right\rfloor
$$

Grover iterate with diffusion over the index register; M_t is the (unknown) number of marked indices, so in practice the exponential-search schedule of Boyer–Brassard–Høyer–Tapp is used (random r in a growing range). This is an approximation: success probability is high but not 1.

Provenance: `standard_background`. The abstract attributes the trivial \tilde{O}(n^{2.5}) bound to Grover search; this is the standard Grover iterate and count.

Equation assumptions:

- n is not necessarily a power of 2; if not, pad the index register and mark padding indices as 0

## eq_5: Quantum minimum finding and baseline cost

$$
\min_{k}\big(D^{(\ell)}_{ik}+D^{(\ell)}_{kj}\big)\ \text{found with}\ O(\sqrt{n})\ \text{oracle queries (expected)},\qquad T_{\text{trivial}}=n^{2}\cdot O(\sqrt{n})\cdot\lceil\log_2 n\rceil=\tilde{O}(n^{2.5})
$$

Dürr–Høyer: repeated Grover threshold search with t updated to the last found value uses O(\sqrt{n}) expected queries. Applying it to all n^2 entries over O(\log n) squarings gives the trivial \tilde{O}(n^{2.5}) quantum APSP algorithm cited in the abstract.

Provenance: `abstract_inferred`. The abstract states the trivial quantum bound and its Grover origin; the decomposition into n^2 entries times \sqrt{n} minimum finding times \log n squarings is one standard way to realize it (an alternative is Dijkstra per source with quantum SSSP).

Abstract evidence: the trivial algorithm in the quantum setting runs in $\tilde{O}(n^{2.5})$ time, using Grover search

Equation assumptions:

- Dürr–Høyer expected query bound
- QRAM access to the current matrix

## eq_6: Paper's claimed improvement (not reconstructed)

$$
T_{\text{paper}}=O(n^{2.5-\varepsilon})\quad\text{for some constant}\ \varepsilon>0
$$

Target running time for the structured APSP variants. The abstract provides no algorithmic details enabling reconstruction of how this bound is achieved.

Provenance: `abstract_explicit`. Directly stated in the abstract.

Abstract evidence: obtain the first nontrivial (i.e. $O(n^{2.5-\varepsilon})$ time) quantum algorithms for the problems

## Registers

- idx: \lceil\log_2 n\rceil (2 qubits for n=4) qubits; Search index k over intermediate vertices; big-endian binary encoding of k
- flag: 1 qubits; Oracle output qubit, prepared in |-\rangle so the oracle acts as a phase oracle
- anc: unknown (depends on arithmetic/comparator implementation) qubits; Work qubits for computing D_{ik}+D_{kj} and comparing with t; uncomputed after each oracle call

## Initial state

|0\rangle^{\otimes\lceil\log_2 n\rceil}|1\rangle on (idx, flag); after H^{\otimes\lceil\log_2 n\rceil}\otimes H this is |\psi\rangle|-\rangle with |\psi\rangle the uniform superposition over k (eq_4). Classical data: D^{(1)} for the tiny instance with rows [0,1,3,INF],[1,0,1,5],[3,1,0,1],[INF,5,1,0].

## Measurement

Computational-basis measurement of the idx register after each Grover search round; outcome k' is a candidate intermediate vertex. The flag and ancilla registers are discarded (ancillas uncomputed).

## Classical postprocessing

Verify each measured candidate classically by computing D_{ik'}+D_{k'j} and comparing with the threshold t; update t to the improved value; after the query budget is exhausted the last threshold is the entry minimum (correct with high probability, not deterministically). Collect all n^2 entries into the squared matrix and iterate the squaring s times.

## Algorithm steps

1. Classical outer loop: set D^{(1)} to the weight matrix with zero diagonal; repeat the squaring step s=\lceil\log_2(n-1)\rceil times (s=2 for n=4). (eq_2)
2. For each entry (i,j), run quantum minimum finding: initialize threshold t=\infty (or a random index's value); prepare idx in uniform superposition and flag in |-\rangle. (eq_4, eq_5)
3. Apply the threshold oracle O_t^{(i,j)} and the diffusion operator r times (r chosen by the exponential-search schedule since the number of marked indices is unknown). (eq_3, eq_4)
4. Measure idx, obtain k'; classically verify f_t(k')=1 (compute D_{ik'}+D_{k'j}<t); if so set t to this value and repeat from the superposition preparation; stop after the Dürr–Høyer budget of O(\sqrt{n}) total queries and output the final t as (D\star D)_{ij}. (eq_3, eq_5)
5. Assemble the new matrix D^{(2\ell)} from all n^2 entries; after s squarings return it as the APSP distance matrix (e.g., d(0,3)=3 in the tiny instance via 0\to1\to2\to3). (eq_2)

## Assumptions

- No experiment_scope was provided; the chosen construction is the trivial Grover-based \tilde{O}(n^{2.5}) baseline via (min,+) squaring with Dürr–Høyer minimum finding, not the paper's improved algorithms.
- Tiny instance choice: undirected graph on 4 vertices with weights w(0,1)=1, w(1,2)=1, w(0,2)=3, w(2,3)=1, w(1,3)=5, non-edges INF.
- Nonnegative edge weights so shortest paths are simple and have at most n-1 edges.
- QRAM-style superposition access to classical matrix entries in polylogarithmic time, as is standard for Grover-based graph algorithms.
- Quantum minimum finding succeeds with high (not unit) probability; running times are expected/with-high-probability bounds.

## Missing information

- The actual algorithms achieving O(n^{2.5-\varepsilon}) for geometrically weighted graphs, small integer weights, few weights per vertex, and all pairs earliest arrivals are not described in the abstract.
- The specific values of \varepsilon obtained for each variant.
- Which classical subcubic techniques are quantized and how (e.g., use of quantum search over structured candidate sets, quantum walks, or fast matrix multiplication).
- Precise computational model assumptions (QRAM, query vs. time complexity) used by the paper.
- Formal definitions of the structured variants (geometric weights, earliest arrivals) as used by the paper.
