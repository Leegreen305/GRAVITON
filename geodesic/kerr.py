"""
Kerr metric geodesics — rotating (spinning) black hole spacetime.

The Kerr metric in Boyer-Lindquist coordinates (t, r, theta, phi):

    ds^2 = -(1 - r_s r / Sigma) c^2 dt^2
           - (2 r_s r a sin^2(theta) / Sigma) c dt dphi
           + (Sigma / Delta) dr^2
           + Sigma dtheta^2
           + (r^2 + a^2 + r_s r a^2 sin^2(theta)/Sigma) sin^2(theta) dphi^2

where:
    a = J/(Mc)         spin parameter [m]
    Sigma = r^2 + a^2 cos^2(theta)
    Delta = r^2 - r_s r + a^2

Reference:
    Kerr, R.P. (1963). Phys. Rev. Lett. 11, 237.
    Boyer & Lindquist (1967). J. Math. Phys. 8, 265.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Dict, Tuple

from graviton.constants import G, C


class KerrGeodesic:
    """
    Compute geodesics in the Kerr spacetime.

    Parameters
    ----------
    mass : float
        Central mass M [kg].
    spin_parameter : float
        Dimensionless spin a* = a c / (GM) in [0, 1).
        The dimensional spin is a = a* GM/c^2.
    """

    def __init__(self, mass: float, spin_parameter: float = 0.9):
        self.M = mass
        self.a_star = spin_parameter
        self.r_s = 2.0 * G * mass / C ** 2
        self.a = spin_parameter * G * mass / C ** 2  # dimensional spin [m]

    # ------------------------------------------------------------------
    # Auxiliary functions
    # ------------------------------------------------------------------

    def _sigma(self, r, theta):
        return r ** 2 + self.a ** 2 * np.cos(theta) ** 2

    def _delta(self, r):
        return r ** 2 - self.r_s * r + self.a ** 2

    # ------------------------------------------------------------------
    # Metric
    # ------------------------------------------------------------------

    def metric(self, coords: np.ndarray) -> np.ndarray:
        """
        4x4 Kerr metric tensor at Boyer-Lindquist coordinates [t, r, theta, phi].
        """
        t, r, theta, phi = coords
        r_safe = max(abs(r), 1e-30)
        sigma = self._sigma(r_safe, theta)
        delta = self._delta(r_safe)

        g = np.zeros((4, 4))
        sin2 = np.sin(theta) ** 2

        g[0, 0] = -(1.0 - self.r_s * r_safe / sigma) * C ** 2
        g[0, 3] = -(self.r_s * r_safe * self.a * sin2 / sigma) * C
        g[3, 0] = g[0, 3]
        g[1, 1] = sigma / delta if abs(delta) > 1e-30 else 1e30
        g[2, 2] = sigma
        g[3, 3] = (
            r_safe ** 2 + self.a ** 2 + self.r_s * r_safe * self.a ** 2 * sin2 / sigma
        ) * sin2

        return g

    # ------------------------------------------------------------------
    # Event horizons
    # ------------------------------------------------------------------

    def outer_horizon(self) -> float:
        """r_+ = (r_s + sqrt(r_s^2 - 4a^2)) / 2"""
        disc = self.r_s ** 2 - 4.0 * self.a ** 2
        if disc < 0:
            return float("nan")  # naked singularity
        return (self.r_s + np.sqrt(disc)) / 2.0

    def inner_horizon(self) -> float:
        """r_- = (r_s - sqrt(r_s^2 - 4a^2)) / 2"""
        disc = self.r_s ** 2 - 4.0 * self.a ** 2
        if disc < 0:
            return float("nan")
        return (self.r_s - np.sqrt(disc)) / 2.0

    # ------------------------------------------------------------------
    # ISCO for Kerr (prograde)
    # ------------------------------------------------------------------

    def isco_radius(self) -> float:
        """
        Prograde ISCO radius for Kerr metric (Bardeen, Press, Teukolsky 1972).
        Uses the dimensionless spin a* = a/M.
        r_ISCO/M = 3 + Z_2 - sqrt((3-Z_1)(3+Z_1+2*Z_2))
        """
        a = self.a_star
        Z1 = 1.0 + (1.0 - a ** 2) ** (1.0 / 3.0) * (
            (1.0 + a) ** (1.0 / 3.0) + (1.0 - a) ** (1.0 / 3.0)
        )
        Z2 = np.sqrt(3.0 * a ** 2 + Z1 ** 2)
        r_isco_over_M = 3.0 + Z2 - np.sqrt((3.0 - Z1) * (3.0 + Z1 + 2.0 * Z2))
        # Convert from units of M (=GM/c^2) to metres
        return r_isco_over_M * G * self.M / C ** 2

    # ------------------------------------------------------------------
    # Equatorial orbit integration
    # ------------------------------------------------------------------

    def integrate_equatorial_orbit(
        self,
        r0: float,
        phi0: float,
        dr_dtau0: float,
        E: float,
        L: float,
        tau_span: Tuple[float, float],
        n_points: int = 10000,
    ) -> Dict[str, np.ndarray]:
        """
        Integrate equatorial (theta=pi/2) Kerr geodesic using
        the radial effective potential.

        For equatorial Kerr geodesics the radial equation is:
            (dr/dtau)^2 = E^2 - V_eff(r)

        where V_eff encodes the angular momentum barrier and spin coupling.

        Parameters
        ----------
        r0 : initial radius [m].
        phi0 : initial azimuth.
        dr_dtau0 : initial radial velocity.
        E : specific energy.
        L : specific angular momentum.
        tau_span : (tau_start, tau_end).

        Returns dict with 'tau', 'r', 'phi', 'x', 'y'.
        """
        a = self.a
        r_s = self.r_s

        def rhs(tau, state):
            r, phi, v_r = state
            r_safe = max(abs(r), self.outer_horizon() * 1.01)
            delta = r_safe ** 2 - r_s * r_safe + a ** 2

            # dphi/dtau for equatorial Kerr
            dphi = (L + a * E * r_s / (r_safe * C)) / \
                (r_safe ** 2 + a ** 2 - a * L * r_s / (r_safe * C))
            if abs(delta) < 1e-30:
                dphi = 0.0

            # Radial acceleration from numerical gradient of effective potential
            eps = r_safe * 1e-6

            def V_eff_r(r_val):
                d = r_val ** 2 - r_s * r_val + a ** 2
                return (
                    -G * self.M / r_val
                    + L ** 2 / (2.0 * r_val ** 2)
                    - G * self.M * (L - a * E / C) ** 2 / (C ** 2 * r_val ** 3)
                )

            dVdr = (V_eff_r(r_safe + eps) -
                    V_eff_r(r_safe - eps)) / (2.0 * eps)
            a_r = -dVdr

            return [v_r, dphi, a_r]

        state0 = [r0, phi0, dr_dtau0]
        tau_eval = np.linspace(tau_span[0], tau_span[1], n_points)

        sol = solve_ivp(
            rhs, tau_span, state0, t_eval=tau_eval,
            method="DOP853", rtol=1e-10, atol=1e-12,
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
