"""Abstract -> numbered LaTeX, matching the Nemotron LoRA training contract.

These predictions are not JSON MathSpecifications or verified equations.
"""

import argparse
import fcntl
import json
import os
import re
import time
from contextlib import contextmanager
from pathlib import Path

import httpx

SYSTEM = (
    "Reconstruct the display equations for the quantum method described by the abstract. "
    "Output only numbered LaTeX equations, in document order."
    " Return up to 8 equations starting at the requested index. "
    "Append <END_EQUATIONS> after the final equation of the paper."
)
END = "<END_EQUATIONS>"
LINE = re.compile(r"^\((\d+)\)\s+(.+)$")


@contextmanager
def generation_slot():
    """Coordinate local clients before their HTTP timeouts start counting."""
    with open(os.getenv("NEMOTRON_GPU_LOCK", "/tmp/algo-discovery-nemotron-gpu.lock"), "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock, fcntl.LOCK_UN)


def equation_key(latex: str) -> str:
    """Detect repeated content even when the model increments equation tags."""
    return " ".join(re.sub(r"\\(?:tag|label)\*?\{[^}]*\}", "", latex).split()).strip(" .,;")


def messages(abstract: str, start: int = 1) -> list[dict[str, str]]:
    return [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": f"Abstract:\n{' '.join(abstract.split())}\n\nStart equation: {start}"}]


def parse_block(text: str, start: int) -> tuple[list[dict], bool]:
    complete = END in text
    text = text.split(END, 1)[0]
    equations = []
    for line in text.splitlines():
        if not line.strip():
            continue
        match = LINE.match(line.strip())
        if match:
            index = int(match[1])
            if index != start + len(equations):
                raise ValueError("Equation numbering is not contiguous from the requested index.")
            equations.append({"index": index, "latex": match[2]})
        elif equations:
            equations[-1]["latex"] += " " + line.strip()
        else:
            raise ValueError("Output does not begin with a numbered equation.")
    if not equations or len(equations) > 8:
        raise ValueError("Expected between one and eight equations per block.")
    return equations, complete


def external_spec(result: dict):
    """Wrap predictions without inventing circuit structure or abstract evidence."""
    from .external_spec import ExternalSpec
    from .schemas import MathSpecification

    if result.get("status") == "failed" or not result.get("equations"):
        raise ValueError("No accepted Nemotron equation predictions to implement.")
    assumption = "This is an unverified model-predicted relation, not a verified equation from the paper."
    spec = MathSpecification(
        status="partial", problem=result["abstract"],
        reconstruction_scope="Implement a scoped operation from these predicted equations; disclose all corrections and scope changes.",
        symbols=[], equations=[{
            "id": f"eq_{e['index']}", "label": f"Nemotron prediction {e['index']}",
            "latex": e["latex"], "description": "Numbered LaTeX predicted from the abstract.",
            "provenance": "assumption", "abstract_quote": None,
            "justification": "Output of the abstract-to-LaTeX fine-tune; correctness is unverified.",
            "assumptions": [assumption],
        } for e in result["equations"]], registers=[], initial_state=None, steps=[],
        measurement=None, classical_postprocessing=None, assumptions=[assumption],
        missing_information=["Register layout, input encoding, algorithm steps and measurement were not supplied by this equation-only model."],
    )
    return ExternalSpec(source="nemotron_numbered_latex", abstract=result["abstract"], specification=spec)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--abstract-file", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--model", default="nemotron-quantum")
    parser.add_argument("--base-url", default=os.getenv("NEMOTRON_BASE_URL", "http://127.0.0.1:8000/v1"))
    parser.add_argument("--max-blocks", type=int, default=4)
    parser.add_argument("--max-output-tokens", type=int, default=2048)
    parser.add_argument("--repetition-penalty", type=float, default=1,
                        help="1 matches greedy training-format inference; 1.12 is a tested diagnostic alternative")
    parser.add_argument("--export-spec", type=Path, help="Export a partial spec for the shared Qiskit code stage")
    args = parser.parse_args()
    if args.max_blocks < 1 or not 1 <= args.max_output_tokens <= 16384:
        parser.error("Require positive block count and 1..16384 output tokens.")
    if not 1 <= args.repetition_penalty <= 2:
        parser.error("Repetition penalty must be between 1 and 2.")
    args.out.mkdir(parents=True, exist_ok=False)
    abstract = args.abstract_file.read_text()
    result = {"model": args.model, "task": "abstract_to_numbered_latex",
              "repetition_penalty": args.repetition_penalty,
              "abstract": " ".join(abstract.split()), "equations": [], "complete": False,
              "blocks": [], "api_usd": 0.0, "status": "partial"}
    headers = {"Authorization": "Bearer " + os.environ["NEMOTRON_API_KEY"]} if os.getenv("NEMOTRON_API_KEY") else {}
    with httpx.Client(timeout=300, headers=headers) as client:
        for block in range(args.max_blocks):
            start = len(result["equations"]) + 1
            body = {"model": args.model, "messages": messages(abstract, start),
                    "max_tokens": args.max_output_tokens, "response_format": {"type": "text"},
                    "temperature": 0, "repetition_penalty": args.repetition_penalty, "max_time_seconds": 240}
            (args.out / f"block_{block + 1}_request.json").write_text(json.dumps(body, indent=2))
            print(f"Requesting equations starting at {start} (plain text, training prompt).", flush=True)
            clock = time.monotonic()
            try:
                with generation_slot():
                    response = client.post(args.base_url.rstrip("/") + "/chat/completions", json=body)
                (args.out / f"block_{block + 1}_response.txt").write_text(response.text)
                response.raise_for_status()
                payload = response.json()
                choice = payload["choices"][0]
                text = choice["message"]["content"]
                (args.out / f"block_{block + 1}.txt").write_text(text)
                result["blocks"].append({"start": start, "usage": payload.get("usage"),
                                        "wall_seconds": round(time.monotonic() - clock, 2),
                                        "finish_reason": choice["finish_reason"]})
                if choice["finish_reason"] != "stop":
                    raise ValueError("Generation truncated; block saved but not accepted.")
                predicted, complete = parse_block(text, start)
                existing = {equation_key(e["latex"]) for e in result["equations"]}
                if existing and all(equation_key(e["latex"]) in existing for e in predicted):
                    raise ValueError("Continuation contains no new equation content; stopping.")
                result["equations"].extend(predicted)
                result["unique_equation_predictions"] = len({equation_key(e["latex"]) for e in result["equations"]})
                result["repeated_equation_predictions"] = len(result["equations"]) - result["unique_equation_predictions"]
                result["complete"] = complete
                if complete:
                    result["status"] = "complete"
            except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
                result.update(status="failed", error=str(exc)[:300],
                              failure_stage="transport" if isinstance(exc, httpx.HTTPError) else "generation_or_parse")
            (args.out / "result.json").write_text(json.dumps(result, indent=2))
            if result["complete"] or result["status"] == "failed":
                break
    print(json.dumps({k: v for k, v in result.items() if k not in {"abstract", "equations"}}, indent=2))
    print(f"Saved {len(result['equations'])} numbered predictions to {args.out}.")
    if args.export_spec and result["status"] != "failed":
        args.export_spec.parent.mkdir(parents=True, exist_ok=True)
        args.export_spec.write_text(external_spec(result).model_dump_json(indent=2) + "\n")
    return 2 if result["status"] == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
