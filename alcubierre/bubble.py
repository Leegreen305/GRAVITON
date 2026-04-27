"""
Warp bubble geometry, propagation, and stability analysis.

References:
    Alcubierre, M. (1994). Class. Quantum Grav. 11, L73.
    Hiscock, W.A. (1997). Class. Quantum Grav. 14, L183.
"""

import numpy as np
from typing import Tuple

from graviton.constants import G, C, HBAR, K_B
from alcubierre.metric import AlcubierreMetric


class WarpBubble:
    """
    Track the warp bubble state over time including position, velocity,
    tidal forces, causal structure, and Hawking-like radiation.

    Parameters
    ----------
    bubble_radius : float
        Bubble radius R [m].
    wall_thickness : float
        sigma parameter.
    warp_velocity : float
        Bubble speed as fraction of c.
    position : tuple
        Initial (x, y, z) position [m].
    """

    def __init__(
        self,
        bubble_radius: float = 100.0,
        wall_thickness: float = 8.0,
        warp_velocity: float = 1.0,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    ):
        self.R = bubble_radius
        self.sigma = wall_thickness
        self.v_s_frac = warp_velocity
        self.v_s = warp_velocity * C
        self.position = np.array(position, dtype=float)
        self.time = 0.0

        self._metric = AlcubierreMetric(
            bubble_radius=bubble_radius,
            wall_thickness=wall_thickness,
            warp_velocity=warp_velocity,
            bubble_center=tuple(self.position),
        )

    # ------------------------------------------------------------------
    # Propagation
    # ------------------------------------------------------------------

    def propagate(self, dt: float) -> np.ndarray:
        """
        Advance the warp bubble by one time-step dt [s].

        The bubble moves along the x-axis at v_s.
        Returns the new position.
        """
        self.position[0] += self.v_s * dt
        self.time += dt
        self._metric.x_s = self.position[0]
        self._metric.y_s = self.position[1]
        self._metric.z_s = self.position[2]
        return self.position.copy()

    # ------------------------------------------------------------------
    # Tidal forces
    # ------------------------------------------------------------------

    def get_tidal_forces(self, x, y, z) -> np.ndarray:
        """
        Estimate tidal acceleration on a test mass at (x, y, z).

        The tidal acceleration scales with the second derivative of the
        shape function:
            a_tidal ~ v_s^2 * d^2 f / dr^2

        Returns acceleration magnitude [m/s^2].
        """
        r_s = np.sqrt(
            (x - self.position[0]) ** 2
            + (y - self.position[1]) ** 2
            + (z - self.position[2]) ** 2
        )

        # Numerical second derivative of shape function
        eps = self.R * 1e-4
        r_plus = r_s + eps
        r_minus = np.maximum(r_s - eps, 0.0)

        def _f(r):
            num = np.tanh(self.sigma * (r + self.R)) - np.tanh(
                self.sigma * (r - self.R)
            )
            den = 2.0 * np.tanh(self.sigma * self.R)
            return num / den

        d2f = (_f(r_plus) - 2.0 * _f(r_s) + _f(r_minus)) / eps ** 2
        return np.abs(self.v_s ** 2 * d2f)

    # ------------------------------------------------------------------
    # Causal structure
    # ------------------------------------------------------------------

    def is_causally_disconnected(self) -> bool:
        """
        Return True if the warp bubble is superluminal (v_s > c).

        At superluminal speeds the bubble interior is causally disconnected
        from the bubble walls — the famous *control problem*.
        """
        return self.v_s > C

    # ------------------------------------------------------------------
    # Hawking-like radiation at bubble walls
    # ------------------------------------------------------------------

    def get_hawking_radiation_flux(self) -> float:
        """
        Estimate the Hawking-like radiation temperature at the bubble wall.

        Reference: Hiscock, W.A. (1997). Class. Quantum Grav. 14, L183.

        The effective surface gravity at the bubble wall is approximately:
            kappa ~ v_s * sigma

        Giving an Unruh-like temperature:
            T_H = hbar * kappa / (2 pi c k_B)

        Returns temperature [K].
        """
        kappa = self.v_s * self.sigma
        T_H = HBAR * kappa / (2.0 * np.pi * C * K_B)
        return float(T_H)
