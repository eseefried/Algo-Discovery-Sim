# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Estimate the small systematic rotation-angle (amplitude) error phi=pi*epsilon of a noisy single-qubit gate U=exp(-i(theta/2) n.sigma), theta=pi(1+epsilon), using only powers U^k, k=2^j, on one qubit with SPAM-robust Higgins-style adaptive phase estimation. Off-resonance estimation is outside the core scope.

Scope: One qubit, no ancilla. Amplitude-error case only with axis n=x (no tilt). A tiny instance: J=3..5 doublings, a fixed epsilon (e.g. 0.05), constant shots per stage, optional constant visibility and bias to model SPAM. The robust theorem, the off-resonance estimator, and the exact robust proof constants are outside the scope.

## Symbols

- $\epsilon$: relative amplitude error of the gate; domain: real, small, |epsilon| much less than 1
- $\phi$: rotation-angle error pi*epsilon (assumed definition); domain: real, |phi|<pi/2 for the initial window
- $k_j=2^j$: number of sequential gate applications at stage j (queries); domain: integers, j=0..J-1
- $J$: number of doubling stages; domain: positive integer
- $N$: shots per stage; domain: positive integer
- $v,b$: unknown constant SPAM visibility and bias; domain: 0<v<=1, b real
- $\hat\phi_j$: estimate of phi after stage j; domain: real
- $\alpha_j$: measured angle atan2(s_j,c_j) estimating k_j phi mod 2pi; domain: (-pi,pi]

## eq_1: Gate model

$$
U=\exp\!\left(-i\frac{\pi(1+\epsilon)}{2}\,\sigma_x\right)=-i\,\sigma_x\,\exp\!\left(-i\frac{\phi}{2}\sigma_x\right),\quad \phi=\pi\epsilon
$$

Noisy pi pulse equals an ideal pi pulse (up to a phase) times a small rotation by phi about x.

Provenance: `abstract_inferred`. Amplitude error theta=pi(1+epsilon) is given in the sketch; the factorization is an algebraic identity.

Abstract evidence: amplitude and off-resonance errors

Equation assumptions:

- axis n=x, no off-resonance tilt

## eq_2: Power of the gate

$$
U^{2k}=(-1)^{k}\exp\!\left(-i\,k\phi\,\sigma_x\right)
$$

Even powers 2k of U give a pure rotation by 2k phi up to global phase. For odd k an ideal pi pulse remains, which can be undone by a known pi pulse or tracked classically.

Provenance: `standard_background`. sigma_x^2=I and sigma_x commutes with the rotation. This holds for the x-axis model.

Equation assumptions:

- no drift
- axis n=x

## eq_3: Signal model with SPAM

$$
s_k=b_s+v\sin(k\phi'),\quad c_k=b_c+v\cos(k\phi')
$$

Measured quadrature expectation values after the k-fold gate, where phi' is the effective angle per application (equal to phi up to a known offset or sign convention). SPAM scales the signals by v and adds a bias.

Provenance: `assumption`. Sketch states SPAM rescales by visibility and adds bias. The exact form is an assumed model. The sign and offset convention must be fixed by the builder, and the bias must be calibrated or cancelled.

Equation assumptions:

- constant unknown v,b
- the same quadrature mapping for all k

## eq_4: Angle readout

$$
\alpha_k=\operatorname{atan2}(s_k,c_k)\equiv k\phi \pmod{2\pi}
$$

The angle is recovered modulo 2 pi when the bias is zero or removed. Otherwise it is approximate.

Provenance: `abstract_inferred`. Higgins-style phase estimation reads the angle k*phi modulo 2 pi from sin and cos estimates.

Abstract evidence: a robust version of the phase estimation procedure of Higgins et al.

Equation assumptions:

- bias small or calibrated

## eq_5: Branch unwrapping and refinement

$$
\hat\phi_{j}=\frac{1}{k_j}\left(\alpha_{k_j}+2\pi m_j\right),\quad m_j=\operatorname*{arg\,min}_{m\in\mathbb Z}\left|\frac{\alpha_{k_j}+2\pi m}{k_j}-\hat\phi_{j-1}\right|
$$

Choose the 2 pi branch so that the new estimate is nearest the previous one. This is equivalent to choosing the branch nearest to 2*k_{j-1}*previous estimate. It is correct if the previous error is less than pi/k_j.

Provenance: `assumption`. The branch rule follows the sketch. The exact thresholds and the robust proof are not given in the abstract.

Equation assumptions:

- previous estimate error < pi/k_j (sketch suggests pi/3 window margin)
- initial estimate from k=1 within the unambiguous window

## eq_6: Heisenberg scaling

$$
\delta\phi_J\sim\frac{C}{k_{J-1}\sqrt N},\quad Q_{\mathrm{tot}}=N\sum_{j<J}k_j\approx N\,2^{J}
$$

Final error scales inversely with the largest k, so inversely with the total query count up to constants.

Provenance: `abstract_inferred`. Heisenberg scaling means error proportional to 1/total queries. The constants are not given.

Abstract evidence: our estimates achieve the optimal efficiency, Heisenberg scaling

Equation assumptions:

- constant shots per stage

## Registers

- q: 1 qubits; single data qubit holding the state, with U^k applied to it

## Initial state

|0> for one quadrature. |+> or a basis-change gate before U^k for the other quadrature. Both are prepared with fixed standard gates.

## Measurement

Single-qubit measurement in the Z basis after a basis-change gate that selects the sin or cos quadrature. Each stage uses N shots.

## Classical postprocessing

Estimate sin and cos from the counts and compute atan2. Perform the 2 pi branch unwrapping against the previous estimate, iterate over doublings, and output hat phi and epsilon=hat phi/pi.

## Algorithm steps

1. Pick J and N, and set k_j=2^j. For each k_j and each quadrature setting, build a one-qubit circuit with state preparation, then k_j sequential placements of the black-box gate (k_j queries). The runner substitutes the real gate. (eq_1, eq_2)
2. Add a basis-change gate and measure the single qubit (Z, X or Y) with N shots. Estimate the sin and cos quadrature expectations from the counts, with the little-endian bit read as bit 0 of the one-qubit register. (eq_3)
3. Compute alpha_k=atan2(s,c). For k=1 take the coarse estimate directly. (eq_4)
4. For j=1..J-1, unwrap alpha using the previous estimate, set the new estimate, and finally report epsilon=hat phi/pi. (eq_5, eq_6)

## Assumptions

- Chosen smallest construction: amplitude error about the x axis only, with phi=pi*epsilon.
- The quadrature mapping and sign convention for sin and cos are fixed by the builder, with a known pi pulse used to remove the odd-k ideal pulse.
- The SPAM model is a constant visibility and bias, with bias removed or negligible.
- The coarse estimate is within the unambiguous window.
- Constant N per stage.

## Missing information

- The paper's exact robust theorem, its constants and shot counts per stage.
- The exact pulse sequences for the off-resonance error and for the universal gate set.
- The exact SPAM-robust estimator and how the bias is handled.
- The exact definition of the angle estimated for the general gate with a tilted axis.
