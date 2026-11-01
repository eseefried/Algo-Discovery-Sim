# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Perfect transfer of an unknown coin (qubit) state from an initial position to a target position via a discrete-time quantum walk on a line or circle, using a final state-independent coin operator. The abstract gives only qualitative results, so the reconstruction is a background walk model on a tiny instance.

Scope: Assumed smallest instance: a coin-position walk on a 4-site circle with a identity or flip coin, showing a standard walk update plus a final correcting coin. Outside scope: general proofs of the distance limits for biased and Hadamard coins, the periodicity theorem, the explicit form of the additional end coin for general coins, and the line case.

## Symbols

- $|\psi\rangle=a|0\rangle+b|1\rangle$: unknown qubit state to transfer, stored in the coin; domain: a,b in C, |a|^2+|b|^2=1
- $N$: number of circle sites; domain: integer, assumed N=4
- $x$: walker position; domain: Z_N
- $C$: coin operator used at each step; domain: 2x2 unitary, e.g. I, X, H
- $S$: conditional shift; domain: unitary on coin⊗position
- $C_f$: additional final coin operator, independent of the state; domain: 2x2 unitary
- $t$: number of walk steps; domain: nonnegative integer

## eq_1: Conditional shift

$$
S=|0\rangle\langle 0|\otimes\sum_{x}|x+1\rangle\langle x|+|1\rangle\langle 1|\otimes\sum_{x}|x-1\rangle\langle x|
$$

Coin 0 moves right and coin 1 moves left, with positions mod N.

Provenance: `standard_background`. Standard discrete-time walk shift; the abstract does not give the convention.

Equation assumptions:

- Shift convention chosen here
- Positions mod N on the circle

## eq_2: Walk evolution

$$
U=S\,(C\otimes I_N),\quad |\Psi_t\rangle=U^t|\psi\rangle|x_0\rangle
$$

Evolution of the coin-position state after t steps from the initial position x_0.

Provenance: `standard_background`. Generic discrete-time quantum walk definition for a walk driven by a coin operator.

Equation assumptions:

- The same coin is applied at every step

## eq_3: Perfect state transfer condition

$$
(C_f\otimes I_N)\,U^t\,|\psi\rangle|x_0\rangle=(a|0\rangle+b|1\rangle)\otimes|x_t\rangle\ \ \forall a,b
$$

After t steps and the final coin, the coin holds the original state and the walker is at the target x_t.

Provenance: `abstract_inferred`. Inferred from the stated goal and the final coin independent of the state; the exact formal definition is not given in the abstract.

Abstract evidence: perfect transfer of an unknown qubit state via the discrete-time quantum walk on a line or a circle

Equation assumptions:

- Target position x_t is deterministic
- Transfer is exact for all states

## eq_4: Illustrative flip-coin case

$$
C=X:\ U^t|\psi\rangle|x_0\rangle=X^t|\psi\rangle|x_0+(-1)^t\ldots\rangle,\ \text{with }C_f=X^t
$$

Illustrative reading for the flip coin: the walker moves in a fixed direction pattern and the coin only flips, so a final X^t restores the state.

Provenance: `assumption`. Chosen to illustrate the abstract's claim that identity and flip coins allow arbitrary distance; the walker position expression is schematic and not derived. The exact position pattern is not verified.

Equation assumptions:

- Schematic only; position dynamics under X and the shift not worked out

## Registers

- coin: 1 qubit qubits; carries the unknown state
- position: 2 qubits (N=4) qubits; walker site on circle, basis |x>, x in Z_4

## Initial state

|psi>_coin ⊗ |x_0>_position with x_0=0 (assumed)

## Algorithm steps

1. Prepare the unknown coin state and walker at x_0. (eq_2)
2. Apply t iterations of coin C then shift S. (eq_1, eq_2)
3. Apply final state-independent coin C_f on the coin register. (eq_3)
4. Check transfer condition at target position (flip coin illustration). (eq_3, eq_4)

## Assumptions

- Tiny instance N=4 and x_0=0 chosen by me, not by the abstract
- Shift convention and walk operator are standard background
- Equation for flip coin is schematic

## Missing information

- Explicit form of the additional final coin operator for general coins
- Precise definition of perfect transfer and target positions
- Parametrization of biased coins and finite distance bounds
- Periodicity statement and proof
- Line-walk details
