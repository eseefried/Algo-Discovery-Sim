"""Regenerate the four cross-domain claim cards and sealed vaults.

Run from the repository root: `uv run python scripts/build_domain_tasks.py`. Abstracts come
from the arXiv API so they are verbatim. Rubrics are written from the papers' method sections
by a curator (see docs/ADDING_TASKS.md) and live here so they can be reviewed in one place.
Targets in `criteria` are calibrated against the reference implementations with margin; see
tests/test_domain_evaluators.py, which fails if a reference stops meeting its own claim.
"""

from __future__ import annotations

import html
import json
import pathlib
import re
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from a2m.domains import get as get_domain  # noqa: E402
from a2m.evaluators import get as get_evaluator  # noqa: E402

ARXIV = ("https://export.arxiv.org/api/query?id_list="
         "cond-mat/9803344,1909.11655,2010.02141,cond-mat/0205527&max_results=10")

TASK_IDS = {
    "cond-mat/9803344": "arxiv-cond-mat-9803344",
    "1909.11655": "arxiv-1909.11655",
    "2010.02141": "arxiv-2010.02141",
    "cond-mat/0205527": "arxiv-cond-mat-0205527",
}

# Coined names for the paper's own method, blanked so the swarm cannot look the method up by
# name. Descriptive wording that states the claim is always kept.
REDACTIONS = {
    "arxiv-cond-mat-9803344": ["basin-hopping", "basin hopping"],
    "arxiv-2010.02141": ["AdaLead"],
}


def fetch_abstracts() -> dict[str, dict]:
    with urllib.request.urlopen(ARXIV, timeout=60) as r:  # noqa: S310 - fixed https URL
        xml = r.read().decode()
    out = {}
    for entry in re.findall(r"<entry>(.*?)</entry>", xml, re.S):
        def field(name, e=entry):
            return html.unescape(re.sub(r"\s+", " ", re.search(
                rf"<{name}>(.*?)</{name}>", e, re.S).group(1))).strip()

        url = field("id")
        key = url.split("/abs/")[1].rsplit("v", 1)[0]
        out[key] = {"title": field("title"), "abstract": field("summary"), "url": url}
    missing = set(TASK_IDS) - set(out)
    if missing:
        raise SystemExit(f"arXiv did not return {sorted(missing)}")
    return out


def redact(task_id: str, abstract: str) -> str:
    for term in REDACTIONS.get(task_id, []):
        abstract = re.sub(re.escape(term), "[METHOD]", abstract, flags=re.I)
    return abstract


CARDS = {
    "arxiv-cond-mat-9803344": {
        "domain": "materials",
        "evaluator": "cluster_global_opt",
        "claim": ("Reliably locate the lowest-energy structure of a Lennard-Jones cluster of up "
                  "to a few tens of atoms from random starting configurations."),
        "criteria": [
            {"metric": "success_rate", "comparator": ">=", "target": 1.0, "tolerance": 0.0,
             "scale": 1.0},
        ],
        "test_systems": [
            {"name": "n7", "params": {"n": 7, "seeds": [0, 1], "time_budget_s": 10}},
        ],
        "limits": {"eval_timeout_s": 300},
        "notes": ("Scope: clusters of 7 to 17 atoms in reduced Lennard-Jones units, where the "
                  "global minima are tabulated and a run fits in seconds. The paper's results "
                  "for up to 110 atoms, and its seeded runs from neighbouring sizes, are out "
                  "of scope. Known limitation: at these sizes the funnel is wide enough that "
                  "repeated local optimization from random starts also reaches the global "
                  "minimum, so reproducing the claim does not by itself imply the paper's "
                  "method; the rubric score is what separates them, and a run that reproduces "
                  "the claim by another route is reported as a valid alternative. The sizes "
                  "where the distinction bites (38, 75-77, 98) need far more compute than a "
                  "bounded benchmark run. Development case, not held out."),
    },
    "arxiv-1909.11655": {
        "domain": "chemistry",
        "evaluator": "molecule_opt",
        "claim": ("Substantially improve the penalized logP of a given molecule while keeping "
                  "the result chemically similar to it."),
        "criteria": [
            {"metric": "mean_improvement", "comparator": ">=", "target": 1.0, "tolerance": 0.0,
             "scale": 2.0},
            {"metric": "success_rate", "comparator": ">=", "target": 1.0, "tolerance": 0.0,
             "scale": 1.0},
            {"metric": "validity", "comparator": ">=", "target": 1.0, "tolerance": 0.0,
             "scale": 1.0},
        ],
        "test_systems": [
            {"name": "delta06", "params": {
                "starts": ["CC(=O)Oc1ccccc1C(=O)O", "CN1C=NC2=C1C(=O)N(C)C(=O)N2C"],
                "similarity_threshold": 0.6, "n_return": 10, "seed": 0,
                "time_budget_s": 45}},
        ],
        "limits": {"eval_timeout_s": 240},
        "notes": ("Scope: similarity-constrained improvement of penalized logP, the paper's "
                  "constrained task. The unconstrained version is excluded on purpose: its "
                  "objective is maximised by degenerate structures such as a long carbon "
                  "chain, which any method can emit without reasoning. The paper's "
                  "property-targeted generation and its 250k-molecule reference set are out "
                  "of scope. The visible system uses the tighter similarity threshold of 0.6 "
                  "because at 0.4 the constraint is loose enough that blind chain extension "
                  "passes without any search. Development case, not held out."),
    },
    "arxiv-2010.02141": {
        "domain": "biology",
        "evaluator": "sequence_design",
        "claim": ("Design RNA sequences that bind a hidden target, reaching near-optimal binding "
                  "within a fixed budget of measurements spread over a few rounds."),
        "criteria": [
            {"metric": "best_fitness", "comparator": ">=", "target": 0.9, "tolerance": 0.0,
             "scale": 0.5},
            {"metric": "invalid_proposed", "comparator": "<=", "target": 0, "tolerance": 0.0,
             "scale": 50.0},
        ],
        "test_systems": [
            {"name": "rna14_a", "params": {"length": 14, "target_length": 50, "target_seed": 11,
                                           "rounds": 8, "batch_size": 100, "seed": 0}},
        ],
        "limits": {"eval_timeout_s": 120},
        "notes": ("Scope: single hidden RNA target, length-14 designs, binding measured by "
                  "duplex folding energy. The paper's transcription-factor and protein "
                  "landscapes, and its comparisons against specific baselines, are out of "
                  "scope. Development case, not held out."),
    },
    "arxiv-cond-mat-0205527": {
        "domain": "dynamics",
        "evaluator": "transition_path",
        "claim": ("Compute the transition path between two stable states of a rugged energy "
                  "surface, recovering the true barrier height."),
        "criteria": [
            {"metric": "barrier_error", "comparator": "<=", "target": 0.5, "tolerance": 0.0,
             "scale": 20.0},
            {"metric": "endpoint_error", "comparator": "<=", "target": 0.02, "tolerance": 0.0,
             "scale": 0.5},
        ],
        "test_systems": [
            {"name": "mb_30", "params": {"n_images": 30, "seed": 0, "time_budget_s": 20}},
        ],
        "limits": {"eval_timeout_s": 180},
        "notes": ("Scope: the zero-temperature minimum-energy path on a two-dimensional "
                  "Mueller-Brown surface, the standard test problem for this class of method. "
                  "The paper's finite-temperature sampling, free-energy barriers and transition "
                  "rates are out of scope, as are its Lennard-Jones and magnetic-film examples. "
                  "Note the abstract itself describes evolving smooth curves with an intrinsic "
                  "parametrization, so this task is more revealing than most. Development case, "
                  "not held out."),
    },
}

VAULTS = {
    "arxiv-cond-mat-9803344": {
        "reference_family": "minimize_then_metropolis_basin_hopping",
        "hidden_test_systems": [
            {"name": "n10", "params": {"n": 10, "seeds": [2, 3], "time_budget_s": 20}},
            {"name": "n13", "params": {"n": 13, "seeds": [4, 5], "time_budget_s": 30}},
            {"name": "n17_tight", "params": {"n": 17, "seeds": [6, 7, 8], "time_budget_s": 6}},
        ],
        "reported_numbers": {
            "lowest_energies": {"5": -9.103852, "13": -44.326801, "38": -173.928427,
                                "55": -279.248470, "110": -621.788224},
            "mc_temperature": 0.8, "acceptance_ratio_target": 0.5,
            "steps_per_unseeded_run": 5000,
            "source": "Table 1 and Secs. 2-3 of cond-mat/9803344",
        },
        "rubric": [
            {"id": "r1", "weight": 2.5,
             "keywords": ["local minim", "relax", "minimize", "quench", "transformed"],
             "text": ("Transforms the energy surface by local minimization: a configuration is "
                      "scored by the energy of the minimum reached from it, not by its own "
                      "energy, which turns the surface into a set of plateaus and leaves the "
                      "global minimum unchanged.")},
            {"id": "r2", "weight": 2.5,
             "keywords": ["metropolis", "accept", "temperature", "exp("],
             "text": ("Runs a Monte Carlo walk that accepts or rejects a step using a Metropolis "
                      "criterion at finite temperature applied to the *minimized* energies, "
                      "rather than only accepting downhill steps.")},
            {"id": "r3", "weight": 1.0,
             "keywords": ["reset", "current", "from the minimum", "relaxed"],
             "text": ("After an accepted step the walk continues from the minimized "
                      "configuration, so it hops between basins instead of wandering the raw "
                      "surface.")},
            {"id": "r4", "weight": 1.0,
             "keywords": ["acceptance", "step size", "0.5", "adjust", "tune"],
             "text": ("Adapts the displacement size during the run to hold the acceptance ratio "
                      "near a target of about one half.")},
            {"id": "r5", "weight": 0.5,
             "keywords": ["angular", "surface atom", "pair energy", "highest energy atom",
                          "container", "evapor"],
             "text": ("Handles poorly bound surface atoms specially, for example by moving the "
                      "atom with the highest pair energy to a new point on the cluster surface, "
                      "or by containing atoms so the cluster cannot evaporate.")},
            {"id": "r6", "weight": 0.5,
             "keywords": ["gradient", "bfgs", "conjugate", "jac", "forces"],
             "text": "Uses a gradient-based local optimizer for the minimization step."},
        ],
        "provenance": ("Rubric written from cond-mat/9803344 Secs. 2-3 before any scored run. "
                       "Global minima independently reproduced by multistart optimization in "
                       "tests/test_domain_evaluators.py."),
    },
    "arxiv-1909.11655": {
        "reference_family": "selfies_mutation_ga_with_discriminator",
        "hidden_test_systems": [
            {"name": "delta04_unseen", "params": {
                "starts": ["CC(C)Cc1ccc(cc1)C(C)C(=O)O", "CC(=O)Nc1ccc(O)cc1"],
                "similarity_threshold": 0.4, "n_return": 10, "seed": 3,
                "time_budget_s": 45}},
            {"name": "delta06_tight", "params": {
                "starts": ["CC(=O)Oc1ccccc1C(=O)O", "CC(C)Cc1ccc(cc1)C(C)C(=O)O"],
                "similarity_threshold": 0.6, "n_return": 10, "seed": 4,
                "time_budget_s": 45}},
        ],
        "reported_numbers": {
            "max_penalized_logp": {"random_selfies": 6.19, "ga_beta0": 12.61,
                                   "ga_discriminator_beta10": 13.31, "ga_time_dependent": 20.72},
            "constrained_improvement": {"delta_0.4": 5.93, "delta_0.6": 3.44},
            "constrained_success_rate": {"delta_0.4": 1.0, "delta_0.6": 0.998},
            "population": 500, "generations_unconstrained": 100,
            "source": "Table 1 and Secs. 2-3 of arXiv:1909.11655",
        },
        "rubric": [
            {"id": "r1", "weight": 2.5,
             "keywords": ["selfies", "sf.encoder", "sf.decoder", "robust"],
             "text": ("Represents molecules in a string encoding whose every mutation still "
                      "decodes to a valid molecule (SELFIES), rather than mutating SMILES and "
                      "discarding the invalid results.")},
            {"id": "r2", "weight": 1.5,
             "keywords": ["insert", "replace", "mutat", "no crossover", "point mutation"],
             "text": ("Evolves by random single-character insertions and replacements on that "
                      "string encoding, without a crossover operator.")},
            {"id": "r3", "weight": 2.5,
             "keywords": ["discriminator", "beta", "fitness =", "j(m)", "penalty"],
             "text": ("Scores each molecule with the objective plus a weighted discriminator "
                      "term, F = J + beta * D, so fitness is not the objective alone.")},
            {"id": "r4", "weight": 2.0,
             "keywords": ["train", "neural", "network", "classifier", "logistic", "reference",
                          "zinc", "epoch"],
             "text": ("The discriminator is a model trained during the run to tell the evolving "
                      "population apart from a reference set of real molecules, and is retrained "
                      "as the population changes, so molecules that linger lose fitness and the "
                      "search is pushed off stale optima.")},
            {"id": "r5", "weight": 1.0,
             "keywords": ["rank", "replace", "survivor", "fittest", "worst"],
             "text": ("Replaces the weakest members of the population with mutants of the "
                      "fittest, rather than restarting or keeping everything.")},
            {"id": "r6", "weight": 0.5,
             "keywords": ["stagnat", "adaptive", "increase", "switch"],
             "text": ("Raises the discriminator's weight when the search stops improving, as an "
                      "adaptive escape from stagnation.")},
            {"id": "r7", "weight": 0.5,
             "keywords": ["penal", "1e6", "similarity", "constraint", "-10"],
             "text": ("Keeps violating molecules out by giving them a large fitness penalty "
                      "rather than by filtering only at the end.")},
        ],
        "provenance": "Rubric written from arXiv:1909.11655 Secs. 2-3 before any scored run.",
    },
    "arxiv-2010.02141": {
        "reference_family": "threshold_greedy_model_guided_rollouts",
        "hidden_test_systems": [
            {"name": "rna14_b", "params": {"length": 14, "target_length": 50, "target_seed": 29,
                                           "rounds": 8, "batch_size": 100, "seed": 1}},
            {"name": "rna20_tight", "params": {"length": 20, "target_length": 60,
                                               "target_seed": 31, "rounds": 6, "batch_size": 60,
                                               "seed": 2}},
        ],
        "reported_numbers": {
            "kappa": 0.05, "recombination_rate": 0.2, "mutation_rate": "1/L",
            "model_queries_per_round": "rho * batch, rho = 20", "ground_truth_budget": 1000,
            "source": "Alg. 1 and Secs. 3-4 of arXiv:2010.02141",
        },
        "rubric": [
            {"id": "r1", "weight": 2.5,
             "keywords": ["threshold", "kappa", "1 - ", "within", "max(", "best"],
             "text": ("Chooses parents by an adaptive threshold relative to the best measured "
                      "fitness so far - keeping everything within a small fraction of the best - "
                      "rather than a fixed top-k or the single best sequence.")},
            {"id": "r2", "weight": 1.5,
             "keywords": ["mutat", "1 / length", "1/l", "recombin", "crossover"],
             "text": ("Generates children from those parents by per-position mutation at a rate "
                      "of about one over the sequence length, and by recombining parents.")},
            {"id": "r3", "weight": 2.5,
             "keywords": ["rollout", "while", "keep mutating", "until", "improv", "break"],
             "text": ("Extends each child by repeated mutation for as long as a surrogate model "
                      "says it is still at least as good as its parent, stopping that walk when "
                      "the surrogate score drops - a rollout, not a single mutation step.")},
            {"id": "r4", "weight": 2.0,
             "keywords": ["model", "surrogate", "fit", "predict", "regress", "ensemble"],
             "text": ("Fits a surrogate model to the measurements collected so far and uses it "
                      "to screen a candidate pool much larger than the measurement batch.")},
            {"id": "r5", "weight": 1.0,
             "keywords": ["top", "sort", "argsort", "batch_size", "budget"],
             "text": ("Spends the real measurement budget only on the top-scoring candidates "
                      "from that pool, staying within the batch size each round.")},
        ],
        "provenance": ("Rubric written from arXiv:2010.02141 Alg. 1 and Secs. 3-4 before any "
                       "scored run."),
    },
    "arxiv-cond-mat-0205527": {
        "reference_family": "normal_force_string_with_reparametrization",
        "hidden_test_systems": [
            {"name": "mb_12_coarse", "params": {"n_images": 12, "seed": 1, "time_budget_s": 20}},
            {"name": "mb_reversed", "params": {"n_images": 24, "seed": 2, "time_budget_s": 20,
                                               "start": [0.623, 0.028], "end": [-0.558, 1.442]}},
        ],
        "reported_numbers": {
            "images_used": 200, "comparison": "critical points match transition path sampling",
            "acceleration": "limited-memory Broyden in the perpendicular hyperplane",
            "source": "Secs. 2-3 of cond-mat/0205527",
        },
        "rubric": [
            {"id": "r1", "weight": 1.0,
             "keywords": ["images", "discret", "linspace", "interpolat", "curve"],
             "text": ("Represents the path as an ordered set of images between the two states "
                      "and evolves all of them together.")},
            {"id": "r2", "weight": 3.0,
             "keywords": ["normal", "perpendicular", "project", "tangent", "dot", "- (g"],
             "text": ("Moves each image by only the component of the force perpendicular to the "
                      "path, explicitly projecting out the component along the tangent, which is "
                      "what stops the images from sliding into the minima.")},
            {"id": "r3", "weight": 1.0,
             "keywords": ["tangent", "gradient(path", "diff", "finite difference", "unit"],
             "text": "Computes the tangent from the path itself at each step."},
            {"id": "r4", "weight": 2.5,
             "keywords": ["reparametr", "arc length", "arclength", "equal", "cumsum", "interp"],
             "text": ("Redistributes the images along the curve to an even spacing (equal arc "
                      "length) after the motion step, instead of holding them apart with spring "
                      "forces between neighbours.")},
            {"id": "r5", "weight": 0.5,
             "keywords": ["endpoint", "fixed", "path[0]", "path[-1]"],
             "text": "Holds the two endpoints fixed at the given stable states."},
            {"id": "r6", "weight": 0.5,
             "keywords": ["max", "barrier", "highest"],
             "text": ("Reads the barrier as the highest energy along the converged path.")},
        ],
        "provenance": "Rubric written from cond-mat/0205527 Secs. 2-3 before any scored run.",
    },
}


def main():
    papers = fetch_abstracts()
    tasks_dir = ROOT / "data" / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    for arxiv_id, task_id in TASK_IDS.items():
        spec = CARDS[task_id]
        paper = papers[arxiv_id]
        profile = get_domain(spec["domain"])
        card = {
            "task_id": task_id,
            "domain": spec["domain"],
            "evaluator": spec["evaluator"],
            "abstract": redact(task_id, paper["abstract"]),
            "claim": spec["claim"],
            "criteria": spec["criteria"],
            "interface": get_evaluator(spec["evaluator"]).interface,
            "test_systems": spec["test_systems"],
            "limits": spec["limits"],
            "allowed_imports": list(profile.libraries),
            "curation_status": "curated",
            "notes": spec["notes"] + f" Paper: {paper['url']}",
        }
        (tasks_dir / f"{task_id}.json").write_text(json.dumps(card, indent=2) + "\n")

        vault = {"task_id": task_id, "reference_file": "reference.py", **VAULTS[task_id]}
        vdir = ROOT / "data" / "vaults" / task_id
        vdir.mkdir(parents=True, exist_ok=True)
        if not (vdir / "reference.py").exists():
            raise SystemExit(f"{task_id}: write data/vaults/{task_id}/reference.py first")
        (vdir / "vault.json").write_text(json.dumps(vault, indent=2) + "\n")
        print(f"wrote {task_id} ({spec['domain']})")


if __name__ == "__main__":
    main()
