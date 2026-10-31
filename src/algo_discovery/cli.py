import argparse
import json
import sys
from pathlib import Path

from pydantic import ValidationError

from .config import ConfigurationError, Settings
from .equations import GenerationError, generate_equations
from .prompt import PROMPT_VERSION, SYSTEM_PROMPT, user_message
from .schemas import EquationRequest, MathSpecification


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reconstruct equations from an abstract with Claude."
    )
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--abstract-file", type=Path)
    inputs.add_argument("--abstract")
    inputs.add_argument("--stdin", action="store_true")
    parser.add_argument("--scope", help="Optional finite experiment target; not abstract evidence")
    parser.add_argument("--model", help="Override CLAUDE_MODEL for this invocation")
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument(
        "--dry-run", action="store_true", help="Show payload/schema without an API call"
    )
    args = parser.parse_args()
    try:
        if args.abstract_file:
            abstract = args.abstract_file.read_text(encoding="utf-8")
        elif args.stdin:
            abstract = sys.stdin.read()
        else:
            abstract = args.abstract
        request = EquationRequest(abstract=abstract, experiment_scope=args.scope)
        if args.dry_run:
            print(
                json.dumps(
                    {
                        "prompt_version": PROMPT_VERSION,
                        "system": SYSTEM_PROMPT,
                        "user": user_message(request),
                        "schema": MathSpecification.model_json_schema(),
                    },
                    indent=2,
                    ensure_ascii=False,
                )
            )
            return 0
        settings = Settings.from_env()
        if args.model or args.artifact_dir:
            from dataclasses import replace

            settings = replace(
                settings,
                model=args.model or settings.model,
                artifact_dir=args.artifact_dir
                if args.artifact_dir is not None
                else settings.artifact_dir,
            )
        result = generate_equations(request, settings)
        print(result.model_dump_json(indent=2))
        print(f"Artifacts: {settings.artifact_dir / result.run_id}", file=sys.stderr)
        return 0
    except (ConfigurationError, GenerationError) as exc:
        print(str(exc), file=sys.stderr)
    except ValidationError:
        print(
            "Invalid input: abstract must contain 20–30,000 characters; check scope length.",
            file=sys.stderr,
        )
    except OSError:
        print(
            "Could not read the input or write artifacts. Check paths and permissions.",
            file=sys.stderr,
        )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
