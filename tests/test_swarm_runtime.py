import json
from pathlib import Path

from algo_discovery.config import Settings
from algo_discovery.external_spec import load_spec
from algo_discovery.swarm.cli import export
from algo_discovery.swarm.domain import final_specification, planned_parts
from algo_discovery.swarm.ledger import Ledger
from algo_discovery.swarm.model import ProviderBlocked
from algo_discovery.swarm.models import Contribution
from algo_discovery.swarm.supervisor import run_ecosystem


class FakeExecutor:
    """Picklable offline model stand-in used by real independent spawned processes."""

    def __init__(self, settings):
        pass

    def execute(self, ctx, genotype):
        task = {"requirements": json.dumps(ctx["requirements"])}
        solved = planned_parts(task, set(ctx["already_completed"]), genotype)
        remaining = [p for p in ctx["requirements"] if p not in solved]
        spec = {
            "status": "partial",
            "problem": "Prepare a Hadamard state.",
            "reconstruction_scope": "One qubit.",
            "symbols": [],
            "equations": [
                {
                    "id": "eq_1",
                    "label": "Hadamard",
                    "latex": "H|0> = |+>",
                    "description": "Hadamard gate.",
                    "provenance": "standard_background",
                    "abstract_quote": None,
                    "justification": "Definition.",
                    "assumptions": [],
                }
            ],
            "registers": [{"name": "q", "size": "1", "role": "Data"}],
            "initial_state": "|0>",
            "steps": [{"description": "Apply H.", "equation_ids": ["eq_1"]}],
            "measurement": "Z basis",
            "classical_postprocessing": None,
            "assumptions": ["Tiny fixture instance."],
            "missing_information": [],
        }
        return Contribution(
            completed_requirements=solved,
            specification=spec,
            child_groups=[remaining] if remaining else [],
            changes=["Reviewed the whole fixture."],
            summary="Completed a scoped portion.",
        ), {"input_tokens": 100, "output_tokens": 50, "elapsed": 0.1}


class CrashingExecutor(FakeExecutor):
    def execute(self, ctx, genotype):
        if (
            ctx["attempts"] == 1
            and "circuit_plan" in ctx["requirements"]
            and "problem" not in ctx["requirements"]
        ):
            raise MemoryError("Injected worker crash")
        return super().execute(ctx, genotype)


class BlockedExecutor(FakeExecutor):
    def execute(self, ctx, genotype):
        raise ProviderBlocked("Provider HTTP 400; request ID test.")


def make_ledger(tmp_path):
    ledger = Ledger(tmp_path / "ledger.sqlite3")
    ledger.initialize()
    root = ledger.submit(
        {
            "abstract": "We propose a quantum algorithm using a Hadamard gate.",
            "experiment_scope": "One qubit.",
            "arxiv_id": None,
        },
        max_calls=8,
    )
    return ledger, root


def test_three_real_processes_complete_and_export_blackbox_contract(tmp_path):
    ledger, root = make_ledger(tmp_path)
    run_ecosystem(
        ledger,
        Settings(api_key="not-used"),
        root_id=root,
        max_seconds=20,
        auction_seconds=0.2,
        executor_factory=FakeExecutor,
    )
    summary = ledger.summary(root)
    assert summary["status"] == "completed", summary
    assert len(summary["agents"]) == 3
    assert len(summary["model_calls"]) == 3
    assert summary["paid_cents"] == 50000
    assert summary["escrow_remaining_cents"] == 0
    assert summary["history_valid"]
    assert len({t["agent_id"] for t in summary["tasks"]}) == 3
    assert sorted(a["balance"] for a in summary["agents"]) == [18000, 28000, 28000]
    assert all(a["reserved"] == 0 for a in summary["agents"])
    assert final_specification(ledger, root).status == "partial"
    exported = export(ledger, root, tmp_path / "outputs")
    spec = load_spec(Path(exported["specification"]))
    assert spec.source == "ledger_swarm"
    assert spec.specification.equations[0].id == "eq_1"


def test_actual_crash_requeues_clones_mutates_and_restores_triad(tmp_path):
    ledger, root = make_ledger(tmp_path)
    run_ecosystem(
        ledger,
        Settings(api_key="not-used"),
        root_id=root,
        max_seconds=25,
        lease_seconds=1.5,
        auction_seconds=0.2,
        executor_factory=CrashingExecutor,
    )
    summary = ledger.summary(root)
    assert summary["status"] == "completed", summary
    dead = [a for a in summary["agents"] if a["status"] == "dead"]
    assert len(dead) == 1 and dead[0]["balance"] == 0
    assert len(summary["agents"]) == 4
    replacement = summary["agents"][-1]
    assert replacement["parent_id"] is not None
    assert any(e["kind"] == "genotype_mutated" for e in ledger.history())
    assert summary["paid_cents"] == 50000
    assert summary["history_valid"]


def test_bad_provider_configuration_stops_without_evolution_loop(tmp_path):
    ledger, root = make_ledger(tmp_path)
    run_ecosystem(
        ledger,
        Settings(api_key="not-used"),
        root_id=root,
        max_seconds=15,
        auction_seconds=0.1,
        executor_factory=BlockedExecutor,
    )
    summary = ledger.summary(root)
    assert summary["status"] == "failed"
    assert "HTTP 400" in summary["error"]
    assert len(summary["model_calls"]) == 1
    assert len(summary["agents"]) == 3
