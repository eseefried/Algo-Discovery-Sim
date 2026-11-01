# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Simulate time evolution of the one-dimensional quantum harmonic oscillator (QHO) by Trotter-Suzuki splitting of H = p^2/2 + x^2/2 into kinetic and potential parts. The abstract does not specify the refined Lie-algebraic analysis or the actual product-formula schedule.

Scope: Smallest useful construction: a first-order Trotter splitting for the QHO on a discretized position grid with N=4 points, plus the abstract's stated complexity scaling. The refined Lie-algebra analysis, eigenstate preparation, quartic potential, general 1D systems, and fractional Fourier transform are outside this scope.

## Symbols

- $H$: QHO Hamiltonian; domain: Hermitian operator on L^2(R), discretized to N x N
- $T=p^2/2$: kinetic part; domain: operator
- $V=x^2/2$: potential part; domain: operator
- $t$: total evolution time; domain: positive real
- $r$: number of Trotter steps; domain: positive integer
- $\epsilon$: target precision; domain: positive real
- $N$: energy-cutoff quantum number (QHO evolution) or grid size (state preparation); domain: positive integer
- $\gamma$: constant in complexity bound; domain: positive real
- $F$: discrete Fourier transform converting between position and momentum bases; domain: unitary on N-dimensional space
- $x_j$: grid positions; domain: real

## eq_1: QHO Hamiltonian

$$
H=\tfrac12 p^2+\tfrac12 x^2,\quad H|n\rangle=(n+\tfrac12)|n\rangle
$$

Standard QHO in units with hbar=m=omega=1.

Provenance: `standard_background`. Textbook definition; the abstract names the QHO but gives no equations.

Equation assumptions:

- Units hbar=m=omega=1

## eq_2: First-order Trotter step

$$
U(t)=e^{-iHt}\approx\left(e^{-iVt/r}e^{-iTt/r}\right)^r
$$

Product formula splitting the potential and kinetic parts. Approximation, not exact equality.

Provenance: `standard_background`. The abstract mentions Trotter-Suzuki; this generic form is background, not the paper's refined schedule.

Equation assumptions:

- First-order formula chosen as the simplest instance
- Truncated or discretized space

## eq_3: Kinetic term via Fourier transform

$$
e^{-iTs}=F^{\dagger}\,\mathrm{diag}_k\!\left(e^{-i s k^2/2}\right)F,\qquad e^{-iVs}=\mathrm{diag}_j\!\left(e^{-i s x_j^2/2}\right)
$$

Diagonal phases in position and momentum bases, so each factor is implementable as a diagonal phase plus a Fourier transform.

Provenance: `assumption`. Proposed discretization for the tiny instance; the abstract does not state it.

Equation assumptions:

- Uniform grid x_j=j\,\delta - offset
- Periodic boundary conditions
- N=4 points

## eq_4: Stated complexity

$$
C=O\!\left(\exp\!\left(\gamma\sqrt{\log(N/\epsilon)}\right)\right)
$$

Claimed complexity of the paper's QHO evolution method; subpolynomial in N/epsilon.

Provenance: `abstract_explicit`. Stated directly in the abstract.

Abstract evidence: the complexity of our method is $O(\exp(\gamma\sqrt{\log(N/\epsilon)}))$

## eq_5: Trotter error scaling

$$
\left\|U(t)-\left(e^{-iVt/r}e^{-iTt/r}\right)^r\right\|\le \frac{t^2}{2r}\|[V,T]\|
$$

Generic first-order error bound. Unbounded operators make it only meaningful on an energy-cutoff subspace; the paper's refined bound is not reproduced.

Provenance: `standard_background`. Standard commutator bound, which the abstract's refined Lie-algebra analysis is said to improve on.

Equation assumptions:

- Restriction to a bounded-energy subspace

## Registers

- pos: 2 qubits (N=4 grid points) qubits; position register; computational basis index j labels x_j

## Initial state

Assumed: a state supported on energy cutoff n<=N, e.g. |0> of the QHO discretized on the grid, or a basis state |j_0> for the tiny instance. The abstract does not specify it.

## Measurement

Assumed: computational-basis measurement of the position register to estimate the position distribution.

## Classical postprocessing

Assumed: estimate probabilities from measurement frequencies. None is specified in the abstract.

## Algorithm steps

1. Prepare the initial state on the position register. (no equation reference)
2. Apply the diagonal potential phase e^{-iVt/r}. (eq_3)
3. Apply F, the diagonal momentum phase e^{-iTt/r}, then F^\dagger. (eq_3)
4. Repeat steps 2-3 r times to approximate U(t), choosing r so the error is below epsilon. (eq_2, eq_5)

## Assumptions

- No scope was given, so the tiny N=4 first-order Trotter instance was chosen
- The grid, boundary conditions and initial state are proposed here, not taken from the abstract
- The paper's refined Lie-algebraic Trotter-Suzuki construction is not reconstructed

## Missing information

- Actual product-formula order and step schedule achieving the subpolynomial complexity
- Definition of gamma and the exact meaning of the energy cutoff
- Details of the discretized-eigenstate preparation method
- Quartic-potential method and general 1D system assumptions
- Fractional Fourier transform construction
