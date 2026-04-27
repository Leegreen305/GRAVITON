"""
Geodesic Module

Solves geodesic equations in curved spacetime for Schwarzschild and Kerr metrics.

References:
    Schwarzschild, K. (1916). Sitzungsber. Preuss. Akad. Wiss. Berlin, 189.
    Kerr, R.P. (1963). Phys. Rev. Lett. 11, 237.
    Misner, Thorne & Wheeler (1973). "Gravitation." W.H. Freeman.
"""

from geodesic.solver import GeodesicSolver
from geodesic.schwarzschild import SchwarzschildGeodesic
from geodesic.kerr import KerrGeodesic

__all__ = [
    "GeodesicSolver",
    "SchwarzschildGeodesic",
    "KerrGeodesic",
]
