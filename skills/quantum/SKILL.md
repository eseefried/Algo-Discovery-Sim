---
domain: quantum
eval_timeout_s: 120
role_bias: {hypothesize: 1.0, implement: 1.0, simulate: 1.0, critique: 1.0}
colony_genome: {min_families: 3, max_attempts: 3, critiques_required: 1}
roles:
  hypothesize: propose a circuit construction, the register layout it needs, and the
    measurement or amplitude that reads the answer out
  implement: write the circuit builder and any classical post-processing, respecting the
    qubit cap and the query budget
  simulate: run the trusted simulator over the test instances
  critique: look for bit-order mistakes, uncomputation left undone, queries spent beyond the
    budget, and constructions that only work at the sizes or parameters listed
libraries: [qiskit, numpy, math, cmath, time, itertools, functools, collections,
            heapq, random, fractions, statistics, typing, dataclasses]
tools: []
skills:
  - signature: "from a2m_task import oracle; qc.append(oracle(k), qubits)"
    description: The black box as an opaque k-qubit gate. Place it, never inspect it; the
      runner substitutes the real operation afterwards and each placement counts as one query.
  - signature: "qc.append(oracle(k, phase), qubits)"
    description: Where a task says the black box takes a phase, the extra argument is passed
      through to the runner unchanged. It still cannot be inspected, and still counts as one
      query per placement.
---

# Quantum

## Summary
Rebuild a quantum algorithm as circuits that a trusted statevector simulator runs on small
instances, together with whatever classical post-processing reads the answer out.

## Conventions
- **Bit order.** Qiskit is little-endian: in a counts key the last character is classical bit
  0, so `bits[::-1][i]` is the bit you set with `measure(i, i)`. Getting this backwards is the
  single most common way a correct construction scores zero.
- **The qubit cap counts everything**, including ancillas and work registers. A circuit over
  the cap is rejected before it is simulated.
- **The black box is opaque.** It arrives as a placeholder gate with no definition; the runner
  substitutes the real operation for each hidden instance after your circuit is built. You
  cannot read it, differentiate it, or branch on what it contains, and every placement is
  counted as one query against the task's budget. Building the same effect out of ordinary
  gates is not a shortcut, because the runner only substitutes placeholders.
- **Unitary tasks take no measurements.** When a task says the runner reads the statevector or
  the unitary, leave the measurements out; adding them collapses the state and the task fails.
  When a task does ask for counts, measure exactly the bits you need.
- **Ancillas should be returned to |0>.** A task that checks a unitary will fail if work
  qubits stay entangled with the answer, even when the measured bits look right.
- **Global phase is unobservable.** A quantity that ends up only as an overall phase cannot be
  measured; it has to be brought into relative phase or into an ancilla before it can be read.
- **Use Qiskit's standard gate library**, or circuits built from it. An opaque dense unitary,
  `initialize`, or a state-preparation gate that encodes the answer directly is recorded as a
  loophole and scores zero, however well it simulates.
- Resources are measured after unrolling to `u` and `cx`, with the black box excluded, so
  circuit depth and two-qubit count are comparable across different constructions.
