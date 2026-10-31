import os
import subprocess
from math import pi

import pytest
from qiskit import QuantumCircuit
from qiskit.circuit.library import QFTGate

from algo_discovery.sandbox import validate_in_docker
from algo_discovery.verification import check_weighted_sum


def trusted_weighted_sum(n, weights):
    m = len(weights)
    qc = QuantumCircuit(m + n)
    target = list(range(m, m + n))
    qc.append(QFTGate(n), target)
    for j, weight in enumerate(weights):
        for k in range(n):
            qc.cp(2 * pi * weight / (2 ** (n - k)), j, m + k)
    qc.append(QFTGate(n).inverse(), target)
    return qc


@pytest.mark.parametrize(("n", "weights"), [(3, [1, 2]), (2, [-1, 3]), (1, [0, 2])])
def test_independent_reference_covers_overflow_and_negative_weights(n, weights):
    check = check_weighted_sum(
        trusted_weighted_sum(n, weights), {"num_target_qubits": n, "weights": weights}
    )
    assert check["status"] == "reference_passed"
    assert check["basis_states_checked"] == 2 ** (n + len(weights))
    assert check["superposition_fidelity"] > 1 - 1e-10


def test_basis_measurements_alone_miss_relative_phase_error():
    qc = trusted_weighted_sum(3, [1, 2])
    qc.z(0)
    check = check_weighted_sum(qc, {"num_target_qubits": 3, "weights": [1, 2]})
    assert check["basis_probabilities_passed"]
    assert check["status"] == "failed"
    assert check["full_operator_error"] > 0.1


def test_wrong_bit_order_fails_reference():
    qc = trusted_weighted_sum(3, [1, 2])
    qc.swap(2, 4)
    assert check_weighted_sum(qc, {"num_target_qubits": 3, "weights": [1, 2]})["status"] == "failed"


@pytest.mark.skipif(
    os.environ.get("RUN_DOCKER_TESTS") != "1", reason="Opt-in Docker integration test"
)
def test_actual_container_isolation_and_wire_validation():
    # Trusted probe source intentionally inspects the worker boundary, only inside Docker.
    source = """from qiskit import QuantumCircuit
def build_circuit(instance):
    import os
    assert os.getuid() == 65534
    assert 'CLAUDE_HACKATHON_API' not in os.environ
    assert 'ANTHROPIC_API_KEY' not in os.environ
    assert not os.path.exists('/mnt/zgx1-shared/Algo-Discovery-Sim/.env')
    assert os.statvfs('/').f_flag & os.ST_RDONLY
    return QuantumCircuit(1)
"""
    report, qasm = validate_in_docker(source, {}, "none")
    assert report.status == "build_passed", report.detail
    assert qasm.startswith("OPENQASM 2.0")


@pytest.mark.skipif(
    os.environ.get("RUN_DOCKER_TESTS") != "1", reason="Opt-in Docker integration test"
)
def test_container_timeout_does_not_leave_worker_running(monkeypatch):
    from algo_discovery.sandbox import docker_command

    names = []

    def record_command(name, image_id, directory):
        names.append(name)
        return docker_command(name, image_id, directory)

    monkeypatch.setattr("algo_discovery.sandbox.docker_command", record_command)
    source = "def build_circuit(instance):\n    while True: pass\n"
    report, _ = validate_in_docker(source, {}, "none", timeout=2)
    assert report.status == "failed"
    running = subprocess.run(
        ["docker", "inspect", names[0]],
        capture_output=True,
        text=True,
        check=False,
    )
    assert running.returncode != 0
