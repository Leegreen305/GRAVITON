"""
Exotic energy density and total energy calculations for the Alcubierre metric.

References:
    Alcubierre, M. (1994). Class. Quantum Grav. 11, L73.
    Pfenning, M.J. & Ford, L.H. (1997). Class. Quantum Grav. 14, 1743.

The Einstein field equations G_{mu nu} = (8 pi G / c^4) T_{mu nu} yield
a *negative* energy density T_00 for the Alcubierre metric — exotic matter.
"""

import numpy as np
from typing import Dict, Tuple

from graviton.constants import G, C, HBAR, SOLAR_LUMINOSITY, JUPITER_MASS_ENERGY


class ExoticEnergyCalculator:
    """
    Calculate the exotic-matter energy density and total energy required
    to sustain an Alcubierre warp bubble.

    Parameters
    ----------
    bubble_radius : float
        Bubble radius R [m].
    wall_thickness : float
        sigma parameter.
    warp_velocity : float
        Bubble speed as fraction of c.
    """

    def __init__(
        self,
        bubble_radius: float = 100.0,
        wall_thickness: float = 8.0,
        warp_velocity: float = 1.0,
    ):
        self.R = bubble_radius
        self.sigma = wall_thickness
        self.v_s = warp_velocity * C
        self.v_s_frac = warp_velocity

    # ------------------------------------------------------------------
    # Energy density
    # ------------------------------------------------------------------

    def compute_energy_density(self, x, y, z) -> np.ndarray:
        """
        Compute T_00 (energy density) from the Alcubierre metric.

        For the Alcubierre metric the dominant energy density component is:
            T_00 = -(c^4 / (32 pi G)) * v_s^2 * (df/dr)^2 * (y^2 + z^2) / r_s^2

        This is manifestly *negative* — exotic matter is required.

        Returns ndarray of T_00 values [J/m^3] on the input grid.
        """
        r_s = np.sqrt(x ** 2 + y ** 2 + z ** 2)
        r_safe = np.where(r_s == 0, 1e-30, r_s)

        # Shape function derivative
        sech2_p = 1.0 / np.cosh(self.sigma * (r_s + self.R)) ** 2
        sech2_m = 1.0 / np.cosh(self.sigma * (r_s - self.R)) ** 2
        den = 2.0 * np.tanh(self.sigma * self.R)
        df_dr = self.sigma * (sech2_p - sech2_m) / den

        rho_perp_sq = (y ** 2 + z ** 2)
        T_00 = (
            -(C ** 4 / (32.0 * np.pi * G))
            * self.v_s ** 2
            * df_dr ** 2
            * rho_perp_sq
            / r_safe ** 2
        )
        return T_00

    # ------------------------------------------------------------------
    # Total exotic energy (numerical integration on a grid)
    # ------------------------------------------------------------------

    def compute_total_exotic_energy(
        self, N: int = 60, extent_factor: float = 3.0
    ) -> float:
        """
        Numerically integrate T_00 over the bubble volume to get total
        exotic energy E_exotic [J].

        Uses a uniform 3-D grid and trapezoidal-rule volume integration.
        """
        extent = extent_factor * self.R
        lin = np.linspace(-extent, extent, N)
        dx = lin[1] - lin[0]
        X, Y, Z = np.meshgrid(lin, lin, lin, indexing="ij")
        T_00 = self.compute_energy_density(X, Y, Z)

        # sqrt(-g) = 1 for the spatial part of Alcubierre metric (to leading order)
        E_exotic = np.sum(T_00) * dx ** 3
        return float(E_exotic)

    # ------------------------------------------------------------------
    # Pfenning-Ford minimum energy bound
    # ------------------------------------------------------------------

    def pfenning_ford_bound(self) -> float:
        """
        Quantum-inequality lower bound on exotic energy.

        Reference: Pfenning & Ford (1997).
        E_min ~ -(c^7 / (G^2 * hbar)) * V_bubble / sigma^2
        where V_bubble = (4/3) pi R^3
        """
        V = (4.0 / 3.0) * np.pi * self.R ** 3
        E_min = -(C ** 7 / (G ** 2 * HBAR)) * V / self.sigma ** 2
        return float(E_min)

    # ------------------------------------------------------------------
    # Comparison utilities
    # ------------------------------------------------------------------

    def compare_to_known_energies(self, E_exotic: float = None) -> Dict[str, float]:
        """
        Express the exotic energy in terms of familiar astrophysical energies.
        """
        if E_exotic is None:
            E_exotic = self.compute_total_exotic_energy()
        abs_E = abs(E_exotic)
        return {
            "exotic_energy_J": E_exotic,
            "fraction_of_solar_annual_output": abs_E / (SOLAR_LUMINOSITY * 3.156e7),
            "fraction_of_jupiter_mass_energy": abs_E / JUPITER_MASS_ENERGY,
            "hiroshima_bombs_equivalent": abs_E / 6.3e13,
            "world_annual_energy_consumption": abs_E / 5.8e20,
        }

    # ------------------------------------------------------------------
    # Scaling curves
    # ------------------------------------------------------------------

    def compute_scaling_curves(
        self, param: str, values: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute how total exotic energy scales with a single parameter.

        Parameters
        ----------
        param : str
            One of 'radius', 'velocity', 'sigma'.
        values : ndarray
            Array of parameter values to sweep.

        Returns (values, energies) arrays.
        """
        energies = np.empty_like(values, dtype=float)
        original = (self.R, self.v_s_frac, self.sigma)

        for i, val in enumerate(values):
            if param == "radius":
                self.R = val
            elif param == "velocity":
                self.v_s = val * C
            elif param == "sigma":
                self.sigma = val
            else:
                raise ValueError(
                    f"Unknown param '{param}'. Use radius/velocity/sigma.")
            energies[i] = self.compute_total_exotic_energy(N=30)

        # Restore originals
        self.R, self.v_s_frac, self.sigma = original
        self.v_s = self.v_s_frac * C
        return values, energies
