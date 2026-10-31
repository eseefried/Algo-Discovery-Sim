"""Trusted-side reconstruction of flattened circuits, oracle substitution, resource stats."""

from __future__ import annotations

from qiskit import QuantumCircuit, transpile
from qiskit.circuit.library import get_standard_gate_name_mapping

_STD = get_standard_gate_name_mapping()
OPAQUE_SHORTCUTS = {"unitary", "isometry", "initialize", "state_preparation", "hamiltonian"}


def load(d: dict, oracle=None) -> QuantumCircuit:
    """Rebuild a circuit, substituting the real black box for every `oracle` placeholder.

    `oracle` is either a QuantumCircuit or a callable taking the placeholder's parameters and
    returning one, which is how a phase-tunable black box is supplied. With `oracle=None` the
    placeholders are dropped, which is what resource counting uses."""
    qc = QuantumCircuit(int(d["num_qubits"]), int(d["num_clbits"]))
    for op in d["ops"]:
        name, qs, cs = op["name"], op["qubits"], op["clbits"]
        if name == "oracle":
            if oracle is None:
                continue
            sub = oracle(*op.get("params", [])) if callable(oracle) else oracle
            if len(qs) != sub.num_qubits:
                raise ValueError(f"oracle expects {sub.num_qubits} qubits, got {len(qs)}")
            qc.compose(sub, qubits=qs, inplace=True)
        elif name == "measure":
            qc.measure(qs[0], cs[0])
        elif name in _STD:
            gate = _STD[name].to_mutable()
            if op["params"]:
                gate.params = list(op["params"])
            qc.append(gate, qs, cs)
        else:
            raise ValueError(f"unknown operation {name}")
    return qc


def stats(circuits: list[dict]) -> dict:
    """Resource metrics with the oracle excluded, after unrolling to {u, cx}."""
    out = {"num_circuits": len(circuits), "num_qubits": 0, "oracle_queries": 0,
           "two_qubit_gates": 0, "depth": 0, "opaque_shortcuts": []}
    for d in circuits:
        out["num_qubits"] = max(out["num_qubits"], int(d["num_qubits"]))
        out["oracle_queries"] += sum(op["name"] == "oracle" for op in d["ops"])
        bare = load(d).remove_final_measurements(inplace=False)
        unrolled = transpile(bare, basis_gates=["u", "cx"], optimization_level=0)
        out["two_qubit_gates"] += int(unrolled.count_ops().get("cx", 0))
        out["depth"] = max(out["depth"], unrolled.depth())
        out["opaque_shortcuts"] += sorted(OPAQUE_SHORTCUTS & set(d.get("operation_names", [])))
    out["opaque_shortcuts"] = sorted(set(out["opaque_shortcuts"]))
    return out
