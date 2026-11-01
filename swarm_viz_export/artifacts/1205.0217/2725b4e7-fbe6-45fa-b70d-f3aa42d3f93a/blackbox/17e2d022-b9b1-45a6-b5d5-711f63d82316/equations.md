# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Reconstruct a first-order dynamically corrected single-qubit gate for a singlet-triplet qubit with H(t)=(J(t)/2)sigma_z+(h/2)sigma_x, with quasi-static nuclear gradient noise delta_h and exchange noise delta_J, using a tiny explicit instance. The circuit is a noiseless ideal target unitary compiled from a classical piecewise-constant pulse; the correction property is checked via the first-order error vectors.

Scope: One tiny instance: ideal piecewise-constant evolution of the two-level system with h=1, two-segment pulse with J values given as assumption, built as a product of exact segment exponentials. Numerical or geometric search for the pulses, non-Markovian noise simulation, and the full universal gate set are outside scope and not implemented. The abstract does not give explicit sequences, so the pulse values are placeholders and are not claimed to cancel errors.

## Symbols

- $J_k$: exchange value in segment k; domain: [0,J_max]
- $h$: fixed gradient field; domain: positive real
- $\tau_k$: duration of segment k; domain: nonnegative real
- $U_0(t)$: ideal evolution; domain: SU(2)
- $E_h,E_J$: first-order error vectors in toggling frame; domain: operators on C^2

## eq_1: Segment Hamiltonian

$$
H_k=\frac{J_k}{2}\sigma_z+\frac{h}{2}\sigma_x
$$

Hamiltonian in segment k of a piecewise-constant pulse

Provenance: `assumption`. Model from the method sketch; the abstract only mentions a singlet-triplet qubit with nuclear and voltage noise.

Equation assumptions:

- Piecewise-constant J
- fixed h

## eq_2: Gate unitary

$$
U=\prod_{k=n}^{1}\exp(-i H_k \tau_k)
$$

Ideal gate as ordered product of segment exponentials

Provenance: `standard_background`. Time-ordered evolution for piecewise-constant Hamiltonian.

Equation assumptions:

- Later segments multiply on the left

## eq_3: First-order error operators

$$
E_h=\int_0^T U_0^\dagger\sigma_x U_0\,dt,\quad E_J=\int_0^T J'(J(t))\,U_0^\dagger\sigma_z U_0\,dt
$$

Cancellation conditions are E_h=0 and E_J=0

Provenance: `abstract_inferred`. Leading-order cancellation corresponds to vanishing first-order Magnus terms; the exact form comes from the sketch and the standard toggling-frame approach.

Abstract evidence: simultaneously cancel to the leading order the dephasing due to non-Markovian nuclear-bath dynamics and voltage noise affecting the control fields

Equation assumptions:

- Quasi-static or low-frequency noise
- J' is the derivative of the noise coupling with respect to J

## Registers

- q: 1 qubits; singlet-triplet logical qubit

## Initial state

Arbitrary input state on q; the circuit is a unitary acting on it

## Classical postprocessing

Classical computation of the error vectors E_h and E_J, and the fidelity against the target gate, for diagnostics only.

## Algorithm steps

1. Fix the instance: h=1, J_max, and two segments with assumed placeholder (J_k,tau_k). (eq_1)
2. Compile each segment as a single-qubit unitary exponential and multiply them in order. (eq_2)
3. Optionally evaluate E_h and E_J classically to check cancellation; this is not part of the circuit. (eq_3)

## Assumptions

- Tiny instance with placeholder pulses
- No noise in the circuit
- No black-box or query claims

## Missing information

- Explicit pulse sequences
- Numerical search procedure and constraints
- Noise spectra and fidelity values
- Exact definition of the control-noise coupling J'(J)
