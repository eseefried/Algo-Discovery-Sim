"""Runs inside the sandbox process. Standalone on purpose: it imports nothing from a2m.

usage: python -I harness.py {build|post} candidate.py payload.json out.json

build: candidate.build_circuits(spec) (or build_circuit) -> flattened JSON circuits.
post:  candidate.postprocess(counts_list, spec) for every item of payload["batch"].

Candidates get the black-box oracle only as an opaque placeholder gate, `a2m_task.oracle(k)`.
The trusted parent process substitutes the real oracle, simulates, and scores.
"""

import json
import sys
import traceback
import types


def _flatten(qc):
    from qiskit.circuit.library import get_standard_gate_name_mapping

    std = set(get_standard_gate_name_mapping()) - {"delay"}
    ops, seen = [], set()

    def walk(circ, qmap, cmap, depth):
        if depth > 32:
            raise ValueError("gate definitions nested too deeply")
        for ins in circ.data:
            op = ins.operation
            qs = [qmap[circ.find_bit(q).index] for q in ins.qubits]
            cs = [cmap[circ.find_bit(c).index] for c in ins.clbits]
            seen.add(op.name)
            if op.name == "barrier":
                continue
            if op.name == "oracle":
                ops.append({"name": "oracle", "qubits": qs, "clbits": [], "params": []})
                continue
            if op.name in std:
                ops.append({"name": op.name, "qubits": qs, "clbits": cs,
                            "params": [float(p) for p in op.params]})
                continue
            if op.definition is None:
                raise ValueError(f"unsupported operation without a gate definition: {op.name}")
            walk(op.definition, qs, cs, depth + 1)

    walk(qc, list(range(qc.num_qubits)), list(range(qc.num_clbits)), 0)
    return {"num_qubits": qc.num_qubits, "num_clbits": qc.num_clbits, "ops": ops,
            "operation_names": sorted(seen)}


def _task_module():
    from qiskit.circuit import Gate

    mod = types.ModuleType("a2m_task")

    def oracle(num_qubits):
        """Opaque black-box oracle on `num_qubits` qubits (inputs first, target last)."""
        return Gate("oracle", int(num_qubits), [])

    mod.oracle = oracle
    return mod


def main():
    mode, cand_path, payload_path, out_path = sys.argv[1:5]
    try:
        with open(payload_path) as f:
            payload = json.load(f)
        sys.modules["a2m_task"] = _task_module()
        import importlib.util

        spec = importlib.util.spec_from_file_location("candidate", cand_path)
        cand = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cand)
        if mode == "build":
            from qiskit import QuantumCircuit

            if hasattr(cand, "build_circuits"):
                circs = cand.build_circuits(payload["spec"])
            else:
                circs = cand.build_circuit(payload["spec"])
            if isinstance(circs, QuantumCircuit):
                circs = [circs]
            if not circs or not all(isinstance(c, QuantumCircuit) for c in circs):
                raise TypeError("build must return a QuantumCircuit or a non-empty list of them")
            result = [_flatten(c) for c in circs]
        elif mode == "post":
            result = [cand.postprocess(item, payload["spec"]) for item in payload["batch"]]
        else:
            raise ValueError(mode)
        out = {"ok": True, "result": result}
    except BaseException:  # noqa: BLE001 - report every candidate failure to the parent
        out = {"ok": False, "error": traceback.format_exc(limit=6)[-3000:]}
    with open(out_path, "w") as f:
        json.dump(out, f, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))


if __name__ == "__main__":
    main()
