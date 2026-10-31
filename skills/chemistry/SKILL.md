---
domain: chemistry
eval_timeout_s: 240
role_bias: {hypothesize: 1.2, implement: 1.0, simulate: 1.0, critique: 1.1}
colony_genome: {min_families: 3, max_attempts: 3, critiques_required: 1}
roles:
  hypothesize: propose how to represent molecules and how to explore chemical space
  implement: write the generator and the selection loop
  simulate: run the trusted scorer over the test instances
  critique: look for invalid or duplicate molecules, answers that drift away from the starting
    molecule, and strategies that only work on the listed seeds
libraries: [rdkit, selfies, numpy, math, cmath, time, itertools, functools, collections,
            heapq, random, fractions, statistics, typing, dataclasses]
tools:
  - module: chem
    sandbox: true
    skills:
      - signature: "a2m_task.score(smiles: str) -> float"
        description: The objective. Returns -inf for anything that is not a valid molecule.
      - signature: "a2m_task.score_many(smiles: list[str]) -> list[float]"
        description: Scores a list.
      - signature: "a2m_task.similarity(a: str, b: str) -> float"
        description: Tanimoto similarity on Morgan fingerprints, radius 2.
      - signature: "a2m_task.is_valid(smiles: str) -> bool"
        description: Whether RDKit can parse the string.
      - signature: "a2m_task.canonical(smiles: str) -> str | None"
        description: Canonical SMILES, for de-duplicating.
backends:
  - NVIDIA BioNeMo NIM (MolMIM, GenMol) for generation, when A2M_BIONEMO_URL is set
---

# Chemistry

## Summary
Rebuild a molecular design method: generate and refine candidate molecules against a scoring
function, and return the molecules you found.

## Conventions
- Molecules are SMILES strings. Many edits to a SMILES string produce something that is not a
  molecule at all, so validity has to be handled, not assumed.
- The score is unbounded above but degenerate: trivial structures such as very long carbon
  chains score well. Tasks therefore constrain the answer, for example by requiring it to stay
  chemically similar to a given starting molecule.
- Scoring one molecule is cheap, around a millisecond. Budget your time by wall clock rather
  than by counting score calls.
- RDKit is available for parsing, fingerprints, descriptors and substructure work.
