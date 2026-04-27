"""
Alcubierre Warp Drive Module

Simulates the Alcubierre warp drive spacetime metric, exotic energy
requirements, bubble geometry, and provides interactive 3D visualizations.

Reference:
    Alcubierre, M. (1994). "The warp drive: hyper-fast travel within
    general relativity." Classical and Quantum Gravity, 11(5), L73.
"""

from alcubierre.metric import AlcubierreMetric
from alcubierre.energy import ExoticEnergyCalculator
from alcubierre.bubble import WarpBubble
from alcubierre.visualizer import AlcubierreVisualizer

__all__ = [
    "AlcubierreMetric",
    "ExoticEnergyCalculator",
    "WarpBubble",
    "AlcubierreVisualizer",
]
