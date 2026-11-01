# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Simulate 1D quantum harmonic oscillator evolution exp(-iHt) with H=p^2/2+x^2/2 on an n-qubit discretized position grid using split-step Trotter-Suzuki with QFT diagonalization of the kinetic term, and read out the final statevector or position distribution.

Scope: Smallest construction: n=3 to 4 qubits (N=8 or 16), second-order Strang splitting with r steps, no ancilla, evaluated by statevector against exact discretized evolution (and optional fractional Fourier transform at angle t=theta). Out of scope: the Lie-algebraic high-order Suzuki error analysis giving exp(gamma sqrt(log(N/eps))), the Hermite eigenstate preparation with polylog(N)/eps cost, the quartic potential N^{1/3} scaling, and the general complex 1D systems bound O~(N).

## Symbols

- $n$: number of qubits in the position register; domain: positive integer, 3 to 5 for small instances
- $N$: grid size 2^n (also used in the abstract as an energy-cutoff quantum number; here only the grid size); domain: N=2^n
- $dx$: grid spacing; domain: positive real, assumed dx=sqrt(2*pi/N) so that the momentum grid spacing equals dx
- $x_j$: position of grid point j; domain: real, x_j=(j-N/2)dx, j in {0..N-1}
- $j=\sum_i 2^i b_i$: little-endian grid index; qubit i holds bit b_i of weight 2^i; domain: b_i in {0,1}
- $t$: total evolution time (equals the fractional Fourier angle theta); domain: real
- $r$: number of Trotter steps, dt=t/r; domain: positive integer
- $\epsilon$: target precision; domain: positive real
- $F$: discrete Fourier transform implemented by the QFT circuit; momentum p_m=(m-N/2)dx with m the Fourier index (shift conventions must be handled); domain: N x N unitary

## eq_1: QHO Hamiltonian split

$$
H=T+V,\quad T=\tfrac12 p^2,\quad V=\tfrac12 x^2
$$

Hamiltonian of the QHO as a sum of kinetic and potential terms.

Provenance: `standard_background`. Standard definition of the QHO; the abstract mentions the QHO but gives no explicit formula.

Equation assumptions:

- Units hbar=m=omega=1

## eq_2: Strang step with QFT

$$
U(dt)=e^{-iV dt/2}\,F^{\dagger}e^{-iT_{\rm diag}dt}F\,e^{-iV dt/2},\quad U_{\rm total}=U(t/r)^r
$$

Second-order split-step Trotter step; V is diagonal in position basis, T diagonal in the Fourier basis.

Provenance: `assumption`. Proposed construction in the sketch; the abstract only mentions Trotter-Suzuki, not the specific splitting or order.

Equation assumptions:

- Periodic grid
- QFT is the position-momentum change of basis
- Error is O(t^3/r^2) for the second-order formula

## eq_3: Diagonal phases as Z-polynomials

$$
x_j=dx\Big(\sum_{i=0}^{n-1}2^i b_i-\tfrac N2\Big),\ b_i=\tfrac{1-z_i}{2},\ x^2=\sum_i a_i z_i+\sum_{i<k}c_{ik}z_iz_k+{\rm const}
$$

The grid coordinate is affine in the Z eigenvalues z_i, so x^2 is a quadratic form, which gives RZ and RZZ gates with angles proportional to dt times the coefficients. The same form with the momentum grid gives p^2 after the QFT, modulo the wrap-around of the signed momentum index.

Provenance: `abstract_inferred`. The diagonal decomposition is a standard construction and is not stated in the abstract; the sketch asserts it.

Abstract evidence: We first describe a method to simulate the evolution of the quantum harmonic oscillator (QHO)

Equation assumptions:

- Signed momentum labeling of the Fourier index needs a shift so that p^2 is quadratic in bits; otherwise the diagonal is a piecewise quadratic and requires an extra sign-bit treatment

## eq_4: Lie algebra closure

$$
[x^2,p^2]=2i(xp+px),\ [xp+px,x^2]=-4i x^2,\ [xp+px,p^2]=4i p^2
$$

Quadratic operators generate su(1,1)=sl(2,R); the continuous-variable Trotter product acts as a 2x2 symplectic matrix on (x,p).

Provenance: `standard_background`. Abstract refers to exploiting the Lie algebra structure; these commutators are standard for the continuum operators, with signs depending on convention.

Equation assumptions:

- Continuum operators; the discretization breaks exact closure

## eq_5: Fractional Fourier transform

$$
\mathcal F_\theta=e^{i\theta/2}\,e^{-i\theta H}\ \text{(up to convention-dependent phase)},\ \theta=t
$$

The fractional Fourier transform at angle theta is the QHO evolution for time theta up to a global phase.

Provenance: `abstract_inferred`. The abstract claims this correspondence; the exact phase convention is background.

Abstract evidence: can be formulated in terms of the evolution of the QHO

Equation assumptions:

- Global phase is unobservable

## Registers

- pos: n qubits; position grid register, little-endian: qubit i is weight 2^i of index j

## Initial state

A small test state on the grid, assumed to be a discretized Gaussian/ground-state-like state or a low-lying basis superposition, supported well within the energy cutoff. For a tiny test, a Gaussian built by Ry rotations on a binary tree is allowed; no initialize or dense state-preparation gate.

## Measurement

Primary: read the final statevector with no measurements and compare with exact discretized evolution via fidelity. Alternative: measure all n position qubits to estimate |psi(x_j,t)|^2, taking counts key bits[::-1][i] as qubit i.

## Classical postprocessing

Compute the exact reference via the matrix exponential of the discretized H (or analytic QHO evolution), compute fidelity or total variation distance, and choose r so the error is below epsilon.

## Algorithm steps

1. Prepare the initial low-energy state on the n-qubit grid with standard gates (e.g. Ry tree, or a basis state for a minimal test). (eq_3)
2. Apply the half-step potential phase e^{-iV dt/2} using RZ and RZZ gates from the quadratic form. (eq_3, eq_2)
3. Apply the QFT, the diagonal kinetic phase e^{-iT dt} (RZ/RZZ), then the inverse QFT, with bit-reversal swaps handled. (eq_2, eq_3)
4. Apply the second half-step potential phase; merge adjacent half-steps across repetitions; repeat r times with dt=t/r. (eq_2)
5. For the fractional Fourier transform, use t=theta in the same circuit. (eq_5)

## Assumptions

- Uniform periodic grid of N=2^n points with cutoffs in x and p
- Initial state supported below the energy cutoff
- Second-order Strang splitting used instead of the paper's high-order Suzuki formulas
- Small instances n=3 to 5
- dx=sqrt(2*pi/N) is a chosen grid convention, not from the abstract
- Units hbar=m=omega=1

## Missing information

- The paper's actual Suzuki order schedule and constants gamma
- Explicit Lie-algebra error bound
- Exact eigenstate preparation circuit and discretization
- The quartic split-step parameters
- The grid and momentum shift convention
- The measurement protocol used by the paper
