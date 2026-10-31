import json
import os
import shutil
from pathlib import Path

import pytest
from qiskit import QuantumCircuit
from test_circuit_verification import trusted_weighted_sum

from algo_discovery.simulation import simulate

INSTANCE = {"num_target_qubits": 3, "weights": [1, 2]}
ARTIFACT = Path("artifacts/24065ab1-da09-469b-a5c2-2b64107ddd09")


def test_aer_reference_covers_every_basis_input_including_wraparound():
    report = simulate(trusted_weighted_sum(3, [1, 2]), INSTANCE, "modular_weighted_sum", shots=64)
    assert report.status == "reference_passed"
    assert report.cases_run == report.cases_passed == 2**5
    # x=3 (both data bits set), b=7: (7 + 1 + 2) mod 8 = 2 -> state 3 + (2 << 2).
    case = next(c for c in report.cases if c.input == {"x": 3, "b": 7})
    assert case.expected_basis_state == 11
    assert case.counts == {"01011": 64}
    assert case.expected_probability == pytest.approx(1)


def test_wrong_weight_fails_and_records_the_missed_cases():
    report = simulate(trusted_weighted_sum(3, [1, 3]), INSTANCE, "modular_weighted_sum", shots=16)
    assert report.status == "failed"
    assert report.cases_passed == 16  # only inputs with x_1 = 0 are unaffected
    assert not next(c for c in report.cases if c.input == {"x": 2, "b": 0}).passed


def test_no_reference_reports_counts_and_probabilities_only():
    qc = QuantumCircuit(2)
    qc.h(0)
    report = simulate(qc, {}, "none", [{"basis_state": 2}], shots=2000, seed=7)
    assert report.status == "simulated"
    case = report.cases[0]
    assert case.passed is None
    assert case.probabilities == pytest.approx({"10": 0.5, "11": 0.5})
    assert sum(case.counts.values()) == 2000 and set(case.counts) == {"10", "11"}


@pytest.mark.parametrize(
    ("reference", "instance", "inputs"),
    [
        ("modular_weighted_sum", INSTANCE, [{"x": 4, "b": 0}]),
        ("modular_weighted_sum", INSTANCE, [{"basis_state": 0}]),
        ("none", {}, [{"basis_state": 32}]),
        ("none", {}, [{"basis_state": True}]),
        ("none", {}, []),
    ],
)
def test_out_of_range_or_malformed_inputs_are_rejected(reference, instance, inputs):
    with pytest.raises(ValueError):
        simulate(trusted_weighted_sum(3, [1, 2]), instance, reference, inputs)


@pytest.mark.skipif(
    os.environ.get("RUN_DOCKER_TESTS") != "1", reason="Opt-in Docker integration test"
)
def test_cli_simulates_saved_artifact_through_worker(tmp_path, monkeypatch, capsys):
    from algo_discovery.simulation_cli import main

    for name in ("circuit.py", "instance.json"):
        shutil.copy(ARTIFACT / name, tmp_path / name)
    monkeypatch.setattr(
        "sys.argv",
        ["simulate-qiskit", "--run-dir", str(tmp_path), "--reference", "modular_weighted_sum"],
    )
    assert main() == 0
    saved = json.loads((tmp_path / "simulation.json").read_text())
    assert saved["simulation"]["status"] == "reference_passed"
    assert saved["simulation"]["backend"] == "qiskit_aer"
    assert capsys.readouterr().out.startswith("{")
