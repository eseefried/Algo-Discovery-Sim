# Examples: abstracts to quantum circuits

These are snapshots from real local runs. Each example includes the full input abstract, the actual model output or generated code, and the recorded execution outcome. This is an illustrative selection, not an aggregate success-rate claim.

**Attribution:** Nemotron is fine-tuned to predict numbered LaTeX equations. Sonnet generates the Qiskit code. In the hybrid swarm, Sonnet also plans, assembles mathematical specifications, and reviews candidates. Raw Nemotron predictions and coordinator corrections are distinguished below.

**Status meanings:** `build_passed` means the code built in the isolated Docker worker; `simulated` means Aer executed it. Independent functional checks below cover the stated small-instance operation. They do not establish full-paper reproduction, asymptotic speedups, or black-box query complexity.

| Example | Configuration | Code / simulation | Independent functional result |
|---|---|---|---|
| Reversible NAND | Native Nemotron → Sonnet/high | Built and simulated | 72/72 basis inputs; full operators checked |
| Affine-function identification | Three-agent hybrid swarm | Built, simulated, and accepted after model review | 28/28 affine functions at n=1,2,3; both coefficients and offset recovered |
| QFT arithmetic abstention | Native Nemotron → Sonnet/high | No code; simulation not run | Not evaluated |

Artifact links point to local, Git-ignored run directories. The abstracts, equations and code included here remain readable without those directories. LaTeX source blocks preserve model text verbatim, including any escaping or mistakes.

## 1. Reversible NAND: executable component, narrower than the paper

**Paper:** Span-program-based quantum algorithm for evaluating formulas (`0710.2630`).

### Input abstract

> We give a quantum algorithm for evaluating formulas over an extended gate set, including all twoand three-bit binary gates (e.g., NAND, 3-majority). The algorithm is optimal on read-once formulas for which each gate's inputs are balanced in a certain sense.
>
> The main new tool is a correspondence between a classical linear-algebraic model of computation, "span programs," and weighted bipartite graphs. A span program's evaluation corresponds to an eigenvalue-zero eigenvector of the associated graph. A quantum computer can therefore evaluate the span program by applying spectral estimation to the graph.
>
> For example, the classical complexity of evaluating the balanced ternary majority formula is unknown, and the natural generalization of randomized alpha-beta pruning is known to be suboptimal. In contrast, our algorithm generalizes the optimal quantum AND-OR formula evaluation algorithm and is optimal for evaluating the balanced ternary majority formula.

### Nemotron equation prediction

```latex
% eq_1 — Nemotron prediction 1
\text{NAND}(x_{0},x_{1}) = x_{0}\oplus\overline{(x_{0}+x_{1})\pmod{2}}. \tag{1}
```

This prediction is incorrect for NAND: at `(x0, x1) = (0, 1)` it gives 0, whereas NAND gives 1. Sonnet explicitly corrected it before generating the circuit.

The implemented operation is:

$$|x_0,x_1,t\rangle \longmapsto |x_0,x_1,t\oplus\neg(x_0\land x_1)\rangle.$$

### Generated Qiskit code

```python
from qiskit import QuantumCircuit


def build_circuit(instance):
    """Return k parallel reversible NAND gates: out_i ^= NOT(x0_i AND x1_i).

    instance: {"num_gates": int in 1..4}. Qubits for gate i: x0=3i, x1=3i+1, out=3i+2.
    """
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    k = instance.get("num_gates", 1)
    if isinstance(k, bool) or not isinstance(k, int):
        raise ValueError("num_gates must be an integer")
    if k < 1 or 3 * k > 12:
        raise ValueError("num_gates must be in 1..4")
    qc = QuantumCircuit(3 * k)
    for i in range(k):
        a = 3 * i
        b = a + 1
        t = a + 2
        # eq_1 (corrected): out ^= 1 XOR (x0 AND x1)
        qc.ccx(a, b, t)
        qc.x(t)
    return qc
```

### Execution and correctness

- **Build:** `build_passed`.
- **Aer:** `simulated`, 1024 shots, seed 42.
- **Saved example instance:** `{"num_gates": 2}`.
- **Observed counts on the all-zero input:** `{"100100": 1024}`.
- **Independent check:** one and two parallel NAND gates passed all 72 basis inputs, with the full unitary compared up to a single global phase. This catches relative-phase errors as well as wrong truth-table outputs.
- **Scope:** this implements a reversible NAND oracle. It does **not** reconstruct the paper's span-program/formula-evaluation algorithm.

[Code artifact](artifacts/nemotron_native_full/results/16408c60-ef3b-4055-9d89-889ca951d5da/result.json) · [Aer report](artifacts/nemotron_native_full/results/16408c60-ef3b-4055-9d89-889ca951d5da/simulation.json) · [Functional checks](artifacts/nemotron_native_full/results/16408c60-ef3b-4055-9d89-889ca951d5da/example_correctness.json)

## 2. Hybrid swarm: recover affine coefficients and offset

**Paper:** A Fast Quantum Algorithm for the Affine Boolean Function Identification (`1407.6402`).

### Input abstract

> Bernstein-Vazirani algorithm (the one-query algorithm) can identify a completely specified linear Boolean function using a single query to the oracle with certainty. The first aim of the paper is to show that if the provided Boolean function is affine, then one more query to the oracle (the two-query algorithm) is required to identify the affinity of the function with certainty. The second aim of the paper is to show that if the provided Boolean function is incompletely defined, then the one-query and the two-query algorithms can be used as bounded-error quantum polynomial algorithms to identify certain classes of incompletely defined linear and affine Boolean functions respectively with probability of success at least $2/3$.

### Mathematical inputs and attribution

The selected candidate was `c002`. It was built, simulated, and accepted by another agent after review. The pilot took **263 seconds** and recorded approximately **$0.31** in estimated paid-model usage.

Nemotron supplied eight equation predictions. The coordinator rejected all eight and assembled four replacement equations from standard background and stated assumptions. **Zero native equations were retained by textual comparison.** This example therefore demonstrates a hybrid-system result, not successful equation recovery by Nemotron alone.

First native prediction (verbatim; rejected):

```latex
\mathcal{F}_{f}:\{0,1\}^{n}\rightarrow\{0,1\}, f\in\{0,1\}^{m},x_{i}=a_{i}y+\epsilon_{i}. \tag{1}
```

Coordinator-assembled equations (verbatim):

```latex
% eq_1 — Affine phase oracle
U_f|x\rangle=(-1)^{a\cdot x\oplus b}|x\rangle,\quad f(x)=a\cdot x\oplus b
% eq_2 — Bernstein-Vazirani step
H^{\otimes n}U_fH^{\otimes n}|0^n\rangle=(-1)^{b}|a\rangle
% eq_3 — Offset readout by controlled phase on |0^n>
(H\otimes I)\,CU_f\,(H\otimes I)|0\rangle_r|0^n\rangle=|b\rangle_r|0^n\rangle
% eq_4 — Final state
|\Psi\rangle=(-1)^{b}|a\rangle_{\mathrm{data}}\otimes|b\rangle_r
```

The intended output on the all-zero input, in the implementation's register order, is:

$$f(x)=a\cdot x\oplus b,\qquad |0^n\rangle_{\mathrm{data}}|0\rangle_{\mathrm{ref}}\longmapsto (-1)^b|a\rangle_{\mathrm{data}}|b\rangle_{\mathrm{ref}}.$$

### Generated Qiskit code

```python
from qiskit import QuantumCircuit, QuantumRegister
import math


def _parse_bits(a, n):
    """Return little-endian bit list of a (int in [0,2^n) or length-n 0/1 sequence)."""
    if isinstance(a, bool):
        raise ValueError('a must be an int or a bit list')
    if isinstance(a, int):
        if a < 0 or a >= 2 ** n:
            raise ValueError('a out of range')
        return [(a >> i) & 1 for i in range(n)]
    if isinstance(a, (list, tuple)):
        if len(a) != n:
            raise ValueError('a must have length n')
        bits = []
        for v in a:
            if isinstance(v, bool) or not isinstance(v, int) or v not in (0, 1):
                raise ValueError('a entries must be 0 or 1')
            bits.append(int(v))
        return bits
    raise ValueError('a must be an int or a bit list')


def build_circuit(instance):
    """Offset readout (controlled phase oracle on |0^n>) then one BV step.
    Data qubits 0..n-1 (little-endian), reference qubit n.
    Ideal map: |0>|0^n> -> (-1)^b |a>_data |b>_ref."""
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = instance.get('n')
    if isinstance(n, bool) or not isinstance(n, int) or n < 1 or n + 1 > 12:
        raise ValueError('n must be an integer with 1 <= n <= 11')
    b = instance.get('b')
    if isinstance(b, bool) or not isinstance(b, int) or b not in (0, 1):
        raise ValueError('b must be 0 or 1')
    bits = _parse_bits(instance.get('a'), n)

    data = QuantumRegister(n, 'data')
    ref = QuantumRegister(1, 'ref')
    qc = QuantumCircuit(data, ref)
    r = n

    # eq_3: offset readout. H on reference, controlled U_f, H on reference.
    qc.h(r)
    # CU_f for f(x)=a.x xor b: CZ(r, q_i) for a_i=1, and Z on r for the offset b (eq_1)
    for i in range(n):
        if bits[i] == 1:
            qc.cz(r, data[i])
    if b == 1:
        qc.z(r)
    qc.h(r)

    # eq_2: Bernstein-Vazirani step H^n U_f H^n on data
    for i in range(n):
        qc.h(data[i])
    # plain U_f (eq_1): Z on q_i for a_i=1, global phase (-1)^b
    for i in range(n):
        if bits[i] == 1:
            qc.z(data[i])
    if b == 1:
        qc.global_phase += math.pi
    for i in range(n):
        qc.h(data[i])
    return qc
```

### Execution and correctness

- **Build:** `build_passed`.
- **Swarm selection:** `ready` after execution and an independent-agent model review.
- **Aer:** the exact selected code was rerun for this example: `simulated`, 1024 shots, seed 42.
- **Example instance:** `{"n": 2, "a": 1, "b": 1}`.
- **Observed counts from the all-zero input:** `{"101": 1024}`. For `n=2`, Qiskit reads this as reference `b=1`, then data bits `a=01`.
- **Independent check:** all 28 combinations of `(a, b)` for `n=1,2,3` returned the expected output with probability 1 within numerical tolerance.
- **Scope:** the oracle is compiled from explicit classical `a` and `b`. Controlled-phase-oracle access is assumed. This does **not** certify the paper's black-box query model, its original construction, or its claims for incompletely defined functions.

[Swarm summary](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/summary.json) · [Native evidence](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/native_evidence.json) · [Code artifact](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/8abdf1a6-7062-47b4-8ada-4b3155188b52/result.json) · [Aer rerun](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/8abdf1a6-7062-47b4-8ada-4b3155188b52/example_simulation.json) · [Functional checks](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/8abdf1a6-7062-47b4-8ada-4b3155188b52/example_correctness.json)

## 3. QFT arithmetic: insufficient-information abstention

**Paper:** Quantum arithmetic with the Quantum Fourier Transform (`1411.5949`).

### Input abstract

> The Quantum Fourier Transform offers an interesting way to perform arithmetic operations on a quantum computer. We review existing Quantum Fourier Transform adders and multipliers and comment some simple variations that extend their capabilities. These modified circuits can perform modular and non-modular arithmetic operations and work with signed integers. Among the operations, we discuss a quantum method to compute the weighted average of a series of inputs in the transform domain. One of the circuits, the controlled weighted sum, can be interpreted as a circuit to compute the inner product of two data vectors.

### Nemotron equation prediction

```latex
% eq_1 — Nemotron prediction 1
\sum_{x=0}^{N-1}a_{x}|x\rangle|y\rangle=\frac{1}{\sqrt{N}}\sum_{k=0}^{N-1}\left(\sum_{x=0}^{N-1}a_{x}e^{2\pi i k x/N}\right)|k\rangle|\tilde{y}_{k}\rangle,\quad(A)\,(B)\,.
```

### Code and simulation status

- **Code generation:** `insufficient_information`; the generated source is empty.
- **Docker validation:** `not_run`.
- **Aer simulation:** not run.
- **Functional correctness:** not evaluated; no circuit exists for this attempt.

**Recorded reason:** Abstained: the only supplied equation is an unverified, malformed model prediction. It has no register layout, input encoding, or algorithm steps, and no experiment scope or validation contract was given. Any circuit would be an invention rather than a reconstruction.

The recorded unresolved issues are:

- The meaning of |y~_k> and its dependence on k is undefined.
- The left and right sides of eq_1 are not equal as written.
- No register sizes, encoding, or choice of operation (adder, multiplier, weighted sum) was specified.
- No experiment scope or validation contract was provided to narrow the construction.

[Code-stage result](artifacts/nemotron-e2e-qft/code-sim/bdac9dec-609e-4d02-976f-9e06246944e8/result.json) · [Pipeline outcome](artifacts/nemotron-e2e-qft/code-sim/bdac9dec-609e-4d02-976f-9e06246944e8/pipeline.json)

## Inspect or reproduce locally

The generated modules above expose `build_circuit(instance)` and contain no measurements. The trusted runner supplies inputs and performs simulation. To rerun a saved code artifact without a model call:

```bash
uv run simulate-qiskit \
  --run-dir artifacts/nemotron_native_full/results/16408c60-ef3b-4055-9d89-889ca951d5da \
  --report /tmp/nand-example-simulation.json
```

This reproduces execution only. The independent functional checks described above are separate from the default no-reference simulation.
