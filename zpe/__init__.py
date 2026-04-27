"""
Zero-Point Energy (ZPE) Module

Simulates Casimir vacuum energy, quantum vacuum field density,
and exotic matter negative-energy-density regions.

References:
    Casimir, H.B.G. (1948). Proc. Kon. Ned. Akad. Wetensch. 51, 793.
    Ford, L.H. (1978). Proc. R. Soc. Lond. A 364, 227.
"""

from zpe.casimir import CasimirEffect
from zpe.quantum_vacuum import QuantumVacuumField
from zpe.exotic_matter import ExoticMatter

__all__ = [
    "CasimirEffect",
    "QuantumVacuumField",
    "ExoticMatter",
]
