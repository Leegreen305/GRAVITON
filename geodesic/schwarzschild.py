"""
Schwarzschild metric geodesics.

The Schwarzschild line element in Schwarzschild coordinates (t, r, theta, phi):

    ds^2 = -(1 - r_s/r) c^2 dt^2 + (1 - r_s/r)^{-1} dr^2
           + r^2 dtheta^2 + r^2 sin^2(theta) dphi^2

where r_s = 2GM/c^2 is the Schwarzschild radius.

Reference:
    Schwarzschild, K. (1916). Sitzungsber. Preuss. Akad. Wiss. Berlin, 189.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, Tuple

from graviton.constants import G, C


class SchwarzschildGeodesic:
    """
    Compute geodesics in the Schwarzschild spacetime.

    Uses the effective potential formalism for equatorial orbits
    (theta = pi/2) to reduce the problem to a 1-D equation.

    Parameters
    ----------
    mass : float
        Central mass M [kg].
    """

    def __init__(self, mass: float):
        self.M = mass
        self.r_s = 2.0 * G * mass / C ** 2  # Schwarzschild radius

    # ------------------------------------------------------------------
    # Metric
    # ------------------------------------------------------------------

    def metric(self, coords: np.ndarray) -> np.ndarray:
        """
        4x4 Schwarzschild metric tensor at coordinates [t, r, theta, phi].
        """
        t, r, theta, phi = coords
        r_safe = max(abs(r), 1e-30)
        f = 1.0 - self.r_s / r_safe

        g = np.zeros((4, 4))
        g[0, 0] = -f * C ** 2
        g[1, 1] = 1.0 / f if abs(f) > 1e-30 else 1e30
        g[2, 2] = r_safe ** 2
        g[3, 3] = r_safe ** 2 * np.sin(theta) ** 2
        return g

    # ------------------------------------------------------------------
    # Effective potential (equatorial, theta = pi/2)
    # ------------------------------------------------------------------

    def effective_potential(self, r: np.ndarray, L: float, mu: float = 1.0) -> np.ndarray:
        """
        Effective potential for equatorial geodesics:

            V_eff(r) = -GMmu/r + L^2/(2 mu r^2) - G M L^2/(mu c^2 r^3)

        The last term is the GR correction absent in Newtonian gravity.

        Parameters
        ----------
        r : ndarray
            Radial coordinate [m].
        L : float
            Specific angular momentum [m^2/s].
        mu : float
            Particle mass parameter (1 for massive, 0 for photon).

        For massless particles (photons), use:
            V_eff = L^2/(2 r^2) - G M L^2/(c^2 r^3)
        """
        r_safe = np.where(r <= 0, 1e-30, r)
        if mu > 0:
            V = (
                -G * self.M * mu / r_safe
                + L ** 2 / (2.0 * mu * r_safe ** 2)
                - G * self.M * L ** 2 / (mu * C ** 2 * r_safe ** 3)
            )
        else:
            V = L ** 2 / (2.0 * r_safe ** 2) - G * self.M * \
                L ** 2 / (C ** 2 * r_safe ** 3)
        return V

    # ------------------------------------------------------------------
    # Equatorial orbit integration
    # ------------------------------------------------------------------

    def integrate_orbit(
        self,
        r0: float,
        phi0: float,
        dr_dtau0: float,
        L: float,
        tau_span: Tuple[float, float],
        n_points: int = 10000,
    ) -> Dict[str, np.ndarray]:
        """
        Integrate equatorial geodesic in (r, phi) using the effective
        potential formalism.

        d^2 r / d tau^2 = -dV_eff/dr
        d phi / d tau   = L / r^2

        Returns dict with 'tau', 'r', 'phi', 'x', 'y'.
        """

        def rhs(tau, state):
            r, phi, v_r = state
            r_safe = max(abs(r), self.r_s * 1.01)

            # -dV_eff/dr (numerical)
            eps = r_safe * 1e-6
            Vp = float(self.effective_potential(
                np.array([r_safe + eps]), L)[0])
            Vm = float(self.effective_potential(
                np.array([r_safe - eps]), L)[0])
            dVdr = (Vp - Vm) / (2.0 * eps)

            a_r = -dVdr
            dphi = L / r_safe ** 2
            return [v_r, dphi, a_r]

        state0 = [r0, phi0, dr_dtau0]
        tau_eval = np.linspace(tau_span[0], tau_span[1], n_points)

        sol = solve_ivp(
            rhs,
            tau_span,
            state0,
            t_eval=tau_eval,
            method="DOP853",
            rtol=1e-10,
            atol=1e-12,
        )

        r = sol.y[0]
        phi = sol.y[1]

        return {
            "tau": sol.t,
            "r": r,
            "phi": phi,
            "x": r * np.cos(phi),
            "y": r * np.sin(phi),
        }

    # ------------------------------------------------------------------
    # ISCO (innermost stable circular orbit)
    # ------------------------------------------------------------------

    def isco_radius(self) -> float:
        """
        Innermost stable circular orbit radius for Schwarzschild:
            r_ISCO = 3 r_s = 6 GM/c^2
        """
        return 3.0 * self.r_s

    def circular_orbit_velocity(self, r: float) -> float:
        """
        Orbital velocity for a circular orbit at radius r:
            v = sqrt(GM/r) * 1/sqrt(1 - 3GM/(rc^2))
        """
        return np.sqrt(G * self.M / r) / np.sqrt(1.0 - 3.0 * G * self.M / (r * C ** 2))
