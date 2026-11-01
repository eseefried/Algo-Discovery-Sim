# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Perfect state transfer of an arbitrary unknown two-qubit state between sites via a discrete-time quantum walk with coin flips; the abstract gives no explicit dynamics, so only a generic background framework and a tiny assumed instance can be specified.

Scope: One smallest construction: a generic discrete-time coined quantum walk on a 4-site cycle, with the two-qubit state to be transferred encoded in a placeholder way. The paper's specific coin settings, multi-qubit entanglement distribution, multi-dimensional network and routing protocol are outside the scope.

## Symbols

- $|\psi\rangle$: arbitrary unknown two-qubit state to transfer; domain: unit vector in C^4
- $C_t$: coin operator at step t (coin setting); domain: U(2)
- $S$: conditional shift operator; domain: unitary on coin x position space
- $U_t$: one-step walk operator; domain: unitary
- $N$: number of sites on cycle; domain: integer, assumed 4
- $T$: number of walk steps; domain: nonnegative integer
- $x$: site label; domain: {0,...,N-1}
- $F$: transfer fidelity; domain: [0,1]

## eq_1: Walk step

$$
U_t = S\,(C_t\otimes I_{N}),\quad |W_T\rangle = U_{T}\cdots U_{1}|W_0\rangle
$$

Generic discrete-time coined walk with possibly step-dependent coin operators.

Provenance: `standard_background`. Abstract mentions a discrete-time quantum walk with various coin flippings; this is the standard form, not the paper's specific one.

Equation assumptions:

- Step-dependent coins allowed

## eq_2: Shift operator

$$
S=\sum_{x}\left(|0\rangle\langle 0|\otimes|x+1\rangle\langle x|+|1\rangle\langle 1|\otimes|x-1\rangle\langle x|\right),\ x \bmod N
$$

Coin-conditioned shift on an N-site cycle with modular arithmetic.

Provenance: `assumption`. Assumed 1D cycle instance; the paper's network geometry is not given in the abstract.

Equation assumptions:

- N=4 cycle

## eq_3: Transfer condition

$$
|W_T\rangle=|\psi\rangle_{\mathrm{target}}\otimes|\phi\rangle_{\mathrm{rest}},\quad |\psi\rangle_{\mathrm{init}}\to|\psi\rangle_{\mathrm{target}}
$$

Perfect transfer means the target sites hold the input state exactly for every |\psi\rangle, with the remainder in a state independent of \psi.

Provenance: `abstract_inferred`. The claim of perfect transfer for arbitrary states implies exact, state-independent transfer.

Abstract evidence: perfect state transfer of an arbitrary unknown two-qubit state can be achieved via a discrete-time quantum walk

Equation assumptions:

- The encoding of the two qubits into walk degrees of freedom is unspecified

## eq_4: Fidelity

$$
F=\langle\psi|\rho_{\mathrm{target}}|\psi\rangle=1\ \forall\,|\psi\rangle
$$

Perfect transfer criterion in terms of fidelity.

Provenance: `standard_background`. Standard figure of merit for state transfer.

## Registers

- coin: 1 qubit qubits; walker coin degree of freedom (assumed)
- position: 2 qubits (N=4) qubits; site label, computational-basis integer encoding

## Initial state

Unspecified in the abstract; assumed |\psi\rangle encoded in the walker's initial coin/position degrees of freedom at the source sites, remaining degrees in a fixed reference state.

## Algorithm steps

1. Encode the unknown two-qubit state at the source sites (encoding assumed). (eq_3)
2. Apply T walk steps with a chosen coin sequence and shift. (eq_1, eq_2)
3. Check the perfect-transfer condition at the target sites. (eq_3, eq_4)

## Assumptions

- Tiny instance: N=4 cycle, which is not from the abstract.
- Coin sequence, encoding and T are not specified by the abstract.
- All equations are generic background or assumptions.

## Missing information

- Actual coin settings for perfect transfer
- Encoding of two-qubit state into the walk
- Network geometry and dimension
- Multi-qubit entangled state distribution protocol
- Routing protocol and architecture
