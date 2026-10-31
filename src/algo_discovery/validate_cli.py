"""Validate saved source without loading any provider credentials or calling a model."""

import argparse
import json
import sys
from pathlib import Path

from .equations import sha256
from .sandbox import validate_in_docker
from .source_checks import check_source


def main() -> int:
    parser = argparse.ArgumentParser(description="Check saved Qiskit source without a model call.")
    parser.add_argument("--code", required=True, type=Path)
    parser.add_argument("--instance-file", required=True, type=Path)
    parser.add_argument("--reference", choices=["none", "modular_weighted_sum"], default="none")
    parser.add_argument("--report", type=Path, help="Optional path to a JSON validation report")
    args = parser.parse_args()
    try:
        source = args.code.read_text(encoding="utf-8")
        instance = json.loads(args.instance_file.read_text(encoding="utf-8"))
        if not isinstance(instance, dict):
            raise ValueError("Instance must be a JSON object.")  # noqa: TRY004 - CLI input error.
        if len(source) > 40000:
            raise ValueError("Source exceeds the size limit.")
        check_source(source)
        report, _ = validate_in_docker(source, instance, args.reference)
        output = (
            json.dumps(
                {
                    "source_python_sha256": sha256(source.strip()),
                    "instance": instance,
                    "static_checks_passed": True,
                    "validation": report.model_dump(),
                },
                indent=2,
                allow_nan=False,
            )
            + "\n"
        )
        print(output, end="")
        if args.report:
            args.report.write_text(output, encoding="utf-8")
        return 0 if report.status in {"build_passed", "reference_passed"} else 2
    except (ValueError, SyntaxError, TypeError, RecursionError) as exc:
        print("Validation input/static check failed: " + str(exc)[:300], file=sys.stderr)
    except OSError:
        print("Unable to read source/instance or write the report.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
