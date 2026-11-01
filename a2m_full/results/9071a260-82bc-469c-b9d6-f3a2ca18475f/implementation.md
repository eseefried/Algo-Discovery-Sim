# Equation to Qiskit

Builds the first-order Lie-Trotter product (e^{-i dt|w><w|} e^{-i dt|s><s|})^m for Grover's Hamiltonian H=|w><w|+|s><s|, on n search qubits and with no ancilla. Each projector phase factor is an exact multi-controlled phase gate, so any dt is allowed. At dt=pi each factor is an exact reflection and one step is the Grover iterate. Input-state preparation and measurement are left to the runner.

Source equation run: `fcde32b7-66cc-4b73-8835-bba35e90bf9f`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- qubits 0..n-1: 'search' register, little-endian computational basis (qubit i = bit i of the basis-state integer)
- marked item w is the integer 'marked'; its bit i corresponds to qubit i
- no ancilla qubits; total qubits = n <= 6
- example: n=3, qubits 0,1,2; marked=5 is |101> (q2=1,q1=0,q0=1)

## Assumptions

- Marked item w is a single computational-basis integer, with bit i on qubit i (little endian)
- Initial state |s> is prepared by the runner, not by this circuit
- The Hamiltonian normalisation is exactly H=|w><w|+|s><s|, as in eq_1
- In each step the |s> factor is applied before the |w> factor, following the operator product order in eq_2
- Multi-controlled phases use qc.mcp without ancilla, which is fine for n<=6

## Unresolved issues

- The paper's exact Hamiltonian normalisation and evolution time are unknown
- The fixed-point or generalised-reflection scheme for logarithmic error scaling is not implemented
- The Trotter error exponent p and constant C in eq_5 are not given in the abstract

## Equation mapping

- `eq_1`: background; no code location. Defines the two projectors in H whose evolution factors are used. The exact e^{-iHT} is not built; only the product formula of eq_2 is.
- `eq_2`: implemented; build_circuit loop over steps, with _s_factor and _w_factor. Implements (e^{-i dt|w><w|} e^{-i dt|s><s|})^m. The s factor acts first, since it is the rightmost operator. dt and m are given independently in the instance.
- `eq_3`: implemented; _w_factor and _s_factor with dt=pi. At dt=pi the factors are exactly I-2|w><w| and I-2|s><s|, so one step is the Grover iterate up to a global sign. No special code path is used; it is the dt=pi case of the same construction.
- `eq_4`: background; no code location. Analytic success probability sin^2((2k+1)theta), used for choosing k and for post-hoc analysis. It is not part of the operation.
- `eq_5`: out_of_scope; no code location. Power-law error fit of the Trotter arm is classical post-processing of simulation results, not a circuit.

## Specification changes

- eq_2, eq_3: The oracle is not a black box. e^{-i dt|w><w|} is built explicitly from X gates on the zero bits of w and a multi-controlled phase of angle -dt. No ancilla is used. Reason: The spec left the non-pi oracle rotation unspecified. An explicit marked-state phase gate resolves this, and the dt=pi case reproduces the standard phase oracle exactly.
- eq_2, eq_3: The circuit contains the evolution operation only, with a single scope: the Trotter product with free dt and m. Separate Arm A and Arm B circuits, |s> preparation and measurement are dropped. The Grover arm is the dt=pi case. Reason: The task requires an operation without state preparation or measurement, and a single construction.
- eq_1, eq_2: Total time T=m*dt is not an input. dt and steps are given independently, and any real dt is accepted. Reason: This simplifies the interface and covers both the dt=T/m Trotter regime and the maximal-step regime.
- eq_5: The fixed-point/recursive scheme and the exponential-error-control construction are excluded. Reason: The phase schedule is not specified in the abstract and is not invented here.
- eq_1: The search register size is restricted to n in 3..6, and steps to at most 200. Reason: This keeps the circuit well under the 12-qubit cap and follows the specified domain of n.
