"""Independent host-side references. No generated Python is imported here."""

import math

import numpy as np
from pydantic import Field, model_validator
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator

from .code_schemas import CircuitValidation
from .schemas import StrictModel


class WeightedSumInstance(StrictModel):
    num_target_qubits: int = Field(ge=1, le=4, strict=True)
    weights: list[int] = Field(min_length=1, max_length=4)

    @model_validator(mode="before")
    @classmethod
    def strict_weights(cls, data):
        if isinstance(data, dict) and any(type(w) is not int for w in data.get("weights", [])):
            raise ValueError("Weights must be integers.")
        return data

    @model_validator(mode="after")
    def cap(self):
        if len(self.weights) + self.num_target_qubits > 8:
            raise ValueError("Full-operator reference is limited to 8 total qubits.")
        if any(abs(w) > 2**20 for w in self.weights):
            raise ValueError("Weight magnitude exceeds the reference limit.")
        return self


def circuit_from_wire(wire: dict) -> QuantumCircuit:
    """Decode bounded elementary gate data, never generated source or serialized objects."""
    n = wire["num_qubits"]
    if type(n) is not int or not 1 <= n <= 12 or len(wire["gates"]) > 50000:
        raise ValueError("Worker circuit exceeds limits.")
    phase = float(wire["global_phase"])
    if not math.isfinite(phase):
        raise ValueError("Invalid global phase.")
    circuit = QuantumCircuit(n, global_phase=phase)
    for gate in wire["gates"]:
        name, qubits, params = gate["name"], gate["qubits"], gate["params"]
        if any(type(q) is not int or not 0 <= q < n for q in qubits):
            raise ValueError("Invalid gate qubits.")
        if len(set(qubits)) != len(qubits) or not all(math.isfinite(float(p)) for p in params):
            raise ValueError("Invalid gate parameters.")
        if name == "u" and len(qubits) == 1 and len(params) == 3:
            circuit.u(*map(float, params), qubits[0])
        elif name == "cx" and len(qubits) == 2 and not params:
            circuit.cx(*qubits)
        else:
            raise ValueError("Worker output contains a non-elementary gate.")
    return circuit


def check_weighted_sum(circuit: QuantumCircuit, instance: dict) -> dict:
    spec = WeightedSumInstance.model_validate(instance)
    m, n = len(spec.weights), spec.num_target_qubits
    if circuit.num_qubits != m + n:
        raise ValueError("Circuit qubit count does not match the public reference layout.")
    if len(circuit.data) > 2000:
        raise ValueError("Full-operator checks are limited to 2,000 elementary gates.")
    dimension = 2 ** (m + n)
    reference = np.zeros((dimension, dimension), dtype=complex)
    for basis in range(dimension):
        x, b = basis % (2**m), basis >> m
        result = (b + sum(w * ((x >> j) & 1) for j, w in enumerate(spec.weights))) % (2**n)
        reference[x + (result << m), basis] = 1
    actual = Operator(circuit).data
    basis_passed = bool(np.allclose(np.abs(actual) ** 2, np.abs(reference) ** 2, atol=1e-8, rtol=0))
    overlap = np.vdot(reference, actual)
    phase = overlap / abs(overlap) if abs(overlap) > 1e-12 else 1
    error = float(np.max(np.abs(actual - phase * reference)))
    rng = np.random.default_rng(42)
    state = rng.normal(size=dimension) + 1j * rng.normal(size=dimension)
    state /= np.linalg.norm(state)
    fidelity = float(abs(np.vdot(reference @ state, actual @ state)) ** 2)
    passed = basis_passed and error < 1e-8 and fidelity > 1 - 1e-8
    return {
        "status": "reference_passed" if passed else "failed",
        "detail": "Compared all basis states and the full unitary up to a single global phase; "
        + "also checked a seeded complex superposition. This checks the scoped operation, not paper fidelity.",
        "basis_states_checked": dimension,
        "basis_probabilities_passed": basis_passed,
        "full_operator_error": error,
        "superposition_fidelity": fidelity,
    }


def assess_wire(
    wire: dict, instance: dict, reference: str, image_id: str
) -> tuple[CircuitValidation, str]:
    from qiskit import qasm2

    circuit = circuit_from_wire(wire)
    fields = {
        "status": "build_passed",
        "detail": "Circuit built and transpiled successfully; no independent correctness reference selected.",
        "reference": reference,
        "worker_image_id": image_id,
        "qiskit_version": wire["qiskit_version"],
        "num_qubits": circuit.num_qubits,
        "gate_count": len(circuit.data),
        "depth": circuit.depth(),
    }
    if reference == "modular_weighted_sum":
        fields.update(check_weighted_sum(circuit, instance))
    return CircuitValidation.model_validate(fields), qasm2.dumps(circuit)
