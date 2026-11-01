import pytest
from qiskit import QuantumCircuit

from algo_discovery.code_correctness import coherent_permutation_check, weighted_outputs


def test_operator_check_accepts_global_phase_but_rejects_relative_phase():
    circuit = QuantumCircuit(2, global_phase=0.37)
    circuit.cx(0, 1)
    target = [0, 3, 2, 1]
    assert coherent_permutation_check(circuit, target)["passed"]
    circuit.z(0)
    check = coherent_permutation_check(circuit, target)
    assert check["min_basis_success_probability"] == pytest.approx(1)
    assert not check["passed"]


def test_weighted_reference_preserves_data_and_wraps_negative_sum():
    # Accumulator q0,q1; binary data q2. Data=1, accumulator=0 -> accumulator=3.
    outputs = weighted_outputs(2, [2], [0, 1], [-1])
    assert outputs[4] == 7
    assert outputs[5] == 4
    assert outputs[:4] == [0, 1, 2, 3]
