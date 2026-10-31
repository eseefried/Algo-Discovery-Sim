# Equation to Qiskit

Implements the scoped construction: a Toffoli network G=(g_1,...,g_L) of positive-control MCT gates T(C;t) on n<=12 wires (paper setting n=4) applied in order to realize a reversible function as a permutation, with the additive quantum-cost and gate-count metrics attached as metadata. The GC/QC search tool, benchmark set and savings computation are out of scope; the example instance is the tiny target f_0 = T({1,2,3};4) of eq_7.

Source equation run: `14fbc71a-f922-4335-838f-664ad16f0752`

Generation: **generated**; validation: **build_passed**.

Circuit built and transpiled successfully; no independent correctness reference selected.

Paper fidelity has not been independently verified.

## Register layout

- Register x of n=4 qubits; wire i of the specification is mapped to Qiskit qubit n - i so the truth-table label x = sum_i x_i 2^(4-i) equals Qiskit's little-endian basis index.
- qubit 3 = wire 1 = x_1 (top line, most significant bit)
- qubit 2 = wire 2 = x_2
- qubit 1 = wire 3 = x_3
- qubit 0 = wire 4 = x_4 (target of the example gate, least significant bit)
- Example circuit: single 3-control Toffoli with controls on qubits [3,2,1] and target qubit 0, realizing |x1 x2 x3 x4> -> |x1 x2 x3 (x4 xor x1 x2 x3)>; metadata gate_count=1, quantum_cost=13.

## Assumptions

- Positive-control MCT library only; no ancilla lines (n equals the number of function variables).
- Quantum-cost table NOT/CNOT=1, Toffoli=5, 3-control Toffoli=13 is assumed and may differ from the paper's metric.
- qc.mcx with >=3 controls is left to Qiskit's standard MCX gate; its internal decomposition is irrelevant to the realized permutation but is not the cost model of eq_4.
- The example instance f_0=T({1,2,3};4) is a chosen tiny target, not a benchmark from the paper.
- An empty gate list is accepted and yields the identity network (GC=QC=0).

## Unresolved issues

- The GC-optimal synthesis tool's algorithm and its adaptation to QC minimization are unspecified, so no optimization is performed.
- The paper's exact QC cost model (negative controls, free-line discounts) and benchmark circuits achieving up to 74% savings are unknown.

## Equation mapping

- `eq_1`: background; no code location. The target as a bijection/permutation of {0,1}^n is the semantic model the circuit realizes; the module takes a gate list as input rather than a permutation, so no explicit permutation data structure is built.
- `eq_2`: implemented; _apply_mct. Each MCT gate T(C;t) is realized by x / cx / ccx / mcx on the mapped qubits, flipping the target iff all controls are 1.
- `eq_3`: implemented; build_circuit (gate loop) and metadata 'gate_count'. The circuit is the sequential composition g_L o ... o g_1 with g_1 appended first; GC(G)=L is recorded. The minimization GC^*(f) itself is not performed.
- `eq_4`: implemented; gate_quantum_cost, quantum_cost. Additive quantum cost with the assumed table NOT/CNOT=1, Toffoli=5, 3-control=13 (generalized as 2^(k+1)-3 for k>=1 controls), stored in qc.metadata.
- `eq_5`: out_of_scope; no code location. The QC-minimizing search over realizing networks (and the GC-optimal synthesis tool) is not specified in the abstract and is not implemented; the module only builds and costs a supplied network.
- `eq_6`: out_of_scope; no code location. Relative savings against previously known circuits require benchmark circuits not given in the abstract; this is classical post-processing outside the circuit operation.
- `eq_7`: implemented; example_instance_json / build_circuit docstring. The example instance is exactly f_0 = T({1,2,3};4), a one-gate network with GC=1 and QC=13 under the assumed table.

## Specification changes

- eq_1, eq_3: The module input is an explicit MCT gate list rather than a target permutation f; realization of f is by construction of the supplied network, and GC^* minimization is not performed. Reason: The synthesis/search algorithm of the GC-optimal tool is missing from the abstract; building and costing a given Toffoli network is the only fully specified construction.
- eq_4: Per-gate cost for k>=4 controls is extrapolated as 2^(k+1)-3 (matching the assumed 1/5/13 values for k=1,2,3); NOT costs 1. Reason: The module accepts n up to 12 wires for generality, so gates with more than 3 controls can occur; the paper's table beyond 4 bits is unknown.
- eq_2: Wire i is mapped to Qiskit qubit n-i (wire 1 = most significant qubit). Reason: Specification labels wire 1 as the MSB of the truth-table index while Qiskit qubit 0 is the least significant bit; the mapping keeps truth-table row labels consistent with Qiskit basis indices.
