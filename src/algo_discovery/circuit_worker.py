"""Trusted worker entrypoint. Executed only inside the restricted Docker container."""

import importlib.util
import json

import qiskit
from qiskit import QuantumCircuit, transpile
from qiskit.circuit import Gate


def main():
    try:
        with open("/input/instance.json") as handle:
            instance = json.load(handle)
        spec = importlib.util.spec_from_file_location("generated_circuit", "/input/circuit.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        circuit = module.build_circuit(instance)
        if not isinstance(circuit, QuantumCircuit):
            raise TypeError("build_circuit did not return QuantumCircuit.")
        if not 1 <= circuit.num_qubits <= 12 or len(circuit.data) > 20000:
            raise ValueError("Circuit exceeds size limits.")
        if circuit.num_clbits or circuit.parameters:
            raise ValueError("Circuit must be bound and have no classical bits.")
        if any(not isinstance(item.operation, Gate) for item in circuit.data):
            raise ValueError("Only unitary gate operations are supported in this block.")
        compiled = transpile(
            circuit, basis_gates=["u", "cx"], optimization_level=0, seed_transpiler=42
        )
        if len(compiled.data) > 50000:
            raise ValueError("Transpiled circuit exceeds the gate limit.")
        output = {
            "ok": True,
            "qiskit_version": qiskit.__version__,
            "num_qubits": compiled.num_qubits,
            "global_phase": float(compiled.global_phase),
            "gates": [
                {
                    "name": item.operation.name,
                    "params": [float(value) for value in item.operation.params],
                    "qubits": [compiled.find_bit(q).index for q in item.qubits],
                }
                for item in compiled.data
            ],
        }
    except Exception as exc:  # noqa: BLE001 - isolate arbitrary generated-code failures.
        output = {"ok": False, "error": type(exc).__name__ + ": " + str(exc)[:1000]}
    print(json.dumps(output, allow_nan=False))


if __name__ == "__main__":
    main()
