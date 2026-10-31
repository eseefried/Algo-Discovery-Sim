"""Run abstract -> equations -> Qiskit -> Aer simulation, stopping at the first failed stage."""

import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

from pydantic import ValidationError

from .code_generation import generate_code, load_code_request
from .config import ConfigurationError, Settings
from .equations import GenerationError, generate_equations
from .schemas import EquationRequest
from .simulation_cli import simulate_source

DATASET_ABSTRACTS = Path("data/circuit_dataset_300_v1/abstracts")


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def read_abstract(args) -> str:
    if args.arxiv_id:
        return (DATASET_ABSTRACTS / f"arxiv-{args.arxiv_id}.txt").read_text(encoding="utf-8")
    if args.abstract_file:
        return args.abstract_file.read_text(encoding="utf-8")
    if args.stdin:
        return sys.stdin.read()
    return args.abstract


def run(args, settings: Settings, summary: dict) -> int:
    """Fill in summary as stages finish, so a crash still records the earlier ones."""
    summary["stopped_at"] = None
    request = EquationRequest(abstract=read_abstract(args), experiment_scope=args.scope)

    log("[1/3] abstract -> equations")
    equations = generate_equations(request, settings)
    equations_dir = settings.artifact_dir / equations.run_id
    summary["equations"] = {
        "run_id": equations.run_id,
        "status": equations.specification.status,
        "artifacts": str(equations_dir),
    }
    log(f"      {equations.specification.status}  {equations_dir}")
    if equations.specification.status not in {"specified", "partial"}:
        summary["stopped_at"] = "equations"
        return 2

    log("[2/3] equations -> Qiskit (Docker validation)")
    instance = json.loads(args.instance_file.read_text()) if args.instance_file else None
    code_request = load_code_request(
        equations_dir / "result.json",
        instance=instance,
        validate_circuit=True,
        reference=args.reference,
    )
    code = generate_code(code_request, settings)
    code_dir = settings.artifact_dir / code.run_id
    summary["code"] = {
        "run_id": code.run_id,
        "status": code.artifact.status,
        "static_checks_passed": code.static_checks_passed,
        "validation_status": code.validation.status,
        "artifacts": str(code_dir),
    }
    log(f"      {code.artifact.status}, validation {code.validation.status}  {code_dir}")
    if code.artifact.status != "generated" or not code.static_checks_passed:
        summary["stopped_at"] = "code"
        return 2
    if code.validation.status not in {"build_passed", "reference_passed"}:
        summary["stopped_at"] = "validation"
        return 2

    log("[3/3] Aer simulation")
    inputs = json.loads(args.inputs.read_text(encoding="utf-8")) if args.inputs else None
    if inputs is not None and not isinstance(inputs, list):
        raise ValueError("Inputs must be a JSON list.")
    output, report = simulate_source(
        code.artifact.source_python,
        json.loads((code_dir / "instance.json").read_text(encoding="utf-8")),
        args.reference,
        inputs,
        shots=args.shots,
        seed=args.seed,
    )
    (code_dir / "simulation.json").write_text(output, encoding="utf-8")
    summary["simulation"] = {
        "status": report.status,
        "cases_run": report.cases_run,
        "cases_passed": report.cases_passed,
        "report": str(code_dir / "simulation.json"),
    }
    log(f"      {report.status}, {report.cases_passed}/{report.cases_run} cases passed")
    if report.status not in {"simulated", "reference_passed"}:
        summary["stopped_at"] = "simulation"
        return 2
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the full abstract-to-simulation pipeline.")
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--arxiv-id", help="Abstract from data/circuit_dataset_300_v1/abstracts")
    inputs.add_argument("--abstract-file", type=Path)
    inputs.add_argument("--abstract")
    inputs.add_argument("--stdin", action="store_true")
    parser.add_argument("--scope", help="Optional finite experiment target; not abstract evidence")
    parser.add_argument("--model", help="Override CLAUDE_MODEL for this invocation")
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument("--instance-file", type=Path, help="Optional circuit parameters")
    parser.add_argument("--reference", choices=["none", "modular_weighted_sum"], default="none")
    parser.add_argument("--inputs", type=Path, help="JSON list of simulation input cases")
    parser.add_argument("--shots", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    summary = {}
    try:
        settings = Settings.from_env()
        settings = replace(
            settings,
            model=args.model or settings.model,
            artifact_dir=args.artifact_dir or settings.artifact_dir,
        )
        code = run(args, settings, summary)
    except (ConfigurationError, GenerationError) as exc:
        log(str(exc))
        code = 1
    except ValidationError:
        log("Invalid input: check the abstract length, scope, instance JSON, and source run.")
        code = 1
    except (ValueError, SyntaxError, TypeError, KeyError, RecursionError) as exc:
        log("Pipeline input/static check failed: " + str(exc)[:300])
        code = 1
    except OSError:
        log("Could not read input or write artifacts; check paths and permissions.")
        code = 1
    if summary:
        if code == 1:
            summary["stopped_at"] = "error"
        output = json.dumps(summary, indent=2) + "\n"
        print(output, end="")
        if "code" in summary:
            Path(summary["code"]["artifacts"], "pipeline.json").write_text(output, encoding="utf-8")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
