"""
Alcubierre warp drive spacetime metric computation.

Reference:
    Alcubierre, M. (1994). "The warp drive: hyper-fast travel within
    general relativity." Classical and Quantum Gravity, 11(5), L73.

The line element in ADM (3+1) formalism:
    ds^2 = -c^2 dt^2 + (dx - v_s f(r_s) dt)^2 + dy^2 + dz^2

where v_s is the bubble velocity, f(r_s) is the shape function,
and r_s is the distance from the bubble centre.
"""

import numpy as np
from typing import Tuple

from graviton.constants import C


class AlcubierreMetric:
    """
    Compute the full Alcubierre warp-drive metric on a spatial grid.

    Parameters
    ----------
    bubble_radius : float
        Radius R of the warp bubble [m]. Default 100.
    wall_thickness : float
        sigma parameter controlling bubble wall steepness. Default 8.0.
    warp_velocity : float
        Bubble velocity as a multiple of c (e.g. 1.0 = c, 10.0 = 10c). Default 1.0.
    bubble_center : tuple
        (x_s, y_s, z_s) position of the bubble centre [m]. Default (0, 0, 0).
    """

    def __init__(
        self,
        bubble_radius: float = 100.0,
        wall_thickness: float = 8.0,
        warp_velocity: float = 1.0,
        bubble_center: Tuple[float, float, float] = (0.0, 0.0, 0.0),
    ):
        self.R = bubble_radius
        self.sigma = wall_thickness
        self.v_s = warp_velocity * C  # convert to m/s
        self.v_s_frac = warp_velocity
        self.x_s, self.y_s, self.z_s = bubble_center

    # ------------------------------------------------------------------
    # Core computations
    # ------------------------------------------------------------------

    def _distance_from_center(self, x, y, z) -> np.ndarray:
        """Compute r_s — distance from every grid point to bubble centre."""
        return np.sqrt(
            (x - self.x_s) ** 2 + (y - self.y_s) ** 2 + (z - self.z_s) ** 2
        )

    def compute_shape_function(self, x, y, z) -> np.ndarray:
        """
        Alcubierre shape function:

            f(r_s) = [tanh(sigma*(r_s + R)) - tanh(sigma*(r_s - R))]
                     / [2 * tanh(sigma * R)]

        Returns ndarray with same shape as the input grids.
        """
        r_s = self._distance_from_center(x, y, z)
        num = np.tanh(self.sigma * (r_s + self.R)) - np.tanh(
            self.sigma * (r_s - self.R)
        )
        den = 2.0 * np.tanh(self.sigma * self.R)
        return num / den

    def _compute_df_dr(self, x, y, z) -> np.ndarray:
        """
        Radial derivative of the shape function df/dr_s, computed analytically.

        df/dr = sigma * [sech^2(sigma*(r_s+R)) - sech^2(sigma*(r_s-R))]
                / [2 * tanh(sigma * R)]
        """
        r_s = self._distance_from_center(x, y, z)
        sech2_plus = 1.0 / np.cosh(self.sigma * (r_s + self.R)) ** 2
        sech2_minus = 1.0 / np.cosh(self.sigma * (r_s - self.R)) ** 2
        den = 2.0 * np.tanh(self.sigma * self.R)
        return self.sigma * (sech2_plus - sech2_minus) / den

    def compute_expansion_scalar(self, x, y, z) -> np.ndarray:
        """
        Volume expansion scalar of the Eulerian observers:

            theta = v_s * (x - x_s) / r_s * df/dr_s

        Positive theta -> space expanding (behind bubble).
        Negative theta -> space contracting (ahead of bubble).
        """
        r_s = self._distance_from_center(x, y, z)
        df_dr = self._compute_df_dr(x, y, z)
        # Avoid division by zero at the centre
        r_safe = np.where(r_s == 0, 1e-30, r_s)
        return self.v_s * (x - self.x_s) / r_safe * df_dr

    def compute_metric_tensor(self, x, y, z) -> np.ndarray:
        """
        Compute the full 4x4 metric tensor g_{mu nu} at each grid point.

        The Alcubierre line element:
            ds^2 = -c^2 dt^2 + (dx - v_s f dt)^2 + dy^2 + dz^2

        Expanding:
            g_00 = -(c^2 - v_s^2 f^2)
            g_01 = g_10 = -v_s f
            g_11 = 1,  g_22 = 1,  g_33 = 1
            (all other components 0)

        Returns shape (4, 4, *grid_shape).
        """
        f = self.compute_shape_function(x, y, z)
        grid_shape = f.shape

        g = np.zeros((4, 4) + grid_shape)

        g[0, 0] = -(C ** 2 - self.v_s ** 2 * f ** 2)
        g[0, 1] = -self.v_s * f
        g[1, 0] = -self.v_s * f
        g[1, 1] = 1.0
        g[2, 2] = 1.0
        g[3, 3] = 1.0

        return g

    def get_bubble_interior(self, x, y, z) -> np.ndarray:
        """Boolean mask: True for grid points inside the warp bubble (r_s < R)."""
        r_s = self._distance_from_center(x, y, z)
        return r_s < self.R

    # ------------------------------------------------------------------
    # Convenience: build a default grid
    # ------------------------------------------------------------------

    def make_grid(
        self, extent: float = None, N: int = 80
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Create a 3-D mesh-grid centred on the bubble.

        Parameters
        ----------
        extent : float or None
            Half-width of the grid. Defaults to 3*R.
        N : int
            Number of points per axis.

        Returns (X, Y, Z) mesh-grids.
        """
        if extent is None:
            extent = 3.0 * self.R
        lin = np.linspace(-extent, extent, N)
        return np.meshgrid(lin, lin, lin, indexing="ij")
