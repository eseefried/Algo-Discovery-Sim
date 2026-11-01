# Examples from the hybrid swarm

**Every example below comes from your three-agent hybrid swarm.** There are no single-attempt Nemotron baseline examples in this file. The snapshots cover three candidates from two completed swarm runs; examples 1 and 2 belong to the same affine-function pilot.

Nemotron proposes numbered LaTeX equations. Sonnet coordinates method plans, assembles mathematical specifications, generates Qiskit code, and reviews candidates. The raw native equations and coordinator additions are stored separately. These are hybrid-system outputs, not code written by the fine-tuned Nemotron model.

| Example | Swarm run | Candidate | Docker / Aer | Swarm decision |
|---|---|---|---|---|
| Affine identification, selected | Corrected three-agent pilot | `c002` | Built and simulated | `ready` |
| Affine identification, earlier attempt | Same pilot | `c001` | Built and simulated | Returned for revision |
| Order finding with gate errors | 65-paper swarm, paper `0704.0516` | `c003` | Built and simulated | Returned for revision; run ended without a reviewed candidate |

`simulated` means the unitary executed in Aer. `ready` additionally means a different agent approved its stated scope. Neither status proves full-paper reproduction or oracle-query complexity. The independent numerical checks cited below cover only their documented inputs and small sizes. Reviewer objections are model judgments unless explicitly marked as reproduced counterexamples.

Code and mathematical inputs are copied from actual saved swarm artifacts. LaTeX blocks preserve model text, including escaping and mistakes. Artifact links are local evidence under Git-ignored run directories; the full abstracts and generated code are included here so the examples are self-contained.

## 1. Selected affine-identification circuit

**Paper:** A Fast Quantum Algorithm for the Affine Boolean Function Identification (`1407.6402`).

**Run:** `artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f`

**Candidate:** `c002`; attempt 1; parent `root`.

**Method family:** `deutsch_jozsa_style_parity_test_with_ancilla_phase_kickback_`.

### Input abstract

> Bernstein-Vazirani algorithm (the one-query algorithm) can identify a completely specified linear Boolean function using a single query to the oracle with certainty. The first aim of the paper is to show that if the provided Boolean function is affine, then one more query to the oracle (the two-query algorithm) is required to identify the affinity of the function with certainty. The second aim of the paper is to show that if the provided Boolean function is incompletely defined, then the one-query and the two-query algorithms can be used as bounded-error quantum polynomial algorithms to identify certain classes of incompletely defined linear and affine Boolean functions respectively with probability of success at least $2/3$.

### Math produced inside the swarm

The Nemotron proposal contained 8 numbered equation predictions. The coordinator assembled 4 equations, retaining 0 verbatim by normalized textual comparison and adding or rewriting 4. This attribution matters: the executable result includes substantial Sonnet reconstruction.

First native equation prediction (verbatim):

```latex
\mathcal{F}_{f}:\{0,1\}^{n}\rightarrow\{0,1\}, f\in\{0,1\}^{m},x_{i}=a_{i}y+\epsilon_{i}. \tag{1}
```

Coordinator-assembled mathematical specification (verbatim LaTeX):

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

### Generated Qiskit code

The following module is the actual Sonnet-generated source from this swarm candidate; it has not been rewritten for the example.

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

### Simulation status and swarm outcome

- **Code status:** `generated`.
- **Docker validation:** `build_passed`.
- **Aer execution:** built and simulated; 1 smoke-test input case.
- **Example instance:** `{"n": 2, "a": 1, "b": 1}`.
- **Candidate status:** `ready`.
- **Whole-paper swarm outcome:** `ready`.
- **Run time:** 263 seconds for the whole paper; **estimated paid usage:** $0.31.

**Selected after review:** another agent approved this candidate. On the all-zero input, the intended operation is:

$$f(x)=a\cdot x\oplus b,\qquad |0^n\rangle_{\mathrm{data}}|0\rangle_{\mathrm{ref}}\longmapsto(-1)^b|a\rangle_{\mathrm{data}}|b\rangle_{\mathrm{ref}}.$$

- **Observed Aer counts:** `{"101": 1024}` for the saved example (`n=2`, `a=1`, `b=1`), with 1,024 shots and seed 42. The Qiskit bitstring `101` encodes reference `b=1` and data `a=01`.
- **Independent functional check:** 28/28 combinations of `(a,b)` at `n=1,2,3` returned both values correctly, within numerical tolerance.
- **Limitations:** the oracle is compiled from explicit parameters and controlled-phase-oracle access is assumed. Black-box query complexity, the paper's original construction, and incompletely defined functions are not verified.

[Independent checks](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/8abdf1a6-7062-47b4-8ada-4b3155188b52/example_correctness.json) · [Aer rerun](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/8abdf1a6-7062-47b4-8ada-4b3155188b52/example_simulation.json)

<details>
<summary>Recorded reviewer feedback</summary>

**Reviewer `a02`:** `pass`, reproduced failure: `false`.

> The circuit matches the spec. H on the reference qubit, then CU_f on data in |0^n>, then H on the reference gives |b>. The CZ(r,q_i) gates act on |0> data and are harmless no-ops; only the Z on r contributes, and it correctly implements the (-1)^b phase. The BV step H^n U_f H^n then maps |0^n> to (-1)^b|a>, using Z on q_i for a_i=1 and a global phase of pi when b=1. The final state is (-1)^b|a>_data|b>_ref, with little-endian ordering and index a+2^n*b, which is 5 for the instance. The scope is honestly limited to the promised-affine, completely specified case, with no black-box or query-complexity claims and the incompletely defined 2/3 results declared out of scope. The parameters are compiled into gates, which the contract permits. The circuit does implement the two-use structure (one controlled use and one plain use) that the spec describes.

</details>

[Swarm summary](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/summary.json) · [All candidates](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/all_candidates.json) · [Native/assembly evidence](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/native_evidence.json) · [Code artifact](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/8abdf1a6-7062-47b4-8ada-4b3155188b52/result.json)

## 2. Earlier affine candidate returned for revision

**Paper:** A Fast Quantum Algorithm for the Affine Boolean Function Identification (`1407.6402`).

**Run:** `artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f`

**Candidate:** `c001`; attempt 1; parent `root`.

**Method family:** `bernstein_vazirani_one_and_two_query_affine_identification`.

### Input abstract

> Bernstein-Vazirani algorithm (the one-query algorithm) can identify a completely specified linear Boolean function using a single query to the oracle with certainty. The first aim of the paper is to show that if the provided Boolean function is affine, then one more query to the oracle (the two-query algorithm) is required to identify the affinity of the function with certainty. The second aim of the paper is to show that if the provided Boolean function is incompletely defined, then the one-query and the two-query algorithms can be used as bounded-error quantum polynomial algorithms to identify certain classes of incompletely defined linear and affine Boolean functions respectively with probability of success at least $2/3$.

### Math produced inside the swarm

The Nemotron proposal contained 8 numbered equation predictions. The coordinator assembled 4 equations, retaining 0 verbatim by normalized textual comparison and adding or rewriting 4. This attribution matters: the executable result includes substantial Sonnet reconstruction.

First native equation prediction (verbatim):

```latex
\mathcal{O}_{f}|x\rangle|y\rangle=\left|x\right\rangle\left|y\oplus f(x)\right\rangle,\quad x\in\{0,1\}^{n},y\in\{0,1\}. \tag{1}
```

Coordinator-assembled mathematical specification (verbatim LaTeX):

```latex
% eq_1 — Oracle and phase kickback
U_f|x\rangle|y\rangle=|x\rangle|y\oplus f(x)\rangle,\qquad U_f|x\rangle|-\rangle=(-1)^{f(x)}|x\rangle|-\rangle

% eq_2 — One-query BV output
(H^{\otimes n}\otimes I)\,U_f\,(H^{\otimes n}\otimes I)|0^n\rangle|-\rangle=(-1)^{b}|a\rangle|-\rangle

% eq_3 — Second query: controlled oracle on |0^n>
CU_f\,|+\rangle_c|0^n\rangle|-\rangle=\tfrac{1}{\sqrt2}\big(|0\rangle+(-1)^{f(0^n)}|1\rangle\big)_c|0^n\rangle|-\rangle,\quad f(0^n)=b

% eq_4 — Final state
|\Psi\rangle=|b\rangle_c\,|0^n\rangle_{x_2}\,|a\rangle_{x}\,|-\rangle_{anc}\quad(\text{up to global phase})
```

### Generated Qiskit code

The following module is the actual Sonnet-generated source from this swarm candidate; it has not been rewritten for the example.

```python
from qiskit import QuantumCircuit, QuantumRegister


def _int_field(instance, key, lo, hi):
    v = instance.get(key)
    if isinstance(v, bool) or not isinstance(v, int) or v < lo or v > hi:
        raise ValueError("invalid value for " + key)
    return v


def build_circuit(instance):
    """Affine-function BV operation with a second controlled query.
    Layout: c=qubit 0, x=1..n, x2=n+1..2n, anc=2n+1.
    Expects anc supplied in |-> by the runner. Compiled oracle is U_f for f(x)=a.x xor b."""
    if not isinstance(instance, dict):
        raise ValueError("instance must be a dict")
    n = _int_field(instance, "n", 1, 5)
    a = _int_field(instance, "a", 0, 2 ** n - 1)
    b = _int_field(instance, "b", 0, 1)
    c = QuantumRegister(1, "c")
    x = QuantumRegister(n, "x")
    x2 = QuantumRegister(n, "x2")
    anc = QuantumRegister(1, "anc")
    qc = QuantumCircuit(c, x, x2, anc)
    # Hadamard layers: control to |+>, query-1 input register to uniform superposition
    qc.h(c[0])
    qc.h(x)
    # Query 1 (eq_1, eq_2): U_f on (x, anc) compiled from a and b
    for j in range(n):
        if (a >> j) & 1:
            qc.cx(x[j], anc[0])
    if b:
        qc.x(anc[0])
    qc.h(x)
    # Query 2 (eq_3): controlled U_f on (x2, anc), control c
    for j in range(n):
        if (a >> j) & 1:
            qc.ccx(c[0], x2[j], anc[0])
    if b:
        qc.cx(c[0], anc[0])
    # Close the interferometer on c so that c reads b (eq_4)
    qc.h(c[0])
    return qc
```

### Simulation status and swarm outcome

- **Code status:** `generated`.
- **Docker validation:** `build_passed`.
- **Aer execution:** built and simulated; 1 smoke-test input case.
- **Example instance:** `{"n": 2, "a": 3, "b": 1}`.
- **Candidate status:** `failing`.
- **Whole-paper swarm outcome:** `ready`.
- **Run time:** 263 seconds for the whole paper; **estimated paid usage:** $0.31.

**Returned for revision:** the reviewer found a mismatch between the specification's ancilla-preparation step and the code's documented expectation that the runner supplies that input. The objection was not a reproduced counterexample (`confirmed=false`).

An independent check of this exact operation, using its documented input with the final ancilla in `|->`, passed 28/28 affine-function instances for `n=1,2,3`. That does not resolve the spec/code input-contract disagreement; it explains why executable code and a rejected review can coexist.

This candidate was not the final selection. It led to repair candidate `c003`, which then failed a schema check because an algorithm step referenced an unknown equation ID. A separate method branch, candidate `c002` in example 1, was eventually selected.

[Independent checks under documented input](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/5fe599b6-ce2b-4b19-923b-567cfc77909f/correctness.json)

<details>
<summary>Recorded reviewer feedback</summary>

**Reviewer `a01`:** `break`, reproduced failure: `false`.

> The circuit never prepares anc in |->, but the spec says it should. Step 1 requires X then H on anc, and the actual code only has a docstring saying 'Expects anc supplied in |-> by the runner'. The runner contract gives no such guarantee, and the function must build a self-contained, documented unitary. With anc left in |0>, X on anc for b=1 and the CX/CCX gates act as bit flips, not phase kickback. Then Query 1 gives no clean a, and c does not read b. Under the default all-zero input, the circuit therefore does not implement the stated BV plus affinity operation. The fix is to add qc.x(anc[0]); qc.h(anc[0]) at the start, and to document the output decoding (c gives b, x gives a). Smaller issues: the eq_2 statement is misleading. For b=1 the state is |a>|-> with a global phase of -1, which is fine, but the spec's eq_2 uses the textbook check, and the circuit's X on anc for b=1 only equals the (-1)^b phase because anc is in |->. The ancilla is also not returned to a clean state, so only the |-> prep matters. The query-2 affinity test only reads f(0)=b, so a is still decoded only from query 1. Its limitations are disclosed in the spec, but the code docstring should say this too. The instance range n up to 5 is fine.

</details>

[Swarm summary](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/summary.json) · [All candidates](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/all_candidates.json) · [Native/assembly evidence](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/native_evidence.json) · [Code artifact](artifacts/native_swarm_pilot_v2/runs/1407.6402/006a0f3c-d783-47be-8bed-c8359b81141f/blackbox/5fe599b6-ce2b-4b19-923b-567cfc77909f/result.json)

## 3. Order-finding candidate from the 65-paper swarm run

**Paper:** Effects of Imperfect Gate Operations in Shor's Prime Factorization Algorithm (`0704.0516`).

**Run:** `artifacts/native_swarm_65/runs/0704.0516/35f6fd8f-a8e7-4650-950a-186a0c6dc3b1`

**Candidate:** `c003`; attempt 2; parent `c001`.

**Method family:** `shor_order_finding_with_gate_error_models`.

### Input abstract

> The effects of imperfect gate operations in implementation of Shor's prime factorization algorithm are investigated. The gate imperfections may be classified into three categories: the systematic error, the random error, and the one with combined errors. It is found that Shor's algorithm is robust against the systematic errors but is vulnerable to the random errors. Error threshold is given to the algorithm for a given number N to be factorized.

### Math produced inside the swarm

The Nemotron proposal contained 1 numbered equation predictions. The coordinator assembled 6 equations, retaining 0 verbatim by normalized textual comparison and adding or rewriting 6. This attribution matters: the executable result includes substantial Sonnet reconstruction.

First native equation prediction (verbatim):

```latex
\mathcal{E}_{i}=\left(\begin{array}[]{cc}\alpha_{i}&0\\ 0&\beta_{i}\\ \end{array}\right), \tag{1}
```

Coordinator-assembled mathematical specification (verbatim LaTeX):

```latex
% eq_1 — Modular multiplication unitary
U|y\rangle=|a y \bmod N\rangle,\quad \Lambda|x\rangle|y\rangle=|x\rangle|a^{x}y \bmod N\rangle=\prod_k (c\text{-}U^{2^k})_k|x\rangle|y\rangle

% eq_2 — Ideal output distribution
P(x)=\frac{1}{r}\sum_{s=0}^{r-1}\left|\frac{1}{2^t}\sum_{j=0}^{2^t-1}e^{2\pi i j(s/r-x/2^t)}\right|^2

% eq_3 — Systematic error model
\theta_m\to\theta_m(1+\epsilon)\ \text{or}\ \theta_m+\delta,\ \text{same at every gate}

% eq_4 — Random and combined error models
\theta_{m,j}\to\theta_m+\delta_j,\ \delta_j\sim\mathcal{D}(0,\sigma^2);\quad \text{combined: }\theta_m+\delta+\delta_j

% eq_5 — Success probability and threshold
P_{succ}=\sum_{x:\,|x/2^t-s/r|\le 2^{-t-1}\text{ for some }s}P(x),\quad \sigma_c=\max\{\sigma:\overline{P_{succ}}(\sigma)\ge \eta P_{succ}^{ideal}\}

% eq_6 — Ideal inverse QFT gate decomposition
\mathrm{QFT}^{-1}:\ \text{H on qubit } k \text{ and CP}(-\pi/2^{m}) \text{ between qubits separated by } m,\ \text{then bit-reversal swaps}
```

### Generated Qiskit code

The following module is the actual Sonnet-generated source from this swarm candidate; it has not been rewritten for the example.

```python
"""Shor order finding for N=15 with optionally imperfect inverse-QFT phase gates."""
from __future__ import annotations

import math

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister

_MODELS = ('ideal', 'systematic', 'random', 'combined')


def _num(instance, key, default_value):
    v = instance.get(key, default_value)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        raise ValueError(key + ' must be a real number')
    v = float(v)
    if not math.isfinite(v):
        raise ValueError(key + ' must be finite')
    return v


def _int(instance, key, default_value):
    v = instance.get(key, default_value)
    if isinstance(v, bool) or not isinstance(v, int):
        raise ValueError(key + ' must be an integer')
    return v


def _controlled_rotate_left(qc, ctrl, work, s):
    # eq_1: multiplication by 2^s mod 15 on y in 0..14 is a left cyclic rotation of 4 bits by s.
    # Controlled by ctrl via a chain of Fredkin gates; 15 (1111) is also fixed, so U is a permutation.
    for _ in range(s):
        for i in (2, 1, 0):
            qc.cswap(ctrl, work[i], work[i + 1])


def build_circuit(instance):
    if not isinstance(instance, dict):
        raise ValueError('instance must be a dict')
    n = _int(instance, 'N', 15)
    a = _int(instance, 'a', 2)
    t = _int(instance, 't', 4)
    seed = _int(instance, 'seed', 0)
    model = instance.get('error_model', 'ideal')
    if n != 15:
        raise ValueError('only N=15 is supported')
    if a not in (2, 4, 8):
        raise ValueError('a must be one of 2, 4, 8')
    if t < 1 or t > 8:
        raise ValueError('t must be in 1..8 (total qubits <= 12)')
    if not isinstance(model, str) or model not in _MODELS:
        raise ValueError('error_model must be ideal, systematic, random or combined')
    if seed < 0:
        raise ValueError('seed must be nonnegative')
    eps = _num(instance, 'epsilon', 0.0)
    dl = _num(instance, 'delta', 0.0)
    sg = _num(instance, 'sigma', 0.0)
    if sg < 0.0:
        raise ValueError('sigma must be >= 0')
    sys_on = model in ('systematic', 'combined')
    rnd_on = model in ('random', 'combined')
    e = eps if sys_on else 0.0
    d = dl if sys_on else 0.0
    w = sg * math.sqrt(3.0) if rnd_on else 0.0  # uniform on [-w,w] has variance sigma^2
    rng = np.random.default_rng(seed)

    count = list(range(t))
    work = list(range(t, t + 4))
    qc = QuantumCircuit(QuantumRegister(t, 'count'), QuantumRegister(4, 'work'))

    # Step 1: uniform superposition over counting register
    for q in count:
        qc.h(q)

    # Step 2 (eq_1): controlled U^(2^k), U^(2^k) = multiplication by a^(2^k) mod 15
    rot = {1: 0, 2: 1, 4: 2, 8: 3}
    for k in range(t):
        m = pow(a, 2 ** k, n)
        s = rot[m]
        if s:
            _controlled_rotate_left(qc, count[k], work, s)

    # Step 3 (eq_6, eq_3, eq_4): inverse QFT, swaps first then ascending H/CP ladder
    for i in range(t // 2):
        qc.swap(count[i], count[t - 1 - i])
    for j in range(t):
        for k in range(j):
            mag = math.pi / (2 ** (j - k))
            off = float(rng.uniform(-w, w)) if rnd_on else 0.0
            ang = -(mag * (1.0 + e) + d + off)
            qc.cp(ang, count[k], count[j])
        qc.h(count[j])
    return qc
```

### Simulation status and swarm outcome

- **Code status:** `generated`.
- **Docker validation:** `build_passed`.
- **Aer execution:** built and simulated; 1 smoke-test input case.
- **Example instance:** `{"N": 15, "a": 2, "t": 4, "error_model": "combined", "epsilon": 0.02, "delta": 0.01, "sigma": 0.05, "seed": 7}`.
- **Candidate status:** `failing`.
- **Whole-paper swarm outcome:** `no_reviewed_candidate`.
- **Run time:** 303 seconds for the whole paper; **estimated paid usage:** $0.47.

**Returned for revision:** the reviewer requested alignment of the work-register initialization (`y=1`) between the specification, code, and runner input. The recorded default-zero-input simulation returned:

```json
[
  {
    "00000000": 0.9999999999999996
  }
]
```

This is an execution observation, not evidence that order finding succeeded. The reviewer objection was a model judgment (`confirmed=false`), not an independently reproduced numerical counterexample. No independent algorithm-correctness pass is claimed for this example.

### What the swarm did with the failure

- Root candidate `c001` failed the equation-reference checks.
- Its child `c003` is the code snapshot above: it built and simulated, then was returned for revision.
- Child `c004` generated another circuit, but review again requested changes. A separate branch also produced a repair candidate.
- This actual run recorded **2 agent deaths and 2 replacements**. The replacements were fresh explorations because no reviewed-success donor existed yet.
- The paper ended as `no_reviewed_candidate` at its time budget. Building a circuit did not automatically earn acceptance.

<details>
<summary>Recorded reviewer feedback</summary>

**Reviewer `a03`:** `break`, reproduced failure: `false`.

> The circuit never prepares the work register in |0001> (y=1). The spec's initial_state requires this, but build_circuit applies no X to work[0]. The work register therefore stays |0000>, and every controlled cyclic rotation acts on |0000>, which it leaves unchanged. The controlled modular exponentiation is then an identity, so no phase information is kicked back onto the counting register. The counting register stays in a uniform superposition, and the ideal inverse QFT maps it to x=0 with probability 1. The circuit therefore does not produce the order-finding distribution of eq_2 (peaks at x=0,4,8,12 with probability 1/4 each). The perturbed phase gates only act on a trivial state, so any success probability or threshold measured from this circuit is meaningless. The rotation chain itself looks correct: multiplication by 2 mod 15 is a left cyclic bit rotation, and the cswap order (2,3), (1,2), (0,1) implements it. The fix is to add X on work[0] before the controlled multiplications and re-check that the ideal output has peaks at 0,4,8,12 for t=4, a=2. The documentation should also state that the circuit covers only N=15 with a in {2,4,8}, that the error models are assumed definitions, and that it does not reproduce the paper's analytic threshold.

</details>

[Swarm summary](artifacts/native_swarm_65/runs/0704.0516/35f6fd8f-a8e7-4650-950a-186a0c6dc3b1/summary.json) · [All candidates](artifacts/native_swarm_65/runs/0704.0516/35f6fd8f-a8e7-4650-950a-186a0c6dc3b1/all_candidates.json) · [Native/assembly evidence](artifacts/native_swarm_65/runs/0704.0516/35f6fd8f-a8e7-4650-950a-186a0c6dc3b1/native_evidence.json) · [Code artifact](artifacts/native_swarm_65/runs/0704.0516/35f6fd8f-a8e7-4650-950a-186a0c6dc3b1/blackbox/d90cf5e0-795d-4c55-abbb-50a7e1f6905d/result.json)

## Reading these examples

All three are outcomes of the same hybrid swarm implementation. One candidate was selected, and two illustrate review and repair behavior. They are not three independent successful paper reproductions. The full benchmark's success rate, cost and culling statistics must be computed from all completed paper runs, including failures.
