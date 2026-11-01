"""Model-free functional audit of saved circuits for three curated quantum papers.

Bindings below were reviewed against these specific artifacts' documented interfaces.
Generated Python runs only in the existing locked-down Docker worker. This audit
does not certify black-box query complexity or arbitrary problem sizes.
"""

import argparse
import itertools
import json
import math
from pathlib import Path

import numpy as np
from qiskit.quantum_info import Operator, Statevector

from .equations import sha256
from .sandbox import build_in_docker
from .source_checks import check_source
from .verification import circuit_from_wire

SYSTEMS = {
    "fable": ("baseline_results", ["14887a09-afe8-44d1-a06a-5cc3a5883a19", "60140e6b-9dda-4641-948c-ed30979451f3", "e170fba3-1f4e-4e63-a5ac-33372ea2d799"]),
    "sonnet": ("baseline_sonnet", ["755ea04f-32d4-4b57-b8b2-2fa5d0ce1c57", "d27351e0-787c-46c5-9a4c-a5a0326ee8b6", "d83420e0-498c-411b-94b6-0a2945c27074"]),
    "ledger": ("swarm_full/results", ["19654656-f4c0-4d6c-b873-9037f4f696fd", "c1e3f11c-603f-4359-a91b-3bbbdf13179f", "5b84113c-66ec-44c1-bb40-45b2d739cca9"]),
    "a2m": ("a2m_full/results", ["545f2129-012b-4e4b-a8b4-1eff667a75ff", "63fd606f-587d-4e50-9349-cf675bc7843a", "fd93026c-97db-4cfe-bed7-757aa5661d3d"]),
}
PAPERS = ["1411.5949", "1407.6402", "1409.3305"]
TOL = 1e-8


class BuildFailure(RuntimeError):
    pass


def build(source: str, instance: dict):
    check_source(source)
    wire, image, failure = build_in_docker(source, instance, "none")
    if failure:
        raise BuildFailure(f"{failure.status}: {failure.detail}")
    circuit = circuit_from_wire(wire)
    if circuit.num_qubits > 8 or len(circuit.data) > 2000:
        raise BuildFailure("Correctness audit cap: 8 qubits / 2000 elementary gates.")
    return circuit, image


def coherent_permutation_check(circuit, outputs: list[int]) -> dict:
    """Every basis input plus relative phases: one common global phase is allowed."""
    actual = Operator(circuit).data
    dimension = len(outputs)
    if actual.shape != (dimension, dimension) or sorted(outputs) != list(range(dimension)):
        raise ValueError("Expected a full permutation reference matching the circuit size.")
    reference = np.zeros_like(actual)
    reference[outputs, np.arange(dimension)] = 1
    success = np.abs(actual[outputs, np.arange(dimension)]) ** 2
    overlap = np.vdot(reference, actual)
    phase = overlap / abs(overlap) if abs(overlap) > 1e-12 else 1
    error = float(np.max(np.abs(actual - phase * reference)))
    return {"passed": bool(error < TOL), "basis_inputs": dimension,
            "min_basis_success_probability": float(success.min()),
            "full_operator_error_up_to_global_phase": error}


def weighted_binding(system, n, widths, weights, signed):
    bit_weights = [w * (-2**j if signed and j == width - 1 else 2**j)
                   for width, w in zip(widths, weights) for j in range(width)]
    data_n = sum(widths)
    if system == "fable":
        return {"n": n, "weights": bit_weights}, list(range(n, n + data_n)), list(range(n))
    if system == "sonnet":
        if signed:
            # Its documented interface is unsigned; test unsigned plus negative weights.
            raise ValueError("Signed input registers are outside this artifact's declared scope.")
        return {"n_acc": n, "input_bits": widths, "weights": weights}, list(range(n, n + data_n)), list(range(n))
    if len(set(widths)) != 1:
        raise ValueError("This artifact uses equal-width input registers.")
    if system == "ledger":
        instance = {"n_acc": n, "n_x": widths[0], "weights": weights, "signed": signed}
    else:
        instance = {"m": n, "n": widths[0], "weights": weights, "signed_inputs": signed}
    return instance, list(range(data_n)), list(range(data_n, data_n + n))


def weighted_outputs(n, data_bits, accumulator_bits, bit_weights):
    outputs = []
    mask = sum(1 << q for q in accumulator_bits)
    for basis in range(2 ** (n + len(data_bits))):
        b = sum(((basis >> q) & 1) << j for j, q in enumerate(accumulator_bits))
        value = (b + sum(w * ((basis >> q) & 1) for q, w in zip(data_bits, bit_weights))) % (2**n)
        outputs.append((basis & ~mask) | sum(((value >> j) & 1) << q for j, q in enumerate(accumulator_bits)))
    return outputs


def arithmetic(system, source):
    cases = []
    # Same basic modular-adder contract at m=1,2,3, with arbitrary accumulator input.
    suite = [(m, [m], [1], False, "modular_adder") for m in (1, 2, 3)]
    suite += [(3, [2, 2], [-1, 3], False, "negative_weight_and_wraparound"),
              (2, [1, 1], [0, 2], False, "zero_weight_and_wraparound")]
    if system != "sonnet":
        suite.append((3, [2, 2], [1, -2], True, "signed_inputs"))
    for n, widths, weights, signed, kind in suite:
        instance, data, acc = weighted_binding(system, n, widths, weights, signed)
        circuit, image = build(source, instance)
        if circuit.num_qubits != len(data) + len(acc):
            raise BuildFailure("Unexpected register/ancilla count.")
        bit_weights = [w * (-2**j if signed and j == width - 1 else 2**j)
                       for width, w in zip(widths, weights) for j in range(width)]
        check = coherent_permutation_check(circuit, weighted_outputs(n, data, acc, bit_weights))
        cases.append({"kind": kind, "instance": instance, "worker_image_id": image, **check})
    return {"scoped_functional_status": "passed" if all(c["passed"] for c in cases) else "failed",
            "coverage": "Modular addition m=1..3; weighted sums, negative/zero weights, wraparound; signed inputs where declared.",
            "curated_task_status": "passed_on_tested_sizes" if all(c["passed"] for c in cases if c["kind"] == "modular_adder") else "failed",
            "cases": cases}


def affine(system, source):
    cases = []
    full = system in {"fable", "sonnet"}
    for n in (1, 2, 3):
        for a in itertools.product((0, 1), repeat=n):
            for b in (0, 1):
                instance = {"n": n, "a": list(a)}
                if system != "ledger":
                    instance["b"] = b
                if system == "fable":
                    instance["two_query"] = True
                circuit, image = build(source, instance)
                expected_n = n + {"fable": 2, "sonnet": 1, "ledger": 0, "a2m": 1}[system]
                if circuit.num_qubits != expected_n:
                    raise BuildFailure("Unexpected affine-circuit layout.")
                state = np.zeros(2**expected_n, complex)
                if system == "fable":
                    state[1 << n] = 1  # Documented |0^n>|1>|0> input.
                elif system == "a2m":
                    state[0], state[1 << n] = 1 / math.sqrt(2), -1 / math.sqrt(2)
                else:
                    state[0] = 1
                probs = Statevector(state).evolve(circuit).probabilities()
                a_value = sum(bit << i for i, bit in enumerate(a))
                coefficient_p = sum(float(p) for index, p in enumerate(probs) if index % (2**n) == a_value)
                full_p = None
                if full:
                    full_p = 0.0
                    for index, p in enumerate(probs):
                        observed_a = index % (2**n)
                        offset = (index >> n) & 1
                        if system == "fable":
                            offset = ((index >> (n + 1)) & 1) ^ (observed_a.bit_count() % 2)
                        if observed_a == a_value and offset == b:
                            full_p += float(p)
                passed = (full_p if full else coefficient_p) > 1 - TOL
                cases.append({"instance": instance, "truth_b": b, "worker_image_id": image,
                              "coefficient_success_probability": coefficient_p,
                              "full_output_success_probability": full_p, "passed": passed})
    return {"scoped_functional_status": "passed" if all(c["passed"] for c in cases) else "failed",
            "coverage": "a and b" if full else "a only; offset b is not recovered",
            "curated_task_status": ("functional_pass_query_contract_unverified" if all(c["passed"] for c in cases) else "failed") if full else "incomplete_offset_missing",
            "query_contract": "Not certified: artifacts compile explicit a/b into gates, rather than accepting the curated opaque XOR oracle.",
            "cases": cases}


def lambda_floor(length, delta):
    return 1 - 1 / math.cosh(math.acosh(1 / delta) / length) ** 2


def amplification(system, source):
    cases = []
    if system == "a2m":
        for d in (1, 2, 3):
            epsilon = 0.04
            floor = lambda_floor(2 * d + 1, math.sqrt(epsilon))
            for lam in np.linspace(floor + 1e-5, 1, 4):
                instance = {"lambda": float(lam), "epsilon": epsilon, "d": d}
                circuit, image = build(source, instance)
                if circuit.num_qubits != 1:
                    raise BuildFailure("Expected single-qubit amplitude-amplification model.")
                p = float(Statevector.from_int(0, 2).evolve(circuit).probabilities()[1])
                cases.append({"instance": instance, "worker_image_id": image, "lambda_floor": floor,
                              "success_probability": p, "required_probability": 1 - epsilon,
                              "passed": p >= 1 - epsilon - TOL})
    else:
        n, delta, length = 3, 0.2, 5
        floor = lambda_floor(length, delta)
        for count in (2, 3, 4, 6, 8):
            for seed in (7, 19):
                marked = sorted(int(v) for v in np.random.default_rng(seed).choice(2**n, count, replace=False))
                if system == "fable":
                    instance = {"n": n, "targets": marked, "L": length, "delta": delta, "apply_state_preparation": True}
                else:
                    # Its L is ordinary Grover iterations. Give it the same two query rounds.
                    instance = {"n": n, "marked": marked, "L": (length - 1) // 2}
                circuit, image = build(source, instance)
                if circuit.num_qubits != n:
                    raise BuildFailure("Unexpected search-register size.")
                state = Statevector.from_int(0, 2**n) if system == "fable" else Statevector(np.ones(2**n) / math.sqrt(2**n))
                p = float(sum(state.evolve(circuit).probabilities()[marked]))
                cases.append({"instance": instance, "worker_image_id": image, "lambda": count / 2**n,
                              "lambda_floor": floor, "success_probability": p,
                              "required_probability": 1 - delta**2, "passed": p >= 1 - delta**2 - TOL})
    passed = all(c["passed"] for c in cases)
    return {"scoped_functional_status": "passed" if passed else "failed",
            "coverage": "One-qubit known-amplitude model" if system == "a2m" else ("Fixed-point success bound across marked sets" if system == "fable" else "Ordinary Grover circuit tested against fixed-point bound"),
            "curated_task_status": "bound_pass_query_contract_unverified" if passed else "failed_fixed_point_bound",
            "query_contract": "Not certified: explicit marked sets or known scalar amplitudes, not the curated opaque-oracle interface; no asymptotic claim tested.",
            "minimum_success_probability": min(c["success_probability"] for c in cases), "cases": cases}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("artifacts/code-correctness"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    rows = []
    for system, (root, ids) in SYSTEMS.items():
        for paper, reviewed_id in zip(PAPERS, ids):
            row = {"system": system, "arxiv_id": paper, "reviewed_run_id": reviewed_id}
            print(f"Checking {system} / {paper}", flush=True)
            try:
                log = json.loads((Path(root) / "logs" / f"{paper}.json").read_text())
                if log.get("code", {}).get("run_id") != reviewed_id:
                    raise ValueError("Saved run differs from the reviewed binding; audit its interface first.")
                directory = Path(root) / reviewed_id
                result = json.loads((directory / "result.json").read_text())
                artifact = result["artifact"]
                row.update(artifact_dir=str(directory), code_model=result["model"], source_sha256=sha256(artifact["source_python"]))
                if artifact["status"] != "generated":
                    row.update(scoped_functional_status="no_code", curated_task_status="no_code", detail=artifact["summary"])
                else:
                    source = (directory / "circuit.py").read_text()
                    if source.strip() != artifact["source_python"].strip():
                        raise ValueError("Saved circuit differs from the recorded code artifact.")
                    fn = {"1411.5949": arithmetic, "1407.6402": affine, "1409.3305": amplification}[paper]
                    row.update(fn(system, source))
            except (OSError, ValueError, KeyError, TypeError, BuildFailure) as exc:
                row.update(scoped_functional_status="evaluation_error", curated_task_status="not_assessed", error=str(exc)[:500])
            rows.append(row)
            (args.out / f"{system}_{paper}.json").write_text(json.dumps(row, indent=2))
            (args.out / "results.json").write_text(json.dumps(rows, indent=2))
            print(f"  {row['scoped_functional_status']} / {row['curated_task_status']}", flush=True)
    lines = ["# Saved-code correctness audit", "", "Independent small-instance functional checks. No model calls. Generated source executed only in Docker.", "", "| System | Paper | Scoped functional result | Curated-task coverage |", "|---|---|---|---|"]
    lines += [f"| {r['system']} | {r['arxiv_id']} | {r['scoped_functional_status']} | {r['curated_task_status']} |" for r in rows]
    lines += ["", "Arithmetic checks all basis inputs and the full operator up to one global phase at the tested sizes. Affine checks all hidden-coefficient values for n=1..3, using the source's declared input preparation and output decoding. Search checks the success bound over multiple inputs. Oracle parameters remain explicit in generated code: query complexity, oracle restrictions, general-size correctness and full-paper reproduction are not certified. Fable's original code stage used Fable; the other three used Sonnet."]
    (args.out / "REPORT.md").write_text("\n".join(lines) + "\n")
    return 0 if not any(r["scoped_functional_status"] == "evaluation_error" for r in rows) else 2


if __name__ == "__main__":
    raise SystemExit(main())
