"""Reference: genetic algorithm on SELFIES with a neural discriminator (Nigam et al.,
arXiv:1909.11655, Secs. 2-3).

Molecules are SELFIES strings, so random single-character insertions and replacements always
decode to a valid molecule - that robustness is what makes mutation-only evolution possible
with no crossover. Fitness is F(m) = J(m) + beta * D(m): the objective plus a discriminator
trained each generation to tell the evolving population from a reference set of real
molecules. Because long-surviving molecules are trained against for longer, their
discriminator score decays, which pushes the population off stale optima and keeps diversity
up. Replacement is by fitness rank: mutants of the fittest replace the weakest.

The discriminator is logistic regression on RDKit descriptors over a small built-in reference
set, standing in for the paper's fully connected network trained against 250k ZINC molecules.
"""

import time

import numpy as np
import selfies as sf
from rdkit import Chem
from rdkit.Chem import Descriptors

import a2m_task

BETA = 10.0             # paper: discriminator weight in the unconstrained runs
BETA_STAGNANT = 1000.0  # paper: GA-D(t) raises the weight while the search stagnates
STAGNATION = 8
INSERT_PROBABILITY = 0.5
PHENYL_PROBABILITY = 0.04    # paper: a domain rule that directly adds a phenyl group
PHENYL = "[C][=C][C][=C][C][=C][Ring1][=Branch1]"
CONSTRAINT_PENALTY = 1e6     # paper: similarity-constrained runs penalise violations heavily
POPULATION = 100

# Stand-in for the paper's ZINC reference sample: common drug-like molecules.
REFERENCE = [
    "CC(=O)Oc1ccccc1C(=O)O", "CN1C=NC2=C1C(=O)N(C)C(=O)N2C", "CC(C)Cc1ccc(cc1)C(C)C(=O)O",
    "CC(=O)Nc1ccc(O)cc1", "CN1CCC[C@H]1c1cccnc1", "OC(=O)c1ccccc1O",
    "Clc1ccccc1C1=NCC(=O)Nc2ccc(Cl)cc12", "CC(C)NCC(O)COc1ccccc1CC=C",
    "CN(C)CCCN1c2ccccc2CCc2ccccc21", "COc1ccc2cc(ccc2c1)C(C)C(=O)O",
    "CC12CCC3C(CCc4cc(O)ccc34)C1CCC2O", "NC(=O)c1ccccc1O", "CCN(CC)CCNC(=O)c1ccc(N)cc1",
    "Cc1ccccc1Nc1ccccc1C(=O)O", "CC(C)(C)NCC(O)c1ccc(O)c(CO)c1", "CCOC(=O)c1ccccc1N",
    "c1ccc2[nH]ccc2c1", "CC(N)Cc1ccccc1", "OCC1OC(O)C(O)C(O)C1O", "CCCCOC(=O)c1ccccc1",
]


def _descriptors(mol):
    return np.array([
        Descriptors.MolWt(mol), Descriptors.MolLogP(mol), Descriptors.TPSA(mol),
        Descriptors.NumHDonors(mol), Descriptors.NumHAcceptors(mol),
        Descriptors.NumRotatableBonds(mol), Descriptors.RingCount(mol),
        Descriptors.FractionCSP3(mol), float(mol.GetNumAtoms()),
    ], dtype=float)


def _features(smiles_list):
    rows = []
    for s in smiles_list:
        mol = Chem.MolFromSmiles(s)
        rows.append(_descriptors(mol) if mol is not None else np.zeros(9))
    return np.array(rows)


class Discriminator:
    """Logistic regression: 1 = looks like a real molecule, 0 = looks GA-generated."""

    def __init__(self):
        self.w = None
        self.mu = self.sigma = None

    def train(self, generated, epochs=120, lr=0.3):
        x = np.vstack([_features(generated), _features(REFERENCE)])
        y = np.concatenate([np.zeros(len(generated)), np.ones(len(REFERENCE))])
        self.mu, self.sigma = x.mean(0), x.std(0) + 1e-9
        xs = np.hstack([(x - self.mu) / self.sigma, np.ones((len(x), 1))])
        w = np.zeros(xs.shape[1])
        for _ in range(epochs):
            p = 1.0 / (1.0 + np.exp(-np.clip(xs @ w, -30, 30)))
            w -= lr * xs.T @ (p - y) / len(y)
        self.w = w

    def score(self, smiles_list):
        if self.w is None:
            return np.zeros(len(smiles_list))
        xs = np.hstack([(_features(smiles_list) - self.mu) / self.sigma,
                        np.ones((len(smiles_list), 1))])
        return 1.0 / (1.0 + np.exp(-np.clip(xs @ self.w, -30, 30)))


def _mutate(selfie, alphabet, rng):
    if rng.random() < PHENYL_PROBABILITY:
        return selfie + PHENYL            # the paper's domain-specific rule
    tokens = list(sf.split_selfies(selfie))
    if not tokens:
        tokens = ["[C]"]
    i = int(rng.integers(len(tokens) + 1))
    token = alphabet[int(rng.integers(len(alphabet)))]
    if rng.random() < INSERT_PROBABILITY or not tokens:
        tokens.insert(i, token)           # insertion
    else:
        tokens[min(i, len(tokens) - 1)] = token   # replacement
    return "".join(tokens)


def run(spec):
    rng = np.random.default_rng(int(spec["seed"]))
    deadline = time.time() + float(spec["time_budget_s"]) * 0.85
    start = spec["start"]
    threshold = float(spec["similarity_threshold"])
    alphabet = sorted(sf.get_semantic_robust_alphabet())

    pool = [sf.encoder(start)]
    while len(pool) < POPULATION:
        pool.append(_mutate(pool[int(rng.integers(len(pool)))], alphabet, rng))

    discriminator = Discriminator()
    hall_of_fame: dict[str, float] = {}      # constraint-satisfying molecules only
    best_seen, stagnant = -np.inf, 0

    while time.time() < deadline:
        smiles = [sf.decoder(s) for s in pool]
        objective = np.array([a2m_task.score(s) for s in smiles])
        objective = np.where(np.isfinite(objective), objective, -CONSTRAINT_PENALTY)
        similarity = np.array([a2m_task.similarity(s, start) for s in smiles])
        satisfies = similarity >= threshold

        for s, j, ok in zip(smiles, objective, satisfies):
            if ok and j > -1e5 and a2m_task.is_valid(s):
                hall_of_fame[a2m_task.canonical(s)] = float(j)

        beta = BETA_STAGNANT if stagnant >= STAGNATION else BETA
        # Fitness is the objective plus the discriminator, with violations pushed out.
        fitness = objective + beta * discriminator.score(smiles)
        fitness = np.where(satisfies, fitness, fitness - CONSTRAINT_PENALTY)
        discriminator.train(smiles)

        top = float(objective[satisfies].max()) if satisfies.any() else -np.inf
        stagnant = stagnant + 1 if top <= best_seen + 1e-9 else 0
        best_seen = max(best_seen, top)

        order = np.argsort(-fitness)
        survivors = [pool[i] for i in order[: max(2, POPULATION // 2)]]
        pool = list(survivors)
        while len(pool) < POPULATION:         # mutants of the fittest replace the weakest
            parent = survivors[int(rng.integers(len(survivors)))]
            pool.append(_mutate(parent, alphabet, rng))

    ranked = sorted(hall_of_fame, key=lambda s: -hall_of_fame[s])
    return ranked[: int(spec["n_return"])]
