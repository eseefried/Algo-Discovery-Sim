# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Approximate e^{-iHt} on a small d-sparse Hermitian H (n-qubit system) with error eps, by an LCU of Szegedy/Berry-Childs quantum-walk powers weighted by Bessel functions J_m(tau), given black-box sparse-access oracles O_H (entries) and O_F (column indices).

Scope: One tiny instance: a single segment with tau=O(1) (e.g. n=1 or 2, d<=2), truncated at M chosen numerically, one LCU round plus optionally one round of oblivious amplitude amplification. Out of scope: the full multi-segment complexity analysis, the new lower bound proof, the exact oracle-level walk construction for general sparse H, and gate-count optimality.

## Symbols

- $H$: d-sparse Hermitian Hamiltonian on n qubits; domain: Hermitian 2^n x 2^n matrix
- $d$: sparsity (max nonzero entries per row); domain: positive integer
- $H_{\max}$: bound on entry magnitudes; domain: positive real
- $t$: evolution time; domain: positive real
- $\tau$: product of t, d, and H_max; domain: positive real
- $W$: quantum-walk unitary built from O_H and O_F; domain: unitary on system+neighbor ancilla space
- $\lambda$: eigenvalue of H; domain: real, |lambda|<=d H_max
- $J_m$: Bessel function of first kind, order m; domain: real functions, integer m
- $M$: truncation order of the Jacobi-Anger sum; domain: positive integer
- $\epsilon$: target error; domain: (0,1)
- $|\psi_j\rangle$: walk-state for row j; domain: normalized vector on neighbor register plus sink

## eq_1: Walk state

$$
|\psi_j\rangle=\sum_k \sqrt{\frac{H_{jk}^*}{d H_{\max}}}\,|k\rangle+\sqrt{1-\sum_k \frac{|H_{jk}|}{d H_{\max}}}\,|\text{sink}\rangle
$$

States whose span is reflected about to define the walk; the amplitude sign/phase convention is an assumption (Hermitian entries may need phase handling).

Provenance: `abstract_inferred`. Walk construction is named in the abstract; the explicit form is recalled from Berry-Childs, not stated in it.

Abstract evidence: Hamiltonian simulation via a quantum walk

Equation assumptions:

- entries taken nonnegative or phases handled by O_H
- sink absorbs the remaining norm

## eq_2: Walk eigenphases

$$
W\,|\mu_\pm\rangle=\pm e^{\pm i\arcsin(\lambda/(d H_{\max}))}|\mu_\pm\rangle
$$

Walk eigenvalues on the invariant subspace tied to eigenvalue lambda of H.

Provenance: `standard_background`. Recalled Szegedy/Berry-Childs relation; the abstract does not state it.

Equation assumptions:

- input embedded in the invariant subspace
- the sign branch is fixed by the initial projection

## eq_3: Jacobi-Anger

$$
e^{-i\tau\sin\theta}=\sum_{m\in\mathbb{Z}}J_m(\tau)\,e^{-im\theta}
$$

Expansion giving the Bessel coefficients.

Provenance: `standard_background`. Standard identity; the abstract mentions only Bessel-function coefficients.

## eq_4: Hamiltonian as walk-power sum

$$
e^{-iHt}\approx\sum_{m=-M}^{M}J_m(\tau)\,W^m\ \text{on the right eigenspace},\quad \theta=\arcsin(\lambda/(dH_{\max})),\ \tau=dH_{\max}t
$$

Truncated LCU target; the restriction and sign handling are assumed. Negative m uses W^dagger.

Provenance: `abstract_inferred`. Combining eq_2 and eq_3 gives this relation; the abstract states the linear combination only in words.

Abstract evidence: By implementing a linear combination of quantum walk steps with coefficients given by Bessel functions

Equation assumptions:

- the odd/even branch signs for m<0 and the (±1)^m factor are handled by the initial projection or a Z-type correction

## eq_5: LCU success amplitude

$$
\|\text{success}\|\approx \frac{1}{\sum_{|m|\le M}|J_m(\tau)|}
$$

Postselection amplitude on index register |0> after prepare, controlled-W^m, unprepare, with state prep amplitudes sqrt|J_m|/sqrt(sum|J_m|).

Provenance: `standard_background`. Standard LCU; the sketch says this is O(1) per segment with tau/r=O(1).

Equation assumptions:

- one round of oblivious amplitude amplification then needs the LCU normalization to be near 2, which this sum does not give exactly; verify numerically

## Registers

- sys: n qubits; system register holding input state
- nbr: n qubits; neighbor index ancilla (walk edge space)
- idx: ceil(log2(2M+1)) qubits; LCU index register for m in [-M,M] (offset or sign-bit encoding)
- flag: 1 qubits; flag/amplitude amplification qubit

## Initial state

|psi>_sys |0>_nbr |0>_idx |0>_flag, with the input embedded in the walk's invariant subspace

## Measurement

If the runner reads the statevector, do not measure; compare the system state with idx and flag in |0>. If counts are required, measure only sys in the computational basis.

## Classical postprocessing

Compute fidelity against the classically computed expm(-iHt)|psi>; precompute J_m(tau) and choose M.

## Algorithm steps

1. Build W from O_H and O_F: prepare |psi_j>, reflect about their span, apply SWAP. One W costs O(1) oracle queries. Each placement of the placeholder counts as a query. (eq_1, eq_2)
2. Classically compute J_m(tau) for |m|<=M, choosing M numerically so that the tail is below eps; set the LCU weights sqrt|J_m|. (eq_3, eq_4)
3. Prepare the index register with standard rotation gates (not initialize), with sign bits phase-correcting negative Bessel values. (eq_4)
4. Apply controlled-W^m via a controlled-W ladder (W^dagger for m<0), then unprepare the index register. (eq_4, eq_5)
5. Project/postselect idx=|0>, or apply one round of oblivious amplitude amplification per segment if tau/r=O(1); the output system state should approximate e^{-iHt}|psi>. (eq_5)

## Assumptions

- Tiny instance chosen by us since no scope was given
- H Hermitian with oracles as given, entries in the walk are real nonnegative or phases are handled
- Coefficients are precomputed and loaded via rotation gates
- Sign/branch ambiguity resolved by the initial projection
- Segmentation and oblivious amplitude amplification are acceptable

## Missing information

- Exact gate-level circuit for O_H/O_F-based walk preparation
- Exact handling of the (-1)^m or branch factors and the isometry embedding
- Exact amplitude amplification reflection details
- Precise M, r for the paper's bounds
