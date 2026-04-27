"""
Gravitoelectromagnetic (GEM) field equations.

In the weak-field, slow-motion limit of GR the linearised Einstein equations
take a form analogous to Maxwell's equations.

Reference:
    Mashhoon, B. (2008). "Gravitoelectromagnetism: A Brief Review."
    arXiv:gr-qc/0311030

GEM field equations (SI):
    div E_g  = -4 pi G rho
    div B_g  = 0
    curl E_g = -dB_g/dt
    curl B_g = (-4 pi G / c^2) J_g  +  (1/c^2) dE_g/dt

Gravitomagnetic Lorentz-like force:
    F = m (E_g  +  v x B_g)
"""

import numpy as np
from typing import Tuple

from graviton.constants import G, C


class GravitoElectroMagneticField:
    """
    Compute gravitoelectric and gravitomagnetic fields for a massive
    rotating body.

    Parameters
    ----------
    mass : float
        Central mass M [kg].
    angular_momentum : array-like (3,)
        Angular momentum vector J [kg m^2 / s].  Default along z-axis.
    """

    def __init__(
        self,
        mass: float,
        angular_momentum: Tuple[float, float, float] = (0.0, 0.0, 1e33),
    ):
        self.M = mass
        self.J = np.asarray(angular_momentum, dtype=float)

    # ------------------------------------------------------------------
    # Gravitoelectric field  E_g = -grad Phi_g  where Phi_g = -GM/r
    # ------------------------------------------------------------------

    def compute_gravitoelectric(
        self, x, y, z
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute the gravitoelectric field E_g = -GM r_hat / r^2
        at each grid point.

        Returns (E_x, E_y, E_z) component arrays.
        """
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        r_safe = np.where(r == 0, 1e-30, r)
        prefactor = -G * self.M / r_safe ** 3
        return prefactor * x, prefactor * y, prefactor * z

    # ------------------------------------------------------------------
    # Gravitomagnetic field  B_g = -curl A_g
    # A_g = -(G / c^2) (J x r) / r^3
    # ------------------------------------------------------------------

    def compute_gravitomagnetic(
        self, x, y, z
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Compute the gravitomagnetic field B_g from the vector potential
        A_g = -(G / c^2) (J x r) / r^3.

        The result is the dipole gravitomagnetic field:
            B_g = (G / c^2 r^5) [3(J . r) r  -  r^2 J]

        Returns (B_x, B_y, B_z) component arrays.
        """
        r = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        r_safe = np.where(r == 0, 1e-30, r)

        # J . r (dot product broadcast over grid)
        J_dot_r = self.J[0] * x + self.J[1] * y + self.J[2] * z

        prefactor = G / (C ** 2 * r_safe ** 5)

        Bx = prefactor * (3.0 * J_dot_r * x - r_safe ** 2 * self.J[0])
        By = prefactor * (3.0 * J_dot_r * y - r_safe ** 2 * self.J[1])
        Bz = prefactor * (3.0 * J_dot_r * z - r_safe ** 2 * self.J[2])

        return Bx, By, Bz

    # ------------------------------------------------------------------
    # Lorentz-like force  F = m (E_g + v x B_g)
    # ------------------------------------------------------------------

    @staticmethod
    def compute_force(
        m: float,
        v: np.ndarray,
        E_g: Tuple[np.ndarray, np.ndarray, np.ndarray],
        B_g: Tuple[np.ndarray, np.ndarray, np.ndarray],
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Gravitomagnetic Lorentz force on a mass m moving at velocity v.

        Parameters
        ----------
        m : float
            Test mass [kg].
        v : array (3,)
            Velocity vector [m/s].
        E_g : tuple of arrays
            (E_x, E_y, E_z) gravitoelectric field.
        B_g : tuple of arrays
            (B_x, B_y, B_z) gravitomagnetic field.

        Returns (F_x, F_y, F_z).
        """
        v = np.asarray(v, dtype=float)
        # v x B_g
        vxB_x = v[1] * B_g[2] - v[2] * B_g[1]
        vxB_y = v[2] * B_g[0] - v[0] * B_g[2]
        vxB_z = v[0] * B_g[1] - v[1] * B_g[0]

        Fx = m * (E_g[0] + vxB_x)
        Fy = m * (E_g[1] + vxB_y)
        Fz = m * (E_g[2] + vxB_z)
        return Fx, Fy, Fz
