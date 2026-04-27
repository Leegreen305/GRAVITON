"""
Gravitomagnetic force calculator — particle trajectories in combined
gravitoelectric + gravitomagnetic fields.

Integrates the equation of motion:
    m dv/dt = m (E_g + v x B_g)
using scipy.integrate.solve_ivp.
"""

import numpy as np
from scipy.integrate import solve_ivp
from typing import Tuple

from graviton.constants import G, C
from gravitomagnetic.gem_equations import GravitoElectroMagneticField


class GravitomagneticForce:
    """
    Compute a test-particle trajectory in the GEM field of a massive
    rotating body.

    Parameters
    ----------
    mass_source : float
        Central mass [kg].
    angular_momentum : array-like (3,)
        Angular momentum of central body [kg m^2/s].
    test_mass : float
        Mass of the test particle [kg]. Cancels in EOM but kept for force units.
    """

    def __init__(
        self,
        mass_source: float,
        angular_momentum: Tuple[float, float, float] = (0.0, 0.0, 1e33),
        test_mass: float = 1.0,
    ):
        self.gem = GravitoElectroMagneticField(
            mass=mass_source, angular_momentum=angular_momentum
        )
        self.m = test_mass

    def _eom(self, t, state):
        """Equations of motion: d/dt [x, y, z, vx, vy, vz]."""
        x, y, z, vx, vy, vz = state
        Ex, Ey, Ez = self.gem.compute_gravitoelectric(x, y, z)
        Bx, By, Bz = self.gem.compute_gravitomagnetic(x, y, z)

        # Force per unit mass: a = E_g + v x B_g
        ax = float(Ex) + (vy * float(Bz) - vz * float(By))
        ay = float(Ey) + (vz * float(Bx) - vx * float(Bz))
        az = float(Ez) + (vx * float(By) - vy * float(Bx))

        return [vx, vy, vz, ax, ay, az]

    def integrate_trajectory(
        self,
        r0: Tuple[float, float, float],
        v0: Tuple[float, float, float],
        t_span: Tuple[float, float],
        n_points: int = 5000,
        **kwargs,
    ) -> dict:
        """
        Integrate the test-particle trajectory.

        Returns dict with 't', 'x', 'y', 'z', 'vx', 'vy', 'vz'.
        """
        state0 = list(r0) + list(v0)
        t_eval = np.linspace(t_span[0], t_span[1], n_points)

        sol = solve_ivp(
            self._eom,
            t_span,
            state0,
            t_eval=t_eval,
            rtol=1e-10,
            atol=1e-12,
            method="DOP853",
            **kwargs,
        )

        return {
            "t": sol.t,
            "x": sol.y[0],
            "y": sol.y[1],
            "z": sol.y[2],
            "vx": sol.y[3],
            "vy": sol.y[4],
            "vz": sol.y[5],
        }
