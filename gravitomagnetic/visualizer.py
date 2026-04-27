"""
Visualizations for gravitomagnetic fields and frame-dragging effects.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from gravitomagnetic.gem_equations import GravitoElectroMagneticField
from gravitomagnetic.frame_dragging import FrameDragging
from graviton.constants import EARTH_MASS, EARTH_RADIUS, EARTH_ANGULAR_MOMENTUM


class GravitomagneticVisualizer:
    """
    Produce 2-D field-line and quiver plots for GEM fields.

    Parameters
    ----------
    mass : float
        Central mass [kg].
    angular_momentum : array-like (3,)
        Angular momentum vector J [kg m^2/s].
    """

    def __init__(self, mass: float = EARTH_MASS, angular_momentum=None):
        if angular_momentum is None:
            angular_momentum = (0.0, 0.0, EARTH_ANGULAR_MOMENTUM)
        self.gem = GravitoElectroMagneticField(mass, angular_momentum)
        self.fd = FrameDragging(mass, angular_momentum)
        self.mass = mass

    def plot_gravitoelectric_field(
        self, extent: float = None, N: int = 30, show: bool = True
    ):
        """Quiver plot of E_g on the z=0 plane."""
        if extent is None:
            extent = 4.0 * EARTH_RADIUS
        lin = np.linspace(-extent, extent, N)
        X, Y = np.meshgrid(lin, lin, indexing="ij")
        Z = np.zeros_like(X)

        Ex, Ey, Ez = self.gem.compute_gravitoelectric(X, Y, Z)
        mag = np.sqrt(Ex ** 2 + Ey ** 2)
        mag_safe = np.where(mag == 0, 1e-30, mag)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.quiver(X, Y, Ex / mag_safe, Ey / mag_safe, mag, cmap="inferno")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title("Gravitoelectric Field E_g (z=0)")
        ax.set_aspect("equal")
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    def plot_gravitomagnetic_field(
        self, extent: float = None, N: int = 30, show: bool = True
    ):
        """Quiver plot of B_g on the x-z plane (meridional plane)."""
        if extent is None:
            extent = 4.0 * EARTH_RADIUS
        lin = np.linspace(-extent, extent, N)
        X, Z = np.meshgrid(lin, lin, indexing="ij")
        Y = np.zeros_like(X)

        Bx, By, Bz = self.gem.compute_gravitomagnetic(X, Y, Z)
        mag = np.sqrt(Bx ** 2 + Bz ** 2)
        mag_safe = np.where(mag == 0, 1e-30, mag)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.quiver(X, Z, Bx / mag_safe, Bz / mag_safe, mag, cmap="cool")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("z [m]")
        ax.set_title("Gravitomagnetic Field B_g (y=0 meridional plane)")
        ax.set_aspect("equal")
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    def plot_frame_drag_field(
        self, extent: float = None, N: int = 25, show: bool = True
    ):
        """Quiver plot of frame-dragging angular velocity on the z=0 plane."""
        if extent is None:
            extent = 4.0 * EARTH_RADIUS
        lin = np.linspace(-extent, extent, N)
        X, Y = np.meshgrid(lin, lin, indexing="ij")
        Z = np.zeros_like(X)

        Ox, Oy, Oz = self.fd.compute_frame_drag_field(X, Y, Z)
        mag = np.sqrt(Ox ** 2 + Oy ** 2)
        mag_safe = np.where(mag == 0, 1e-30, mag)

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.quiver(X, Y, Ox / mag_safe, Oy / mag_safe, mag, cmap="plasma")
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title("Frame-Dragging Angular Velocity (z=0)")
        ax.set_aspect("equal")
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    def run_all(self, show: bool = True):
        """Generate all gravitomagnetic visualizations."""
        self.plot_gravitoelectric_field(show=show)
        self.plot_gravitomagnetic_field(show=show)
        self.plot_frame_drag_field(show=show)
