"""Reference: the zero-temperature string method (E, Ren & Vanden-Eijnden, cond-mat/0205527).

A string of images between the two stable states evolves under the component of the force
*normal to the string*, phi_t = -(grad V)_perp, where (grad V)_perp = grad V - (grad V . t) t
and t is the unit tangent. After each motion step the images are redistributed to equal arc
length by interpolation, which is what the intrinsic parametrization buys over a chain of
states held together by springs. Endpoints stay fixed at the two minima.
"""

import time

import numpy as np

import a2m_task

DT = 1e-4            # explicit step on the normal force
MAX_STEPS = 20000
TOLERANCE = 1e-6     # convergence on the largest image displacement per step


def _reparametrize(path):
    """Redistribute images to equal arc length along the current curve."""
    seg = np.linalg.norm(np.diff(path, axis=0), axis=1)
    s = np.concatenate([[0.0], np.cumsum(seg)])
    if s[-1] <= 0:
        return path
    target = np.linspace(0.0, s[-1], len(path))
    return np.stack([np.interp(target, s, path[:, k]) for k in range(path.shape[1])], axis=1)


def _tangents(path):
    t = np.gradient(path, axis=0)
    norm = np.linalg.norm(t, axis=1, keepdims=True)
    return t / np.maximum(norm, 1e-12)


def find_path(start, end, spec):
    start, end = np.asarray(start, float), np.asarray(end, float)
    m = max(6, int(spec.get("n_images", 30)))
    deadline = time.time() + float(spec["time_budget_s"]) * 0.9

    alpha = np.linspace(0.0, 1.0, m)[:, None]
    path = start + alpha * (end - start)          # straight-line initial string

    for step in range(MAX_STEPS):
        grad = a2m_task.gradient(path)
        tang = _tangents(path)
        normal = grad - (grad * tang).sum(axis=1, keepdims=True) * tang   # (grad V)_perp
        normal[0] = normal[-1] = 0.0              # endpoints are fixed at the minima
        shift = DT * normal
        cap = 0.05                                 # guard against the stiff outer regions
        big = np.linalg.norm(shift, axis=1) > cap
        if big.any():
            shift[big] *= (cap / np.linalg.norm(shift[big], axis=1))[:, None]
        path = _reparametrize(path - shift)
        if np.abs(shift).max() < TOLERANCE or (step % 50 == 0 and time.time() > deadline):
            break

    path[0], path[-1] = start, end
    return path.tolist()
