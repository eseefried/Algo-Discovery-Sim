from a2m.evaluators.affine_boolean import AffineBooleanId
from a2m.evaluators.base import CallEvaluator, CircuitEvaluator, Evaluator
from a2m.evaluators.cluster_global_opt import ClusterGlobalOpt
from a2m.evaluators.fixed_point_search import FixedPointSearch
from a2m.evaluators.modular_adder import ModularAdder
from a2m.evaluators.molecule_opt import MoleculeOpt
from a2m.evaluators.sequence_design import SequenceDesign
from a2m.evaluators.transition_path import TransitionPath

REGISTRY: dict[str, Evaluator] = {e.name: e for e in (
    AffineBooleanId(), ModularAdder(), FixedPointSearch(),   # quantum
    ClusterGlobalOpt(),                          # materials
    MoleculeOpt(),                               # chemistry
    SequenceDesign(),                            # biology
    TransitionPath(),                            # dynamics
)}

__all__ = ["REGISTRY", "CallEvaluator", "CircuitEvaluator", "Evaluator", "by_domain", "get"]


def get(name: str) -> Evaluator:
    try:
        return REGISTRY[name]
    except KeyError:
        raise KeyError(f"no evaluator named {name!r}; known: {sorted(REGISTRY)}") from None


def by_domain(domain: str) -> list[str]:
    return sorted(n for n, e in REGISTRY.items() if e.domain == domain)
