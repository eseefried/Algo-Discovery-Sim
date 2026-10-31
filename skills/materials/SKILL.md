---
domain: materials
eval_timeout_s: 300
role_bias: {hypothesize: 1.0, implement: 1.3, simulate: 1.0, critique: 0.9}
colony_genome: {min_families: 3, max_attempts: 4, critiques_required: 1}
roles:
  hypothesize: propose a search strategy over the energy surface
  implement: write the search and the local optimization it relies on
  simulate: run the trusted energy model over the test cluster sizes
  critique: look for broken-up clusters, sizes that only work by luck, and searches that stall
    on larger clusters
libraries: [scipy, ase, numpy, math, cmath, time, itertools, functools, collections,
            heapq, random, fractions, statistics, typing, dataclasses]
tools:
  - module: lj
    sandbox: true
    skills:
      - signature: "a2m_task.energy(positions) -> float"
        description: Total energy of an (N, 3) array.
      - signature: "a2m_task.energy_forces(positions) -> (float, ndarray)"
        description: Energy and the (N, 3) analytic forces, -dE/dx.
      - signature: "a2m_task.random_cluster(n, seed, radius=5.5) -> ndarray"
        description: N atoms placed uniformly in a sphere, for starting points.
      - signature: "a2m_task.is_connected(positions, cutoff=1.6) -> bool"
        description: Whether every atom is in contact with the cluster.
backends:
  - NVIDIA ALCHEMI Toolkit for batched GPU energy and force evaluation, when installed
    (pip install 'abstract2method[alchemi]'). Used as an independent recomputation of every
    scored energy.
---

# Materials

## Summary
Rebuild a structure-search method: find the lowest-energy arrangement of atoms in a cluster
and return the coordinates.

## Conventions
- Positions are an (N, 3) array in reduced Lennard-Jones units; energies are in units of the
  well depth.
- The energy surface has very many local minima, and the number grows steeply with N, so plain
  local optimization from a random start almost never reaches the best structure.
- Atoms can drift apart during a search. A cluster whose atoms are not all in contact is
  rejected, however low its reported energy.
- Energy and analytic forces are both available, so gradient-based local optimization is cheap.
  Budget by wall clock.
