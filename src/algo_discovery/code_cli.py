import argparse
import json
import sys
from dataclasses import replace
from pathlib import Path

from pydantic import ValidationError

from .code_generation import generate_code, load_code_request
from .code_prompt import PROMPT_VERSION, SYSTEM_PROMPT, code_messages
from .code_schemas import CircuitArtifact
from .config import ConfigurationError, Settings
from .equations import GenerationError


def main() -> int:
    parser = argparse.ArgumentParser(description="Continue a saved equation run into Qiskit code.")
    parser.add_argument("--equations", required=True, type=Path, help="Block-one result.json")
    parser.add_argument(
        "--request", type=Path, help="Original request.json; defaults to sibling file"
    )
    parser.add_argument(
        "--instance-file", type=Path, help="Optional JSON object of circuit parameters"
    )
    parser.add_argument("--validate", action="store_true", help="Build/transpile only in Docker")
    parser.add_argument("--reference", choices=["none", "modular_weighted_sum"], default="none")
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument(
        "--dry-run", action="store_true", help="Inspect prompt/schema without a model call"
    )
    args = parser.parse_args()
    try:
        instance = json.loads(args.instance_file.read_text()) if args.instance_file else None
        request = load_code_request(
            args.equations,
            request_file=args.request,
            instance=instance,
            validate_circuit=args.validate,
            reference=args.reference,
        )
        if args.dry_run:
            print(
                json.dumps(
                    {
                        "prompt_version": PROMPT_VERSION,
                        "system": SYSTEM_PROMPT,
                        "messages": code_messages(request),
                        "schema": CircuitArtifact.model_json_schema(),
                    },
                    indent=2,
                )
            )
            return 0
        settings = Settings.from_env()
        if args.artifact_dir is not None:
            settings = replace(settings, artifact_dir=args.artifact_dir)
        result = generate_code(request, settings)
        print(result.model_dump_json(indent=2))
        print(f"Artifacts: {settings.artifact_dir / result.run_id}", file=sys.stderr)
        if result.artifact.status != "generated" or not result.static_checks_passed:
            return 2
        if args.validate and result.validation.status not in {"build_passed", "reference_passed"}:
            return 2
        return 0
    except (ConfigurationError, GenerationError) as exc:
        print(str(exc), file=sys.stderr)
    except (ValidationError, ValueError):
        print(
            "Invalid input: check source run/request hashes, instance JSON, and --validate/--reference.",
            file=sys.stderr,
        )
    except OSError:
        print(
            "Could not read input or write artifacts; check paths and permissions.", file=sys.stderr
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
