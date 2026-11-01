# Abstract to equations

Status: **partial**

Model: `external:ledger_swarm`

Mathematics has not been independently verified.

Define ternary controlled X (TCX) or controlled Z (TCZ) as a two-qutrit elementary gate that is universal when assisted by arbitrary one-qutrit gates, with one-qutrit elementary gates from Cartan decomposition, and use them to synthesize ternary SWAP, Toffoli and Muthukrishnan-Stroud gates, extended to qudits.

Scope: Small finite qutrit gate-level reconstruction: TCX/TCZ definitions, a qutrit Fourier relation, and an outline of SWAP synthesis. The abstract gives no explicit formulas, so these are standard-background instances rather than the paper's exact constructions.

## Symbols

- $X$: Qutrit shift gate, X|j> = |j+1 mod 3>; domain: 3x3 unitary
- $Z$: Qutrit clock gate, Z|j> = omega^j |j>; domain: 3x3 unitary
- $\omega$: Primitive cube root of unity; domain: complex, e^{2\pi i/3}
- $F$: Qutrit Fourier gate (generalized Hadamard), convention-dependent; domain: 3x3 unitary

## eq_1: TCX gate

$$
TCX=\sum_{c=0}^{2}|c\rangle\langle c|\otimes X^{c}
$$

Control qutrit |c> applies X^c to the target qutrit. This is one standard convention; the paper's exact definition may differ.

Provenance: `standard_background`. The abstract names the TCX gate but gives no formula; this is the standard generalized CNOT form.

Equation assumptions:

- Control value c applies X^c to the target

## eq_2: TCZ gate

$$
TCZ=\sum_{c=0}^{2}|c\rangle\langle c|\otimes Z^{c}
$$

Control qutrit |c> applies Z^c to the target qutrit.

Provenance: `standard_background`. The abstract names the TCZ gate but gives no formula; this is the standard generalized CZ form.

Equation assumptions:

- Control value c applies Z^c to the target

## eq_3: TCX-TCZ relation

$$
TCX=(I\otimes F)\,TCZ\,(I\otimes F^{\dagger})
$$

The two gates are equivalent up to one-qutrit gates on the target, for a Fourier gate F satisfying F Z F^dagger = X.

Provenance: `standard_background`. Consistent with the abstract's claim that TCX or TCZ is universal with arbitrary one-qutrit gates. Exact conventions for F are assumed.

Equation assumptions:

- F satisfies F Z F^dagger = X

## Registers

- a: 1 qutrit qubits; first qutrit, control in TCX/TCZ
- b: 1 qutrit qubits; second qutrit, target in TCX/TCZ

## Initial state

Generic computational-basis input |a,b> with a,b in {0,1,2}; no specific state is given in the abstract.

## Measurement

Not specified in the abstract; assume a computational-basis measurement of both qutrits to verify gate action.

## Classical postprocessing

None specified; none needed beyond reading out the trit values.

## Algorithm steps

1. Apply TCX (or TCZ conjugated by F on the target) as the two-qutrit entangling elementary gate, with a as control and b as target. (eq_1, eq_2, eq_3)
2. Illustrative SWAP synthesis (assumed): interleave TCX gates with control and target roles exchanged, plus one-qutrit gates. The exact sequence is not given in the abstract and is not specified here. (eq_1, eq_3)

## Assumptions

- Standard qutrit Weyl-Heisenberg conventions are used for X, Z and F.
- The SWAP synthesis steps are an assumed illustrative outline, not the paper's circuit.
- The measurement is an assumed generic readout, not from the abstract.
- The measurement is an assumed generic computational-basis readout.

## Missing information

- Explicit gate matrices and the Cartan decomposition details are not in the abstract.
- Synthesis circuits for SWAP, Toffoli and Muthukrishnan-Stroud gates are not given.
- Exact gate sequences and the initial state are not specified in the abstract.
- The physical implementation details are not given.
- The qudit generalization is not formalized.
- The physical implementation details and the qudit generalization are not formalized.
