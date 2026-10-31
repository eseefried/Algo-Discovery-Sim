# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Quantify how systematic phase errors in the two phase-inversion operators of an amplitude-amplification-type search (the paper's 'optimized quantum random-walk search algorithm', treated here through its geometric two-dimensional rotation description) change the success rate as a function of database size N, iteration number k and phase error, and determine the maximal success rate and the iteration count at which it occurs.

Scope: Finite scope chosen by the reconstruction agent (no user scope given): a single-marked-item unstructured search over N items whose dynamics are reduced, as in the geometric (two-dimensional invariant subspace) description, to products of two generalized phase inversions with systematic phase errors. Equations give the erroneous iteration operator, the exact definition of the success rate, the effective rotation angle and a closed-form success probability for matched phase errors, and a tiny explicit instance N=4 (2 data qubits), k=1. Outside scope: the actual coin/shift/oracle structure of the optimized quantum random-walk (hypercube-type) search algorithm and its 'optimization', the paper's specific success-rate and iteration-count formulas, the treatment of unmatched errors in the two inversions, and the numerical robustness comparison with Grover's algorithm.

## Symbols

- $N$: database size (number of items searched); domain: positive integer, N = 2^n with n = \log_2 N data qubits in the instance
- $|t\rangle, |r\rangle$: normalized marked (target) state and normalized uniform superposition of the N-1 unmarked states; orthonormal basis of the invariant two-dimensional subspace; domain: unit vectors in \mathbb{C}^N
- $\theta$: half-angle of the initial state with respect to the unmarked axis, \sin\theta = 1/\sqrt{N}; domain: (0,\pi/2)
- $\phi,\ \psi$: actual phases applied by the marked-state inversion and the mean-state inversion; ideal value \pi; domain: real, modulo 2\pi
- $\delta$: systematic phase error, \phi = \pi+\delta (and \psi = \pi+\delta in the matched-error model); domain: real, |\delta|<\pi
- $\beta,\ \omega$: effective half rotation angle and rotation angle per erroneous iteration, \omega = 2\beta; domain: \beta\in[0,\pi/2]
- $k$: number of search iterations; domain: non-negative integer
- $P_k(N,\delta)$: success rate: probability of measuring the marked item after k iterations; domain: [0,1]
- $G_{\phi,\psi}$: one erroneous search iteration (mean-state inversion times marked-state inversion, with overall sign convention of Grover's diffusion); domain: unitary on \mathbb{C}^N

## eq_1: Initial state and two-dimensional geometric decomposition

$$
|s\rangle = \frac{1}{\sqrt{N}}\sum_{x=0}^{N-1}|x\rangle = \sin\theta\,|t\rangle + \cos\theta\,|r\rangle,\qquad \sin\theta = \frac{1}{\sqrt{N}},\qquad |r\rangle = \frac{1}{\sqrt{N-1}}\sum_{x\neq t}|x\rangle
$$

Uniform superposition over the database written in the orthonormal basis of the marked state and the normalized unmarked superposition; all iterates stay in span{|t>,|r>}.

Provenance: `standard_background`. Standard geometric picture of Grover/amplitude-amplification search; the abstract's 'geometric description' is taken to refer to this invariant-plane picture.

Equation assumptions:

- Exactly one marked item
- Initial state is the uniform superposition over the database (for a coined walk, the coin part is assumed to be absorbed into an analogous two-dimensional reduction)

## eq_2: Phase inversions with systematic phase errors and one iteration

$$
I_t^{\phi} = I - (1-e^{i\phi})|t\rangle\langle t|,\qquad I_s^{\psi} = I - (1-e^{i\psi})|s\rangle\langle s|,\qquad G_{\phi,\psi} = -\,I_s^{\psi}\, I_t^{\phi},\qquad \phi = \pi+\delta_1,\ \psi = \pi+\delta_2
$$

Ideal phase inversions (\phi=\psi=\pi give the oracle I-2|t><t| and diffusion 2|s><s|-I) are replaced by generalized phase rotations whose phases deviate systematically from \pi by \delta_1,\delta_2; the same erroneous operator is applied in every iteration.

Provenance: `abstract_inferred`. The abstract states that systematic errors in the phase inversions are modeled; the standard way to model a systematic phase-inversion error is a fixed deviation of the inversion phase from \pi. The specific operators of the optimized random-walk algorithm are not given in the abstract, so a generic two-inversion iteration is used.

Abstract evidence: systematic errors in phase inversions

Equation assumptions:

- Errors are systematic (identical in every iteration), not random
- The random-walk search iteration can be written as a product of two phase-type reflections acting in the invariant plane

## eq_3: Success rate after k iterations (exact definition)

$$
P_k(N,\delta_1,\delta_2) = \left|\langle t|\,G_{\phi,\psi}^{\,k}\,|s\rangle\right|^2
$$

Probability that a computational-basis measurement after k iterations returns the marked item; this is the quantity the abstract relates to N, k and the phase error.

Provenance: `abstract_inferred`. Success rate of a search algorithm is the probability of measuring the marked item; the abstract says it is expressed as a function of N, k and the phase error.

Abstract evidence: the relationship between the success rate of the algorithm, the database size, the number of iterations and the phase error is depicted

Equation assumptions:

- Measurement is in the computational basis of the database register

## eq_4: Effective rotation angle for matched phase errors

$$
\phi=\psi=\pi+\delta:\qquad \cos\omega = 1 - 2\sin^2\!\left(\tfrac{\phi}{2}\right)\sin^2\theta,\qquad \omega = 2\beta,\qquad \sin\beta = \sin\!\left(\tfrac{\phi}{2}\right)\sin\theta = \cos\!\left(\tfrac{\delta}{2}\right)\frac{1}{\sqrt{N}}
$$

When both inversions carry the same phase, the eigenvalues of G_{\phi,\phi} in the invariant plane are -e^{i\phi}e^{\pm i\omega}; the per-iteration rotation angle shrinks from 2\theta (\delta=0) to 2\beta.

Provenance: `standard_background`. Phase-matching result of Long et al. for Grover-type search with equal oracle and diffusion phases; follows from the trace and determinant of the 2x2 matrix of G_{\phi,\phi} in the basis {|t>,|r>}.

Equation assumptions:

- Matched errors \delta_1=\delta_2=\delta (phase matching); unmatched errors are not treated in closed form here

## eq_5: Closed-form success rate for matched phase errors

$$
P_k(N,\delta) = \left|\sin\theta\,\cos(2k\beta) + \frac{\sin(2k\beta)}{\cos\beta}\Big(\cos^2\theta\,\sin\tfrac{\phi}{2} + i\cos\tfrac{\phi}{2}\Big)\right|^2,\qquad \phi=\pi+\delta
$$

Exact success probability in the two-dimensional model with equal phase errors. Checks: \delta=0 gives \beta=\theta and P_k=\sin^2((2k+1)\theta) (ideal Grover); \phi\to 0 gives G=-I and P_k=1/N; if (2k+1)\beta=\pi/2 then P_k=1 (Long's zero-failure condition). The maximal success rate and the iteration number attaining it are obtained by maximizing this expression over integer k, approximately k^{*} \approx \lfloor \pi/(4\beta)\rfloor.

Provenance: `standard_background`. Obtained by writing G_{\phi,\phi} = -e^{i\phi}U with U in SU(2), U^k = \cos(k\omega) I + i\sin(k\omega)\,\hat n\cdot\vec\sigma, and evaluating <t|U^k|s> from the explicit 2x2 matrix of eq_2; consistent with the known Grover and Long zero-failure limits. This is the agent's analytic reduction of the background model, not a formula taken from the paper.

Equation assumptions:

- Matched errors \delta_1=\delta_2
- Single marked item
- Approximation sign in k^{*} indicates that the optimal integer iteration count must be found by evaluating P_k, not by exact rounding

## eq_6: Tiny explicit instance: N=4, one iteration, matched error

$$
N=4,\ \theta=\tfrac{\pi}{6},\ \sin\beta=\tfrac{1}{2}\cos\tfrac{\delta}{2}:\qquad P_1(4,\delta) = \Big(\tfrac{1}{2} + \tfrac{1}{2}\cos^2\tfrac{\delta}{2}\Big)^2 + \tfrac{1}{4}\sin^2\delta
$$

Two-qubit database, single marked item, one erroneous iteration; P_1(4,0)=1 (ideal), P_1(4,\pi)=1/4 (inversions become identities and no amplification occurs).

Provenance: `assumption`. Specialization of eq_5 to the smallest nontrivial instance where the ideal algorithm succeeds with certainty after one iteration, chosen so the circuit-generation stage has a concrete target.

Equation assumptions:

- Choice of N=4, k=1 and matched error is the agent's instance selection, not from the abstract

## Registers

- data: n = \log_2 N (n=2 in the instance) qubits; Holds the database index; the marked item t is a computational-basis state of this register and it is the register measured.
- coin: unknown (for a hypercube-type quantum random walk typically \lceil\log_2 n\rceil qubits) qubits; Coin register of the quantum random-walk search algorithm; its coin/shift operators are not reconstructable from the abstract and are not used in the two-dimensional model.

## Initial state

Uniform superposition |s> over the N database items on the data register (eq_1); any coin register of the actual random-walk algorithm is assumed prepared in the state that makes the walk's dynamics reduce to the two-dimensional model.

## Measurement

Measure the data register in the computational basis; the success event is obtaining the marked index t, with probability P_k given by eq_3 (and eq_5/eq_6 in the matched-error model).

## Classical postprocessing

Verify the measured index against the marking predicate; estimate the empirical success rate from repeated runs and compare with P_k(N,\delta); sweep \delta and N to obtain the maximal success rate and the optimal iteration count.

## Algorithm steps

1. Prepare the uniform superposition over the database (Hadamard on every data qubit for N=2^n). (eq_1)
2. Apply the erroneous iteration G_{\phi,\psi} = -I_s^{\psi} I_t^{\phi} k times, where the marked-state and mean-state phase inversions carry the systematic phase errors \delta_1,\delta_2 (matched case \delta_1=\delta_2=\delta). (eq_2, eq_4)
3. Choose k as the integer maximizing the modeled success rate P_k(N,\delta); for the instance N=4 use k=1. (eq_5, eq_6)

## Assumptions

- The 'optimized quantum random-walk search algorithm' is assumed to admit, like Grover's algorithm, a geometric description as a rotation in a two-dimensional invariant subspace generated by two phase-inversion-type operators; its specific coin, shift and optimization are unknown to this reconstruction.
- Phase errors are systematic (fixed) deviations of the inversion phases from \pi, identical in every iteration.
- Closed-form results (eq_4, eq_5, eq_6) assume matched errors in the two inversions; the general unmatched case is only defined implicitly via eq_2 and eq_3.
- Instance choice N=4, k=1, single marked item is the agent's choice.
- No claim is made about the paper's actual formulas, its stated maximal success rate, or its numerical comparison with Grover's algorithm.

## Missing information

- Definition of the optimized quantum random-walk search algorithm: graph (e.g., hypercube), coin operator, shift operator, marked-vertex oracle and the nature of the 'optimization'.
- Which operators in that algorithm are the 'phase inversions' subject to error, and whether the paper's error enters one or both inversions (matched or unmatched).
- The paper's own expressions for the success rate as a function of N, k and the phase error, the maximal success rate and the required iteration number.
- The precise robustness metric and numerical results used to conclude that the algorithm is more robust than Grover's algorithm.
- Database sizes and error ranges used in the paper's numerical simulations.
