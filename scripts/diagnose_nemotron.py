"""Bounded local-only base/LoRA comparisons. Requires server --serve-base."""

import argparse
import json
import time
from pathlib import Path

import httpx

from algo_discovery.a2m_spec import check_spec


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--base-url", default="http://127.0.0.1:8000/v1")
    args = parser.parse_args()
    original = json.loads(args.request.read_text())
    abstract = Path("data/circuit_dataset_300_v1/abstracts/arxiv-1411.5949.txt").read_text()
    args.out.mkdir(parents=True, exist_ok=True)
    summaries = []
    for name, model, penalty in [
        ("base_greedy", "nemotron-quantum-base", 1.0),
        ("lora_greedy", "nemotron-quantum", 1.0),
        ("lora_repetition_control", "nemotron-quantum", 1.12),
    ]:
        body = json.loads(json.dumps(original))
        body.update(model=model, max_tokens=2048, max_time_seconds=240,
                    temperature=0, repetition_penalty=penalty, seed=0)
        body["messages"][-1]["content"] += (
            "\nKeep this diagnostic response compact: at most 3 equations and 5 steps. "
            "Use brief descriptions and justifications. Quote abstract evidence once per "
            "equation; do not repeat sentences or pad fields. Preserve honest provenance "
            "and abstain if the construction cannot be reconstructed."
        )
        path = args.out / name
        path.mkdir(exist_ok=True)
        (path / "request.json").write_text(json.dumps(body, indent=2))
        print(f"Starting {name}: max 2048 tokens / 240 generation seconds", flush=True)
        start = time.monotonic()
        report = {"case": name, "schema_valid": False, "spec_checks_passed": False}
        try:
            with httpx.Client(timeout=300) as client:
                response = client.post(args.base_url.rstrip("/") + "/chat/completions", json=body)
            (path / "response.txt").write_text(response.text)
            response.raise_for_status()
            data = response.json()
            choice = data["choices"][0]
            content = choice["message"]["content"]
            (path / "content.txt").write_text(content)
            report.update(finish_reason=choice["finish_reason"], usage=data.get("usage"),
                          adapter_enabled=data.get("adapter_enabled"))
            try:
                import jsonschema

                obj = json.loads(content)
                jsonschema.validate(obj, body["response_format"]["json_schema"]["schema"])
                report["schema_valid"] = True
                _gap, issues, spec = check_spec(json.dumps(obj["specification"]), abstract)
                report.update(spec_checks_passed=not issues and choice["finish_reason"] == "stop", issues=issues,
                              specification_status=spec.status if spec else None)
                (path / "specification.json").write_text(json.dumps(obj["specification"], indent=2))
            except (ValueError, KeyError, TypeError, jsonschema.ValidationError) as exc:
                report["validation_error"] = type(exc).__name__
        except (httpx.HTTPError, ValueError, KeyError, TypeError) as exc:
            report["request_error"] = type(exc).__name__
        report["wall_seconds"] = round(time.monotonic() - start, 2)
        report["output_tokens_per_wall_second"] = round(
            (report.get("usage") or {}).get("completion_tokens", 0) / report["wall_seconds"], 2)
        (path / "summary.json").write_text(json.dumps(report, indent=2))
        summaries.append(report)
        (args.out / "summary.json").write_text(json.dumps(summaries, indent=2))
        print(json.dumps(report), flush=True)
        if report.get("request_error"):
            print("Stopping diagnostics after request failure; no further requests queued.", flush=True)
            break


if __name__ == "__main__":
    main()
