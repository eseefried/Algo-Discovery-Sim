"""Black-box stages 2-3: a math specification from any source -> Qiskit -> Aer simulation."""

import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .external_spec import ExternalSpec, load_spec, save_as_equation_run
from .pipeline_cli import add_stage_arguments, describe, execute, log, run_code_and_simulation


def run(args, settings, summary: dict) -> int:
    summary["stopped_at"] = None
    try:
        spec = load_spec(args.spec)
        if args.source or args.arxiv_id:
            spec = ExternalSpec.model_validate(
                spec.model_dump()
                | {"source": args.source or spec.source, "arxiv_id": args.arxiv_id or spec.arxiv_id}
            )
        log(f"[1/3] specification from {spec.source}")
        equations = save_as_equation_run(spec, settings)
    except (ValidationError, ValueError) as exc:
        # A malformed spec is the producer's result, like invalid model output: count it.
        error = describe(exc) if isinstance(exc, ValidationError) else str(exc)[:500]
        summary["equations"] = {"status": "invalid_spec", "error": error}
        summary["stopped_at"] = "equations"
        log(f"      invalid_spec: {error}")
        return 2
    equations_dir = settings.artifact_dir / equations.run_id
    status = equations.specification.status
    summary["equations"] = {
        "run_id": equations.run_id,
        "status": status,
        "source": spec.source,
        "artifacts": str(equations_dir),
    }
    log(f"      {status}  {equations_dir}")
    if status not in {"specified", "partial"}:
        summary["stopped_at"] = "equations"
        return 2
    return run_code_and_simulation(equations_dir, args, settings, summary)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate Qiskit code and simulate it from a supplied math specification."
    )
    parser.add_argument(
        "--spec", required=True, type=Path, help="Spec JSON, or a block-one result.json"
    )
    parser.add_argument("--source", help="Label for the producer, e.g. swarm or single_agent")
    parser.add_argument("--arxiv-id", help="Dataset paper the spec is for")
    parser.add_argument(
        "--print-schema", action="store_true", help="Print the input JSON schema and exit"
    )
    add_stage_arguments(parser)
    if "--print-schema" in sys.argv:
        print(json.dumps(ExternalSpec.model_json_schema(), indent=2))
        return 0
    return execute(run, parser.parse_args())


if __name__ == "__main__":
    raise SystemExit(main())
