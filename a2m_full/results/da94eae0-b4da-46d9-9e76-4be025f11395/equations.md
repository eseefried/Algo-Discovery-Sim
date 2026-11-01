# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given a classically specified d-dimensional qudit channel E (Choi matrix or Kraus list), classically decompose it into a convex combination of generalized extreme channels within diamond-norm error eps/2, sample one term per shot, and implement the sampled term as a Stinespring dilation on system plus one ancillary qudit, so that shot-averaged statistics approximate E(rho).

Scope: Smallest useful instance (assumed): d=2 (one system qubit) with a single ancilla qubit, i.e. 2 qubits total. The classical decomposition is taken as given or computed offline; the circuit builder implements one sampled term E_k as a unitary U_k with ancilla starting in |0>, built from standard gates (e.g. a 2-qubit unitary via the Qiskit standard-gate decomposition into CX and single-qubit gates). Outside scope: the paper's nonlinear coupled-equation solver, exact generalized-extreme-channel parametrization, the d^2 gate-count and log(1/eps) run-time proofs, fault-tolerant compilation, and general d.

## Symbols

- $d$: qudit (system) Hilbert-space dimension; domain: integer >= 2
- $\mathcal{E}$: target channel; domain: CPTP map on d x d matrices
- $\mathcal{E}_k$: k-th generalized extreme channel; domain: CPTP map
- $p_k$: mixture probability of term k; domain: p_k >= 0, sum_k p_k = 1
- $K_{k,j}$: Kraus operators of E_k; domain: d x d complex matrices
- $V_k$: Stinespring isometry of E_k, V_k|psi> = sum_j K_{k,j}|psi>|j>; domain: C^d -> C^d (x) C^m
- $U_k$: unitary on system+ancilla whose action on system (x) |0> equals V_k; domain: U(d*m)
- $\epsilon$: target diamond-norm error; domain: (0,1)
- $\epsilon_{dec},\epsilon_{syn}$: decomposition and gate-synthesis errors; domain: nonnegative reals
- $N$: number of mixture terms; domain: integer <= d^2 (Caratheodory-type bound, assumed)

## eq_1: Convex decomposition

$$
\mathcal{E}\approx\sum_{k=1}^{N}p_k\,\mathcal{E}_k,\quad p_k\ge0,\ \sum_k p_k=1,\quad \Big\|\mathcal{E}-\sum_k p_k\mathcal{E}_k\Big\|_\diamond\le\epsilon_{dec}
$$

Channel written as a convex combination of generalized extreme channels, approximate within tolerance.

Provenance: `abstract_inferred`. The abstract states the decomposition; the explicit error bound form is inferred from the diamond-norm tolerance claim.

Abstract evidence: decomposing a quantum channel into a convex combination of generalized extreme channels

Equation assumptions:

- Decomposition error epsilon_dec <= eps/2 (from sketch)

## eq_2: Stinespring form of each term

$$
\mathcal{E}_k(\rho)=\mathrm{Tr}_{A}\big[U_k(\rho\otimes|0\rangle\langle0|_A)U_k^\dagger\big]=\sum_j K_{k,j}\rho K_{k,j}^\dagger,\quad \sum_j K_{k,j}^\dagger K_{k,j}=I
$$

Each generalized extreme channel is realized by a dilation with one ancilla qudit initialized in |0>, then discarded or measured.

Provenance: `standard_background`. Standard Stinespring dilation; consistent with the single-ancilla claim but the specific U_k is not given in the abstract.

Equation assumptions:

- Ancilla dimension m <= d suffices (sketch assumption)
- Ancilla traced out or measured with outcomes stored as classical dits

## eq_3: Random-circuit average

$$
\bar{\mathcal{E}}(\rho)=\mathbb{E}_{k\sim p}\,\mathcal{E}_k(\rho)=\sum_k p_k\,\mathcal{E}_k(\rho)
$$

Sampling k with probability p_k per shot gives the mixture channel on average.

Provenance: `abstract_inferred`. A randomly chosen circuit realizes the convex combination in expectation.

Abstract evidence: The resultant circuit is a randomly chosen generalized extreme channel circuit

Equation assumptions:

- Sampling distribution is exactly p_k via classical random bits

## eq_4: Error budget

$$
\Big\|\mathcal{E}-\sum_k p_k\tilde{\mathcal{E}}_k\Big\|_\diamond\le\epsilon_{dec}+\max_k\|\mathcal{E}_k-\tilde{\mathcal{E}}_k\|_\diamond\le\epsilon_{dec}+\epsilon_{syn}\le\epsilon
$$

Triangle inequality and convexity of diamond norm combine decomposition and gate-synthesis errors.

Provenance: `abstract_inferred`. Standard norm argument supporting the stated tolerance guarantee.

Abstract evidence: within a pre-specified error tolerance with respect to diamond-norm distance

Equation assumptions:

- tilde E_k is the synthesized (gate-approximated) version of E_k

## eq_5: Shot-averaged readout

$$
\Pr(x)=\sum_k p_k\,\mathrm{Tr}\big[\Pi_x\,\mathcal{E}_k(\rho)\big]\approx\mathrm{Tr}[\Pi_x\,\mathcal{E}(\rho)]
$$

Measurement statistics on the system over shots with fresh k each shot approximate the target output distribution.

Provenance: `assumption`. Proposed readout from the sketch; not stated in abstract.

Equation assumptions:

- Pi_x projectors in the chosen measurement basis on the system register only

## Registers

- sys: ceil(log2 d) qubits (1 qubit for d=2) qubits; system qudit holding input rho; measured at the end
- anc: ceil(log2 d) qubits (1 qubit for d=2) qubits; ancillary qudit for Stinespring dilation, starts in |0>, discarded or measured
- k_dits: classical, ceil(log2 N) bits qubits; classical record of sampled index k (and optional ancilla outcomes)

## Initial state

rho_in on sys (a chosen input state prepared by standard gates, e.g. |0> or |+>), anc in |0>.

## Measurement

Measure sys qubit(s) in the computational basis (or after basis-change gates); optionally measure anc. Qiskit little-endian: bits[::-1][i] is the bit set by measure(i,i).

## Classical postprocessing

Average counts over shots and k to estimate E(rho) statistics; no further decoding.

## Algorithm steps

1. Classically compute (or load) the decomposition {p_k, V_k} of E with error <= eps/2. (eq_1)
2. Per shot, sample k with probability p_k using classical random bits and store as classical dits. (eq_3)
3. Build U_k completing the isometry V_k to a unitary on sys+anc (anc in |0>) and compile with standard gates (e.g. a unitary decomposition into CX and single-qubit gates, with no initialize or dense-unitary shortcuts). (eq_2)
4. Apply U_k, then measure sys in the required basis (ancilla is traced out or measured with outcomes recorded), reset anc between shots. (eq_2, eq_5)
5. Aggregate counts across shots with fresh k each; bound total error via the budget. (eq_4, eq_5)

## Assumptions

- Choose d=2, one system qubit plus one ancilla qubit, as the tiny instance (scope not given).
- Channel is classically known (Choi/Kraus), not a black box, so no queries are used.
- Nonlinear optimization is assumed to converge to a valid decomposition; it is not reconstructed.
- Qudit dimension is padded to a power of 2 for qubit embedding.
- Mixing is via classical sampling over shots, not coherent LCU.
- Gate synthesis error is assumed bounded by eps/2.

## Missing information

- Exact definition of generalized extreme channels and the nonlinear coupled algebraic equations.
- Explicit parametrization of U_k and the optimization procedure.
- Exact gate-count and run-time derivation (log(1/eps), d^2).
- How ancilla outcomes and classical dits are used within the circuit.
