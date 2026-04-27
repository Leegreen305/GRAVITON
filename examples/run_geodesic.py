#!/usr/bin/env python3
"""
Example: Geodesic orbits in Schwarzschild and Kerr spacetimes.

Run:
    python examples/run_geodesic.py
"""

from graviton.constants import SOLAR_MASS, G, C
from simulation.dashboard import Dashboard
from geodesic.visualizer import GeodesicVisualizer
from geodesic.kerr import KerrGeodesic
from geodesic.schwarzschild import SchwarzschildGeodesic
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


def main():
    Dashboard.header()
    mass = 10.0 * SOLAR_MASS

    # --- Schwarzschild ---
    print("=" * 60)
    print("  SCHWARZSCHILD GEODESICS")
    print("=" * 60)

    schw = SchwarzschildGeodesic(mass)
    print(f"  Mass: {mass:.3e} kg  ({mass / SOLAR_MASS:.0f} M_sun)")
    print(f"  Schwarzschild radius: {schw.r_s:.3e} m")
    print(
        f"  ISCO radius: {schw.isco_radius():.3e} m  ({schw.isco_radius() / schw.r_s:.1f} r_s)")

    Dashboard.show_geodesic(
        metric_type="Schwarzschild",
        mass=mass,
        r_s=schw.r_s,
        isco=schw.isco_radius(),
    )

    # --- Kerr ---
    print("\n" + "=" * 60)
    print("  KERR GEODESICS (a* = 0.9)")
    print("=" * 60)

    kerr = KerrGeodesic(mass, spin_parameter=0.9)
    print(f"  Outer horizon: {kerr.outer_horizon():.3e} m")
    print(f"  Inner horizon: {kerr.inner_horizon():.3e} m")
    print(f"  Prograde ISCO: {kerr.isco_radius():.3e} m")

    Dashboard.show_geodesic(
        metric_type="Kerr (a*=0.9)",
        mass=mass,
        r_s=kerr.r_s,
        isco=kerr.isco_radius(),
    )

    # Visualizations
    print("\n  Generating geodesic visualizations...")
    viz = GeodesicVisualizer(mass=mass)
    viz.run_all(show=True)


if __name__ == "__main__":
    main()
