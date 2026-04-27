"""
Quantum vacuum (zero-point) energy field density model.

The electromagnetic vacuum has a zero-point energy density arising from
quantum fluctuations. For each mode of frequency omega the ZPE is hbar*omega/2.

References:
    Milonni, P.W. (1994). "The Quantum Vacuum." Academic Press.
    Weinberg, S. (1989). Rev. Mod. Phys. 61, 1. (cosmological constant problem)
"""

import numpy as np
from typing import Tuple

from graviton.constants import HBAR, C, PLANCK_LENGTH


class QuantumVacuumField:
    """
    Model the zero-point energy spectral density and total regularised
    vacuum energy density.

    Parameters
    ----------
    cutoff_frequency : float or None
        UV cutoff frequency [rad/s]. Defaults to Planck frequency c/l_P.
    """

    def __init__(self, cutoff_frequency: float = None):
        if cutoff_frequency is None:
            self.omega_max = C / PLANCK_LENGTH  # ~ 1.85e43 rad/s
        else:
            self.omega_max = cutoff_frequency

    # ------------------------------------------------------------------
    # Spectral density
    # ------------------------------------------------------------------

    def spectral_density(self, omega: np.ndarray) -> np.ndarray:
        """
        ZPE spectral energy density [J/m^3 per rad/s]:

            u(omega) = hbar * omega^3 / (2 pi^2 c^3)

        This is the energy per unit volume per unit frequency for all
        electromagnetic modes.
        """
        return HBAR * omega ** 3 / (2.0 * np.pi ** 2 * C ** 3)

    # ------------------------------------------------------------------
    # Total regularised energy density
    # ------------------------------------------------------------------

    def total_energy_density(self, N_modes: int = 10000) -> float:
        """
        Numerically integrate the ZPE spectral density up to the cutoff.

            U = integral_0^{omega_max} u(omega) d_omega
              = hbar omega_max^4 / (8 pi^2 c^3)

        Returns energy density [J/m^3].
        """
        # Analytic result
        return HBAR * self.omega_max ** 4 / (8.0 * np.pi ** 2 * C ** 3)

    def total_energy_density_numerical(self, N: int = 10000) -> float:
        """Numerical integration (trapezoidal) as a cross-check."""
        omega = np.linspace(0, self.omega_max, N)
        u = self.spectral_density(omega)
        return float(np.trapezoid(u, omega))

    # ------------------------------------------------------------------
    # Mode summation (discrete box)
    # ------------------------------------------------------------------

    def box_mode_energy(self, L: float, n_max: int = 50) -> float:
        """
        Sum ZPE contributions from discrete modes in a cubic box of side L [m].

            E = sum_{n_x, n_y, n_z} (1/2) hbar omega_n
            omega_n = pi c / L * sqrt(n_x^2 + n_y^2 + n_z^2)

        Returns total ZPE [J] (unregularised — divergent, but truncated at n_max).
        """
        E = 0.0
        for nx in range(1, n_max + 1):
            for ny in range(1, n_max + 1):
                for nz in range(1, n_max + 1):
                    omega_n = np.pi * C / L * \
                        np.sqrt(nx ** 2 + ny ** 2 + nz ** 2)
                    E += 0.5 * HBAR * omega_n
        return E

    # ------------------------------------------------------------------
    # Cosmological constant comparison
    # ------------------------------------------------------------------

    def cosmological_constant_discrepancy(self) -> dict:
        """
        Compare QFT vacuum energy density to observed cosmological constant.

        Observed: rho_Lambda ~ 5.96e-27 kg/m^3  (Planck 2018)
        QFT at Planck cutoff: rho_QFT ~ 10^113 J/m^3

        This is the famous 120 order-of-magnitude discrepancy.
        """
        rho_qft = self.total_energy_density()
        rho_obs = 5.96e-27 * C ** 2  # convert to J/m^3
        ratio = rho_qft / rho_obs if rho_obs > 0 else float("inf")
        return {
            "rho_qft_J_per_m3": rho_qft,
            "rho_observed_J_per_m3": rho_obs,
            "ratio": ratio,
            "log10_ratio": np.log10(ratio) if ratio > 0 else float("inf"),
        }
