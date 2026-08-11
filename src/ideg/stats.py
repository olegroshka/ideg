"""Statistics for AR-010: r-statistic, exact AUC, bootstrap CIs (spec §6.1)."""

from __future__ import annotations

import numpy as np


def r_statistic(evals: np.ndarray, degeneracy_tol: float = 1e-10) -> float:
    """Mean adjacent-gap ratio <r> = <min(g_i, g_{i+1}) / max(g_i, g_{i+1})>.

    GOE ~ 0.5307, Poisson ~ 0.3863. Exact degeneracies (below tol) dropped."""
    e = np.sort(evals)
    gaps = np.diff(e)
    gaps = gaps[gaps > degeneracy_tol]
    r = np.minimum(gaps[:-1], gaps[1:]) / np.maximum(gaps[:-1], gaps[1:])
    return float(np.mean(r))


def auc(x: np.ndarray, y: np.ndarray) -> float:
    """Exact Mann-Whitney AUC: P(X > Y) + 0.5 P(X = Y), symmetrized to
    max(AUC, 1 - AUC) since separation direction is not preregistered."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    greater = np.sum(x[:, None] > y[None, :])
    equal = np.sum(x[:, None] == y[None, :])
    a = (greater + 0.5 * equal) / (len(x) * len(y))
    return float(max(a, 1.0 - a))


def bootstrap_ci_mean(data: np.ndarray, n_resamples: int = 1000,
                      alpha: float = 0.05,
                      rng: np.random.Generator | None = None):
    """BCa bootstrap CI for the mean (spec §6.1)."""
    from scipy.stats import norm

    rng = rng or np.random.default_rng(0)
    data = np.asarray(data, dtype=float)
    n = len(data)
    if n < 2:
        return float(data.mean()), float(data.mean()), float(data.mean())
    idx = rng.integers(0, n, size=(n_resamples, n))
    boots = data[idx].mean(axis=1)
    theta = data.mean()

    # bias correction
    prop = np.mean(boots < theta)
    prop = min(max(prop, 1.0 / (n_resamples + 1)),
               1.0 - 1.0 / (n_resamples + 1))
    z0 = norm.ppf(prop)
    # acceleration via jackknife
    jack = np.array([np.delete(data, i).mean() for i in range(n)])
    jm = jack.mean()
    num = np.sum((jm - jack) ** 3)
    den = 6.0 * np.sum((jm - jack) ** 2) ** 1.5
    a = num / den if den != 0.0 else 0.0

    def bca_quantile(q):
        z = norm.ppf(q)
        adj = norm.cdf(z0 + (z0 + z) / (1.0 - a * (z0 + z)))
        return float(np.quantile(boots, min(max(adj, 0.0), 1.0)))

    return float(theta), bca_quantile(alpha / 2), bca_quantile(1 - alpha / 2)


def cis_disjoint(ci_a, ci_b) -> bool:
    """Disjoint 95% CIs criterion (spec §5.2/§5.3)."""
    return ci_a[2] < ci_b[1] or ci_b[2] < ci_a[1]
