# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Given oracle access to an N-bit input x in {0,1}^N and a fixed balanced binary NAND formula (a complete binary tree of depth d with N = 2^d leaves, every internal node a 2-input NAND gate), compute the formula value f(x) in {0,1} using O(sqrt(N)) discrete queries to x; the abstract also claims N^{1/2+O(1/sqrt(log N))} queries for arbitrary binary NAND formulas via a more general construction.

Scope: Scope (assumed, since no experiment_scope was supplied): the balanced-formula O(sqrt(N)) algorithm only, reconstructed from standard background on quantum-walk NAND-tree evaluation (Farhi–Goldstone–Gutmann Hamiltonian criterion and its discrete-query quantization by phase estimation on a Szegedy/coined walk). Tiny explicit instance: depth d = 2, N = 4, f(x) = NAND(NAND(x_1,x_2), NAND(x_3,x_4)). Out of scope: the paper's exact edge weights and tail/output-edge construction, its precise spectral-gap theorem, the formula-rebalancing step and the resulting N^{1/2+O(1/sqrt(log N))} bound for arbitrary (unbalanced) formulas, and any analysis of error probability constants.

## Symbols

- $N$: number of input bits / leaves of the formula tree; domain: positive integer, N = 2^d for the balanced case
- $d$: depth of the balanced binary formula tree; domain: non-negative integer
- $x = (x_1,\dots,x_N)$: input bit string accessed only through the query oracle; domain: \{0,1\}^N
- $f(x)$: value of the NAND formula on input x; domain: \{0,1\}
- $T, V, E$: formula tree, its vertex set (root r, internal gate vertices, leaves 1..N, plus an extra tail/output vertex t adjacent to r) and its edge set; domain: finite graph
- $T_x$: input-dependent graph obtained from T by keeping leaf i (and its edge) iff x_i = 0; domain: finite graph
- $H_x$: adjacency matrix of T_x, viewed as a Hamiltonian; domain: real symmetric matrix on \mathbb{C}^{|V|}
- $O_x$: phase query oracle for the input; domain: unitary on the leaf-index register
- $W_x$: one step of the discrete-time quantum walk on T encoding x through the leaf coins; domain: unitary on span\{|u,v\rangle : (u,v) directed edge of T\}
- $\delta$: phase-estimation precision; domain: positive real, \delta = \Theta(1/\sqrt{N})
- $m$: number of phase-estimation ancilla qubits; domain: positive integer, m = \lceil \log_2(1/\delta) \rceil + O(1)
- $r_v$: zero-energy amplitude ratio \psi_v/\psi_{p(v)} between vertex v and its parent p(v); domain: \mathbb{R}\cup\{\infty\}

## eq_1: Balanced binary NAND formula

$$
f_v(x)=\begin{cases} x_i & v=\text{leaf } i\\ \mathrm{NAND}\big(f_{c_1(v)}(x),f_{c_2(v)}(x)\big)=1-f_{c_1(v)}(x)\,f_{c_2(v)}(x) & v \text{ internal}\end{cases},\qquad f(x)=f_r(x),\quad N=2^d
$$

Recursive definition of the function to be evaluated on the complete binary tree of depth d; for the tiny instance d=2, f(x)=1-(1-x_1x_2)(1-x_3x_4).

Provenance: `abstract_inferred`. The abstract names the problem class; the recursive NAND definition and N=2^d for a balanced binary tree are the standard meaning of that phrase.

Abstract evidence: evaluating balanced binary NAND formulas

Equation assumptions:

- 'balanced binary' is taken to mean a complete binary tree with N=2^d leaves, each leaf a distinct variable

## eq_2: Discrete query oracle

$$
O_x\,|i\rangle=(-1)^{x_i}\,|i\rangle,\qquad i\in\{1,\dots,N\}
$$

Standard phase oracle counted as one discrete query; equivalent up to one ancilla to the bit-flip oracle |i,b\rangle\mapsto|i,b\oplus x_i\rangle.

Provenance: `standard_background`. The abstract specifies the 'discrete query' model; this is the standard quantum query oracle definition.

## eq_3: Zero-energy eigenvector criterion (Hamiltonian picture)

$$
H_x=\sum_{(u,v)\in E(T_x)}\big(|u\rangle\langle v|+|v\rangle\langle u|\big),\qquad H_x\psi=0\ \Rightarrow\ r_v=-\Big(\sum_{c\in\text{children}(v)} r_c\Big)^{-1},\quad r_{\text{leaf } i}=\begin{cases}\infty & x_i=0 \text{ (leaf present)}\\ 0 & x_i=1 \text{ (leaf absent)}\end{cases},\qquad f_v(x)=1\iff r_v=0,\ \ f_v(x)=0\iff r_v=\infty
$$

Zero-energy eigenvector equations of the adjacency Hamiltonian propagate the formula value up the tree: a vertex whose subtree forces its parent's amplitude to vanish (r_v=\infty) carries value 0, otherwise value 1. For the tiny instance, x=(1,1,0,0) gives r_a=0 (NAND(1,1)=0 would require r_a=\infty) — note the recursion must be read with the stated leaf convention.

Provenance: `standard_background`. This is the Farhi–Goldstone–Gutmann NAND-tree mechanism recalled from memory; the leaf-presence convention (present iff x_i=0) is one of two dual conventions and may differ from the paper's.

Equation assumptions:

- Unit edge weights (sufficient for the balanced case in the recalled background; the paper may use non-uniform weights)
- Leaf i present iff x_i=0; the dual convention yields the complemented NOR tree

## eq_4: Discrete-time walk step with input-dependent leaf coins

$$
W_x=S\,C_x,\qquad S|u,v\rangle=|v,u\rangle,\qquad C_x=\bigoplus_{v\in V}C_v,\quad C_v=2|\phi_v\rangle\langle\phi_v|-I_v\ (v \text{ non-leaf}),\quad C_{\text{leaf } i}=(-1)^{x_i}\,I,\qquad |\phi_v\rangle=\frac{1}{\sqrt{\deg v}}\sum_{u\sim v}|v,u\rangle
$$

Szegedy/coined quantization of the walk on the tree T; the only input dependence is the leaf coin, which is the oracle O_x applied to the leaf-index part of the edge register, so one application of W_x costs O(1) queries. Its eigenphase-0 eigenvectors correspond to zero-energy eigenvectors of H_x.

Provenance: `standard_background`. Standard quantum-walk quantization used in discrete-query NAND-tree algorithms (Ambainis–Childs–Reichardt–Špalek–Zhang); exact weights, tail construction and the leaf sign convention in the paper are not available.

Equation assumptions:

- Coins use uniform (unweighted) Grover diffusion; the paper may use weighted coins
- Leaf coin sign convention chosen to match eq_3's leaf-presence convention; it may be the opposite in the paper

## eq_5: Phase estimation decision rule and query count

$$
|\psi_0\rangle=|t,r\rangle,\qquad \text{PE}\big(W_x,\delta\big)\ \text{with}\ \delta=\frac{c}{\sqrt{N}}:\quad \hat f(x)=\begin{cases}1 & \text{estimated phase }\hat\theta=0\\ 0 & |\hat\theta|\ge\delta\end{cases},\qquad Q=O(1/\delta)=O(\sqrt{N})\ \text{queries}
$$

Start on the output (tail) edge, run phase estimation on W_x to precision \delta; the formula value is read off from whether the initial state has large overlap with an eigenphase-0 eigenvector (f=1) or lies in the subspace with eigenphases bounded away from 0 by \Omega(1/\sqrt N) (f=0). Phase estimation to precision \delta uses O(1/\delta) applications of W_x, each O(1) queries.

Provenance: `abstract_inferred`. The abstract asserts the O(sqrt N) query bound; the phase-estimation route and the Θ(1/sqrt N) gap are the standard mechanism recalled from background and are the natural way to achieve a discrete-query bound of this form. Which value corresponds to phase 0 depends on the sign/leaf conventions.

Abstract evidence: O(√N) discrete query quantum algorithm for evaluating balanced binary NAND formulas

Equation assumptions:

- Spectral gap of W_x away from eigenphase 0 is Ω(1/sqrt N) when f(x)=0 and the initial state has Ω(1) overlap with an eigenphase-0 eigenvector when f(x)=1 (recalled as a background theorem, not verified)
- Constant c and the success-probability amplification (O(1) repetitions) are unspecified

## Registers

- edge: \lceil \log_2 (2|E|) \rceil (for N=4: 14 directed edges, 4 qubits) qubits; holds a directed edge |u,v\rangle of the tree T including the tail edge; the leaf-index part addresses the oracle
- phase: m = O(\log N) qubits; phase-estimation ancilla register controlling powers of W_x
- oracle_ancilla: 1 qubits; optional target qubit if a bit-flip oracle is converted to the phase oracle of eq_2

## Initial state

|\psi_0\rangle = |t,r\rangle_{\text{edge}} \otimes |0\rangle^{\otimes m}_{\text{phase}}, i.e. the walker localized on the output edge from the tail vertex t to the root r.

## Measurement

Measure the m-qubit phase register in the computational basis to obtain an estimate \hat\theta of an eigenphase of W_x.

## Classical postprocessing

Output \hat f(x)=1 if \hat\theta = 0 (within the resolution \delta) and \hat f(x)=0 otherwise, per eq_5; repeat O(1) times and take a majority vote to reduce error probability to a constant below 1/3. Which outcome maps to 1 vs 0 must be fixed consistently with the chosen leaf convention.

## Algorithm steps

1. Fix the balanced NAND tree T (tiny instance: root r with children a,b; a has leaves 1,2; b has leaves 3,4; tail vertex t attached to r) and the target function f of eq_1. (eq_1)
2. Prepare the edge register in |t,r\rangle and the phase register in |0\rangle^{\otimes m}. (eq_5)
3. Build one walk step W_x = S C_x where the leaf coins are implemented by the oracle O_x acting on the leaf-index part of the edge register (O(1) queries per step). (eq_2, eq_4)
4. Run quantum phase estimation of W_x on |\psi_0\rangle to precision \delta = c/\sqrt N, using controlled-W_x^{2^k} for k = 0..m-1, i.e. O(1/\delta) = O(\sqrt N) total walk steps and queries. (eq_3, eq_4, eq_5)

## Assumptions

- No experiment_scope was given, so the balanced O(sqrt N) algorithm with a depth-2, N=4 instance was chosen as the single smallest useful construction.
- The algorithm is reconstructed from recalled background on quantum-walk NAND-tree evaluation, not from the paper itself; the paper's specific construction may differ in weights, tail structure and conventions.
- Unit edge weights and uniform Grover coins are assumed throughout.
- Leaf i is present in T_x (equivalently leaf coin trivial) iff x_i = 0; the dual convention computes the complemented NOR formula and would be handled by complementing inputs/outputs.

## Missing information

- Exact edge weights and the tail/output-edge construction used by the paper, and the precise statement of its spectral-gap theorem.
- Whether the paper uses a Szegedy walk, a coined walk, or a different discretization of the continuous-time walk.
- The rebalancing procedure for arbitrary formulas and how it yields the N^{1/2+O(1/sqrt(log N))} query bound (entirely outside the reconstruction).
- Precision constant c, number of repetitions, and error-probability analysis.
- The paper's sign/leaf convention mapping eigenphase 0 to f(x)=1 versus f(x)=0.
