# Equation to Qiskit

build_circuit(instance) reads an explicit 4-bit permutation pi, runs a classical bucket-based Dijkstra (Dial's algorithm) over S_16 with the 32-gate NOT/CNOT/TOF3/TOF4 library (costs 1/1/5/13) to find a minimum-quantum-cost network, and compiles it to x/cx/ccx/mcx gates on 4 qubits. The circuit is the permutation unitary U_pi: |x> -> |pi(x)>, little-endian, with no ancillas, measurements or state preparation.

Source equation run: `43678126-4368-4799-b3c5-d819f2925e97`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- q0 = bit 0 of x (least significant)
- q1 = bit 1 of x
- q2 = bit 2 of x
- q3 = bit 3 of x (most significant)
- No ancilla qubits; total 4 qubits; basis state |x> maps to |pi(x)> (little-endian)

## Assumptions

- Gate costs are NOT=CNOT=1, TOF3=5, TOF4=13 (convention).
- Little-endian encoding: qubit i holds bit i of x.
- The search is a stand-in for the paper's gate-count-optimal tool.
- Minimality holds only within the 32-gate library and within the max_cost bound.
- The search is classical preprocessing at build time. Larger-cost permutations may be slow because the reachable state count grows quickly, so small max_cost and low-cost pi are intended.

## Unresolved issues

- The internals of the paper's optimal synthesis tool and its exact cost model are unknown.
- The paper's benchmarks and the 74% saving claim are not reproduced.
- Runtime of the in-builder search for high-cost permutations is not guaranteed to be small.

## Equation mapping

- `eq_1`: implemented; _gate_library. Each of the 32 NOT/CNOT/TOF3/TOF4 placements is defined as a permutation of {0..15} that flips the target bit when all controls are 1.
- `eq_2`: implemented; build_circuit (gate compilation loop, G_1 appended first). The network found for pi is compiled to x/cx/ccx/mcx in order, giving U_pi = G_k...G_1 with little-endian qubit indexing.
- `eq_3`: implemented; _gate_library (cost field) and _search (edge weights). Costs 1/1/5/13 are used as Dijkstra edge weights, so the total network cost is additive.
- `eq_4`: implemented; _search. Dial's bucket-queue Dijkstra from the identity with relaxation sigma' = g o sigma, stopping when pi is settled and recovering the network via predecessor links. It is pruned at max_cost.
- `eq_5`: out_of_scope; no code location. The saving percentage compares against a baseline network and is classical post-processing that is not part of the circuit. No baseline is accepted.

## Specification changes

- eq_4: Added a required-bounded search parameter max_cost (default 13, at most 16). The search is pruned at that cost and raises ValueError if pi is not reachable within it. Dijkstra uses an integer bucket queue (Dial's algorithm) rather than a heap. Reason: The full S_16 space is infeasible to enumerate, and heapq is not an allowed import. Costs are small integers, so buckets are exact.
- eq_5: The saving percentage and the optional baseline network input are dropped from the implementation. Reason: They are not part of the unitary operation, and the builder must return only a circuit.
- eq_1: The rejected majority-like Toffoli expression is not used. The Toffoli map is c XOR ab (and d XOR abc for TOF4). Reason: Consistent with the specification's correction.
