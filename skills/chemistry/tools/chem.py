"""Penalized logP on SMILES, the standard molecular-optimization objective.

Shipped into the sandbox as `a2m_task` and imported by the trusted runner, so candidates
optimize exactly the function the runner scores with. Public objective: the task is the search
strategy over chemical space.
"""

from __future__ import annotations

import os
import sys

from rdkit import Chem, DataStructs, RDLogger
from rdkit.Chem import Crippen, RDConfig, rdFingerprintGenerator

RDLogger.DisableLog("rdApp.*")

_sa_path = os.path.join(RDConfig.RDContribDir, "SA_Score")
if _sa_path not in sys.path:
    sys.path.append(_sa_path)
import sascorer

# Normalisation over 250k ZINC molecules, as used by the penalized-logP literature.
LOGP_MEAN, LOGP_STD = 2.4570953396190123, 1.434324401111988
SA_MEAN, SA_STD = -3.0525811293166134, 0.8335207024513095
CYCLE_MEAN, CYCLE_STD = -0.0485696876403053, 0.2860212110245455


def parse(smiles: str):
    """Mol object, or None when the string is not a valid molecule."""
    if not isinstance(smiles, str) or not smiles:
        return None
    return Chem.MolFromSmiles(smiles)


def is_valid(smiles: str) -> bool:
    return parse(smiles) is not None


def canonical(smiles: str) -> str | None:
    mol = parse(smiles)
    return Chem.MolToSmiles(mol) if mol is not None else None


def largest_ring_penalty(mol) -> float:
    cycles = mol.GetRingInfo().AtomRings()
    largest = max((len(c) for c in cycles), default=0)
    return float(max(0, largest - 6))


def score(smiles: str) -> float:
    """Penalized logP: normalized (logP - synthetic accessibility - large-ring penalty).

    Returns -inf for anything that is not a valid molecule.
    """
    mol = parse(smiles)
    if mol is None or mol.GetNumAtoms() == 0:
        return float("-inf")
    try:
        logp = (Crippen.MolLogP(mol) - LOGP_MEAN) / LOGP_STD
        sa = (-sascorer.calculateScore(mol) - SA_MEAN) / SA_STD
        ring = (-largest_ring_penalty(mol) - CYCLE_MEAN) / CYCLE_STD
    except (ValueError, RuntimeError):
        return float("-inf")
    return float(logp + sa + ring)


def score_many(smiles_list) -> list[float]:
    return [score(s) for s in smiles_list]


_morgan = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=2048)


def fingerprint(smiles: str):
    """Morgan fingerprint, radius 2, or None for an invalid molecule."""
    mol = parse(smiles)
    return _morgan.GetFingerprint(mol) if mol is not None else None


def similarity(a: str, b: str) -> float:
    """Tanimoto similarity between two molecules; 0.0 if either is invalid."""
    fa, fb = fingerprint(a), fingerprint(b)
    if fa is None or fb is None:
        return 0.0
    return float(DataStructs.TanimotoSimilarity(fa, fb))
