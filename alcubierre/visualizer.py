"""
Interactive 3-D visualizations for the Alcubierre warp drive.

Produces:
  - 3D Plotly surface of the expansion scalar theta(x, y, z=0)
  - 2D heatmap of energy density T_00 cross-section
  - Shape function profile f(r_s) vs radius
  - Summary metrics panel
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt

from alcubierre.metric import AlcubierreMetric
from alcubierre.energy import ExoticEnergyCalculator
from graviton.constants import C, JUPITER_MASS_ENERGY


class AlcubierreVisualizer:
    """
    Generate interactive visualizations of the Alcubierre warp bubble.

    Parameters
    ----------
    bubble_radius : float
        Bubble radius R [m].
    wall_thickness : float
        sigma parameter.
    warp_velocity : float
        Bubble speed as fraction of c.
    N : int
        Grid resolution per axis for 2-D slices.
    """

    def __init__(
        self,
        bubble_radius: float = 100.0,
        wall_thickness: float = 8.0,
        warp_velocity: float = 1.0,
        N: int = 120,
    ):
        self.R = bubble_radius
        self.sigma = wall_thickness
        self.v_frac = warp_velocity
        self.N = N

        self.metric = AlcubierreMetric(
            bubble_radius=bubble_radius,
            wall_thickness=wall_thickness,
            warp_velocity=warp_velocity,
        )
        self.energy_calc = ExoticEnergyCalculator(
            bubble_radius=bubble_radius,
            wall_thickness=wall_thickness,
            warp_velocity=warp_velocity,
        )

    # ------------------------------------------------------------------
    # Main interactive figure (Plotly)
    # ------------------------------------------------------------------

    def plot_expansion_scalar_3d(self, show: bool = True) -> go.Figure:
        """
        3-D surface plot of the expansion scalar theta on the z=0 plane.

        Blue  = expanding space (behind bubble)
        Red   = contracting space (ahead of bubble)
        Green = flat interior
        """
        extent = 3.0 * self.R
        lin = np.linspace(-extent, extent, self.N)
        X, Y = np.meshgrid(lin, lin, indexing="ij")
        Z = np.zeros_like(X)

        theta = self.metric.compute_expansion_scalar(X, Y, Z)

        fig = go.Figure(
            data=[
                go.Surface(
                    x=X,
                    y=Y,
                    z=theta,
                    colorscale=[
                        [0.0, "rgb(220,50,50)"],
                        [0.5, "rgb(240,240,240)"],
                        [1.0, "rgb(50,80,220)"],
                    ],
                    colorbar=dict(title="Expansion Scalar"),
                )
            ]
        )
        fig.update_layout(
            title=f"Alcubierre Expansion Scalar (v={self.v_frac}c, R={self.R}m)",
            scene=dict(
                xaxis_title="x [m]",
                yaxis_title="y [m]",
                zaxis_title="theta",
            ),
        )
        if show:
            fig.show()
        return fig

    # ------------------------------------------------------------------
    # Energy density heatmap (Plotly)
    # ------------------------------------------------------------------

    def plot_energy_density_heatmap(self, show: bool = True) -> go.Figure:
        """2-D heatmap of T_00 on the z=0 plane."""
        extent = 3.0 * self.R
        lin = np.linspace(-extent, extent, self.N)
        X, Y = np.meshgrid(lin, lin, indexing="ij")
        Z = np.zeros_like(X)

        T_00 = self.energy_calc.compute_energy_density(X, Y, Z)

        fig = go.Figure(
            data=go.Heatmap(
                x=lin,
                y=lin,
                z=T_00,
                colorscale="RdBu",
                colorbar=dict(title="T_00 [J/m^3]"),
            )
        )
        fig.update_layout(
            title="Exotic Energy Density T_00 (z=0 cross-section)",
            xaxis_title="x [m]",
            yaxis_title="y [m]",
        )
        if show:
            fig.show()
        return fig

    # ------------------------------------------------------------------
    # Shape function profile (Matplotlib)
    # ------------------------------------------------------------------

    def plot_shape_function(self, show: bool = True):
        """Plot the shape function f(r_s) vs radial distance."""
        r = np.linspace(0, 3.0 * self.R, 500)
        x = r
        y = np.zeros_like(r)
        z = np.zeros_like(r)

        f = self.metric.compute_shape_function(x, y, z)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(r, f, "b-", linewidth=2)
        ax.axvline(self.R, color="gray", linestyle="--",
                   label=f"R = {self.R} m")
        ax.set_xlabel("r_s [m]")
        ax.set_ylabel("f(r_s)")
        ax.set_title("Alcubierre Shape Function")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    # ------------------------------------------------------------------
    # Summary metrics
    # ------------------------------------------------------------------

    def print_metrics(self):
        """Print key warp bubble metrics to the console."""
        E = self.energy_calc.compute_total_exotic_energy(N=40)
        comparisons = self.energy_calc.compare_to_known_energies(E)

        print("=" * 60)
        print("  ALCUBIERRE WARP BUBBLE METRICS")
        print("=" * 60)
        print(f"  Bubble radius         : {self.R:.1f} m")
        print(f"  Wall thickness (sigma) : {self.sigma:.1f}")
        print(f"  Warp velocity          : {self.v_frac:.2f} c")
        print(f"  Total exotic energy    : {E:.3e} J")
        print(
            f"  Jupiter mass-energy eq.: {comparisons['fraction_of_jupiter_mass_energy']:.3e}x"
        )
        print(
            f"  World annual energy    : {comparisons['world_annual_energy_consumption']:.3e}x"
        )
        print(f"  Causally disconnected  : {self.v_frac > 1.0}")
        print("=" * 60)

    # ------------------------------------------------------------------
    # Combined dashboard
    # ------------------------------------------------------------------

    def run_dashboard(self, show: bool = True):
        """Generate all plots and print metrics."""
        self.print_metrics()
        self.plot_expansion_scalar_3d(show=show)
        self.plot_energy_density_heatmap(show=show)
        self.plot_shape_function(show=show)
