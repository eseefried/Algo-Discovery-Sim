# Abstract to equations

Status: **partial**

Model: `external:a2m_swarm`

Mathematics has not been independently verified.

Build the 1D coinless (staggered, tessellation-based) quantum walk U=U1 U0 on a cycle of N=2^n sites, and a coined-walk circuit on n+1 qubits (position plus one coin qubit) intended to be equivalent on an invariant subspace. Compare position distributions, then compute total variation distance to uniform and the time-averaged distribution.

Scope: Tiny instance: n=2 or 3 (N=4 or 8), 3 or 4 qubits for the coined circuit, localized initial site, statevector simulation without measurement. The exact paper mapping from coinless to extended coined walk for general evolution operators, asymptotics, and the general tessellation families are outside scope.

## Symbols

- $N=2^n$: number of cycle sites; domain: power of two, N>=4
- $P_0,P_1$: projectors onto the uniform superposition of each polygon (pair of adjacent sites) in the even-odd and odd-even tessellations; domain: orthogonal projectors on C^N
- $U_i$: reflection 2P_i-I; domain: unitary on C^N
- $c$: coin qubit; domain: {0,1}
- $S_\pm$: shift x -> x±1 mod N; domain: permutation of sites
- $P_t(x)$: position probability after t steps, coin traced out; domain: [0,1]
- $D_t$: total variation distance of P_t to uniform; domain: [0,1]
- $\bar P_T(x)$: time-averaged distribution over t=0..T-1; domain: probability vector

## eq_1: Coinless evolution

$$
U=U_1U_0,\quad U_i=2P_i-I
$$

One step of the coinless walk as a product of two tessellation reflections.

Provenance: `abstract_inferred`. The abstract says the operators come from tessellations; the product of reflections form is the standard staggered walk from background and the sketch.

Abstract evidence: they have evolution operators that can be obtained by a graphical method based on lattice tessellations

Equation assumptions:

- Two-polygon tessellations in 1D
- P_i are sums of projectors onto uniform pair states

## eq_2: Polygon projector

$$
P_0=\sum_{k=0}^{N/2-1}|\phi_{2k}\rangle\langle\phi_{2k}|,\ P_1=\sum_{k=0}^{N/2-1}|\phi_{2k+1}\rangle\langle\phi_{2k+1}|,\ |\phi_j\rangle=\tfrac{1}{\sqrt2}(|j\rangle+|j+1 \bmod N\rangle)
$$

Pair states for even-odd and odd-even tessellations.

Provenance: `assumption`. Standard 1D staggered construction chosen from the sketch.

Equation assumptions:

- Pairs (2k,2k+1) for U0 and (2k+1,2k+2) for U1

## eq_3: Candidate coined step

$$
W=(S\otimes I)\,(H_c)\,\ \text{with}\ S=S_+\otimes|0\rangle\langle0|_c+S_-\otimes|1\rangle\langle1|_c,\ W_{\rm step}=S\,(I\otimes H)
$$

Coin-controlled shift after a Hadamard coin. The second Hadamard-like coin and shift back are left to be tuned so that the two-step operator matches U1U0 on an invariant subspace.

Provenance: `assumption`. Taken from the sketch; the exact equivalence is not derived from the abstract and may need a different coin or shift.

Equation assumptions:

- Hadamard coin
- Equivalence only on an invariant subspace
- The exact paper mapping is unknown

## eq_4: Position distribution

$$
P_t(x)=\sum_{c}|\langle x,c|\psi_t\rangle|^2
$$

Position probabilities with the coin traced out; for the coinless walk, P_t(x)=|\langle x|\psi_t\rangle|^2.

Provenance: `standard_background`. Definition of the marginal.

## eq_5: Mixing and limiting distribution

$$
D_t=\tfrac12\sum_x\left|P_t(x)-\tfrac1N\right|,\quad \bar P_T(x)=\tfrac1T\sum_{t=0}^{T-1}P_t(x)
$$

Total variation distance to uniform and the Cesaro-averaged limiting distribution, with mixing time the first t at which D_t falls below epsilon, or the same for the averaged distribution.

Provenance: `standard_background`. The abstract mentions mixing time and limiting distributions on cycles; these are the usual definitions for quantum walks.

Equation assumptions:

- Epsilon chosen by the user
- Time-averaged (not instantaneous) mixing

## Registers

- pos: n qubits; site index, little-endian, x=sum_i q_i 2^i
- coin: 1 qubits; coin qubit for the coined version; absent in the coinless version
- anc: 0 to 1 (if the incrementer needs it) qubits; ancilla, returned to |0>

## Initial state

|x0>_pos|c0>_coin, e.g. x0=0 and c0=0, with a localized site

## Measurement

None; read statevector probabilities of the position register (bit order little-endian, index = integer value of pos).

## Classical postprocessing

Marginalize the coin, compute D_t, the first t with D_t<epsilon, and the average over t.

## Algorithm steps

1. Build the coinless U0 and U1 for N=4 or 8 as matrices or circuits. Compute P_t(x) by simulation. This is a classical reference for the statevector. (eq_1, eq_2)
2. Build the coined circuit: H on coin, coin-controlled incrementer/decrementer on pos using CX/MCX ladders, then the second coin and shift back as per the sketch. Test whether the two-step operator restricted to the invariant subspace matches U1U0, adjusting the coin if it does not. (eq_3)
3. Run t steps without measurement, read statevector probabilities, and trace out the coin. Compare with the coinless distribution and spectra. (eq_4)
4. Compute D_t, the mixing time and the time-averaged distribution. (eq_5)

## Assumptions

- N=2^n with a small n
- Two-polygon even/odd tessellations
- Hadamard coin with controlled shift is the equivalent coined walk
- The mapping is exact only on an invariant subspace
- Localized initial state

## Missing information

- The exact transformation from coinless to extended coined walk
- The exact second coin and shift-back
- The specific family of evolution operators
- The definition of the invariant subspace
- The paper's tessellation examples and quantitative results
