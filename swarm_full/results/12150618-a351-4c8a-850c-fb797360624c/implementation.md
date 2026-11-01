# Equation to Qiskit

Implements the two-qutrit ternary controlled-X (TCX) gate or ternary controlled-Z (TCZ) gate, selected by instance['gate'], with an optional inverse. Each qutrit is stored in 2 qubits as value = q0 + 2*q1, so 4 qubits in total. TCX applies X^c to the target for control value c, built from swap and cx gates and then multi-controlled. TCZ applies the phase omega^(c*t) with multi-controlled phase gates. The unused encoded value 3 is left unchanged.

Source equation run: `d190d913-3de6-425d-9010-1512631c67fb`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubit 0: control qutrit low bit (value = q0 + 2*q1)
- qubit 1: control qutrit high bit
- qubit 2: target qutrit low bit (value = q2 + 2*q3)
- qubit 3: target qutrit high bit
- qutrit values 0,1,2 are valid; encoded value 3 is unused and left unchanged by the gates

## Assumptions

- TCX and TCZ use the standard convention: control value c applies X^c or Z^c to the target.
- X|j> = |j+1 mod 3> and Z|j> = omega^j|j> with omega = exp(2*pi*i/3).
- The control qutrit occupies qubits 0-1 and the target qutrit occupies qubits 2-3.
- The optional 'inverse' flag returns the adjoint circuit.

## Unresolved issues

- The paper's exact gate definitions and conventions are not available from the abstract.
- The Fourier-gate relation (eq_3) is not realized as a circuit.
- Ternary SWAP, Toffoli and Muthukrishnan-Stroud syntheses are not implemented.

## Equation mapping

- `eq_1`: implemented; build_circuit (gate == 'TCX' branch) and _shift_gate. For each control value c in {1,2}, X^c is applied to the target, controlled on the 2-qubit control register in state c. c=0 is the identity.
- `eq_2`: implemented; build_circuit (gate == 'TCZ' branch) and _phase_on_state. The diagonal gate is implemented as phase exp(2*pi*i*c*t/3) on each basis state |c,t>, using X-sandwiched multi-controlled phase gates.
- `eq_3`: background; no code location. The TCX/TCZ equivalence up to target Fourier gates is context only. No Fourier gate is built, and TCX and TCZ are each implemented directly.

## Specification changes

- eq_1, eq_2: Each qutrit is encoded in two qubits (value = q0 + 2*q1). The gates act as the identity on states where either qutrit has encoded value 3. Reason: Qutrits are not native to qubit circuits, so an embedding is required, and the unused level must be handled explicitly.
- eq_3: The relation is not implemented, and its convention is flagged as inconsistent. With F|j> = 3^(-1/2) sum_k omega^(jk)|k>, one gets F Z F^dagger = X^(-1), not X. The correct relation in that convention is TCX = (I (x) F^dagger) TCZ (I (x) F). Reason: Checking the eigenvector relations shows the stated conjugation holds only for the opposite sign convention of F.
- eq_1, eq_2, eq_3: Scope is narrowed to the single two-qutrit TCX or TCZ gate. The SWAP, Toffoli and Muthukrishnan-Stroud syntheses, the Cartan decomposition and the qudit generalization are not implemented. Reason: The abstract and specification give no explicit formulas for these constructions.
