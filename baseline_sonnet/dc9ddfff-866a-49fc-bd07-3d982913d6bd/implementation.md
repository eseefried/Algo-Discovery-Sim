# Equation to Qiskit

First-order Trotter circuit for the 1D quantum harmonic oscillator H=p^2/2+x^2/2 on a periodic grid of N=2^n points (n<=12 qubits). Each step applies the kinetic factor exp(-iT t/r) as QFT^dagger, then the momentum-space phases k^2/2, then QFT. It then applies the potential factor exp(-iV t/r) as position-space phases x_j^2/2. Both diagonal phases are built from single-qubit P gates, CP gates and a global phase, so there is no dense unitary. The refined Lie-algebraic schedule from the abstract is not reconstructed.

Source equation run: `5b64c98f-6828-44de-be70-ee68dc15976f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: position register, little-endian grid index j=sum_k 2^k b_k (qubit 0 least significant)
- position x_j = delta*(j-(N-1)/2), N=2^n, default delta=sqrt(2*pi/N)
- in momentum space (between QFT^dagger and QFT) the index is read as signed two's complement m in [-N/2,N/2-1], k=m*2*pi/(N*delta)

## Assumptions

- Units hbar=m=omega=1
- Periodic boundary conditions on a uniform centered grid
- Input state preparation and measurement are handled by the runner
- The number of steps r is supplied by the user; no automatic choice from epsilon
- trotter_steps is capped at 1000 and n_qubits at 12

## Unresolved issues

- The paper's actual product-formula order and schedule are unknown
- The discretized eigenstate preparation, quartic potential, general 1D systems and fractional Fourier transform are not covered
- No validation contract was provided, so there is no target to check the discretization against

## Equation mapping

- `eq_1`: background; no code location. Defines the QHO Hamiltonian with hbar=m=omega=1; it motivates the circuit but is not a gate-level object.
- `eq_2`: implemented; build_circuit: loop over r Trotter steps. First-order product formula (e^{-iVt/r}e^{-iTt/r})^r, with r=trotter_steps.
- `eq_3`: implemented; build_circuit and _quad_phase: kinetic block (QFTGate inverse, momentum phases, QFTGate) and potential block (position phases). The kinetic factor is F^dag diag(e^{-i s k^2/2}) F and the potential factor is diag(e^{-i s x_j^2/2}), both on a periodic uniform grid. The quadratic phases are decomposed into P, CP and a global phase.
- `eq_4`: out_of_scope; no code location. Asymptotic complexity claim for the paper's refined method; it is not a circuit construction and the method is not reconstructed.
- `eq_5`: background; no code location. Generic Trotter error bound; it informs the choice of trotter_steps, which is user supplied, and no error control is implemented.

## Specification changes

- eq_2, eq_3: Scope generalized from the fixed N=4 grid to N=2^n for n in 1..12, with n, t and r as instance parameters. Reason: The task requires implementation for varying valid parameters. n=2 recovers the specified instance.
- eq_2: Within each step, kinetic is applied first and potential second, following the operator product e^{-iVs}e^{-iTs}. The step list in the specification described potential first. Reason: The equation and the step list disagree on ordering. The operator-product order was chosen, and both are valid first-order formulas.
- eq_3: Grid is x_j=delta*(j-(N-1)/2) with default delta=sqrt(2*pi/N). Momentum is k=2*pi*m/(N*delta) with m signed. The QFTGate sign convention is irrelevant because the kinetic phase is even in k. Reason: The specification left the offset and spacing unspecified. This choice gives a centered, self-dual grid.
- eq_1, eq_4, eq_5: The refined Lie-algebraic Trotter-Suzuki schedule, the energy cutoff and the subpolynomial complexity are not implemented. Only plain first-order Trotterization is built. Reason: The abstract does not give enough detail to reconstruct the refined method.
