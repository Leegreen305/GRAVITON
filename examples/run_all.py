#!/usr/bin/env python3
"""
Run all GRAVITON example simulations sequentially.

Run:
    python examples/run_all.py
"""

from simulation.dashboard import Dashboard
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


def main():
    Dashboard.header()
    print("Running all GRAVITON simulations...\n")

    # Import and run each example's main function
    print("=" * 60)
    print("  [1/4] ALCUBIERRE WARP DRIVE")
    print("=" * 60)
    sys.argv = ["run_alcubierre.py", "--no-plot"]
    from examples.run_alcubierre import main as run_alc
    run_alc()

    print("\n" + "=" * 60)
    print("  [2/4] GRAVITOMAGNETIC FIELDS")
    print("=" * 60)
    # Reset matplotlib
    import matplotlib
    matplotlib.use("Agg")

    from gravitomagnetic.gem_equations import GravitoElectroMagneticField
    from gravitomagnetic.frame_dragging import FrameDragging
    from graviton.constants import EARTH_MASS, EARTH_RADIUS, EARTH_ANGULAR_MOMENTUM
    import numpy as np

    J = np.array([0.0, 0.0, EARTH_ANGULAR_MOMENTUM])
    gem = GravitoElectroMagneticField(mass=EARTH_MASS, angular_momentum=J)
    r = EARTH_RADIUS + 400e3
    Ex, Ey, Ez = gem.compute_gravitoelectric(r, 0, 0)
    print(
        f"  Earth |E_g| at LEO: {np.sqrt(float(Ex)**2+float(Ey)**2+float(Ez)**2):.4e} m/s^2")

    fd = FrameDragging(mass=EARTH_MASS, angular_momentum=J)
    Ox, Oy, Oz = fd.compute_precession_rate(r, 0, 0)
    print(
        f"  LT precession: {np.sqrt(float(Ox)**2+float(Oy)**2+float(Oz)**2):.4e} rad/s")

    print("\n" + "=" * 60)
    print("  [3/4] ZERO-POINT ENERGY")
    print("=" * 60)
    from zpe.casimir import CasimirEffect
    from zpe.quantum_vacuum import QuantumVacuumField

    casimir = CasimirEffect()
    d = 100e-9
    print(
        f"  Casimir F/A at {d*1e9:.0f} nm: {casimir.force_per_area(d):.4e} Pa")

    vacuum = QuantumVacuumField()
    print(
        f"  ZPE density (Planck cutoff): {vacuum.total_energy_density():.3e} J/m^3")

    print("\n" + "=" * 60)
    print("  [4/4] GEODESICS")
    print("=" * 60)
    from geodesic.schwarzschild import SchwarzschildGeodesic
    from graviton.constants import SOLAR_MASS

    schw = SchwarzschildGeodesic(10.0 * SOLAR_MASS)
    print(f"  Schwarzschild ISCO (10 M_sun): {schw.isco_radius():.3e} m")

    print("\n" + "=" * 60)
    print("  ALL SIMULATIONS COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
