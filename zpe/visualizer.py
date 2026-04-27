"""
Visualizations for zero-point energy and Casimir effect.
"""

import numpy as np
import matplotlib.pyplot as plt

from zpe.casimir import CasimirEffect
from zpe.quantum_vacuum import QuantumVacuumField
from graviton.constants import HBAR, C


class ZPEVisualizer:
    """
    Generate plots for Casimir force, vacuum energy spectral density,
    and exotic energy density profiles.
    """

    def __init__(self):
        self.casimir = CasimirEffect()
        self.vacuum = QuantumVacuumField()

    def plot_casimir_force(self, show: bool = True):
        """Plot Casimir force/area vs plate separation."""
        d, fpa, _ = self.casimir.sweep_separation(
            d_min=10e-9, d_max=2e-6, N=500)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.semilogy(d * 1e9, np.abs(fpa), "b-", linewidth=2)
        ax.set_xlabel("Plate separation [nm]")
        ax.set_ylabel("|F/A| [Pa]")
        ax.set_title("Casimir Force per Unit Area vs Plate Separation")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    def plot_casimir_energy_density(self, show: bool = True):
        """Plot Casimir energy density vs plate separation."""
        d, _, u = self.casimir.sweep_separation(d_min=10e-9, d_max=2e-6, N=500)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.semilogy(d * 1e9, np.abs(u), "r-", linewidth=2)
        ax.set_xlabel("Plate separation [nm]")
        ax.set_ylabel("|u| [J/m^3]")
        ax.set_title("Casimir Vacuum Energy Density (negative)")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    def plot_zpe_spectral_density(self, omega_max: float = 1e15, N: int = 1000, show: bool = True):
        """Plot ZPE spectral density u(omega) vs frequency."""
        omega = np.linspace(1e6, omega_max, N)
        u = self.vacuum.spectral_density(omega)

        fig, ax = plt.subplots(figsize=(8, 5))
        ax.loglog(omega, u, "g-", linewidth=2)
        ax.set_xlabel("omega [rad/s]")
        ax.set_ylabel("u(omega) [J/m^3 per rad/s]")
        ax.set_title("Zero-Point Energy Spectral Density")
        ax.grid(True, alpha=0.3, which="both")
        plt.tight_layout()
        if show:
            plt.show()
        return fig

    def run_all(self, show: bool = True):
        """Generate all ZPE visualizations."""
        self.plot_casimir_force(show=show)
        self.plot_casimir_energy_density(show=show)
        self.plot_zpe_spectral_density(show=show)
