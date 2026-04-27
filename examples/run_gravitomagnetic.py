#!/usr/bin/env python3
"""
Example: Gravitomagnetic Field and Frame-Dragging Simulation

Run:
    python examples/run_gravitomagnetic.py
"""

from graviton.constants import EARTH_MASS, EARTH_RADIUS, EARTH_ANGULAR_MOMENTUM
from simulation.dashboard import Dashboard
from gravitomagnetic.visualizer import GravitomagneticVisualizer
from gravitomagnetic.frame_dragging import FrameDragging
from gravitomagnetic.gem_equations import GravitoElectroMagneticField
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


def main():
    Dashboard.header()

    print("=" * 60)
    print("  EARTH GRAVITOMAGNETIC FIELD")
    print("=" * 60)

    J = np.array([0.0, 0.0, EARTH_ANGULAR_MOMENTUM])

    # GEM fields
    gem = GravitoElectroMagneticField(mass=EARTH_MASS, angular_momentum=J)

    # Compute at a satellite altitude (400 km above surface)
    r = EARTH_RADIUS + 400e3
    Ex, Ey, Ez = gem.compute_gravitoelectric(r, 0, 0)
    Bx, By, Bz = gem.compute_gravitomagnetic(r, 0, 0)
    print(f"At r = {r:.3e} m (LEO):")
    print(
        f"  |E_g| = {np.sqrt(float(Ex)**2 + float(Ey)**2 + float(Ez)**2):.4e} m/s^2")
    print(
        f"  |B_g| = {np.sqrt(float(Bx)**2 + float(By)**2 + float(Bz)**2):.4e} rad/s")

    # Frame dragging
    fd = FrameDragging(mass=EARTH_MASS, angular_momentum=J)
    Ox, Oy, Oz = fd.compute_precession_rate(r, 0, 0)
    omega_lt = np.sqrt(float(Ox)**2 + float(Oy)**2 + float(Oz)**2)
    print(f"  LT precession rate = {omega_lt:.4e} rad/s")
    print(
        f"  LT precession rate = {omega_lt * 3.156e7 * 1e3 * 206265:.4f} marcsec/yr")

    Dashboard.show_gravitomagnetic(
        mass=EARTH_MASS,
        angular_momentum_mag=EARTH_ANGULAR_MOMENTUM,
        precession_rate=omega_lt,
    )

    # Gyroscope precession (Gravity Probe B scenario)
    print("\n  Integrating gyroscope precession (1 year)...")
    gyro = fd.integrate_gyroscope(
        r0=(r, 0.0, 0.0),
        S0=(0.0, 1.0, 0.0),
        t_span=(0, 3.156e7),
        n_points=1000,
    )
    dS = np.sqrt(
        (gyro["Sx"][-1] - gyro["Sx"][0]) ** 2
        + (gyro["Sy"][-1] - gyro["Sy"][0]) ** 2
        + (gyro["Sz"][-1] - gyro["Sz"][0]) ** 2
    )
    print(f"  Spin change after 1 year: |dS| = {dS:.6e}")

    # Visualizations
    print("\n  Generating field visualizations...")
    viz = GravitomagneticVisualizer(mass=EARTH_MASS, angular_momentum=J)
    viz.run_all(show=True)


if __name__ == "__main__":
    main()
