# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Perfect transfer of an unknown single-qubit (coin) state from one site of a discrete-time quantum walk (DTQW) on a line or a circle to another site, using a state-independent coin operator applied once at the end of the walk; characterise which driving coins allow transfer over arbitrary vs. finite distances and show that such walks are periodic.

Scope: ONE smallest useful construction (chosen here as an assumption, no experiment_scope was supplied): a DTQW on a circle of N = 4 sites driven by the identity coin, transferring the coin state alpha|0> + beta|1> from site x_0 = 0 to site d = 2 in t = 2 steps, with the final coin operator reducing to the identity in the chosen shift convention. The generic DTQW definitions and the abstract's perfect-state-transfer (PST) and periodicity conditions are stated in general form. Outside scope: the paper's explicit final coin operator C_f for Hadamard and general biased coins, the finite-distance results for those coins, the line (infinite lattice) analysis, the flip-coin case, and the general proof of periodicity.

## Symbols

- $\mathcal{H}_c$: Coin Hilbert space spanned by |0\rangle, |1\rangle (one qubit); domain: \mathbb{C}^2
- $\mathcal{H}_p$: Position Hilbert space spanned by |x\rangle; domain: \mathbb{C}^N for a circle of N sites (x \in \mathbb{Z}_N); \ell^2(\mathbb{Z}) for a line
- $N$: Number of sites of the circle; domain: positive even integer; N = 4 in the chosen instance
- $x_0$: Initial (sender) site; domain: \mathbb{Z}_N; x_0 = 0 in the instance
- $d$: Transfer distance (receiver site is x_0 + d); domain: positive integer; d = 2 in the instance
- $t$: Number of walk steps before the final coin operator; domain: positive integer; t = 2 in the instance
- $C$: Driving coin operator applied at every step; domain: U(2); C = I in the instance
- $C_f$: Additional state-independent coin operator applied once at the end of the walk; domain: U(2)
- $S$: Conditional shift operator; domain: unitary on \mathcal{H}_c \otimes \mathcal{H}_p
- $U$: One step of the walk, U = S (C \otimes I_p); domain: unitary on \mathcal{H}_c \otimes \mathcal{H}_p
- $\alpha, \beta$: Unknown amplitudes of the qubit state to be transferred; domain: \mathbb{C}, |\alpha|^2 + |\beta|^2 = 1
- $\phi$: Irrelevant global phase; domain: [0, 2\pi)
- $T$: Period of the walk; domain: positive integer

## eq_1: Conditional shift operator

$$
S = |0\rangle\langle 0| \otimes \sum_{x} |x-1\rangle\langle x| + |1\rangle\langle 1| \otimes \sum_{x} |x+1\rangle\langle x|, \quad x \pm 1 \text{ taken mod } N \text{ on the circle}
$$

Coin state |0> moves the walker one site to the left, |1> one site to the right; on the circle positions are reduced modulo N, on the line x ranges over all integers.

Provenance: `standard_background`. Standard definition of the DTQW shift on a line/cycle; the abstract only names the walk, not this convention.

Equation assumptions:

- Direction convention (|0> left, |1> right) is a choice; the paper's convention may differ (an equivalent flip of coin labels).
- Position labels on the circle are integers mod N.

## eq_2: Walk step and t-step evolution

$$
U = S\,(C \otimes I_p), \qquad |\psi(t)\rangle = U^{t}\,|\psi_{\mathrm{in}}\rangle
$$

Each step applies the driving coin C to the coin register, then the conditional shift; the walk runs for t steps.

Provenance: `standard_background`. Standard DTQW evolution; the abstract refers to the walk being 'driven by' a coin operator.

Equation assumptions:

- Coin is applied before the shift in each step (standard ordering).

## eq_3: Initial state carrying the unknown qubit

$$
|\psi_{\mathrm{in}}\rangle = (\alpha|0\rangle + \beta|1\rangle) \otimes |x_0\rangle, \qquad |\alpha|^2+|\beta|^2 = 1
$$

The unknown qubit state is encoded in the coin register and the walker is localised at the sender site x_0.

Provenance: `abstract_inferred`. Inferred: the only qubit degree of freedom in a DTQW is the coin, so the unknown state must be encoded in the coin with the walker localised at a sender site.

Abstract evidence: perfect transfer of an unknown qubit state via the discrete-time quantum walk

Equation assumptions:

- Walker initially localised at a single site x_0.

## eq_4: Perfect state transfer condition with final coin operator

$$
(C_f \otimes I_p)\,U^{t}\,\big[(\alpha|0\rangle+\beta|1\rangle)\otimes|x_0\rangle\big] = e^{i\phi}\,(\alpha|0\rangle+\beta|1\rangle)\otimes|x_0+d\rangle \quad \forall\,\alpha,\beta
$$

Exact equality up to a global phase, required for all input amplitudes; C_f must not depend on alpha, beta. This defines perfect transfer over distance d after t steps.

Provenance: `abstract_inferred`. Formalises the abstract's statement that a state-independent coin operator applied after the walk completes the perfect transfer; the explicit form of C_f for general coins is not given in the abstract.

Abstract evidence: we introduce an additional coin operator which is applied at the end of the walk. This operator does not depend on the state to be transferred.

Equation assumptions:

- Global phase phi is allowed (standard for perfect state transfer).
- Receiver site is x_0 + d (mod N on the circle).

## eq_5: Identity-coin walk on an N-cycle and transfer to the antipodal site (chosen instance)

$$
U^{t}|\psi_{\mathrm{in}}\rangle = \alpha\,|0\rangle\otimes|x_0 - t \bmod N\rangle + \beta\,|1\rangle\otimes|x_0 + t \bmod N\rangle; \quad t = d = N/2,\ C_f = I \Rightarrow (\alpha|0\rangle+\beta|1\rangle)\otimes|x_0 + N/2\rangle
$$

With C = I the two coin components travel in opposite directions without mixing; on a circle of even N they recombine exactly at the antipodal site after N/2 steps, giving perfect transfer over distance d = N/2 with trivial final coin. Instance: N = 4, x_0 = 0, t = d = 2.

Provenance: `assumption`. Direct consequence of eq_1-eq_3 for C = I; chosen as the smallest exactly verifiable instance consistent with the abstract's claim that the identity coin allows transfer over arbitrary distance (here by choosing N = 2d). The paper's own setting for the identity/flip coins (line vs circle, shift convention) is not stated in the abstract.

Equation assumptions:

- N even and d = N/2.
- In this shift convention C_f = I; in a flip-flop shift convention the roles of identity and flip coins interchange.

## eq_6: Periodicity of a walk ending with perfect state transfer

$$
\exists\, T \in \mathbb{Z}_{>0}: \quad U^{T}|\psi_{\mathrm{in}}\rangle = e^{i\theta}|\psi_{\mathrm{in}}\rangle; \qquad \text{instance: } C = I,\ N = 4 \Rightarrow U^{4} = I_c \otimes I_p
$$

The abstract claims walks that end with PST are periodic; for the instance the identity-coin walk on the 4-cycle returns exactly to the initial state after T = N = 4 steps (shift by ±4 is the identity).

Provenance: `abstract_inferred`. Formalises the abstract's periodicity claim; the general proof and general period are not available, only the instance value T = N is verifiable from eq_5.

Abstract evidence: we show that quantum walks ending with a perfect state transfer are periodic.

Equation assumptions:

- Periodicity is taken as return of the walker state up to a global phase.
- General period T for other coins unknown.

## Registers

- coin: 1 qubits; Carries the unknown qubit state alpha|0> + beta|1>; acted on by C each step and by C_f at the end.
- position: ceil(log2 N) = 2 for N = 4 qubits; Walker position x in Z_N, encoded as a 2-bit integer (|x> = |x_1 x_0> with x = 2 x_1 + x_0); shifted by ±1 mod N conditioned on the coin.

## Initial state

(alpha|0> + beta|1>)_coin ⊗ |x_0 = 0>_position = (alpha|0> + beta|1>) ⊗ |00> (eq_3).

## Measurement

For verification only (not part of the transfer protocol): measure the position register in the computational basis, expecting outcome x = 2 (|10>) with probability 1; then characterise the coin register (e.g. state tomography for several test inputs alpha, beta, or inverse-preparation and measurement of |0>) to confirm it equals alpha|0> + beta|1>.

## Classical postprocessing

Estimate the position-outcome probability at site d and the coin fidelity F = |<psi_target|rho_coin|psi_target>| from measurement statistics; perfect transfer corresponds to position probability 1 and F = 1 for all test inputs.

## Algorithm steps

1. Prepare the coin register in the unknown state alpha|0> + beta|1> and the position register in |x_0> = |0> (binary |00>). (eq_3)
2. Apply t = 2 walk steps U = S (C ⊗ I) with C = I: each step is a controlled decrement (coin |0>) / controlled increment (coin |1>) of the position modulo N = 4. (eq_1, eq_2, eq_5)
3. Apply the final state-independent coin operator C_f (equal to the identity for this instance) to the coin register, completing the perfect transfer to site x_0 + d = 2. (eq_4, eq_5)
4. (Optional check of periodicity) Continue for a total of T = 4 steps and verify return to the initial state. (eq_6)

## Assumptions

- No experiment_scope was supplied; the instance (circle, N = 4, identity coin, x_0 = 0, d = 2, t = 2, C_f = I) was chosen as the smallest exactly verifiable construction and is not taken from the paper.
- Standard DTQW conventions (coin-then-shift, |0> moves left, |1> moves right, positions mod N) are assumed; the paper's conventions may differ.
- Perfect transfer is defined up to a global phase.
- The identity-coin instance makes the paper's additional final coin operator trivial; the nontrivial C_f relevant for Hadamard/biased coins is not reconstructed.

## Missing information

- Explicit form of the final coin operator C_f for the Hadamard coin and general biased coins, and the finite distances/step numbers at which they achieve perfect transfer.
- The paper's precise setting (line vs circle, shift convention, initial state) under which both identity and flip coins yield transfer over arbitrary distance; in the convention used here the flip coin with a standard shift yields a period-2 walk without transfer, suggesting a different convention in the paper.
- General proof and expression for the period T of walks ending with perfect state transfer.
- Definition and treatment of perfect transfer on the infinite line, where the two coin components of identity/flip-coin walks never recombine in the convention used here.
