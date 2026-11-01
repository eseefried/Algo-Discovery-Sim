# Equation to Qiskit

build_circuit compiles an explicit Toffoli network (NOT, CNOT, TOF3, TOF4) on up to 12 little-endian qubits into a measurement-free circuit of x, cx, ccx and mcx gates. It realizes U_pi = G_k...G_1, and it validates the network and computes its quantum cost with the standard cost table (1, 1, 5, 13). The Dijkstra min-QC search over S_16 is not implemented in the circuit module. It would be a classical offline step, and the network it produces is passed in as the instance.

Source equation run: `a76f8a93-96db-4c1f-9130-8f0c466693aa`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0 = bit 0 (least significant) of x
- q1 = bit 1 of x
- q2 = bit 2 of x
- q3 = bit 3 of x (most significant for the 4-bit example)
- Register q has num_qubits qubits (up to 12), little-endian; no ancillas; computational basis |x> maps to |pi(x)>

## Assumptions

- Gate order: gates[0] is applied first.
- Qiskit little-endian ordering: qubit i is bit i of x.
- Standard quantum cost table NOT=CNOT=1, TOF3=5, TOF4=13.
- The example network was chosen as an illustration and is not claimed to be optimal or taken from the paper.

## Unresolved issues

- Internals of the paper's gate-count-optimal tool and its benchmark functions are unknown and not reproduced.
- The paper's exact cost model is not known.
- The offline min-QC search and the 74% saving figure are not reproduced.

## Equation mapping

- `eq_1`: implemented; build_circuit (little-endian register q; comment 'eq_1 / eq_2'). The circuit's unitary is the permutation unitary of the compiled network, with qubit q_i holding bit i. pi is determined by the network and is not given as an explicit table.
- `eq_2`: implemented; build_circuit gate-appending loop. Gates are appended in list order, so gates[0] is G_1 and the total unitary is G_k...G_1.
- `eq_3`: implemented; _gate_cost and the total_cost accumulation / max_qc check in build_circuit. Standard costs 1/1/5/13 are summed over the network. The sum is used only to enforce the optional max_qc bound, and it does not change the circuit.
- `eq_4`: out_of_scope; no code location. The Dijkstra search over the Cayley graph of S_16 is a classical offline optimization and is not a quantum operation. It is infeasible to run inside a generator that must validate and build quickly, so the minimal network must be supplied as input.
- `eq_5`: out_of_scope; no code location. The saving percentage is classical post-processing comparing costs, with no circuit content.

## Specification changes

- eq_4: The circuit module takes an explicit gate network as input instead of searching for a min-QC network for a target permutation. The synthesis step is moved out of the module. Reason: Exact search over S_16 cannot be run within the module (it is a classical computation and the state space is about 2e13), and the module must be a pure operation builder.
- eq_1: pi is not given as an input table. It is defined implicitly by the network, and no check is made that the network equals a particular target permutation. Reason: Without an in-module synthesis step, the target permutation cannot be enforced, and checking it would require simulation.
- eq_1, eq_2, eq_3: The module accepts any number of qubits from 1 to 12, not only 4, and gates have at most 3 controls (NOT, CNOT, TOF3, TOF4). Reason: This keeps the 4-bit library semantics and allows varied valid instances within the 12-qubit cap.
- eq_3: TOF4 is compiled to a single ancilla-free mcx gate, and the quantum cost is the abstract table value, not the cost of the transpiled gates. Reason: The cost model is a library-level quantity, not a Qiskit gate count.
