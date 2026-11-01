# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Given H=A+B with non-commuting A, B on a small register, find the Trotter number n minimizing the total variation distance between the output distribution of a noisy first-order Trotter circuit for exp(-iHt)|0..0> and the ideal exact distribution. Compare the numerically found n to the analytic n*=sqrt(a/(b*eps)).

Scope: One tiny instance: 2-qubit transverse-field Ising H=Z0Z1+g(X0+X1), initial state |00>, first-order Trotter, coherent over-rotation of size eps after each elementary gate (deterministic, statevector-friendly). Scan n and eps, find argmin of TV distance, compare to analytic n*. Out of scope: the paper's exact derivation and constants, stochastic or depolarizing noise averaging, Suzuki higher-order formulas (only the exponent change is noted), and any hardware calibration.

## Symbols

- $A,B$: non-commuting Hamiltonian terms, A=Z0Z1, B=g(X0+X1); domain: Hermitian operators on 2 qubits
- $t$: total evolution time; domain: positive real, e.g. 1
- $n$: Trotter number (number of repeated steps); domain: positive integer
- $\epsilon$: per-gate coherent over-rotation angle error strength; domain: small positive real, e.g. 1e-4 to 1e-2
- $D(n)$: total variation distance between noisy Trotter and ideal computational-basis distributions; domain: [0,1]
- $a,b$: fitted coefficients of the Trotter error and the gate error; domain: positive reals
- $n^*$: optimal Trotter number; domain: positive real, rounded to an integer
- $p$: product formula order; domain: positive integer

## eq_1: Trotter product with noisy gates

$$
U_n=\left[\,\tilde R_X(2gt/n)\,\tilde R_{ZZ}(2t/n)\right]^n,\quad \tilde R_\sigma(\theta)=R_\sigma(\theta+\epsilon)
$$

First-order Trotter circuit in which each elementary gate has an extra coherent angle error eps. RX is applied to each of the two qubits. The gate count is about 3n.

Provenance: `assumption`. The sketch proposes explicit over-rotation gates, and the abstract only says each gate is applied imperfectly.

Equation assumptions:

- Coherent over-rotation noise model
- Qiskit RZZ(θ)=exp(-iθ ZZ/2) and RX(θ)=exp(-iθ X/2)

## eq_2: Total variation distance

$$
D(n)=\tfrac12\sum_{x\in\{0,1\}^2}\left|\,|\langle x|U_n|00\rangle|^2-|\langle x|e^{-iHt}|00\rangle|^2\right|
$$

Statistical distance between computational-basis distributions, computed classically from the statevector. The exact reference comes from matrix exponentiation.

Provenance: `assumption`. The sketch fixes TV distance as the statistical distance. The abstract only mentions a statistical distance.

Equation assumptions:

- The ideal reference is computed classically

## eq_3: Error tradeoff model

$$
D(n)\approx \frac{a}{n}+b\,n\,\epsilon,\quad a\sim\tfrac12\|[A,B]\|t^2
$$

The first-order Trotter error falls as 1/n while the gate error grows linearly in the gate count. The squared-amplitude variant is a/n^2+b n^2 eps^2.

Provenance: `abstract_inferred`. The abstract states the tradeoff qualitatively. The 1/n and n*eps forms are the standard leading-order scalings from the sketch, not the paper's confirmed result.

Abstract evidence: The resultant tradeoff in errors leads to an ultimate limit on the precision of the simulation.

Equation assumptions:

- Leading-order errors
- Independent identical small gate errors
- Coefficients a and b fitted numerically or estimated

## eq_4: Optimal Trotter number

$$
n^*=\sqrt{\frac{a}{b\,\epsilon}},\qquad D_{\min}\approx 2\sqrt{a\,b\,\epsilon}
$$

Minimizer of eq_3, obtained by setting dD/dn=0. It gives n* proportional to eps^(-1/2) and D_min proportional to eps^(1/2).

Provenance: `abstract_inferred`. The abstract says an optimum n* is computed. This closed form follows from the assumed eq_3 model.

Abstract evidence: We calculate the optimum Trotter number $n^{*}$ that achieves this limit

Equation assumptions:

- eq_3 holds

## eq_5: Higher-order scaling

$$
D(n)\approx a_p n^{-p}+b\,n\,\epsilon\;\Rightarrow\; n^*\propto \epsilon^{-1/(p+1)}
$$

For a p-th order product formula the optimal n shifts to this exponent.

Provenance: `standard_background`. Follows from minimizing the assumed model. Out of scope for the circuit.

Equation assumptions:

- Gate count per step is held fixed in the scaling

## Registers

- sys: 2 qubits; system qubits, little-endian, qubit 0 is the least significant bit of the outcome index

## Initial state

|00> (all qubits in the ground computational state)

## Measurement

No hardware measurement. The simulator reads the statevector, and probabilities |amplitude|^2 are indexed in little-endian order (qubit 0 is the last character of a bit string).

## Classical postprocessing

Compute the exact reference distribution, TV distance for each n, the argmin over n, the fitted a and b, the analytic n*, and log-log slopes of n* versus eps (expect -1/2 for first order).

## Algorithm steps

1. Build H=Z0Z1+g(X0+X1) with e.g. g=1 and t=1. Compute the exact distribution classically by matrix exponentiation of the 4x4 H. (eq_2)
2. For each n in a range (e.g. 1..200) and each eps, build the circuit: n repetitions of RZZ(2t/n+eps) on (0,1), then RX(2gt/n+eps) on qubit 0 and on qubit 1. No measurements; read the statevector. (eq_1)
3. Compute D(n) from the statevector probabilities and the exact distribution. Find the integer n minimizing D. (eq_2)
4. Fit a and b from the small-n regime (eps=0 gives a) and the large-n regime. Compare the numerical argmin with n* and check the scaling in eps and t. (eq_3, eq_4)

## Assumptions

- The target instance (2-qubit TFIM, g=1, t=1) was chosen by me, not given in the abstract
- Coherent noise is used in place of stochastic noise so the statevector run is deterministic
- With coherent noise, errors may add or cancel with the Trotter error, so D(n) may be non-monotone; use a sign-fixed eps
- Order p=1
- No ancilla needed since the readout is computational-basis probabilities

## Missing information

- Paper's actual noise model and definition of statistical distance
- Paper's exact formulas and constants for n*
- Whether the paper treats Hamiltonians with many terms or a specific system
