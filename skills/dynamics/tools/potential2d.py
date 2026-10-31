"""Mueller-Brown potential, the standard two-dimensional test surface for transition paths.

Shipped into the sandbox as `a2m_task` and imported by the trusted runner. The surface is
public; what is measured is the quality of the path a candidate returns, which the runner
compares with an independently computed barrier (see evaluators/transition_path.py).
"""

from __future__ import annotations

import numpy as np

A = np.array([-200.0, -100.0, -170.0, 15.0])
AA = np.array([-1.0, -1.0, -6.5, 0.7])
BB = np.array([0.0, 0.0, 11.0, 0.6])
CC = np.array([-10.0, -10.0, -6.5, 0.7])
X0 = np.array([1.0, 0.0, -0.5, -1.0])
Y0 = np.array([0.0, 0.5, 1.5, 1.0])

# The two outer minima, refined by the runner before use.
MINIMUM_A = (-0.558, 1.442)
MINIMUM_B = (0.623, 0.028)


def energy(points) -> np.ndarray:
    """Potential at an (M, 2) array of points; returns shape (M,)."""
    p = np.atleast_2d(np.asarray(points, dtype=float))
    dx = p[:, 0:1] - X0[None, :]
    dy = p[:, 1:2] - Y0[None, :]
    terms = A[None, :] * np.exp(AA * dx * dx + BB * dx * dy + CC * dy * dy)
    return terms.sum(axis=1)


def gradient(points) -> np.ndarray:
    """Gradient dV/d(x, y) at an (M, 2) array of points; returns shape (M, 2)."""
    p = np.atleast_2d(np.asarray(points, dtype=float))
    dx = p[:, 0:1] - X0[None, :]
    dy = p[:, 1:2] - Y0[None, :]
    terms = A[None, :] * np.exp(AA * dx * dx + BB * dx * dy + CC * dy * dy)
    gx = (terms * (2 * AA * dx + BB * dy)).sum(axis=1)
    gy = (terms * (BB * dx + 2 * CC * dy)).sum(axis=1)
    return np.stack([gx, gy], axis=1)


def energy_gradient(points):
    return energy(points), gradient(points)
