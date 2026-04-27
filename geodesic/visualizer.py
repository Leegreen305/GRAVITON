"""
Geodesic path visualizations — 2D orbital plots and embedding diagrams.
"""

import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from geodesic.schwarzschild import SchwarzschildGeodesic
from geodesic.kerr import KerrGeodesic
from graviton.constants import G, C, SOLAR_MASS


class GeodesicVisualizer:
    """
    Visualize geodesic orbits in Schwarzschild and Kerr spacetimes.
    """

    def __init__(self, mass: float = 10.0 * SOLAR_MASS):
        self.mass = mass
        self.schw = SchwarzschildGeodesic(mass)
        self.kerr = KerrGeodesic(mass, spin_parameter=0.9)

    # ------------------------------------------------------------------
    # Schwarzschild orbit
    # ------------------------------------------------------------------

    def plot_schwarzschild_orbit(
        self,
        r0_factor: float = 10.0,
        L_factor: float = 4.0,
        tau_end: float = 1e4,
        show: bool = True,
    ):
        """Plot an equatorial orbit in Schwarzschild spacetime."""
        r_s = self.schw.r_s
        r0 = r0_factor * r_s
        L = L_factor * r_s * C

        result = self.schw.integrate_orbit(
            r0=r0, phi0=0.0, dr_dtau0=0.0, L=L,
            tau_span=(0, tau_end), n_points=10000,
        )

        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Orbit in x-y
        axes[0].plot(result["x"] / r_s, result["y"] / r_s, "b-", linewidth=0.5)
        circle = plt.Circle((0, 0), 1, color="black",
                            fill=True, label="Event horizon")
        axes[0].add_patch(circle)
        axes[0].set_xlabel("x / r_s")
        axes[0].set_ylabel("y / r_s")
        axes[0].set_title("Schwarzschild Geodesic (equatorial)")
        axes[0].set_aspect("equal")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # Effective potential
        r_range = np.linspace(2 * r_s, 30 * r_s, 1000)
        V = self.schw.effective_potential(r_range, L)
        axes[1].plot(r_range / r_s, V, "r-", linewidth=2)
        axes[1].axhline(V[0], color="gray", linestyle="--", alpha=0.5)
        axes[1].set_xlabel("r / r_s")
        axes[1].set_ylabel("V_eff")
        axes[1].set_title("Effective Potential")
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()
        if show:
            plt.show()
        return fig

    # ------------------------------------------------------------------
    # Kerr orbit
    # ------------------------------------------------------------------

    def plot_kerr_orbit(
        self,
        r0_factor: float = 8.0,
        E: float = 0.95,
        L_factor: float = 3.5,
        tau_end: float = 1e4,
        show: bool = True,
    ):
        """Plot an equatorial orbit in Kerr spacetime."""
        r_s = self.kerr.r_s
        r0 = r0_factor * r_s
        L = L_factor * r_s * C

        result = self.kerr.integrate_equatorial_orbit(
            r0=r0, phi0=0.0, dr_dtau0=0.0, E=E, L=L,
            tau_span=(0, tau_end), n_points=10000,
        )

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.plot(result["x"] / r_s, result["y"] / r_s, "m-", linewidth=0.5)

        # Horizons
        r_plus = self.kerr.outer_horizon()
        r_minus = self.kerr.inner_horizon()
        outer = plt.Circle((0, 0), r_plus / r_s, color="black",
                           fill=True, label="Outer horizon")
        inner = plt.Circle((0, 0), r_minus / r_s, color="gray",
                           fill=True, alpha=0.5, label="Inner horizon")
        ax.add_patch(outer)
        ax.add_patch(inner)

        ax.set_xlabel("x / r_s")
        ax.set_ylabel("y / r_s")
        ax.set_title(f"Kerr Geodesic (a*={self.kerr.a_star})")
        ax.set_aspect("equal")
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    # ------------------------------------------------------------------
    # Schwarzschild embedding diagram (3D Plotly)
    # ------------------------------------------------------------------

    def plot_embedding_diagram(self, show: bool = True) -> go.Figure:
        """
        Flamm's paraboloid embedding of the Schwarzschild geometry.

        The embedding surface z(r) = 2*sqrt(r_s*(r - r_s)) for r >= r_s.
        """
        r_s = self.schw.r_s
        r = np.linspace(r_s * 1.001, 10 * r_s, 200)
        z = 2.0 * np.sqrt(r_s * (r - r_s))

        phi = np.linspace(0, 2 * np.pi, 100)
        R, Phi = np.meshgrid(r / r_s, phi)
        Z_mesh = 2.0 * np.sqrt(1.0 * (R - 1.0))  # normalised
        X = R * np.cos(Phi)
        Y = R * np.sin(Phi)

        fig = go.Figure(
            data=[
                go.Surface(x=X, y=Y, z=Z_mesh,
                           colorscale="Viridis", showscale=False),
                go.Surface(x=X, y=Y, z=-Z_mesh,
                           colorscale="Viridis", showscale=False),
            ]
        )
        fig.update_layout(
            title="Flamm's Paraboloid — Schwarzschild Embedding",
            scene=dict(
                xaxis_title="x / r_s",
                yaxis_title="y / r_s",
                zaxis_title="z (embedding)",
            ),
        )
        if show:
            fig.show()
        return fig

    def run_all(self, show: bool = True):
        """Generate all geodesic visualizations."""
        self.plot_schwarzschild_orbit(show=show)
        self.plot_kerr_orbit(show=show)
        self.plot_embedding_diagram(show=show)
