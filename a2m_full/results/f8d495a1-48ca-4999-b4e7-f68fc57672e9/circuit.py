import math

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import RYGate


def _real(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError("frame_angle must be a finite real number")
    return float(value)


def build_circuit(instance):
    """Trine-POVM Naimark dilation V|psi> = sum_k |k>_pos (x) K_k|psi> on 3 qubits.

    Qubit 0 = pol (input psi), qubits 1,2 = pos (start |00>, outcome k = q1 + 2*q2).
    Instance keys (all optional): povm='trine', frame_angle (float, rotates the trine
    frame about the Bloch y axis), restore_polarisation (bool).
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    if set(instance) - {"povm", "frame_angle", "restore_polarisation"}:
        raise ValueError("unknown instance key")
    if instance.get("povm", "trine") != "trine":
        raise ValueError("only the trine POVM is implemented")
    phi = _real(instance.get("frame_angle", 0.0))
    restore = instance.get("restore_polarisation", True)
    if not isinstance(restore, bool):
        raise ValueError("restore_polarisation must be a bool")

    pol = QuantumRegister(1, "pol")
    pos = QuantumRegister(2, "pos")
    qc = QuantumCircuit(pol, pos)

    # eq_2: frame rotation, <t_k(phi)|psi> = <t_k|ry(-phi)|psi>
    qc.ry(-phi, 0)
    # move psi into the position register (qubit 1); pol becomes |0>
    qc.swap(0, 1)
    # coin-like step: if q1=0 split q2 with cos(t/2)=sqrt(2/3)
    theta = 2.0 * math.atan(1.0 / math.sqrt(2.0))
    qc.cry(theta, 1, 2, ctrl_state=0)
    # Hadamard on the {|10>,|01>} subspace: CX(2->1) CH(1->2) CX(2->1)
    qc.cx(2, 1)
    qc.ch(1, 2)
    qc.cx(2, 1)
    # eq_2 Kraus form: rotate pol to |t_k> conditioned on position k
    if restore:
        for k in range(3):
            qc.append(RYGate(2.0 * k * math.pi / 3.0 + phi).control(2, ctrl_state=k), [1, 2, 0])
    return qc
