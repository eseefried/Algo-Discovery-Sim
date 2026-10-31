# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Additive approximation of the partition function Z(\beta,J,h) of a classical Ising model with pairwise couplings J_e and local fields h_v on a square lattice, using the Van den Nest–Dür–Briegel overlap mapping (partition function = overlap of a product state with a stabilizer/graph state) estimated on a quantum computer with a Hadamard test. The abstract additionally claims a measurement-based (MBQC) reinterpretation that exponentially improves the approximation scale, BQP-completeness for complex parameters, and hardness evidence for multiplicative approximation; only the baseline overlap-mapping algorithm can be reconstructed here.

Scope: Reconstructed: (i) the Ising partition function, (ii) the overlap mapping Z = 2^{|V|/2} <alpha|psi_G> with psi_G local-Hadamard-equivalent to the graph state of the edge-decorated lattice, (iii) the 'straightforward' constant-depth quantum algorithm: normalise the product state, write Z as a scaled transition amplitude <0|W|0> and estimate it by a Hadamard test, giving an additive approximation with scale Delta_0 equal to the product of local norms. Tiny explicit instance (assumed, no scope supplied): the 2x2 square-lattice plaquette (4 spins, 4 edges, periodic/cycle graph C_4) with uniform real coupling J, zero field, beta=1, needing 8 system qubits plus 1 ancilla. Outside scope (not reconstructable from the abstract): the paper's MBQC reinterpretation of the overlap as a circuit along the lattice and its exponentially improved approximation scale, the precise algorithmic domain, the BQP-completeness construction with complex parameters, and the argument against efficient classical multiplicative approximation.

## Symbols

- $G=(V,E)$: Square-lattice graph; vertices carry spins, edges carry couplings; domain: finite simple graph; instance: 4-cycle C_4 with |V|=|E|=4
- $s_v$: Classical Ising spin at vertex v; domain: \{+1,-1\}
- $x_v$: Bit encoding of spin, x_v=(1-s_v)/2, so |0\rangle\leftrightarrow s_v=+1, |1\rangle\leftrightarrow s_v=-1; domain: \{0,1\}
- $J_e$: Coupling strength on edge e=(u,v); domain: \mathbb{R} (physical region) or \mathbb{C} (BQP-complete construction)
- $h_v$: Local magnetic field at vertex v; domain: \mathbb{R} or \mathbb{C}
- $\beta$: Inverse temperature; domain: \mathbb{R}_{>0} (absorbed into J,h when complex)
- $Z$: Ising partition function; domain: \mathbb{C} (real positive for real parameters)
- $|\psi_G\rangle$: Stabilizer state on |V|+|E| qubits encoding spin configurations and edge parities; domain: unit vector in (\mathbb{C}^2)^{\otimes(|V|+|E|)}
- $|\alpha\rangle$: Unnormalised product state encoding couplings and fields; domain: (\mathbb{C}^2)^{\otimes(|V|+|E|)}
- $\tilde G$: Edge-decorated graph: one new vertex inserted on every edge of G; domain: graph with |V|+|E| vertices and 2|E| edges
- $W$: Unitary whose vacuum amplitude \langle 0|W|0\rangle equals the normalised overlap; domain: U(2^{n}), n=|V|+|E|
- $\Delta_0$: Approximation scale of the straightforward algorithm (product of local norms times 2^{|V|/2}); domain: \mathbb{R}_{>0}
- $\epsilon,\delta$: Target additive error of the normalised amplitude and failure probability; domain: (0,1)
- $N$: Number of Hadamard-test repetitions; domain: \mathbb{N}

## eq_1: Ising partition function

$$
Z(\beta,J,h)=\sum_{s\in\{\pm1\}^{V}}\exp\Big(\beta\sum_{(u,v)\in E}J_{uv}s_u s_v+\beta\sum_{v\in V}h_v s_v\Big)
$$

Partition function of the classical Ising model with couplings J and fields h on the graph G (sign convention H=-\sum J s s-\sum h s).

Provenance: `standard_background`. Standard definition recalled from statistical physics; the abstract names 'partition functions of Ising models' but does not write the formula.

Equation assumptions:

- Sign convention H=-\sum_e J_e s_u s_v-\sum_v h_v s_v; other conventions change J,h by sign only.

## eq_2: Overlap mapping (Van den Nest–Dür–Briegel)

$$
Z=2^{|V|/2}\,\langle\alpha|\psi_G\rangle,\quad |\psi_G\rangle=2^{-|V|/2}\sum_{x\in\{0,1\}^{V}}|x\rangle_V\bigotimes_{e=(u,v)\in E}|x_u\oplus x_v\rangle_e,\quad |\alpha\rangle=\bigotimes_{e\in E}\big(e^{\beta J_e}|0\rangle+e^{-\beta J_e}|1\rangle\big)\otimes\bigotimes_{v\in V}\big(e^{\beta h_v}|0\rangle+e^{-\beta h_v}|1\rangle\big)
$$

Exact identity: the partition function equals (up to 2^{|V|/2}) the overlap of an unnormalised product state, whose edge/vertex factors encode J_e and h_v, with a stabilizer state in which edge qubits hold the parity of their endpoint bits. Complex conjugation of alpha is immaterial for the stated real-coefficient convention; for complex J,h define \langle\alpha| with the listed coefficients as bra entries (no conjugation).

Provenance: `standard_background`. Recalled from the overlap mapping of Van den Nest, Dür, Briegel (PRL 98, 117207), which the abstract cites; verified by direct expansion: s_u s_v=+1 iff x_u\oplus x_v=0 and the bra coefficients reproduce e^{\beta J_e s_u s_v}, e^{\beta h_v s_v}.

Equation assumptions:

- Bit encoding x_v=(1-s_v)/2.
- Register ordering: vertex qubits first, then edge qubits.

## eq_3: Stabilizer state as decorated graph state

$$
|\psi_G\rangle=H^{\otimes E}\,|\tilde G\rangle,\qquad |\tilde G\rangle=\prod_{e=(u,v)\in E}\mathrm{CZ}_{u,e}\,\mathrm{CZ}_{v,e}\;|+\rangle^{\otimes(V\cup E)}
$$

The parity-encoding stabilizer state is obtained from the graph state of the edge-decorated square lattice by a Hadamard on every edge qubit; this gives a constant-depth preparation circuit.

Provenance: `standard_background`. Direct computation: CZ_{u,e}CZ_{v,e} acting on |x\rangle_V|+\rangle_e yields |x\rangle_V\,2^{-1/2}(|0\rangle+(-1)^{x_u\oplus x_v}|1\rangle)_e=H|x_u\oplus x_v\rangle_e. The decorated-graph-state picture underlies the MBQC interpretation mentioned in the abstract, whose details are not reconstructable.

## eq_4: Straightforward constant-depth algorithm: scaled vacuum amplitude

$$
Z=\Delta_0\,\langle 0^{n}|W|0^{n}\rangle,\quad W=\Big(\bigotimes_{k\in V\cup E}R_k\Big)^{\dagger}H^{\otimes E}\prod_{e=(u,v)}\mathrm{CZ}_{u,e}\mathrm{CZ}_{v,e}\,H^{\otimes n},\quad R_k|0\rangle=\frac{|\alpha_k\rangle}{\|\alpha_k\|},\quad \Delta_0=2^{|V|/2}\prod_{e\in E}\sqrt{2\cosh(2\beta J_e)}\prod_{v\in V}\sqrt{2\cosh(2\beta h_v)}
$$

Normalising each local factor turns the overlap into the transition amplitude of a constant-depth unitary W on n=|V|+|E| qubits. For real J_e,h_v one may take R_e=R_y(\theta_e) with \tan(\theta_e/2)=e^{-2\beta J_e} (similarly for h_v), and the norm formula \|\alpha_e\|^2=e^{2\beta J_e}+e^{-2\beta J_e}=2\cosh(2\beta J_e) holds; for complex parameters replace 2\cosh(2\beta J_e) by |e^{\beta J_e}|^2+|e^{-\beta J_e}|^2 and choose a unitary R_e with the stated first column.

Provenance: `abstract_inferred`. The abstract compares the proposed method against a straightforward constant-depth algorithm; the natural candidate is estimating the overlap of eq_2 directly as a constant-depth transition amplitude, whose additive scale is the product of the local norms. This identification is an inference, not stated in the abstract.

Abstract evidence: a straightforward constant depth quantum algorithm

Equation assumptions:

- The 'straightforward' algorithm is the direct Hadamard-test estimate of eq_2.
- Local unitaries R_k exist with first column \alpha_k/\|\alpha_k\| (always true).

## eq_5: Hadamard test and additive approximation guarantee

$$
\Pr[a=0]-\Pr[a=1]=\mathrm{Re}\langle 0^{n}|W|0^{n}\rangle\;(\text{with }S^{\dagger}\text{ on the ancilla: }\mathrm{Im}),\qquad \hat Z=\Delta_0\big(\hat r+i\hat m\big),\qquad \Pr\big[|\hat Z-Z|\le\epsilon\Delta_0\big]\ge1-\delta\;\text{ for }N=O(\epsilon^{-2}\log(1/\delta))\text{ samples per part}
$$

Estimating the real (and, for complex parameters, imaginary) part of the amplitude by the Hadamard test and rescaling by \Delta_0 yields an additive approximation of Z whose accuracy is set by the approximation scale \Delta_0 (here with \hat r,\hat m the empirical estimates of Re and Im). For real J,h the amplitude is real and only the Re test is needed. This is a statistical estimate, not exact equality.

Provenance: `abstract_inferred`. The abstract states the algorithm gives an additive approximation with an approximation scale; the standard meaning (error \epsilon\Delta with \epsilon=1/\mathrm{poly}) combined with the Hadamard test and the Hoeffding bound gives this guarantee. The paper's own improved scale \Delta (from the MBQC interpretation) is not recoverable and is claimed to be exponentially smaller than \Delta_0.

Abstract evidence: an approximation scale, which determines the accuracy of the approximation

Equation assumptions:

- Hoeffding bound for N i.i.d. ±1 outcomes.
- Success probability threshold 1-\delta with \delta constant, e.g. 1/4.

## eq_6: Tiny instance: 2x2 plaquette (4-cycle), uniform real J, h=0, beta=1

$$
Z_{C_4}(J)=2e^{4J}+12+2e^{-4J},\qquad n=|V|+|E|=8,\qquad \Delta_0=2^{2}\,(\sqrt2)^{4}\,\big(2\cosh 2J\big)^{2}=64\cosh^{2}(2J)
$$

Explicit target value for the smallest square-lattice instance: 2 aligned configurations contribute e^{4J}, 8 single-flip and 4 adjacent-double-flip configurations contribute 1 each, 2 antiferromagnetic configurations contribute e^{-4J}. The algorithm estimates \langle0^{8}|W|0^{8}\rangle=Z_{C_4}/\Delta_0 (which equals 1/4 at J=0 and tends to 1/8 as J\to\infty).

Provenance: `assumption`. No experiment_scope was supplied; the 2x2 plaquette is the smallest square-lattice fragment and its partition function is computed by direct enumeration of 16 configurations for validation of a circuit implementation.

Equation assumptions:

- Open plaquette identified with the cycle graph C_4 (4 vertices, 4 edges).
- Zero field so vertex factors are \sqrt2|+\rangle (R_v=H).

## Registers

- anc: 1 qubits; Hadamard-test control qubit
- vtx: |V| (instance: 4, row-major order of the lattice sites) qubits; Vertex qubits encoding spin bits x_v
- edg: |E| (instance: 4, edges ordered (0,1),(1,2),(2,3),(3,0)) qubits; Edge qubits encoding parities x_u\oplus x_v / couplings J_e

## Initial state

|0\rangle_{anc}\otimes|0\rangle^{\otimes|V|}_{vtx}\otimes|0\rangle^{\otimes|E|}_{edg} (total 9 qubits for the instance of eq_6)

## Measurement

Computational-basis measurement of the single ancilla qubit after the final Hadamard; the system register is discarded (or measured and ignored). Statistics \Pr[a=0]-\Pr[a=1] estimate \mathrm{Re}\langle0^n|W|0^n\rangle (or Im with the S^{\dagger} variant).

## Classical postprocessing

Compute \hat r=(\#\{a=0\}-\#\{a=1\})/N (and \hat m analogously), output \hat Z=\Delta_0(\hat r+i\hat m) with \Delta_0 from eq_4; the result is an additive approximation |\hat Z-Z|\le\epsilon\Delta_0 with probability at least 1-\delta. For the instance of eq_6 compare with Z_{C_4}(J)=2e^{4J}+12+2e^{-4J}.

## Algorithm steps

1. Fix the instance (lattice G, J_e, h_v, beta); compute classically the local unitaries R_k with first column \alpha_k/\|\alpha_k\| and the scale \Delta_0. (eq_2, eq_4, eq_6)
2. Apply H to anc (and S^{\dagger} when the imaginary part is required for complex parameters). (eq_5)
3. Apply controlled-W with control anc: controlled H^{\otimes n}, controlled CZ_{u,e}CZ_{v,e} for every edge (graph state of the decorated lattice), controlled H on edge qubits, then controlled R_k^{\dagger} on every qubit; depth is constant up to the control overhead. (eq_3, eq_4)
4. Apply H to anc and measure anc in the computational basis; record outcome a\in\{0,1\}. (eq_5)
5. Repeat steps 2-4 N=O(\epsilon^{-2}\log(1/\delta)) times (for each of Re and Im if complex) and form the empirical estimate. (eq_5)

## Assumptions

- No experiment_scope was provided; the 2x2 plaquette (C_4) with uniform real J, h=0, beta=1 was chosen as the tiny explicit instance.
- The 'straightforward constant depth quantum algorithm' mentioned in the abstract is identified with the direct Hadamard-test estimate of the overlap of eq_2 with scale \Delta_0; this is the baseline being reconstructed, not the paper's improved MBQC-based algorithm.
- Spin-to-bit encoding x_v=(1-s_v)/2 and register ordering vertices-then-edges.
- Sign convention of the Ising Hamiltonian as in eq_1.

## Missing information

- The paper's MBQC reinterpretation of the overlap (how measurement patterns on the decorated square-lattice graph state are converted into a circuit along the lattice) and the resulting exponentially improved approximation scale \Delta are not given in the abstract and cannot be reconstructed.
- The precise 'algorithmic domain' (admissible ranges of complex and real J_e, h_v) is not specified.
- The explicit approximation-scale formula for the real physical parameter region is not available.
- The BQP-completeness construction (which complex coupling/field values encode a universal gate set) is not described.
- The argument that no efficient classical multiplicative approximation exists on the square lattice is not described.
- Whether the lattice has open or periodic boundaries and how boundary spins/fields are treated is unspecified; the instance choice C_4 is an assumption.
