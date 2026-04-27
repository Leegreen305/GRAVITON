"""
Physical constants for GRAVITON simulations.

All values in SI units. Sources cited inline.
"""

import math

# ---------------------------------------------------------------------------
# Fundamental constants
# Source: CODATA 2018 recommended values (NIST)
# ---------------------------------------------------------------------------

G = 6.67430e-11          # Gravitational constant [m^3 kg^-1 s^-2]
C = 2.99792458e8         # Speed of light in vacuum [m s^-1]
HBAR = 1.054571817e-34   # Reduced Planck constant [J s]
H = 6.62607015e-34       # Planck constant [J s]
K_B = 1.380649e-23       # Boltzmann constant [J K^-1]
EPSILON_0 = 8.8541878128e-12  # Vacuum permittivity [F m^-1]

# ---------------------------------------------------------------------------
# Planck units
# Source: Derived from fundamental constants (Planck, 1899)
# ---------------------------------------------------------------------------

PLANCK_LENGTH = 1.616255e-35       # sqrt(ħG/c³) [m]
PLANCK_TIME = 5.391247e-44         # sqrt(ħG/c⁵) [s]
PLANCK_MASS = 2.176434e-8          # sqrt(ħc/G) [kg]
PLANCK_ENERGY = 1.956e9            # sqrt(ħc⁵/G) [J]
PLANCK_TEMPERATURE = 1.416784e32   # sqrt(ħc⁵/(G·k_B²)) [K]

# ---------------------------------------------------------------------------
# Casimir effect
# Source: Casimir, H.B.G. (1948). Proc. Kon. Ned. Akad. Wetensch. 51, 793.
# ---------------------------------------------------------------------------

# Dimensionless coefficient in Casimir formula
CASIMIR_COEFFICIENT = math.pi**2 / 240

# ---------------------------------------------------------------------------
# Alcubierre warp drive reference energies
# Source: Alcubierre, M. (1994). Class. Quantum Grav. 11, L73.
#         Pfenning & Ford (1997). Class. Quantum Grav. 14, 1743.
# ---------------------------------------------------------------------------

# Estimated exotic energy for a 1 m radius warp bubble at v_s = c
# E ~ -(c^4 / G) * R  (order-of-magnitude from metric integration)
EXOTIC_ENERGY_ALCUBIERRE = -(C**4 / G) * 1.0  # ~ -1.21e44 J for R = 1 m

# ---------------------------------------------------------------------------
# Astrophysical reference values
# ---------------------------------------------------------------------------

SOLAR_MASS = 1.989e30         # kg
SOLAR_LUMINOSITY = 3.828e26   # W (J/s)
EARTH_MASS = 5.972e24         # kg
EARTH_RADIUS = 6.371e6        # m
EARTH_ANGULAR_MOMENTUM = 7.07e33  # kg m^2 s^-1  (J = I * omega)
JUPITER_MASS_ENERGY = SOLAR_MASS * 1e-3 * C**2  # ~1.7e44 J

# ---------------------------------------------------------------------------
# Schwarzschild radius helper
# ---------------------------------------------------------------------------


def schwarzschild_radius(mass: float) -> float:
    """Compute the Schwarzschild radius r_s = 2GM/c^2 [m]."""
    return 2.0 * G * mass / C**2
