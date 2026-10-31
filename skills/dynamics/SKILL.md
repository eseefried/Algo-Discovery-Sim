---
domain: dynamics
eval_timeout_s: 180
role_bias: {hypothesize: 1.0, implement: 1.2, simulate: 1.1, critique: 1.0}
colony_genome: {min_families: 3, max_attempts: 4, critiques_required: 1}
roles:
  hypothesize: propose how to represent and evolve a path between the two states
  implement: write the path update and its stopping rule
  simulate: run the trusted surface over the test instances
  critique: look for collapsed or drifting paths, endpoints that moved, and paths that cut
    through forbidden regions
libraries: [scipy, numpy, math, cmath, time, itertools, functools, collections,
            heapq, random, fractions, statistics, typing, dataclasses]
tools:
  - module: potential2d
    sandbox: true
    skills:
      - signature: "a2m_task.energy(points) -> ndarray"
        description: "Energy at an (M, 2) array; shape (M,)."
      - signature: "a2m_task.gradient(points) -> ndarray"
        description: "Gradient dV/d(x, y); shape (M, 2)."
      - signature: "a2m_task.energy_gradient(points) -> (ndarray, ndarray)"
        description: Both at once.
---

# Dynamics

## Summary
Rebuild a transition-path method: return the path a system takes between two stable states
over an energy surface.

## Conventions
- A path is an ordered (M, 2) array of points; the first and last must stay at the two given
  stable states.
- The surface is stiff: naive descent pulls every interior point into a minimum and destroys
  the path, so what happens to the points along the path is the whole problem.
- Energy and analytic gradients are available at any set of points at once.
- The barrier of a path is the highest energy along it. A correct path makes that as low as it
  can be, and the runner compares it with an independently computed value, so adding points
  only where the energy is low does not help.
