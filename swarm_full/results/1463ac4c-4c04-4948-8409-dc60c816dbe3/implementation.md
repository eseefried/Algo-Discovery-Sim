# Equation to Qiskit

Abstained: the specification gives no explicit cyclic generator unitary, no gate sequences for the 3- and 4-qubit entanglement classes, and no controlled-phase placement. The only equations are standard background (MUB definition and basis count), so there is no faithful construction to implement. Inventing a generator would not preserve the source's meaning.

Source equation run: `9e12565e-74cf-4dd1-ad6c-4aaebd8f085e`

Generation: **insufficient_information**; validation: **not_run**.

No generated source was executed.

Paper fidelity has not been independently verified.

## Assumptions

- No public validation contract or requested instance was supplied, so there is nothing to narrow the scope to.

## Unresolved issues

- The explicit cyclic generator unitary is not specified.
- The gate sequences for the 3- and 4-qubit entanglement classes are not specified.
- The qubit pairs that receive controlled-phase gates in each basis circuit are not specified.
- The controlled-phase angles are not specified, and it is unclear whether additional single-qubit phase gates are needed.
- Choosing a stabilizer MUB construction, such as symmetric binary matrices with H and phase gates, would be an unsupported substitution for the paper's generator.

## Equation mapping

- `eq_1`: background; no code location. Standard definition of mutual unbiasedness. It is a property that a correct set of basis-change circuits should satisfy, not an operation to build. No circuit is generated.
- `eq_2`: background; no code location. Standard count of 2^n+1 bases in a complete MUB set. It gives the number of bases to generate but does not define the generator circuit, so nothing is implemented.

## Specification changes

