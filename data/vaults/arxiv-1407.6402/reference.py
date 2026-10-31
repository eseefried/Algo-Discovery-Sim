"""Reference: the paper's two-query algorithm A1 = U_f H^(n+1) U_f H^(n+1) (Sec. 3.1, Eq. 5-12).
One circuit, two coherent oracle queries, n+1 qubits, success with certainty."""

from qiskit import QuantumCircuit

from a2m_task import oracle


def build_circuits(spec):
    n = spec["n"]
    qc = QuantumCircuit(n + 1, n + 1)
    qc.x(n)                                    # |0>^n |1>
    qc.h(range(n + 1))
    qc.append(oracle(n + 1), range(n + 1))     # query 1: phase (-1)^f(x)
    qc.h(range(n + 1))                         # inputs -> |c>, extra qubit back to |1>
    qc.append(oracle(n + 1), range(n + 1))     # query 2: extra qubit -> 1 xor c_n xor p_c
    qc.measure(range(n + 1), range(n + 1))
    return [qc]


def postprocess(counts_list, spec):
    n = spec["n"]
    counts = counts_list[0]
    bits = max(counts, key=counts.get)[::-1]   # bits[k] is classical bit k
    a = [int(bits[i]) for i in range(n)]
    parity = sum(a) % 2
    return {"a": a, "b": int(bits[n]) ^ 1 ^ parity}
