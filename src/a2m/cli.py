"""a2m command line."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from a2m import config


def _tasks(args):
    from a2m.tasks import load_manifest, ready_task_ids

    ready = ready_task_ids()
    print("Runnable tasks (curated claim card + sealed vault):")
    for t in ready:
        print(f"  {t}")
    if args.all:
        recs = load_manifest()
        print(f"\nDataset {config.dataset_dir()}: {len(recs)} papers")
        for fam, n in Counter(r.family for r in recs).most_common():
            print(f"  {n:4d}  {fam}")


def _check_vault(args):
    from a2m.evaluators import get
    from a2m.run import load_defaults, make_sandbox
    from a2m.scoring import meets_claim
    from a2m.tasks import load_card, load_vault

    card = load_card(args.task)
    vault, ref = load_vault(args.task)
    sb = make_sandbox(load_defaults(), None, False)
    ev = get(card.evaluator)
    res = {t.name: ev.evaluate(ref, t.params, sb, card)
           for t in card.test_systems + vault.hidden_test_systems}
    for k, v in res.items():
        print(f"{k}: {json.dumps(v.get('metrics') or v.get('error'))}")
    ok = meets_claim(card.criteria, res)
    print(f"reference meets claim: {ok}  (sandbox profile: {sb.profile})")
    sys.exit(0 if ok else 1)


def _run(args):
    from a2m.run import run

    d = run(args.system, args.task, args.seed, args.llm, args.budget_usd, not args.quiet,
            args.sandbox, args.require_isolation)
    print(f"run written to {d}")
    if args.judge:
        _judge_dirs([d], args.llm)


def _judge_dirs(dirs, llm_mode):
    from a2m.judge.sealed import SealedJudge

    judge = SealedJudge(llm_mode)
    for d in dirs:
        r = judge.judge(Path(d))
        print(f"{r.run_id}: claim_reproduced={r.claim_reproduced} "
              f"method_match={r.method_match:.2f} valid_alternative={r.valid_alternative}")


def _judge(args):
    _judge_dirs(args.runs, args.llm)


def _learn(args):
    from a2m.learnings import distill, distill_all

    paths = distill_all(args.runs[0]) if args.all else [distill(d) for d in args.runs]
    for p in paths:
        print(f"wrote {p}")
    if not paths:
        print("no judged runs found")


def _bench(args):
    from a2m.judge.sealed import SealedJudge
    from a2m.learnings import distill
    from a2m.report import write
    from a2m.run import run
    from a2m.tasks import ready_task_ids

    tasks = ready_task_ids() if args.tasks == "all" else args.tasks.split(",")
    systems = args.systems.split(",")
    judge = SealedJudge(args.llm, verbose=not args.quiet)
    for task in tasks:
        for system in systems:
            for seed in range(args.seeds):
                d = run(system, task, seed, args.llm, args.budget_usd, not args.quiet,
                        args.sandbox, args.require_isolation)
                r = judge.judge(d)
                distill(d)
                print(f"{task} {system} s{seed}: reproduced={r.claim_reproduced} "
                      f"match={r.method_match:.2f} ${r.usage.get('usd', 0):.4f}")
    print(write(config.runs_dir(), Path(args.out)).read_text())


def _report(args):
    from a2m.report import write

    print(write(Path(args.runs_dir), Path(args.out)).read_text())


def _curate(args):
    from a2m.curation.drafts import draft, recall_check

    if args.action == "draft":
        print(f"draft written to {draft(args.task, args.model)}; review before use")
    else:
        print(f"recall check written to {recall_check(args.task, args.models.split(','))}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="a2m", description="Abstract2Method benchmark")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("tasks", help="list runnable tasks")
    s.add_argument("--all", action="store_true", help="also summarise the full dataset")
    s.set_defaults(fn=_tasks)

    s = sub.add_parser("check-vault", help="verify a task's reference meets its own claim")
    s.add_argument("task")
    s.set_defaults(fn=_check_vault)

    def common(s):
        s.add_argument("--llm", choices=["anthropic", "mock"], default="anthropic")
        s.add_argument("--budget-usd", type=float, default=None)
        s.add_argument("--sandbox", choices=["auto", "bwrap", "none"], default=None)
        s.add_argument("--require-isolation", action="store_true",
                       help="refuse to run candidate code without bubblewrap")
        s.add_argument("--quiet", action="store_true")

    s = sub.add_parser("run", help="run one system on one task")
    s.add_argument("--system", required=True, help="config name in configs/systems/")
    s.add_argument("--task", required=True)
    s.add_argument("--seed", type=int, default=0)
    s.add_argument("--judge", action="store_true", help="judge the run when it finishes")
    common(s)
    s.set_defaults(fn=_run)

    s = sub.add_parser("judge", help="judge finished runs against the sealed vault")
    s.add_argument("runs", nargs="+")
    s.add_argument("--llm", choices=["anthropic", "mock"], default="anthropic")
    s.set_defaults(fn=_judge)

    s = sub.add_parser("learn", help="distill judged runs into skills/<domain>/learnings/")
    s.add_argument("runs", nargs="+", help="run directories, or one runs/ root with --all")
    s.add_argument("--all", action="store_true", help="walk the directory for judged runs")
    s.set_defaults(fn=_learn)

    s = sub.add_parser("bench", help="systems x tasks x seeds, judged, then reported")
    s.add_argument("--systems", default="swarm,single_agent,central_planner")
    s.add_argument("--tasks", default="all")
    s.add_argument("--seeds", type=int, default=3)
    s.add_argument("--out", default="reports")
    common(s)
    s.set_defaults(fn=_bench)

    s = sub.add_parser("report", help="aggregate judge reports")
    s.add_argument("runs_dir", nargs="?", default=str(config.runs_dir()))
    s.add_argument("--out", default="reports")
    s.set_defaults(fn=_report)

    s = sub.add_parser("curate", help="curator tools (real model required)")
    s.add_argument("action", choices=["draft", "recall"])
    s.add_argument("--task", required=True)
    s.add_argument("--model", default="claude-fable-5-1")
    s.add_argument("--models", default="claude-fable-5-1,claude-opus-5-5,claude-haiku-5-5")
    s.set_defaults(fn=_curate)

    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
