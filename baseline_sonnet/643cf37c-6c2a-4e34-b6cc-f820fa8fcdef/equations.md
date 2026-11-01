# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Synthesize dynamically corrected gates for a singlet-triplet spin qubit by numerically searching control sequences that perturbatively cancel, to leading order, sensitivity to non-Markovian dephasing noise (nuclear bath) and control (voltage) noise.

Scope: Generic background framework only: a single-qubit gate under a control Hamiltonian with a classical slow dephasing noise term, toggling-frame first-order error cancellation, and a numerical-search cost function, on a tiny assumed instance. The paper's specific singlet-triplet pulse sequences, control constraints, noise spectra, and fidelity predictions are outside this scope.

## Symbols

- $H(t)$: total Hamiltonian of the qubit; domain: Hermitian operators on C^2, t in [0,T]
- $u_x(t),u_z(t)$: control amplitudes (assumed exchange/gradient-like controls); domain: real functions, bounded
- $\beta(t)$: classical noise process modelling slow non-Markovian dephasing (assumed quasi-static); domain: real
- $U_0(t)$: ideal control propagator; domain: SU(2)
- $\tilde{\sigma}_z(t)$: noise operator in the toggling frame; domain: 2x2 Hermitian
- $U_{target}$: target gate; domain: SU(2)
- $\theta$: vector of piecewise-constant control parameters; domain: R^N
- $T$: gate duration; domain: positive real

## eq_1: Noisy Hamiltonian

$$
H(t)=\tfrac12\left[u_x(t)\sigma_x+u_z(t)\sigma_z\right]+\tfrac12\beta(t)\sigma_z
$$

Control Hamiltonian plus a classical dephasing term as a stand-in for the nuclear-bath and voltage noise.

Provenance: `assumption`. The abstract mentions dephasing and control noise but gives no model; this is a generic assumed instance.

Equation assumptions:

- Classical noise approximation
- Quasi-static beta

## eq_2: Toggling-frame error

$$
\tilde{\sigma}_z(t)=U_0^\dagger(t)\sigma_z U_0(t),\quad U(T)\approx U_0(T)\exp\!\left[-\tfrac{i}{2}\beta\int_0^T\tilde{\sigma}_z(t)\,dt\right]
$$

First-order Magnus approximation (not exact) of the noisy propagator for quasi-static noise.

Provenance: `standard_background`. Standard perturbative error treatment underlying dynamically corrected gates.

Equation assumptions:

- Leading order in beta
- Quasi-static noise

## eq_3: First-order cancellation condition

$$
\int_0^T\tilde{\sigma}_z(t)\,dt=0
$$

Condition for leading-order dephasing cancellation.

Provenance: `abstract_inferred`. Leading-order cancellation is interpreted as vanishing of the first-order Magnus term; the specific form is inferred.

Abstract evidence: simultaneously cancel to the leading order the dephasing

Equation assumptions:

- Same form of condition applies to control-noise terms with their own toggling-frame operators

## eq_4: Gate target constraint

$$
U_0(T;\theta)=U_{target}\ \text{up to global phase}
$$

The ideal propagator must realize the target gate.

Provenance: `assumption`. Needed for a gate-synthesis problem; not stated explicitly.

Equation assumptions:

- Piecewise-constant controls parameterized by theta

## eq_5: Numerical search cost

$$
\min_{\theta}\;J(\theta)=\left(1-F_0(\theta)\right)+\lambda\left\|\int_0^T\tilde{\sigma}_z(t;\theta)\,dt\right\|^2,\quad \text{s.t. bounds on }u_x,u_z
$$

Cost combining gate infidelity and the first-order error norm, minimized subject to control constraints.

Provenance: `assumption`. The abstract says sensitivity is minimized via numerical search; this specific cost is an assumed form.

Equation assumptions:

- Weight lambda is chosen by the user
- F_0 is the noise-free gate fidelity

## Registers

- q: 1 qubits; Effective singlet-triplet logical qubit

## Classical postprocessing

Evaluate the resulting sequence's fidelity under sampled noise values to check robustness (assumed).

## Algorithm steps

1. Choose a control parametrization (piecewise-constant with bounded amplitudes) and a target gate, e.g. an X rotation by pi. (eq_1, eq_4)
2. Compute the toggling-frame noise operators and their first-order integrals. (eq_2, eq_3)
3. Numerically minimize the cost function over the controls to obtain a robust gate sequence. (eq_5)

## Assumptions

- Tiny instance: a single qubit with a quasi-static dephasing noise model and generic controls.
- Control noise is treated analogously to beta with its own toggling-frame operator.
- No specific pulse shapes or constraints from the paper are used.

## Missing information

- Actual singlet-triplet Hamiltonian and control constraints
- Noise models and spectra for the nuclear bath and voltage noise
- Exact non-Markovian perturbative formalism used
- Explicit pulse sequences and predicted fidelities
- Handling of universal gate sets and of non-quasi-static noise
