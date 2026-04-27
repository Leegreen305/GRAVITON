#!/usr/bin/env python3
"""
Example: Alcubierre Warp Drive Simulation

Run:
    python examples/run_alcubierre.py --velocity 10 --radius 100 --sigma 8
"""

from simulation.dashboard import Dashboard
from alcubierre.visualizer import AlcubierreVisualizer
from alcubierre.bubble import WarpBubble
from alcubierre.energy import ExoticEnergyCalculator
from alcubierre.metric import AlcubierreMetric
import numpy as np
import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


def main():
    parser = argparse.ArgumentParser(
        description="Alcubierre Warp Drive Simulator")
    parser.add_argument("--velocity", type=float, default=10.0,
                        help="Warp velocity as fraction of c")
    parser.add_argument("--radius", type=float,
                        default=100.0, help="Bubble radius [m]")
    parser.add_argument("--sigma", type=float, default=8.0,
                        help="Wall thickness parameter")
    parser.add_argument("--no-plot", action="store_true",
                        help="Skip visualizations")
    args = parser.parse_args()

    Dashboard.header()

    # Metric computation
    metric = AlcubierreMetric(
        bubble_radius=args.radius,
        wall_thickness=args.sigma,
        warp_velocity=args.velocity,
    )

    X, Y, Z = metric.make_grid(N=50)
    theta = metric.compute_expansion_scalar(X, Y, Z)
    print(f"Expansion scalar range: [{theta.min():.3e}, {theta.max():.3e}]")

    # Energy calculation
    energy_calc = ExoticEnergyCalculator(
        bubble_radius=args.radius,
        wall_thickness=args.sigma,
        warp_velocity=args.velocity,
    )
    E = energy_calc.compute_total_exotic_energy(N=40)
    comparisons = energy_calc.compare_to_known_energies(E)
    print(f"Total exotic energy: {E:.3e} J")
    print(
        f"Jupiter mass-energy equivalent: {comparisons['fraction_of_jupiter_mass_energy']:.3e}x")

    # Bubble properties
    bubble = WarpBubble(
        bubble_radius=args.radius,
        wall_thickness=args.sigma,
        warp_velocity=args.velocity,
    )
    T_H = bubble.get_hawking_radiation_flux()

    Dashboard.show_alcubierre(
        velocity_c=args.velocity,
        radius=args.radius,
        sigma=args.sigma,
        exotic_energy=E,
        hawking_temp=T_H,
        causally_disconnected=bubble.is_causally_disconnected(),
    )

    # Visualizations
    if not args.no_plot:
        viz = AlcubierreVisualizer(
            bubble_radius=args.radius,
            wall_thickness=args.sigma,
            warp_velocity=args.velocity,
        )
        viz.run_dashboard(show=True)


if __name__ == "__main__":
    main()
