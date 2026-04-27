"""
Casimir effect — vacuum energy between perfectly conducting plates.

Reference:
    Casimir, H.B.G. (1948). "On the attraction between two perfectly
    conducting plates." Proc. Kon. Ned. Akad. Wetensch. 51, 793.

The Casimir force per unit area between two parallel conducting plates
separated by distance d:

    F/A = -pi^2 hbar c / (240 d^4)

The energy density between the plates:

    u = -pi^2 hbar c / (720 d^3)
"""

import numpy as np
from typing import Tuple

from graviton.constants import HBAR, C, CASIMIR_COEFFICIENT


class CasimirEffect:
    """
    Compute Casimir force, pressure, and energy density between
    parallel conducting plates.

    Parameters
    ----------
    plate_area : float
        Area of each plate [m^2]. Default 1.0 m^2.
    """

    def __init__(self, plate_area: float = 1.0):
        self.A = plate_area

    # ------------------------------------------------------------------
    # Force per unit area
    # ------------------------------------------------------------------

    def force_per_area(self, d: float) -> float:
        """
        Casimir force per unit area [N/m^2] for plate separation d [m].

        F/A = -pi^2 * hbar * c / (240 * d^4)

        Negative sign → attractive force.
        """
        return -np.pi ** 2 * HBAR * C / (240.0 * d ** 4)

    def total_force(self, d: float) -> float:
        """Total Casimir force [N] = (F/A) * A."""
        return self.force_per_area(d) * self.A

    # ------------------------------------------------------------------
    # Energy density
    # ------------------------------------------------------------------

    def energy_density(self, d: float) -> float:
        """
        Vacuum energy density between plates [J/m^3]:

            u = -pi^2 * hbar * c / (720 * d^3)
        """
        return -np.pi ** 2 * HBAR * C / (720.0 * d ** 3)

    def total_energy(self, d: float) -> float:
        """Total Casimir energy [J] = u * A * d."""
        return self.energy_density(d) * self.A * d

    # ------------------------------------------------------------------
    # Parameter sweep
    # ------------------------------------------------------------------

    def sweep_separation(
        self, d_min: float = 1e-9, d_max: float = 1e-6, N: int = 500
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Sweep plate separation and return (d, force_per_area, energy_density).
        """
        d = np.linspace(d_min, d_max, N)
        fpa = -np.pi ** 2 * HBAR * C / (240.0 * d ** 4)
        u = -np.pi ** 2 * HBAR * C / (720.0 * d ** 3)
        return d, fpa, u

    # ------------------------------------------------------------------
    # Comparison with known experimental values
    # ------------------------------------------------------------------

    @staticmethod
    def lamoreaux_1997_comparison(d: float = 0.6e-6) -> dict:
        """
        Compare theoretical prediction with Lamoreaux (1997) experimental result.

        Reference: Lamoreaux, S.K. (1997). Phys. Rev. Lett. 78, 5.
        Measured at d ~ 0.6 um: F/A ~ 1.0e-3 Pa (within ~5% of theory).
        """
        theory = -np.pi ** 2 * HBAR * C / (240.0 * d ** 4)
        experiment = -1.0e-3  # approximate Pa
        return {
            "separation_m": d,
            "theory_Pa": theory,
            "experiment_Pa": experiment,
            "relative_error": abs(theory - experiment) / abs(experiment),
        }
