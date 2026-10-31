"""RNA binding fitness via ViennaRNA duplex folding.

Only the trusted runner imports this: the binding target is hidden, so the candidate never
receives the oracle. It proposes batches of sequences and the runner measures them.
"""

from __future__ import annotations

import RNA

ALPHABET = "ACGU"
_PAIR = {"A": "U", "U": "A", "C": "G", "G": "C"}


def reverse_complement(target: str) -> str:
    return "".join(_PAIR[c] for c in reversed(target))


def random_target(length: int, seed: int) -> str:
    import random

    rng = random.Random(seed)
    return "".join(rng.choice(ALPHABET) for _ in range(length))


def duplex_energy(sequence: str, target: str) -> float:
    """Free energy of the sequence-target duplex in kcal/mol (negative binds more tightly)."""
    return float(RNA.duplexfold(sequence, target).energy)


def fitness(sequence: str, target: str, normalizer: float) -> float:
    """Binding strength normalized so the target's perfect complement scores about 1.0."""
    return -duplex_energy(sequence, target) / normalizer


def best_binder(target: str, length: int) -> str:
    """Strongest binder of `length` nucleotides: the complement of the best target window."""
    windows = [reverse_complement(target[i:i + length])
               for i in range(max(1, len(target) - length + 1))]
    return min(windows, key=lambda s: duplex_energy(s, target))


def normalizer_for(target: str, length: int) -> float:
    """Binding energy of the best binder of this length, so top fitness is about 1.0."""
    return max(1e-9, -duplex_energy(best_binder(target, length), target))


def is_valid(sequence, length: int) -> bool:
    return (isinstance(sequence, str) and len(sequence) == length
            and all(c in ALPHABET for c in sequence))
