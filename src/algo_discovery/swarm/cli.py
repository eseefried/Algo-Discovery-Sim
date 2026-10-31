"""Run a three-worker ecosystem, or post tasks and inspect its ledger separately."""

import argparse
import json
import re
import sys
from dataclasses import replace
from pathlib import Path

from pydantic import ValidationError

from ..config import ConfigurationError, Settings
from ..equations import GenerationError
from ..external_spec import ExternalSpec
from ..schemas import EquationRequest
from .domain import final_specification
from .ledger import Ledger
from .model import PROMPT_VERSION
from .supervisor import run_ecosystem

DEFAULT_DB = Path("/tmp/algo-discovery-swarm/ledger.sqlite3")


def add_input(parser):
    inputs = parser.add_mutually_exclusive_group(required=True)
    inputs.add_argument("--arxiv-id")
    inputs.add_argument("--abstract-file", type=Path)
    inputs.add_argument("--abstract")
    parser.add_argument("--scope")
    parser.add_argument("--max-calls", type=int, default=12)
    parser.add_argument("--max-attempts", type=int, default=3)


def add_runtime(parser):
    parser.add_argument("--max-seconds", type=float, default=600)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--model", help="Default: CLAUDE_MODEL / claude-haiku-5-5")
    parser.add_argument("--output-dir", type=Path, default=Path("artifacts/swarm"))


def submit(ledger, args):
    if args.arxiv_id:
        if not re.fullmatch(r"\d{4}\.\d{4,5}", args.arxiv_id):
            raise ValueError("Invalid arXiv ID.")
        abstract = Path(
            f"data/circuit_dataset_300_v1/abstracts/arxiv-{args.arxiv_id}.txt"
        ).read_text()
    elif args.abstract_file:
        abstract = args.abstract_file.read_text()
    else:
        abstract = args.abstract
    request = EquationRequest(abstract=abstract, experiment_scope=args.scope)
    return ledger.submit(
        request.model_dump() | {"arxiv_id": args.arxiv_id},
        max_calls=args.max_calls,
        max_attempts=args.max_attempts,
    )


def export(ledger, root_id, output_dir):
    summary = ledger.summary(root_id)
    directory = output_dir / root_id
    directory.mkdir(parents=True, exist_ok=True)
    summary |= {
        "ledger": str(ledger.path.resolve()),
        "prompt_version": PROMPT_VERSION,
        "wallet_unit": "virtual cents; unrelated to provider billing",
    }
    if summary["status"] == "completed":
        payload = json.loads(ledger.root(root_id)["payload"])
        spec = ExternalSpec(
            source="ledger_swarm",
            arxiv_id=payload.get("arxiv_id"),
            abstract=payload["abstract"],
            experiment_scope=payload.get("experiment_scope"),
            specification=final_specification(ledger, root_id),
        )
        spec_dir = directory / "specs"
        spec_dir.mkdir(exist_ok=True)
        path = spec_dir / f"{payload.get('arxiv_id') or root_id}.json"
        path.write_text(spec.model_dump_json(indent=2) + "\n", encoding="utf-8")
        summary["specification"] = str(path)
        summary["specification_status"] = spec.specification.status
    (directory / "ledger-summary.json").write_text(
        json.dumps(summary, indent=2) + "\n", encoding="utf-8"
    )
    (directory / "events.jsonl").write_text(
        "".join(json.dumps(e) + "\n" for e in ledger.history()), encoding="utf-8"
    )
    return summary


def main():
    parser = argparse.ArgumentParser(
        description="Three Haiku workers reconstruct an abstract via a shared ledger."
    )
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    add_input(parser)
    add_runtime(parser)
    parser.add_argument(
        "--blackbox",
        action="store_true",
        help="Run the exported spec through the existing code/simulation suite",
    )
    parser.add_argument("--reference", choices=["none", "modular_weighted_sum"], default="none")
    args = parser.parse_args()
    try:
        if not 1 <= args.max_seconds <= 86400:
            raise ValueError("Max seconds must be between 1 and 86400.")
        settings = Settings.from_env()
        if args.model:
            settings = replace(settings, model=args.model)
        ledger = Ledger(args.db)
        ledger.initialize()
        root_id = submit(ledger, args)
        print(
            f"Root {root_id}; ledger {ledger.path}; model {settings.model}",
            file=sys.stderr,
            flush=True,
        )
        run_ecosystem(
            ledger, settings, root_id=root_id, max_seconds=args.max_seconds, seed=args.seed
        )
        summary = export(ledger, root_id, args.output_dir)
        if args.blackbox and summary.get("specification"):
            from ..code_sim_cli import run

            blackbox_args = argparse.Namespace(
                spec=Path(summary["specification"]),
                source=None,
                arxiv_id=args.arxiv_id,
                instance_file=None,
                reference=args.reference,
                inputs=None,
                shots=1024,
                seed=args.seed,
            )
            downstream = {}
            blackbox_settings = replace(
                settings, artifact_dir=args.output_dir / root_id / "blackbox"
            )
            try:
                exit_code = run(blackbox_args, blackbox_settings, downstream)
            except (GenerationError, ConfigurationError) as exc:
                exit_code = 1
                downstream = {"stopped_at": "error", "error": str(exc)}
            summary["blackbox"] = downstream | {"exit_code": exit_code}
            (args.output_dir / root_id / "blackbox-summary.json").write_text(
                json.dumps(downstream, indent=2) + "\n"
            )
            (args.output_dir / root_id / "ledger-summary.json").write_text(
                json.dumps(summary, indent=2) + "\n"
            )
        print(
            json.dumps(
                {k: v for k, v in summary.items() if k not in {"tasks", "agents", "model_calls"}},
                indent=2,
            )
        )
        if summary.get("blackbox", {}).get("exit_code") == 1:
            return 1
        return (
            0
            if summary["status"] == "completed"
            and summary.get("specification_status") in {"specified", "partial"}
            and summary.get("blackbox", {}).get("exit_code", 0) == 0
            else 2
        )
    except (ValueError, TypeError, ValidationError, ConfigurationError) as exc:
        print("Swarm input/state error: " + str(exc)[:500], file=sys.stderr)
    except OSError:
        print("Swarm could not access its ledger, abstract, or artifacts.", file=sys.stderr)
    return 1


def ledger_main():
    parser = argparse.ArgumentParser(
        description="Post tasks, serve workers, and inspect the ledger."
    )
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init")
    post = commands.add_parser("submit")
    add_input(post)
    serve = commands.add_parser("serve")
    add_runtime(serve)
    status = commands.add_parser("status")
    status.add_argument("root_id")
    export_command = commands.add_parser("export")
    export_command.add_argument("root_id")
    export_command.add_argument("--output-dir", type=Path, default=Path("artifacts/swarm"))
    commands.add_parser("events")
    commands.add_parser("verify")
    args = parser.parse_args()
    try:
        ledger = Ledger(args.db)
        ledger.initialize()
        if args.command == "submit":
            print(submit(ledger, args))
        elif args.command == "serve":
            settings = Settings.from_env()
            if args.model:
                settings = replace(settings, model=args.model)
            run_ecosystem(ledger, settings, max_seconds=args.max_seconds, seed=args.seed)
        elif args.command == "status":
            print(json.dumps(ledger.summary(args.root_id), indent=2))
        elif args.command == "export":
            summary = export(ledger, args.root_id, args.output_dir)
            print(
                json.dumps(
                    {
                        k: v
                        for k, v in summary.items()
                        if k not in {"tasks", "agents", "model_calls"}
                    },
                    indent=2,
                )
            )
        elif args.command == "events":
            for event in ledger.history():
                print(json.dumps(event))
        elif args.command == "verify":
            valid = ledger.verify_history()
            print(json.dumps({"history_valid": valid}))
            return 0 if valid else 2
        else:
            print(str(ledger.path.resolve()))
        return 0
    except (ValueError, ConfigurationError) as exc:
        print(str(exc)[:500], file=sys.stderr)
    except OSError:
        print("Unable to access ledger files.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
