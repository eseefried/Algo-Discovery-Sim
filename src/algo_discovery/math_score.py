"""Model-free math-likeness scores: agent equations vs. equations extracted from the paper.

Evaluator-only: reads data/.../equations/ (never shown to the agent) after the run.
Scores are lexical/structural LaTeX similarity, not proof of mathematical equivalence.
Unrelated equations share generic tokens (=, |, \\frac) and score ~0.45, so the headline
math_score is chance-adjusted against the same agent equations scored on unrelated papers.
"""

import argparse
import csv
import json
import math
import random
import re
import statistics
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

DATASET = Path("data/circuit_dataset_300_v1")
# Calibrated by inspection: >=0.7 is usually the same equation idea, >=0.85 near-identical.
MATCH_THRESHOLD = 0.7
STRONG_THRESHOLD = 0.85
CONTROL_PAPERS = 5
MAX_TOKENS = 200

SKIP_SECTIONS = re.compile(r"reference|bibliograph|acknowledg", re.IGNORECASE)
DROP = re.compile(
    r"\\(?:tag|label)\{[^}]*\}|\\(?:nonumber|notag|displaystyle|textstyle|left|right|big+l?r?|Big+l?r?)"
    r"|\\[,;:!> ]|\\q?quad|~|&|\$"
)
SPLIT = re.compile(r"\\\\|\\q?quad|\\Rightarrow|\\implies|,\s*\\;")
TOKEN = re.compile(r"\\[a-zA-Z]+|[A-Za-z]|\d+|[^\s{}]")
GREEK = {
    "alpha", "beta", "gamma", "delta", "epsilon", "varepsilon", "zeta", "eta", "theta",
    "vartheta", "iota", "kappa", "lambda", "mu", "nu", "xi", "rho", "sigma", "tau",
    "phi", "varphi", "chi", "psi", "omega", "Gamma", "Delta", "Theta", "Lambda", "Xi",
    "Sigma", "Phi", "Psi", "Omega",
}  # fmt: skip
# \pi and \hbar are constants, not variables, so they stay literal.


def normalize(latex: str) -> str:
    text = re.sub(r"\\ket\{([^}]*)\}", r"|\1\\rangle", latex)
    text = re.sub(r"\\bra\{([^}]*)\}", r"\\langle \1|", text)
    text = re.sub(r"\\(?:mathrm|rm|mathbf|mathcal|mathbb|operatorname|text)\s*", "", text)
    text = re.sub(r"\\[td]frac", r"\\frac", text)
    return DROP.sub(" ", text).strip(" .,;")


def tokens(latex: str) -> list[str]:
    return TOKEN.findall(normalize(latex))[:MAX_TOKENS]


def skeleton(toks: list[str]) -> list[str]:
    """Mask variable names so renamed notation still matches structurally."""
    return [
        "v" if (len(t) == 1 and t.isalpha()) or t.lstrip("\\") in GREEK else t for t in toks
    ]


class Candidate:
    def __init__(self, latex: str, parent: str):
        self.parent = parent
        self.toks = tokens(latex)
        self.bag = Counter(self.toks)
        self.skel = skeleton(self.toks)


def pieces(latex: str, parent: str) -> list[Candidate]:
    """The whole expression plus each row/clause, so combined lines can match singly."""
    parts = [latex] + [p for p in SPLIT.split(latex) if p.strip()]
    found = [Candidate(p, parent) for p in dict.fromkeys(parts)]
    return [c for c in found if len(c.toks) >= 4]


def similarity(a: Candidate, b: Candidate, idf: dict[str, float]) -> float:
    shared = sum(min(n, b.bag[t]) * idf.get(t, 1.0) for t, n in a.bag.items() if t in b.bag)
    total = sum(n * idf.get(t, 1.0) for t, n in (a.bag + b.bag).items())
    lexical = 2 * shared / total if total else 0.0
    structural = SequenceMatcher(None, a.skel, b.skel, autojunk=False).ratio()
    return 0.5 * lexical + 0.5 * structural


def best(agent: list[Candidate], paper: list[Candidate], idf) -> tuple[float, Candidate | None]:
    pairs = [(similarity(a, p, idf), p) for a in agent for p in paper]
    return max(pairs, key=lambda pair: pair[0], default=(0.0, None))


def paper_equations(arxiv_id: str) -> list[dict]:
    path = DATASET / "equations" / f"arxiv-{arxiv_id}.jsonl"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    return [
        r
        for r in records
        if r["kind"] == "display" and not SKIP_SECTIONS.search(r.get("section") or "")
    ]


def score_paper(agent_eqs: list[dict], paper_eqs: list[dict], idf) -> dict:
    paper_cands = [c for r in paper_eqs for c in pieces(r["latex"], r["id"])]
    agent_cands = {e["id"]: pieces(e["latex"], e["id"]) for e in agent_eqs}
    matches = []
    for eq in agent_eqs:
        score, hit = best(agent_cands[eq["id"]], paper_cands, idf)
        matches.append({"agent_equation": eq, "score": score, "paper_id": hit and hit.parent})
    # Recall over numbered (core) paper equations, falling back to all displayed ones.
    core = [r for r in paper_eqs if r.get("equation_number")] or paper_eqs
    flat_agent = [c for cands in agent_cands.values() for c in cands]
    recall_scores = [best(flat_agent, pieces(r["latex"], r["id"]), idf)[0] for r in core]
    precision = statistics.fmean(m["score"] for m in matches) if matches else 0.0
    recall = statistics.fmean(recall_scores) if recall_scores else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "core_paper_equations": len(core),
        "core_equations_recovered": sum(score >= MATCH_THRESHOLD for score in recall_scores),
        "matched_agent_equations": sum(m["score"] >= MATCH_THRESHOLD for m in matches),
        "strong_agent_matches": sum(m["score"] >= STRONG_THRESHOLD for m in matches),
        "matches": matches,
    }


def load_runs(results: Path) -> list[dict]:
    runs = []
    for path in sorted((results / "logs").glob("*.json")):
        text = path.read_text(encoding="utf-8").strip()
        if not text:
            continue
        summary = json.loads(text)
        run = {"arxiv_id": path.stem, "summary": summary, "equations": None}
        artifacts = summary.get("equations", {}).get("artifacts")
        if artifacts and Path(artifacts, "result.json").exists():
            result = json.loads(Path(artifacts, "result.json").read_text(encoding="utf-8"))
            run["equations"] = result["specification"]["equations"]
        runs.append(run)
    return runs


def build_idf(ids: list[str]) -> dict[str, float]:
    documents = Counter()
    for arxiv_id in ids:
        seen = {t for r in paper_equations(arxiv_id) for t in tokens(r["latex"])}
        documents.update(seen)
    return {t: math.log((1 + len(ids)) / (1 + n)) + 1 for t, n in documents.items()}


def main() -> int:
    parser = argparse.ArgumentParser(description="Score agent equations against paper equations.")
    parser.add_argument("--results", type=Path, default=Path("baseline_results"))
    parser.add_argument("--out", type=Path, help="Defaults to RESULTS/eval")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    out = args.out or args.results / "eval"
    out.mkdir(parents=True, exist_ok=True)

    with open(DATASET / "catalog.csv", encoding="utf-8") as handle:
        catalog = {r["arxiv_id"]: r for r in csv.DictReader(handle)}
    runs = load_runs(args.results)
    scored = [r for r in runs if r["equations"]]
    idf = build_idf(list(catalog))
    rng = random.Random(args.seed)
    print(f"Scoring {len(scored)} papers with agent equations ({len(runs)} finished runs).")

    rows, match_lines = [], []
    by_provenance = defaultdict(list)
    for index, run in enumerate(scored, 1):
        arxiv_id, summary = run["arxiv_id"], run["summary"]
        paper_eqs = paper_equations(arxiv_id)
        result = score_paper(run["equations"], paper_eqs, idf)
        # Control: the same agent equations against unrelated papers.
        others = rng.sample([i for i in catalog if i != arxiv_id], CONTROL_PAPERS)
        control = statistics.fmean(
            score_paper(run["equations"], paper_equations(o), idf)["f1"] for o in others
        )
        # 0 = no better than unrelated papers, 1 = perfect; negative = worse than chance.
        math_score = (result["f1"] - control) / (1 - control) if control < 1 else 0.0
        paper_latex = {r["id"]: r["latex"] for r in paper_eqs}
        for m in result["matches"]:
            eq = m["agent_equation"]
            by_provenance[eq["provenance"]].append(m["score"])
            match_lines.append(
                {
                    "arxiv_id": arxiv_id,
                    "agent_equation_id": eq["id"],
                    "provenance": eq["provenance"],
                    "agent_latex": eq["latex"],
                    "score": round(m["score"], 4),
                    "match": "strong" if m["score"] >= STRONG_THRESHOLD
                    else "match" if m["score"] >= MATCH_THRESHOLD else "none",
                    "paper_equation_id": m["paper_id"],
                    "paper_latex": paper_latex.get(m["paper_id"]),
                }
            )
        code = summary.get("code", {})
        rows.append(
            {
                "arxiv_id": arxiv_id,
                "title": catalog[arxiv_id]["title"],
                "family": catalog[arxiv_id]["family"],
                "equation_status": summary["equations"]["status"],
                "stopped_at": summary.get("stopped_at") or "",
                "validation_status": code.get("validation_status", ""),
                "simulation_status": summary.get("simulation", {}).get("status", ""),
                # No paper-specific reference exists yet, so exact correctness is unscored.
                "exact_correctness": "no_reference",
                "math_score": round(math_score, 4),
                "agent_equations": len(run["equations"]),
                "matched_agent_equations": result["matched_agent_equations"],
                "strong_agent_matches": result["strong_agent_matches"],
                "core_paper_equations": result["core_paper_equations"],
                "core_equations_recovered": result["core_equations_recovered"],
                "precision": round(result["precision"], 4),
                "recall": round(result["recall"], 4),
                "f1": round(result["f1"], 4),
                "control_f1": round(control, 4),
            }
        )
        print(f"[{index}/{len(scored)}] {arxiv_id} math_score={rows[-1]['math_score']:.3f}")

    if not rows:
        print("No finished runs with equations yet.")
        return 1
    with open(out / "math_scores.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with open(out / "equation_matches.jsonl", "w", encoding="utf-8") as handle:
        handle.writelines(json.dumps(line) + "\n" for line in match_lines)

    def mean(values):
        return round(statistics.fmean(values), 4) if values else None

    families = defaultdict(list)
    for row in rows:
        families[row["family"]].append(row)
    summary = {
        "papers_scored": len(rows),
        "run_summaries": len(runs),
        "method": "pair similarity = 0.5 * IDF-weighted token Dice + 0.5 * variable-masked "
        "sequence ratio; precision = agent->paper best match, recall = numbered paper eqs->agent; "
        "math_score = (F1 - control F1) / (1 - control F1), control = same agent equations vs "
        f"{CONTROL_PAPERS} random other papers. Lexical/structural similarity, not equivalence.",
        "match_threshold": MATCH_THRESHOLD,
        "strong_threshold": STRONG_THRESHOLD,
        "mean_math_score": mean([r["math_score"] for r in rows]),
        "median_math_score": round(statistics.median(r["math_score"] for r in rows), 4),
        "papers_beating_control": sum(r["math_score"] > 0 for r in rows),
        "mean_f1": mean([r["f1"] for r in rows]),
        "mean_control_f1": mean([r["control_f1"] for r in rows]),
        "agent_equations": sum(r["agent_equations"] for r in rows),
        "agent_equations_matched": sum(r["matched_agent_equations"] for r in rows),
        "agent_equations_strong": sum(r["strong_agent_matches"] for r in rows),
        "core_paper_equations": sum(r["core_paper_equations"] for r in rows),
        "core_paper_equations_recovered": sum(r["core_equations_recovered"] for r in rows),
        "reached_simulation": sum(r["simulation_status"] in {"simulated", "reference_passed"} for r in rows),
        "exact_correctness": "not scored: the dataset has no ground-truth circuits or outputs",
        "by_provenance": {
            p: {"equations": len(s), "mean_similarity": mean(s), "matched": sum(x >= MATCH_THRESHOLD for x in s)}
            for p, s in sorted(by_provenance.items())
        },
        "by_family": {
            f: {"papers": len(r), "mean_math_score": mean([x["math_score"] for x in r])}
            for f, r in sorted(families.items())
        },
    }  # fmt: skip
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "by_family"}, indent=2))
    print(f"Wrote {out}/math_scores.csv, equation_matches.jsonl, summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
