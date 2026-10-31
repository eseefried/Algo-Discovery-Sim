"""Reference: AdaLead (Sinai et al., arXiv:2010.02141, Alg. 1).

Model-guided evolutionary greedy search. Each round: keep as parents only the measured
sequences whose fitness is within (1 - kappa) of the best seen so far - an adaptive filter
that is permissive on flat landscapes and sharp near a peak. Recombine parents, then for each
one perform a *rollout*: mutate at rate 1/L and keep walking while the surrogate's score keeps
improving on the parent. Score the whole candidate pool with the surrogate and measure only
the top batch against the real oracle.

The surrogate here is ridge regression on one-hot sequence features rather than the paper's
CNN ensemble; the paper shows the method is robust to surrogate quality, down to an
uninformative model.
"""

import numpy as np

KAPPA = 0.05        # paper: parents within (1 - kappa) of the best measured fitness
RECOMB_RATE = 0.2   # paper: r, crossover probability per position
RHO = 20            # paper: candidate pool of about rho * batch before measuring
MAX_ROLLOUT = 20
MAX_PASSES = 400    # bound on rollout passes; most rollouts stop after a step or two


def _onehot(seqs, alphabet, length):
    idx = {c: i for i, c in enumerate(alphabet)}
    x = np.zeros((len(seqs), length * len(alphabet)))
    for r, s in enumerate(seqs):
        for p, c in enumerate(s):
            x[r, p * len(alphabet) + idx[c]] = 1.0
    return x


def _fit_surrogate(seqs, ys, alphabet, length, ridge=1.0):
    """Ridge regression on one-hot features; returns a scorer over a list of sequences."""
    x = np.hstack([_onehot(seqs, alphabet, length), np.ones((len(seqs), 1))])
    y = np.asarray(ys, dtype=float)
    w = np.linalg.solve(x.T @ x + ridge * np.eye(x.shape[1]), x.T @ y)

    def scorer(batch):
        feats = np.hstack([_onehot(batch, alphabet, length), np.ones((len(batch), 1))])
        return feats @ w

    return scorer


def _mutate(seq, alphabet, rate, rng):
    chars = list(seq)
    for i in range(len(chars)):
        if rng.random() < rate:
            chars[i] = alphabet[rng.integers(len(alphabet))]
    return "".join(chars)


def _recombine(parents, rng, rate):
    if len(parents) < 2:
        return list(parents)
    out = []
    for _ in range(len(parents)):
        a, b = parents[rng.integers(len(parents))], parents[rng.integers(len(parents))]
        child, source = [], a
        for i in range(len(a)):
            if rng.random() < rate:
                source = b if source is a else a
            child.append(source[i])
        out.append("".join(child))
    return out


def propose(measured, spec):
    alphabet, length = spec["alphabet"], int(spec["length"])
    batch = int(spec["batch_size"])
    rng = np.random.default_rng(int(spec["seed"]) + int(spec["round_index"]))

    if not measured:  # no information yet: a random starting batch
        return ["".join(alphabet[i] for i in rng.integers(len(alphabet), size=length))
                for _ in range(batch)]

    seqs = [m[0] for m in measured]
    ys = [m[1] for m in measured]
    surrogate = _fit_surrogate(seqs, ys, alphabet, length)
    seen = set(seqs)

    best = max(ys)
    threshold = best * (1 - KAPPA) if best > 0 else best - abs(best) * KAPPA
    parents = [s for s, y in zip(seqs, ys) if y >= threshold] or [seqs[int(np.argmax(ys))]]
    parents = _recombine(parents, rng, RECOMB_RATE) + parents

    # Fill a candidate pool of about rho * batch by rolling out from the parents. A rollout
    # keeps mutating while the surrogate says the child is still at least as good as its seed;
    # most rollouts are short, so the pass is repeated until the pool is full.
    pool: dict[str, float] = {}
    target_size = RHO * batch
    for _ in range(MAX_PASSES):
        if len(pool) >= target_size:
            break
        for parent in parents:
            base = float(surrogate([parent])[0])
            child = parent
            for _ in range(MAX_ROLLOUT):
                nxt = _mutate(child, alphabet, 1.0 / length, rng)
                nxt_score = float(surrogate([nxt])[0])
                if nxt_score < base:
                    break
                child = nxt
                if child not in seen:
                    pool[child] = nxt_score
            if len(pool) >= target_size:
                break

    while len(pool) < batch:          # never hand back a short batch and waste budget
        cand = _mutate(parents[int(rng.integers(len(parents)))], alphabet, 1.0 / length, rng)
        if cand not in seen:
            pool[cand] = float(surrogate([cand])[0])

    ranked = sorted(pool, key=lambda s: -pool[s])
    return ranked[:batch]
