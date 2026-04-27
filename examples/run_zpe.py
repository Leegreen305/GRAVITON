#!/usr/bin/env python3
"""
Example: Zero-Point Energy and Casimir Effect

Run:
    python examples/run_zpe.py
"""

from simulation.dashboard import Dashboard
from zpe.visualizer import ZPEVisualizer
from zpe.exotic_matter import ExoticMatter
from zpe.quantum_vacuum import QuantumVacuumField
from zpe.casimir import CasimirEffect
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


def main():
    Dashboard.header()

    print("=" * 60)
    print("  CASIMIR EFFECT")
    print("=" * 60)

    casimir = CasimirEffect(plate_area=1.0)

    # Standard separation
    d = 100e-9  # 100 nm
    fpa = casimir.force_per_area(d)
    u = casimir.energy_density(d)
    E_total = casimir.total_energy(d)

    print(f"  Plate separation: {d * 1e9:.0f} nm")
    print(f"  Force/area:       {fpa:.4e} Pa")
    print(f"  Energy density:   {u:.4e} J/m^3")
    print(f"  Total energy:     {E_total:.4e} J")

    Dashboard.show_casimir(separation=d, force_pa=fpa, energy_density=u)

    # Lamoreaux comparison
    print("\n  Lamoreaux (1997) comparison:")
    comp = CasimirEffect.lamoreaux_1997_comparison()
    print(f"    Theory:  {comp['theory_Pa']:.4e} Pa")
    print(f"    Expt:    {comp['experiment_Pa']:.4e} Pa")
    print(f"    Error:   {comp['relative_error']:.1%}")

    # Quantum vacuum
    print("\n" + "=" * 60)
    print("  QUANTUM VACUUM ENERGY")
    print("=" * 60)

    vacuum = QuantumVacuumField()
    rho = vacuum.total_energy_density()
    print(f"  ZPE density (Planck cutoff): {rho:.3e} J/m^3")

    disc = vacuum.cosmological_constant_discrepancy()
    print(
        f"  Observed Lambda density:     {disc['rho_observed_J_per_m3']:.3e} J/m^3")
    print(f"  QFT/Observed ratio:          10^{disc['log10_ratio']:.0f}")
    print("  (This is the cosmological constant problem)")

    # Exotic matter
    print("\n" + "=" * 60)
    print("  EXOTIC MATTER CONSTRAINTS")
    print("=" * 60)

    tau = 1e-6  # 1 microsecond
    bound = ExoticMatter.quantum_inequality_bound(tau)
    print(f"  QI bound (tau={tau:.0e} s): {bound:.3e} J/m^3")

    r = 1.0
    omega = 1e15
    rho_sq = ExoticMatter.squeezed_vacuum_energy_density(r, omega)
    print(f"  Squeezed vacuum (r={r}, omega={omega:.0e}): {rho_sq:.3e} J/m^3")

    # Visualizations
    print("\n  Generating ZPE visualizations...")
    viz = ZPEVisualizer()
    viz.run_all(show=True)


if __name__ == "__main__":
    main()
