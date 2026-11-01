# Equation to Qiskit

build_circuit(instance) returns the unitary second-order Strang split-step circuit for the 1D QHO, H=p^2/2+x^2/2, on an n-qubit centered periodic grid. The grid is x_j=(j-N/2)dx with dx^2=2*pi/N and little-endian j. The potential and kinetic phases are RZ/RZZ quadratic forms, and the position-to-momentum change of basis is QFTGate conjugated by Z on qubit 0 to handle the centered-grid shift. The circuit has no state preparation or measurement. With t=theta it approximates the fractional Fourier transform up to a global phase.

Source equation run: `2b8c6d84-67e5-4208-83a0-349cd3ab9165`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: register 'pos', little-endian grid index j=sum_i 2^i b_i (qubit 0 is least significant)
- Grid position x_j=(j-N/2)*dx with N=2^n and dx=sqrt(2*pi/N)
- Momentum register after the QFT uses the same layout, with p_k=(k-N/2)*dx
- No ancilla qubits

## Assumptions

- Units hbar=m=omega=1
- dx=sqrt(2*pi/N) so the position and momentum grid spacings are equal
- Periodic grid with signed momentum index in [-N/2, N/2-1]
- Instance keys: n (integer, 2 to 12), t (finite real), r (integer, 1 to 1000)
- QFTGate sign convention is irrelevant here because the kinetic diagonal is even in p, including at k=0

## Unresolved issues

- No public validation contract was supplied, so the choice of r for a target precision is left to the caller
- Exact agreement with the paper's QHO or fractional Fourier transform conventions is not established, and the global phase is not matched
- Discretization error of the periodic grid versus the continuum QHO is not analyzed

## Equation mapping

- `eq_1`: background; no code location. Definition of H=T+V with hbar=m=omega=1. It is realized only through the split into the potential and kinetic phase layers.
- `eq_2`: implemented; build_circuit: initial _diag half step, then the loop over r (Z0, QFTGate, _diag, inverse QFTGate, Z0, _diag). Second-order Strang step U(dt)=e^{-iVdt/2} F^dag e^{-iT dt} F e^{-iVdt/2}, repeated r times. Adjacent half-steps are merged into full potential steps between repetitions, which equals U(dt)^r exactly.
- `eq_3`: implemented; _diag. The affine map x/dx=-(1/2+sum 2^(i-1) z_i) makes x^2 a quadratic form, implemented with RZ and RZZ gates. The same form gives p^2 after the shifted QFT, because the signed momentum index (k-N/2) has the same affine structure.
- `eq_4`: background; no code location. Continuum su(1,1) commutation relations. They motivate the Lie-algebraic analysis but are not part of the circuit. The discretized circuit does not use them.
- `eq_5`: implemented; build_circuit with t set to the fractional Fourier angle theta. The circuit approximates exp(-i*theta*H) on the grid, which is the fractional Fourier transform up to a convention-dependent global phase. The global phase is dropped. No separate FrFT routine exists.

## Specification changes

- eq_2, eq_3: The position-to-momentum transform is implemented as Z(qubit0) . QFTGate . Z(qubit0), instead of a bare QFTGate. The inner Z(qubit0) factors cancel against the diagonal kinetic phase, so the circuit applies Z0, QFT, diagonal, QFT^dagger, Z0. Reason: For centered grids x_j=(j-N/2)dx and p_k=(k-N/2)dx with dx^2=2*pi/N, e^{i x_j p_k}=e^{2 pi i jk/N}(-1)^(j+k) up to a global phase. This resolves the shift convention the specification left open, and it gives a signed p^2 that is quadratic in the bits.
- eq_2: The half-step potential layers are merged across repetitions: half step, then r times (kinetic, full potential), with the last potential layer a half step. Reason: This is algebraically identical to U(dt)^r and uses fewer gates.
- eq_2, eq_3: The circuit is the bare evolution operation. It has no initial Gaussian or state preparation and no measurement. Global phases from the dropped constants are not tracked. Reason: The runner prepares inputs. Global phases are unobservable.
- eq_4, eq_5: Scope is narrowed to fixed second-order Strang splitting. The high-order Suzuki and Lie-algebra error scheduling, Hermite eigenstate preparation, quartic potential, and general complex 1D systems are not implemented. The abstract's epsilon and the choice of r from epsilon are left to the caller, and r is an explicit input. Reason: The specification supplies no concrete formulas for these. They go beyond one explicitly scoped construction.
