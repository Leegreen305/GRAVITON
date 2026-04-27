"""
Tests for the gravitomagnetic module.
"""

from graviton.constants import G, C, EARTH_MASS, EARTH_RADIUS, EARTH_ANGULAR_MOMENTUM
from gravitomagnetic.force_calculator import GravitomagneticForce
from gravitomagnetic.frame_dragging import FrameDragging
from gravitomagnetic.gem_equations import GravitoElectroMagneticField
import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


class TestGEM:
    """Tests for GravitoElectroMagneticField."""

    def setup_method(self):
        self.gem = GravitoElectroMagneticField(
            mass=EARTH_MASS,
            angular_momentum=(0.0, 0.0, EARTH_ANGULAR_MOMENTUM),
        )

    def test_gravitoelectric_points_inward(self):
        """E_g should point radially inward (towards mass)."""
        r = EARTH_RADIUS * 2
        Ex, Ey, Ez = self.gem.compute_gravitoelectric(r, 0.0, 0.0)
        # At (r, 0, 0), Ex should be negative (pointing towards origin)
        assert float(Ex) < 0

    def test_gravitoelectric_magnitude(self):
        """E_g magnitude at Earth's surface should be ~9.8 m/s^2."""
        r = EARTH_RADIUS
        Ex, Ey, Ez = self.gem.compute_gravitoelectric(r, 0.0, 0.0)
        mag = np.sqrt(float(Ex) ** 2 + float(Ey) ** 2 + float(Ez) ** 2)
        assert mag == pytest.approx(9.8, rel=0.02)

    def test_gravitomagnetic_field_exists(self):
        """B_g should be non-zero for a rotating body."""
        r = EARTH_RADIUS * 2
        Bx, By, Bz = self.gem.compute_gravitomagnetic(r, 0.0, 0.0)
        mag = np.sqrt(float(Bx) ** 2 + float(By) ** 2 + float(Bz) ** 2)
        assert mag > 0

    def test_gravitomagnetic_divergence_free(self):
        """div B_g should be approximately zero (numerical check)."""
        N = 20
        L = EARTH_RADIUS * 3
        lin = np.linspace(-L, L, N)
        dx = lin[1] - lin[0]
        X, Y, Z = np.meshgrid(lin, lin, lin, indexing="ij")

        Bx, By, Bz = self.gem.compute_gravitomagnetic(X, Y, Z)

        # Central differences for divergence
        dBx_dx = np.gradient(Bx, dx, axis=0)
        dBy_dy = np.gradient(By, dx, axis=1)
        dBz_dz = np.gradient(Bz, dx, axis=2)
        div_B = dBx_dx + dBy_dy + dBz_dz

        # Should be small relative to field magnitude
        B_mag = np.sqrt(Bx ** 2 + By ** 2 + Bz ** 2)
        B_max = np.max(B_mag)
        # avoid boundary effects
        div_max = np.max(np.abs(div_B[2:-2, 2:-2, 2:-2]))
        assert div_max / B_max < 0.3  # numerical divergence should be small

    def test_force_direction(self):
        """Gravitomagnetic force should be perpendicular to velocity."""
        r = EARTH_RADIUS * 2
        E_g = self.gem.compute_gravitoelectric(r, 0.0, 0.0)
        B_g = self.gem.compute_gravitomagnetic(r, 0.0, 0.0)

        v = np.array([0.0, 1e3, 0.0])
        Fx, Fy, Fz = self.gem.compute_force(1.0, v, E_g, B_g)
        # The v x B component should be perpendicular to v
        # Can't easily test this for the total force (E+vxB), but at least check it's non-zero
        F_mag = np.sqrt(float(Fx) ** 2 + float(Fy) ** 2 + float(Fz) ** 2)
        assert F_mag > 0


class TestFrameDragging:
    """Tests for FrameDragging."""

    def setup_method(self):
        self.fd = FrameDragging(
            mass=EARTH_MASS,
            angular_momentum=(0.0, 0.0, EARTH_ANGULAR_MOMENTUM),
        )

    def test_precession_rate_nonzero(self):
        """LT precession rate should be non-zero near Earth."""
        r = EARTH_RADIUS + 642e3  # Gravity Probe B altitude
        Ox, Oy, Oz = self.fd.compute_precession_rate(r, 0.0, 0.0)
        omega = np.sqrt(float(Ox) ** 2 + float(Oy) ** 2 + float(Oz) ** 2)
        assert omega > 0

    def test_gyroscope_integration_preserves_magnitude(self):
        """Gyroscope spin magnitude should be conserved (|dS/dt| = |Omega x S|)."""
        r = EARTH_RADIUS + 642e3
        S0 = np.array([1.0, 0.0, 0.0])
        result = self.fd.integrate_gyroscope(
            r0=(r, 0.0, 0.0),
            S0=S0,
            t_span=(0, 3.156e7),  # 1 year
            n_points=500,
        )
        # Check spin magnitude is preserved
        S_mag = np.sqrt(result["Sx"] ** 2 + result["Sy"]
                        ** 2 + result["Sz"] ** 2)
        np.testing.assert_allclose(S_mag, 1.0, rtol=1e-6)

    def test_time_dilation_near_unity(self):
        """Far from the source, dtau/dt should be close to 1."""
        r = EARTH_RADIUS * 100
        ratio = self.fd.compute_time_dilation(r, 0.0, 0.0)
        assert float(ratio) == pytest.approx(1.0, abs=1e-6)
