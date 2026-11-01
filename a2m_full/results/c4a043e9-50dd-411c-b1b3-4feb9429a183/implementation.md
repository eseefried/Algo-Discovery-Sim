# Equation to Qiskit

Measurement-free circuit for r second-order Trotter steps of e^{-iHT} for the search Hamiltonian H=-gamma*A-|w><w|. A is the hypercube adjacency, the sum of X_i on n qubits. Each step is an RX(-gamma*dt) layer, a phase e^{i dt} on the marked basis state |w>, then another RX(-gamma*dt) layer. The marked-state phase uses X conjugation and a multi-controlled phase gate, so no ancilla is needed. State preparation (Hadamards) and readout are left to the runner.

Source equation run: `ab10ddc0-e9fd-4274-a87b-46b23f5972c8`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Qubits 0..n-1: vertex register 'v', little-endian: qubit i holds bit i of vertex index x (qubit 0 is least significant).
- Marked vertex w is an integer; bit i of w is the target value on qubit i.
- No ancilla qubit. Total qubits = n (<= 12).

## Assumptions

- Hypercube adjacency A=sum_i X_i with zero self-loop weights stands in for the paper's graphs.
- The sign convention is U=e^{-iHT} with H=-gamma*A-|w><w|, so the hopping layers are RX(-gamma*dt) and the marked phase is +dt.
- The example gamma=0.3 and T near pi*sqrt(8)/2 are illustrative, not verified optimal.
- The marked vertex is given as an integer with little-endian bit order.
- Steps are capped at 500 to bound circuit size.

## Unresolved issues

- The paper's actual graphs, loop weights, and critical gamma are not reconstructed.
- The diagrammatic perturbation-theory method and the growing-dimension subspace argument are not implemented.
- Optimal gamma and T and the Trotter error are left to numerical scanning by the runner.

## Equation mapping

- `eq_1`: background; no code location. Target Hamiltonian H=-gamma*A-|w><w|. It is not applied directly; it is approximated by the product formula in eq_3. Self-loop weights are zero.
- `eq_2`: implemented; _marked_phase. The oracle factor e^{i dt |w><w|} is a phase e^{i dt} on |w>. It is built from X gates on the zero bits of w and a multi-controlled phase gate, so it needs no controlled oracle or ancilla. The global-phase decomposition is not used.
- `eq_3`: implemented; _hop_half and build_circuit loop. Each Trotter step is RX(-gamma*dt) on every qubit, then the marked-state phase, then RX(-gamma*dt) on every qubit, repeated r times with dt=T/r.
- `eq_4`: out_of_scope; no code location. Preparing |s> with Hadamards is an input-state preparation, which the runner does. The circuit is only the evolution operation.
- `eq_5`: out_of_scope; no code location. Success probability is a measurement and post-processing quantity. The circuit has no measurements.

## Specification changes

- eq_2: The oracle step is a direct multi-controlled phase gate on the known marked string, not a controlled-O_w call with an ancilla. The circuit uses n qubits, not n+1. Reason: No opaque oracle is supplied and the marked string is a parameter. The direct gate gives exactly e^{i dt |w><w|} without a controlled oracle or a global-phase correction.
- eq_4, eq_5: Initial-state preparation and readout are excluded from the circuit. Reason: The task requires an operation only, with inputs prepared and outputs read by the runner.
- eq_1, eq_3: Scope is the hypercube with zero loop weights, and n is allowed from 2 to 12, wider than the specification's 2 or 3. gamma, T, steps and the marked vertex are instance parameters. Reason: The paper's weighted self-loop graphs and diagrammatic method are not reconstructable from the abstract.
