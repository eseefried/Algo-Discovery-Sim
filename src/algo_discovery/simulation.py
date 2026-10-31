"""Host-side simulation of circuits reconstructed from worker gate data.

Generated Python is never imported here: the input is the trusted circuit that
verification.circuit_from_wire rebuilt from bounded elementary gates.
"""

from typing import Literal, Protocol

from pydantic import Field
from qiskit import QuantumCircuit

from .code_schemas import Reference
from .schemas import StrictModel
from .verification import WeightedSumInstance

MAX_CASES = 256
MAX_SHOTS = 100_000
PROBABILITY_FLOOR = 1e-12


class BackendRun(StrictModel):
    counts: dict[int, int]
    probabilities: dict[int, float]


class SimulationBackend(Protocol):
    """Interface for simulators; Aer is the first implementation, EQO can follow."""

    name: str
    version: str
    method: str

    def run(self, circuit: QuantumCircuit, shots: int, seed: int) -> BackendRun: ...


class AerBackend:
    name = "qiskit_aer"
    method = "statevector"

    def __init__(self):
        import qiskit_aer

        self.version = qiskit_aer.__version__

    def run(self, circuit: QuantumCircuit, shots: int, seed: int) -> BackendRun:
        from qiskit import transpile
        from qiskit_aer import AerSimulator

        measured = circuit.copy()
        measured.save_probabilities_dict(label="probabilities")
        measured.measure_all()
        simulator = AerSimulator(method=self.method, seed_simulator=seed, max_parallel_threads=1)
        compiled = transpile(measured, simulator, optimization_level=0, seed_transpiler=seed)
        result = simulator.run(compiled, shots=shots).result()
        if not result.success:
            raise ValueError("Aer simulation did not succeed.")
        return BackendRun(
            counts={int(key, 2): value for key, value in result.get_counts().items()},
            probabilities={
                int(key): float(value)
                for key, value in result.data(0)["probabilities"].items()
                if value > PROBABILITY_FLOOR
            },
        )


class SimulationCase(StrictModel):
    input: dict[str, int]
    initial_basis_state: int
    counts: dict[str, int]
    probabilities: dict[str, float]
    expected_basis_state: int | None = None
    expected_probability: float | None = None
    passed: bool | None = None


class SimulationReport(StrictModel):
    status: Literal["simulated", "reference_passed", "failed", "unavailable"]
    detail: str
    reference: Reference = "none"
    backend: str | None = None
    backend_version: str | None = None
    method: str | None = None
    shots: int = 0
    seed: int = 0
    num_qubits: int | None = None
    cases_run: int = 0
    cases_passed: int = 0
    cases: list[SimulationCase] = Field(default_factory=list)
    paper_fidelity_verified: Literal[False] = False


def bitstring(state: int, num_qubits: int) -> str:
    """Qiskit display order: qubit 0 is the rightmost character."""
    return format(state, f"0{num_qubits}b")


def default_inputs(reference: Reference, instance: dict) -> list[dict[str, int]]:
    if reference == "modular_weighted_sum":
        spec = WeightedSumInstance.model_validate(instance)
        m, n = len(spec.weights), spec.num_target_qubits
        return [{"x": x, "b": b} for b in range(2**n) for x in range(2**m)]
    return [{"basis_state": 0}]


def resolve_input(
    case: dict, reference: Reference, instance: dict, num_qubits: int
) -> tuple[int, int | None]:
    """Return (initial basis state, expected output basis state or None)."""
    if any(type(value) is not int for value in case.values()):
        raise ValueError("Input values must be integers.")
    if reference == "modular_weighted_sum":
        spec = WeightedSumInstance.model_validate(instance)
        m, n = len(spec.weights), spec.num_target_qubits
        if set(case) != {"x", "b"}:
            raise ValueError("Weighted-sum inputs need exactly 'x' and 'b'.")
        x, b = case["x"], case["b"]
        if not 0 <= x < 2**m or not 0 <= b < 2**n:
            raise ValueError("Weighted-sum input is outside the register range.")
        result = (b + sum(w * ((x >> j) & 1) for j, w in enumerate(spec.weights))) % (2**n)
        return x + (b << m), x + (result << m)
    if set(case) != {"basis_state"}:
        raise ValueError("Inputs without a reference need exactly 'basis_state'.")
    state = case["basis_state"]
    if not 0 <= state < 2**num_qubits:
        raise ValueError("Basis state is outside the circuit's qubit range.")
    return state, None


def prepare(circuit: QuantumCircuit, basis_state: int) -> QuantumCircuit:
    prepared = QuantumCircuit(circuit.num_qubits)
    for qubit in range(circuit.num_qubits):
        if (basis_state >> qubit) & 1:
            prepared.x(qubit)
    return prepared.compose(circuit)


def simulate(
    circuit: QuantumCircuit,
    instance: dict,
    reference: Reference,
    inputs: list[dict] | None = None,
    *,
    backend: SimulationBackend | None = None,
    shots: int = 1024,
    seed: int = 42,
) -> SimulationReport:
    if not 1 <= shots <= MAX_SHOTS:
        raise ValueError(f"Shots must be between 1 and {MAX_SHOTS}.")
    inputs = default_inputs(reference, instance) if inputs is None else inputs
    if not 1 <= len(inputs) <= MAX_CASES:
        raise ValueError(f"Provide between 1 and {MAX_CASES} inputs.")
    if reference == "modular_weighted_sum":
        spec = WeightedSumInstance.model_validate(instance)
        if circuit.num_qubits != len(spec.weights) + spec.num_target_qubits:
            raise ValueError("Circuit qubit count does not match the public reference layout.")
    backend = backend or AerBackend()
    n = circuit.num_qubits
    cases = []
    for index, case in enumerate(inputs):
        if not isinstance(case, dict):
            raise ValueError("Each input must be a JSON object.")  # noqa: TRY004 - CLI input error.
        initial, expected = resolve_input(case, reference, instance, n)
        run = backend.run(prepare(circuit, initial), shots, seed + index)
        fields = {
            "input": case,
            "initial_basis_state": initial,
            "counts": {bitstring(k, n): v for k, v in sorted(run.counts.items())},
            "probabilities": {bitstring(k, n): p for k, p in sorted(run.probabilities.items())},
        }
        if expected is not None:
            probability = run.probabilities.get(expected, 0.0)
            fields |= {
                "expected_basis_state": expected,
                "expected_probability": probability,
                "passed": probability > 1 - 1e-8 and run.counts.get(expected, 0) == shots,
            }
        cases.append(SimulationCase.model_validate(fields))
    passed = sum(1 for case in cases if case.passed)
    if reference == "none":
        status, detail = (
            "simulated",
            "Simulated basis-state inputs; no correctness reference selected.",
        )
    elif passed == len(cases):
        status = "reference_passed"
        detail = "Every simulated basis input produced the reference output with certainty. "
        detail += (
            "Basis inputs do not test relative phases; use validate-qiskit for the full operator."
        )
    else:
        status, detail = (
            "failed",
            f"{len(cases) - passed} of {len(cases)} inputs missed the reference output.",
        )
    return SimulationReport(
        status=status,
        detail=detail,
        reference=reference,
        backend=backend.name,
        backend_version=backend.version,
        method=backend.method,
        shots=shots,
        seed=seed,
        num_qubits=n,
        cases_run=len(cases),
        cases_passed=passed,
        cases=cases,
    )
