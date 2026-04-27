"""
Generic geodesic equation solver in curved spacetime.

The geodesic equation:
    d^2 x^mu / d tau^2  +  Gamma^mu_{alpha beta} (dx^alpha/dtau)(dx^beta/dtau) = 0

where Gamma^mu_{alpha beta} are the Christoffel symbols of the metric.

Reference:
    Misner, Thorne & Wheeler (1973). "Gravitation." Ch. 25.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Callable, Dict, Tuple


class GeodesicSolver:
    """
    Solve the geodesic equation given a metric function and its
    numerical Christoffel symbols.

    This solver works in coordinate time or affine parameter and uses
    numerical differentiation of the metric to compute Christoffel symbols.

    Parameters
    ----------
    metric_func : callable
        Function(coords) -> 4x4 ndarray of g_{mu nu}
        where coords is a 1-D array [x0, x1, x2, x3].
    ndim : int
        Number of spacetime dimensions (default 4).
    """

    def __init__(self, metric_func: Callable, ndim: int = 4):
        self.metric_func = metric_func
        self.ndim = ndim

    def _numerical_christoffel(self, coords: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """
        Compute Christoffel symbols Gamma^mu_{alpha beta} numerically via
        central-difference differentiation of the metric.

        Gamma^mu_{alpha beta} = (1/2) g^{mu nu} (d_alpha g_{nu beta}
                                + d_beta g_{nu alpha} - d_nu g_{alpha beta})
        """
        n = self.ndim
        g = self.metric_func(coords)

        # Metric derivatives: dg[sigma][alpha][beta] = d g_{alpha beta} / d x^sigma
        dg = np.zeros((n, n, n))
        for sigma in range(n):
            coords_p = coords.copy()
            coords_m = coords.copy()
            coords_p[sigma] += eps
            coords_m[sigma] -= eps
            g_p = self.metric_func(coords_p)
            g_m = self.metric_func(coords_m)
            dg[sigma] = (g_p - g_m) / (2.0 * eps)

        # Inverse metric
        g_inv = np.linalg.inv(g)

        # Christoffel symbols
        gamma = np.zeros((n, n, n))
        for mu in range(n):
            for alpha in range(n):
                for beta in range(n):
                    s = 0.0
                    for nu in range(n):
                        s += 0.5 * g_inv[mu, nu] * (
                            dg[alpha][nu][beta]
                            + dg[beta][nu][alpha]
                            - dg[nu][alpha][beta]
                        )
                    gamma[mu, alpha, beta] = s
        return gamma

    def geodesic_rhs(self, tau, state: np.ndarray) -> np.ndarray:
        """
        Right-hand side of the geodesic ODE system.

        state = [x0, x1, x2, x3, u0, u1, u2, u3]
        where u^mu = dx^mu / d tau.
        """
        n = self.ndim
        coords = state[:n]
        u = state[n:]

        gamma = self._numerical_christoffel(coords)

        dx = u.copy()
        du = np.zeros(n)
        for mu in range(n):
            s = 0.0
            for alpha in range(n):
                for beta in range(n):
                    s += gamma[mu, alpha, beta] * u[alpha] * u[beta]
            du[mu] = -s

        return np.concatenate([dx, du])

    def integrate(
        self,
        x0: np.ndarray,
        u0: np.ndarray,
        tau_span: Tuple[float, float],
        n_points: int = 5000,
        **kwargs,
    ) -> Dict[str, np.ndarray]:
        """
        Integrate the geodesic equation.

        Parameters
        ----------
        x0 : (4,) initial coordinates.
        u0 : (4,) initial 4-velocity.
        tau_span : (tau_start, tau_end).
        n_points : number of output points.

        Returns dict with 'tau' and 'coords' (shape n_points x 4) and 'velocity'.
        """
        state0 = np.concatenate([x0, u0])
        tau_eval = np.linspace(tau_span[0], tau_span[1], n_points)

        sol = solve_ivp(
            self.geodesic_rhs,
            tau_span,
            state0,
            t_eval=tau_eval,
            method="DOP853",
            rtol=1e-10,
            atol=1e-12,
            **kwargs,
        )

        n = self.ndim
        return {
            "tau": sol.t,
            "coords": sol.y[:n].T,  # shape (n_points, 4)
            "velocity": sol.y[n:].T,
        }
