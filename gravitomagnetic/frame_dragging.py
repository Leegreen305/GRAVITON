"""
Lense-Thirring frame-dragging effect.

A rotating mass drags the inertial frames around it, causing gyroscope
precession and gravitomagnetic time dilation.

References:
    Lense, J. & Thirring, H. (1918). Phys. Z. 19, 156.
    Gravity Probe B (2011). Phys. Rev. Lett. 106, 221101.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple

from graviton.constants import G, C


class FrameDragging:
    """
    Simulate the Lense-Thirring frame-dragging effect.

    Parameters
    ----------
    mass : float
        Central mass [kg].
    angular_momentum : array-like (3,)
        Angular momentum vector J [kg m^2 / s].
    """

    def __init__(
        self,
        mass: float,
        angular_momentum: Tuple[float, float, float] = (0.0, 0.0, 1e33),
    ):
        self.M = mass
        self.J = np.asarray(angular_momentum, dtype=float)
        self.J_mag = np.linalg.norm(self.J)

    # ------------------------------------------------------------------
    # Lense-Thirring precession rate
    # ------------------------------------------------------------------

    def compute_precession_rate(
        self, x, y, z
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Lense-Thirring precession angular velocity:

            Omega_LT = (G / c^2 r^3) [3(J . r_hat) r_hat  -  J]

        Returns (Omega_x, Omega_y, Omega_z) arrays.
        """
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        r_safe = np.where(r == 0, 1e-30, r)

        # Unit vector
        rx, ry, rz = x / r_safe, y / r_safe, z / r_safe

        J_dot_rhat = self.J[0] * rx + self.J[1] * ry + self.J[2] * rz

        prefactor = G / (C ** 2 * r_safe ** 3)

        Ox = prefactor * (3.0 * J_dot_rhat * rx - self.J[0])
        Oy = prefactor * (3.0 * J_dot_rhat * ry - self.J[1])
        Oz = prefactor * (3.0 * J_dot_rhat * rz - self.J[2])

        return Ox, Oy, Oz

    # ------------------------------------------------------------------
    # Gyroscope precession integration
    # ------------------------------------------------------------------

    def integrate_gyroscope(
        self,
        r0: Tuple[float, float, float],
        S0: Tuple[float, float, float],
        t_span: Tuple[float, float],
        n_points: int = 2000,
    ) -> dict:
        """
        Integrate the gyroscope spin precession equation:
            dS/dt = Omega_LT x S

        Parameters
        ----------
        r0 : (3,) position of gyroscope [m] (assumed stationary).
        S0 : (3,) initial spin vector.
        t_span : (t_start, t_end) in seconds.
        n_points : number of output points.

        Returns dict with 't', 'Sx', 'Sy', 'Sz' arrays.
        """
        r0 = np.asarray(r0, dtype=float)
        S0 = np.asarray(S0, dtype=float)

        # Compute Omega_LT at the fixed position
        Ox, Oy, Oz = self.compute_precession_rate(r0[0], r0[1], r0[2])
        omega = np.array([float(Ox), float(Oy), float(Oz)])

        def rhs(t, S):
            return np.cross(omega, S)

        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        sol = solve_ivp(rhs, t_span, S0, t_eval=t_eval, rtol=1e-10, atol=1e-12)

        return {
            "t": sol.t,
            "Sx": sol.y[0],
            "Sy": sol.y[1],
            "Sz": sol.y[2],
        }

    # ------------------------------------------------------------------
    # Frame-drag angular velocity field
    # ------------------------------------------------------------------

    def compute_frame_drag_field(
        self, x, y, z
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Angular velocity field of dragged inertial frames.
        This is simply the Lense-Thirring precession rate at each point.
        """
        return self.compute_precession_rate(x, y, z)

    # ------------------------------------------------------------------
    # Gravitomagnetic time dilation
    # ------------------------------------------------------------------

    def compute_time_dilation(self, x, y, z) -> np.ndarray:
        """
        Proper-time ratio including gravitomagnetic correction:

            dtau/dt = sqrt(1 - 2GM/(rc^2) - (Omega_LT . r)^2 / c^2)

        Returns dtau/dt at each grid point.
        """
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        r_safe = np.where(r == 0, 1e-30, r)

        Ox, Oy, Oz = self.compute_precession_rate(x, y, z)

        # Omega_LT . r
        omega_dot_r = Ox * x + Oy * y + Oz * z

        arg = 1.0 - 2.0 * G * self.M / \
            (r_safe * C ** 2) - omega_dot_r ** 2 / C ** 2
        # Clamp to avoid sqrt of negative
        arg = np.maximum(arg, 0.0)
        return np.sqrt(arg)
