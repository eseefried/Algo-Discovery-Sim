# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Reconstruct a minimal Grover search over a small unordered phone-book database (search by number or by name via programmable query), and the effect of misestimating the database size N on the Grover state, which relates to distinguishability of Grover states.

Scope: One tiny instance: N=4 entries encoded in 2 index qubits, with a single marked item and a standard Grover oracle, plus the standard background Grover rotation analysis for a wrong guess of N. The paper's specific quantum database model, programmable query construction, and unambiguous state discrimination analysis and its results are outside scope.

## Symbols

- $N$: true number of database entries; domain: positive integer, assumed N=4 in the tiny instance
- $\tilde N$: guessed database size used to choose the iteration count; domain: positive integer
- $w$: index of the marked entry; domain: {0,...,N-1}
- $\theta$: Grover rotation angle; domain: (0,\pi/2)
- $k$: number of Grover iterations; domain: nonnegative integer
- $|\psi_k\rangle$: state after k Grover iterations; domain: state in C^N
- $O_w$: phase oracle marking w; domain: unitary on C^N

## eq_1: Oracle

$$
O_w=I-2|w\rangle\langle w|
$$

Phase oracle marking the sought entry; a programmable query for a name or number would define w via a lookup, which is not specified here.

Provenance: `standard_background`. Standard Grover oracle; the abstract does not give the paper's database query construction.

Equation assumptions:

- Single marked item
- Query reduced to the index w

## eq_2: Grover iterate

$$
G=(2|s\rangle\langle s|-I)\,O_w,\quad |s\rangle=N^{-1/2}\sum_{x=0}^{N-1}|x\rangle
$$

One Grover iteration: oracle followed by inversion about the mean.

Provenance: `standard_background`. Textbook Grover algorithm.

Equation assumptions:

- Uniform initial superposition

## eq_3: State after k iterations

$$
|\psi_k\rangle=\sin((2k+1)\theta)|w\rangle+\cos((2k+1)\theta)|w^\perp\rangle,\quad \sin\theta=1/\sqrt N
$$

Rotation in the plane spanned by |w> and the normalized uniform superposition of the unmarked states.

Provenance: `standard_background`. Standard Grover analysis.

Equation assumptions:

- Exactly one marked item

## eq_4: Iteration count from guessed size

$$
k(\tilde N)=\left\lfloor \frac{\pi}{4\arcsin(1/\sqrt{\tilde N})}\right\rfloor
$$

Iteration count chosen from the guessed size; the floor is a rounding, not an exact equality. Applied to the true N it gives a success probability that is generally less than 1.

Provenance: `assumption`. Proposed concrete model of the size-misestimation setting; the abstract does not state this formula.

Equation assumptions:

- Rounding to floor chosen arbitrarily

## eq_5: Success probability with wrong guess

$$
P_{\mathrm{succ}}=\sin^2\!\big((2k(\tilde N)+1)\theta\big)
$$

Probability of measuring w when the iteration count is chosen from the guess while the true angle is theta.

Provenance: `abstract_inferred`. The abstract poses this success question; this formula is the standard Grover consequence, not the paper's unambiguous-discrimination success rate.

Abstract evidence: how successful the algorithm can be if the number of elements of the database is not known precisely

Equation assumptions:

- Plain measurement success, not unambiguous discrimination

## Registers

- index: 2 qubits (N=4 instance) qubits; database address register, computational basis |x>, x as binary integer with the first qubit most significant

## Initial state

|0>^{\otimes 2} followed by Hadamards, giving the uniform superposition |s>

## Measurement

Computational-basis measurement of the index register; success if the outcome equals w.

## Classical postprocessing

Look up the database record at the measured index and verify it classically.

## Algorithm steps

1. Prepare the uniform superposition over the index register. (eq_2)
2. Choose the iteration count k from the guessed size. (eq_4)
3. Apply the oracle and diffusion k times. (eq_1, eq_2, eq_3)
4. Evaluate the success probability for the true N. (eq_5)

## Assumptions

- Scope chosen as a tiny N=4 instance with one marked item since no scope was given
- Query-to-index lookup abstracted away
- Only ordinary measurement is modeled, not unambiguous discrimination

## Missing information

- Paper's quantum phone-book data encoding and programmable query construction
- Unambiguous state discrimination formulation and success-rate formulas for Grover states with unknown N
- Quantitative results of the paper
