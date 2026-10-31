"""NVIDIA ALCHEMI Toolkit backend (optional).

Used as an *independent* recomputation of cluster energies: the runner's own NumPy
Lennard-Jones and ALCHEMI's Warp kernel must agree, which catches a scoring bug in either.
Install with `pip install 'abstract2method[alchemi]'`. Without it, scoring is unaffected and
the check simply reports as unavailable. ALCHEMI runs on GPU where one is present and falls
back to CPU through Warp.
"""

from __future__ import annotations

import os

TOLERANCE = 1e-6
_state: dict[str, object] = {}


def available() -> bool:
    if os.getenv("A2M_DISABLE_ALCHEMI"):
        return False
    if "ok" not in _state:
        try:
            import nvalchemi  # noqa: F401

            _state["ok"] = True
        except Exception:  # noqa: BLE001 - any import/runtime failure means unavailable
            _state["ok"] = False
    return bool(_state["ok"])


def energy(positions) -> float | None:
    """Lennard-Jones energy in reduced units via ALCHEMI, or None when unavailable."""
    if not available():
        return None
    try:
        import numpy as np
        import torch
        from nvalchemi.data import AtomicData, Batch
        from nvalchemi.models.lj import LennardJonesModelWrapper
        from nvalchemi.neighbors import compute_neighbors

        pos = np.asarray(positions, dtype=float).reshape(-1, 3)
        model = _state.get("model")
        if model is None:
            # A cutoff far beyond any cluster diameter makes this the full pair sum, matching
            # the reduced-unit definition the runner scores with.
            model = LennardJonesModelWrapper(epsilon=1.0, sigma=1.0, cutoff=50.0)
            _state["model"] = model
        data = AtomicData(positions=torch.tensor(pos, dtype=torch.float64),
                          atomic_numbers=torch.full((len(pos),), 18, dtype=torch.long))
        batch = Batch.from_data_list([data])
        compute_neighbors(batch, config=model.model_config.neighbor_config)
        return float(model(batch)["energy"].sum())
    except Exception:  # noqa: BLE001 - never let an optional backend break scoring
        return None


def cross_check(positions, reference_energy: float) -> str:
    """One-line verdict comparing ALCHEMI's energy with the runner's own."""
    value = energy(positions)
    if value is None:
        return "alchemi:unavailable"
    delta = abs(value - reference_energy)
    return ("alchemi:agrees" if delta <= TOLERANCE * max(1.0, abs(reference_energy))
            else f"alchemi:DISAGREES by {delta:.3e}")
