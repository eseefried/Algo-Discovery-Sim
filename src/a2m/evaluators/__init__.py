from a2m.evaluators.affine_boolean import AffineBooleanId
from a2m.evaluators.base import Evaluator
from a2m.evaluators.modular_adder import ModularAdder

REGISTRY: dict[str, Evaluator] = {e.name: e for e in (AffineBooleanId(), ModularAdder())}


def get(name: str) -> Evaluator:
    try:
        return REGISTRY[name]
    except KeyError:
        raise KeyError(f"no evaluator named {name!r}; known: {sorted(REGISTRY)}") from None
