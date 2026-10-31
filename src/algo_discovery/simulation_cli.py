"""Simulate saved source without loading any provider credentials or calling a model."""

import argparse
import json
import sys
from pathlib import Path

from .code_schemas import Reference
from .equations import sha256
from .sandbox import build_in_docker
from .simulation import SimulationReport, simulate
from .source_checks import check_source
from .verification import circuit_from_wire


def simulate_source(
    source: str,
    instance: dict,
    reference: Reference,
    inputs: list | None = None,
    *,
    shots: int = 1024,
    seed: int = 42,
) -> tuple[str, SimulationReport]:
    """Build in Docker, simulate on the host, and return (report JSON text, report)."""
    if len(source) > 40000:
        raise ValueError("Source exceeds the size limit.")
    check_source(source)
    wire, image_id, failure = build_in_docker(source, instance, reference)
    if failure:
        report = SimulationReport(
            status="unavailable" if failure.status == "unavailable" else "failed",
            reference=reference,
            detail=failure.detail,
        )
    else:
        circuit = circuit_from_wire(wire)
        report = simulate(circuit, instance, reference, inputs, shots=shots, seed=seed)
    output = json.dumps(
        {
            "source_python_sha256": sha256(source.strip()),
            "instance": instance,
            "worker_image_id": image_id,
            "qiskit_version": wire["qiskit_version"] if wire else None,
            "static_checks_passed": True,
            "simulation": report.model_dump(),
        },
        indent=2,
        allow_nan=False,
    )
    return output + "\n", report


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate saved Qiskit source with Aer.")
    parser.add_argument("--run-dir", type=Path, help="Code-stage artifact directory")
    parser.add_argument("--code", type=Path, help="Defaults to RUN_DIR/circuit.py")
    parser.add_argument("--instance-file", type=Path, help="Defaults to RUN_DIR/instance.json")
    parser.add_argument("--reference", choices=["none", "modular_weighted_sum"], default="none")
    parser.add_argument("--inputs", type=Path, help="JSON list of input cases")
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--report", type=Path, help="Defaults to RUN_DIR/simulation.json")
    args = parser.parse_args()
    code = args.code or (args.run_dir and args.run_dir / "circuit.py")
    instance_file = args.instance_file or (args.run_dir and args.run_dir / "instance.json")
    report_path = args.report or (args.run_dir and args.run_dir / "simulation.json")
    if not code or not instance_file:
        parser.error("Provide --run-dir, or both --code and --instance-file.")
    try:
        source = code.read_text(encoding="utf-8")
        instance = json.loads(instance_file.read_text(encoding="utf-8"))
        if not isinstance(instance, dict):
            raise ValueError("Instance must be a JSON object.")  # noqa: TRY004 - CLI input error.
        inputs = None
        if args.inputs:
            inputs = json.loads(args.inputs.read_text(encoding="utf-8"))
            if not isinstance(inputs, list):
                raise ValueError("Inputs must be a JSON list.")
        output, report = simulate_source(
            source, instance, args.reference, inputs, shots=args.shots, seed=args.seed
        )
        print(output, end="")
        if report_path:
            report_path.write_text(output, encoding="utf-8")
        return 0 if report.status in {"simulated", "reference_passed"} else 2
    except (ValueError, SyntaxError, TypeError, KeyError, RecursionError) as exc:
        print("Simulation input/static check failed: " + str(exc)[:300], file=sys.stderr)
    except OSError:
        print("Unable to read source/instance/inputs or write the report.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
