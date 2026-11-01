# Abstract to equations

Status: **partial**

Model: `claude-sonnet-5-5`

Mathematics has not been independently verified.

Reconstruct a minimal mathematical framework for universal quantum computation with interacting bosonic quantum walkers on a graph under the Bose-Hubbard model, with qubits encoded in walker positions. The paper-specific graph geometry, gate constructions and parameters are not given in the abstract.

Scope: Smallest useful instance (an assumption): one walker on a two-vertex graph encoding one qubit, with a tunneling-generated X rotation and an on-site-energy-generated Z rotation, plus the generic Bose-Hubbard Hamiltonian as background. Outside this scope: the actual piecewise-constant graph design, the cphase and swap constructions, linear-vertex scaling, Steane code encoding, 3D extension, and the optical lattice implementation.

## Symbols

- $a_i^\dagger, a_i$: bosonic creation and annihilation operators at vertex i; domain: operators with [a_i,a_j^\dagger]=\delta_{ij}
- $J_{ij}$: hopping amplitude between adjacent vertices i and j; domain: real numbers
- $\epsilon_i$: on-site potential at vertex i; domain: real numbers
- $U$: on-site interaction strength; domain: real numbers
- $n_i$: number operator a_i^\dagger a_i; domain: nonnegative integers
- $\theta,\phi$: X and Z rotation angles; domain: [0,2\pi)
- $|0\rangle_L,|1\rangle_L$: logical qubit states, assumed to be the walker at vertex 1 or vertex 2; domain: single-walker Fock states

## eq_1: Bose-Hubbard Hamiltonian

$$
H=-\sum_{\langle i,j\rangle}J_{ij}\left(a_i^\dagger a_j+a_j^\dagger a_i\right)+\sum_i \epsilon_i n_i+\frac{U}{2}\sum_i n_i(n_i-1)
$$

Generic Bose-Hubbard model on a graph, which the abstract says is two-dimensional.

Provenance: `standard_background`. The abstract names the Bose-Hubbard model but gives no explicit Hamiltonian, so this is the textbook form. The paper's parameters and graph are unknown.

Equation assumptions:

- Standard sign convention
- Spinless bosons

## eq_2: Position encoding of one qubit

$$
|0\rangle_L=a_1^\dagger|\mathrm{vac}\rangle,\quad |1\rangle_L=a_2^\dagger|\mathrm{vac}\rangle
$$

One walker on two vertices encodes one qubit.

Provenance: `assumption`. The abstract says information is encoded in walker positions. The two-vertex dual-rail form is an assumed minimal instance.

Equation assumptions:

- The paper's actual encoding may differ

## eq_3: X rotation by tunneling

$$
H_X=-J\left(a_1^\dagger a_2+a_2^\dagger a_1\right),\quad U_X(\theta)=e^{-iH_Xt}=e^{i J t X_L},\ \theta=-2Jt
$$

Within the single-walker subspace, hopping acts as a logical X rotation, with the convention R_X(\theta)=e^{-i\theta X/2}.

Provenance: `standard_background`. Direct consequence of eq_1 restricted to one particle on two sites. It is not the paper's specific scheme.

Equation assumptions:

- \epsilon_1=\epsilon_2
- Single walker so U is irrelevant

## eq_4: Z rotation by potential offset

$$
H_Z=\frac{\Delta}{2}\left(n_1-n_2\right),\quad U_Z(\phi)=e^{-iH_Zt}=e^{-i\phi Z_L/2},\ \phi=\Delta t
$$

With hopping off, a relative on-site energy gives a logical Z rotation.

Provenance: `standard_background`. The relative phase between the two position states follows from eq_1 with J=0. The paper's mechanism for Z rotations is unknown.

Equation assumptions:

- J=0 during the gate
- Hopping can be switched or localized

## eq_5: Target gate set

$$
\mathrm{cphase}(\varphi)=\mathrm{diag}(1,1,1,e^{i\varphi}),\quad \mathrm{SWAP}|a,b\rangle=|b,a\rangle
$$

Target two-qubit gate definitions, with the cphase phase \varphi left unspecified.

Provenance: `abstract_inferred`. The abstract names the gates. Their matrices are standard definitions, but the bosonic construction is not given.

Abstract evidence: an entangling two-qubit cphase gate and a swap gate

Equation assumptions:

- Computational basis ordering |00>,|01>,|10>,|11>

## Registers

- walker position register: 2 vertices per qubit in the assumed minimal instance; unknown in the paper's scheme (linear in the number of qubits) qubits; Encodes the logical qubit by the walker's location

## Initial state

Assumed: one walker at vertex 1, |0>_L = a_1^\dagger|vac>.

## Measurement

Single-qubit measurement by localized position (occupation) measurement, as the abstract suggests localized operators. The details are not given.

## Algorithm steps

1. Prepare the walker at a chosen vertex to initialize the logical state. (eq_2)
2. Apply an X rotation by evolving under hopping for time t. (eq_1, eq_3)
3. Apply a Z rotation by evolving under a relative on-site potential with hopping off. (eq_1, eq_4)
4. Entangling cphase and swap gates are required for universality, but the interacting multi-walker construction is not specified in the abstract. (eq_5)

## Assumptions

- The smallest instance is chosen by the reconstructor, since no scope was given.
- The single-walker two-vertex model is only illustrative; the paper's piecewise-constant graph and parameters are unknown.
- Global phases are ignored.

## Missing information

- Graph geometry and the piecewise-constant parameter values
- Multi-walker encoding and the construction of the cphase and swap gates
- Time schedules and the interaction regime for U
- Steane code logical encoding and the 3D extension
- Optical lattice implementation details
