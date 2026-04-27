"""
Exotic matter — negative energy density regions and quantum inequality bounds.

References:
    Ford, L.H. & Roman, T.A. (1995). Phys. Rev. D 51, 4277.
    Ford, L.H. (1978). Proc. R. Soc. Lond. A 364, 227.
    Wu & Ford (1999). Phys. Rev. D 60, 104013.  (squeezed vacuum states)
"""

import numpy as np
from typing import Tuple

from graviton.constants import HBAR, C, G, PLANCK_LENGTH, PLANCK_TIME


class ExoticMatter:
    """
    Model negative energy density conditions, quantum inequality bounds,
    and squeezed vacuum states.
    """

    # ------------------------------------------------------------------
    # Quantum inequality bound (Ford-Roman)
    # ------------------------------------------------------------------

    @staticmethod
    def quantum_inequality_bound(tau: float) -> float:
        """
        Ford-Roman quantum inequality: the time-averaged energy density
        of any quantum field measured over a time interval tau satisfies:

            <rho> >= -3 / (32 pi^2 tau^4 c)   * hbar

        Reference: Ford & Roman (1995).

        Parameters
        ----------
        tau : float
            Sampling time [s].

        Returns the lower bound on <rho> [J/m^3].
        """
        return -3.0 * HBAR / (32.0 * np.pi ** 2 * tau ** 4 * C)

    # ------------------------------------------------------------------
    # Negative energy pulse constraints
    # ------------------------------------------------------------------

    @staticmethod
    def max_negative_energy_pulse(delta_E: float) -> float:
        """
        Given a negative energy pulse of magnitude |delta_E|,
        the maximum allowed duration is:

            delta_t <= (hbar / |delta_E|)^(1/3) * (l_P^2 / c)^(1/3)

        This is a rough order-of-magnitude bound from quantum inequalities.

        Returns max duration [s].
        """
        return (HBAR / abs(delta_E)) ** (1.0 / 3.0) * (PLANCK_LENGTH ** 2 / C) ** (1.0 / 3.0)

    # ------------------------------------------------------------------
    # Squeezed vacuum state energy density
    # ------------------------------------------------------------------

    @staticmethod
    def squeezed_vacuum_energy_density(
        squeeze_parameter: float, omega: float
    ) -> float:
        """
        Energy density of a squeezed vacuum state.

        For a single-mode squeezed state with squeeze parameter r:
            <rho> = (hbar omega / (4 pi^2 c^3)) * (cosh(2r) - 1)

        The negative energy regions oscillate in the squeezed quadrature.
        The time-averaged negative contribution is:

            <rho_neg> ~ -(hbar omega / (4 pi^2 c^3)) * sinh^2(r)

        Reference: Wu & Ford (1999).

        Parameters
        ----------
        squeeze_parameter : float
            Dimensionless squeeze parameter r >= 0.
        omega : float
            Mode frequency [rad/s].

        Returns approximate negative energy density [J/m^3].
        """
        r = squeeze_parameter
        return -(HBAR * omega / (4.0 * np.pi ** 2 * C ** 3)) * np.sinh(r) ** 2

    # ------------------------------------------------------------------
    # Exotic matter required for warp drive vs quantum inequalities
    # ------------------------------------------------------------------

    @staticmethod
    def warp_drive_feasibility(
        exotic_energy_J: float, bubble_radius: float
    ) -> dict:
        """
        Assess whether the required exotic energy violates quantum
        inequality bounds for the given bubble size.
        """
        # Characteristic time ~ R / c
        tau = bubble_radius / C
        qi_bound = ExoticMatter.quantum_inequality_bound(tau)

        # Volume of bubble
        V = (4.0 / 3.0) * np.pi * bubble_radius ** 3

        # Required energy density
        rho_required = exotic_energy_J / V

        return {
            "required_energy_density_J_m3": rho_required,
            "qi_lower_bound_J_m3": qi_bound,
            "violates_qi": rho_required < qi_bound,
            "ratio_to_bound": rho_required / qi_bound if qi_bound != 0 else float("inf"),
        }
