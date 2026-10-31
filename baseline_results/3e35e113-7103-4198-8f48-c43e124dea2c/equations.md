# Abstract to equations

Status: **partial**

Model: `claude-fable-5-1`

Mathematics has not been independently verified.

Given black-box access to one of the 2d 'cyclic-type' permutations of d=4 elements (the d cyclic shifts and the d reflections forming the dihedral group D_4 acting on Z_4), decide with a single evaluation of the permutation which of the two classes it belongs to (the class the algorithm literature labels 'even'/positive-cyclic vs 'odd'/negative-cyclic), using a single ququart realized by photon polarization and spatial modes.

Scope: Reconstruct the single-qudit permutation-parity algorithm (Gedik-type) for d=4: one ququart register, Fourier-basis input state, permutation unitary from the 8-element dihedral set, inverse Fourier transform, computational-basis measurement. Explicit instance: d=4, omega=i, test permutations sigma(k)=k+1 mod 4 (shift) and sigma(k)=-k mod 4 (reflection). Outside scope: the linear-optical decomposition of the ququart gates into wave plates/beam splitters, single-photon source and detection details, measured fidelities, and the 'universality' claim of the abstract.

## Symbols

- $d$: qudit dimension; d=4 for the ququart; domain: integer, d=4
- $k$: computational-basis label of the ququart; domain: Z_4 = {0,1,2,3}
- $\omega$: primitive d-th root of unity, \omega = e^{2\pi i/d} = i for d=4; domain: complex unit circle
- $\sigma$: permutation of Z_4 given as a black box; domain: dihedral subset D_4 \subset S_4 (8 elements)
- $m$: shift/reflection parameter of the permutation; domain: Z_4
- $U_\sigma$: permutation unitary acting on the ququart; domain: 4x4 permutation matrix
- $F$: quantum Fourier transform on one ququart; domain: 4x4 unitary
- $|\psi_j\rangle$: j-th Fourier-basis state of the ququart; domain: unit vector in C^4, j in Z_4
- $s,p$: spatial-mode bit and polarization bit (H=0,V=1) encoding the ququart; domain: {0,1} each

## eq_1: Ququart encoding in polarization and spatial modes

$$
|k\rangle = |s\rangle_{\mathrm{spatial}} \otimes |p\rangle_{\mathrm{pol}},\quad k = 2s + p,\quad s,p \in \{0,1\},\ k \in \{0,1,2,3\}
$$

The four-level photonic state is formed from two spatial modes and two polarizations; integer label k uses spatial bit as most significant bit.

Provenance: `assumption`. The abstract states polarization and spatial modes realize ququart states; the specific bit ordering is a chosen convention.

Equation assumptions:

- Spatial bit is the most significant bit; H maps to p=0, V to p=1.

## eq_2: Fourier basis and QFT on the ququart

$$
F|j\rangle = |\psi_j\rangle = \frac{1}{\sqrt{d}}\sum_{k=0}^{d-1}\omega^{jk}|k\rangle,\quad \omega = e^{2\pi i/d},\ d=4,\ \omega = i
$$

Definition of the single-qudit QFT and its basis states; the algorithm's input is |\psi_1\rangle = F|1\rangle.

Provenance: `standard_background`. Standard single-qudit Fourier transform used in the Gedik-type permutation algorithm.

## eq_3: Permutation unitaries (dihedral set)

$$
U_\sigma|k\rangle = |\sigma(k)\rangle,\quad \sigma^{+}_m(k) = k + m \bmod d,\quad \sigma^{-}_m(k) = m - k \bmod d,\quad m \in Z_d
$$

The 2d permutations considered: d cyclic shifts (class '+', labelled even/positive in the algorithm) and d reflections (class '-', labelled odd/negative). Addition is modular.

Provenance: `abstract_inferred`. The single-qudit permutation-parity algorithm is defined on this dihedral family; the abstract's 'essential permutation transformations' is interpreted as this set.

Abstract evidence: we realize the quantum ququart states and all the essential permutation transformations

Equation assumptions:

- The experiment's permutation set is the 8-element dihedral family rather than all 24 elements of S_4; for d=4 the shift/reflection class does not coincide with S_4 sign parity, so 'parity' is understood in the algorithm's sense.

## eq_4: Action of permutations on the Fourier input state

$$
U_{\sigma^{+}_m}|\psi_1\rangle = \omega^{-m}|\psi_1\rangle,\qquad U_{\sigma^{-}_m}|\psi_1\rangle = \omega^{m}|\psi_{d-1}\rangle
$$

Shifts leave |\psi_1\rangle invariant up to a global phase; reflections map it to |\psi_{d-1}\rangle up to a global phase (exact equalities).

Provenance: `standard_background`. Follows by substituting j = sigma(k) in eq_2 and eq_3: sum_k omega^k |k+m> = omega^{-m} sum_j omega^j |j>, and sum_k omega^k |m-k> = omega^m sum_j omega^{-j}|j>.

## eq_5: Readout after inverse QFT

$$
F^{\dagger} U_\sigma F|1\rangle = \begin{cases} \omega^{-m}|1\rangle & \sigma = \sigma^{+}_m \\ \omega^{m}|d-1\rangle = \omega^{m}|3\rangle & \sigma = \sigma^{-}_m \end{cases}
$$

A single computational-basis measurement deterministically yields 1 for the shift class and 3 for the reflection class; one evaluation of U_sigma suffices, versus two evaluations classically.

Provenance: `abstract_inferred`. Combines eq_2 and eq_4 with F^dagger|psi_j> = |j>; the one-query claim is explicit in the abstract, the deterministic outcome mapping is inferred from the standard algorithm.

Abstract evidence: this work determines the parity of the permutation in only one step of evaluation

Equation assumptions:

- Ideal (noiseless) gates and perfect single-photon detection.

## Registers

- q: 1 ququart (d=4), equivalently 2 qubits (spatial bit, polarization bit) qubits; Carries the Fourier-basis probe state and is acted on by the permutation unitary

## Initial state

|1\rangle = |s=0\rangle|p=1\rangle (then transformed by F to |\psi_1\rangle); equivalently prepare |\psi_1\rangle = \frac{1}{2}(|0\rangle + i|1\rangle - |2\rangle - i|3\rangle) directly.

## Measurement

Measure the ququart in the computational basis (spatial mode and polarization of the single photon). Ideal outcome: k=1 for shift-class ('even') permutations, k=3 for reflection-class ('odd') permutations, each with probability 1.

## Classical postprocessing

Map outcome 1 -> shift class ('even'), outcome 3 -> reflection class ('odd'); outcomes 0 or 2 indicate experimental error. Experimentally, repeat over many photons to estimate outcome probabilities / success rate.

## Algorithm steps

1. Prepare the ququart in |1\rangle and apply the QFT F to obtain the Fourier state |\psi_1\rangle. (eq_1, eq_2)
2. Apply the black-box permutation unitary U_\sigma once (instance: sigma^+_1 shift or sigma^-_0 reflection). (eq_3, eq_4)
3. Apply the inverse QFT F^\dagger to map the resulting Fourier state back to a computational-basis state. (eq_5)

## Assumptions

- No experiment_scope was supplied; the smallest useful instance chosen is d=4 with the 8 dihedral permutations, as this matches the ququart in the abstract and the Gedik-type algorithm.
- The experiment implements the single-qudit Fourier-probe algorithm; the abstract does not spell out the algorithm's equations.
- Bit ordering k = 2s + p and the H/V polarization labelling are conventions chosen here.
- The 'parity' in the abstract is taken to mean the shift-vs-reflection class of the dihedral permutations, which for d=4 differs from S_4 sign parity.

## Missing information

- Exact set of permutations realized in the experiment and which were tested.
- Linear-optical decomposition of F, U_sigma and F^dagger into wave plates, beam splitters and phase elements.
- Single-photon source, detection scheme, and measured success probabilities/fidelities.
- Whether the initial Fourier state was prepared directly or via an explicit QFT stage.
- Basis for the 'strong universality in quantum computation' claim.
