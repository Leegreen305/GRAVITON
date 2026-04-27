"""
Gravitomagnetic Module

Simulates gravitoelectromagnetic (GEM) fields, the Lense-Thirring
frame-dragging effect, and gravitomagnetic forces on moving masses.

References:
    Mashhoon, B. (2008). "Gravitoelectromagnetism: A Brief Review."
        arXiv:gr-qc/0311030
    Lense, J. & Thirring, H. (1918). Phys. Z. 19, 156.
"""

from gravitomagnetic.gem_equations import GravitoElectroMagneticField
from gravitomagnetic.frame_dragging import FrameDragging
from gravitomagnetic.force_calculator import GravitomagneticForce

__all__ = [
    "GravitoElectroMagneticField",
    "FrameDragging",
    "GravitomagneticForce",
]
