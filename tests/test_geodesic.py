"""
Tests for the geodesic module.
"""

from graviton.constants import G, C, SOLAR_MASS
from geodesic.solver import GeodesicSolver
from geodesic.kerr import KerrGeodesic
from geodesic.schwarzschild import SchwarzschildGeodesic
import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


class TestSchwarzschildGeodesic:
    """Tests for SchwarzschildGeodesic."""

    def setup_method(self):
        self.mass = 10.0 * SOLAR_MASS
        self.schw = SchwarzschildGeodesic(self.mass)

    def test_schwarzschild_radius(self):
        """r_s = 2GM/c^2 should be correct."""
        expected = 2.0 * G * self.mass / C ** 2
        assert self.schw.r_s == pytest.approx(expected, rel=1e-10)

    def test_isco_is_3rs(self):
        """ISCO for Schwarzschild should be 3 r_s."""
        assert self.schw.isco_radius() == pytest.approx(3.0 * self.schw.r_s, rel=1e-10)

    def test_metric_diagonal(self):
        """Schwarzschild metric should be diagonal."""
        g = self.schw.metric(
            np.array([0.0, 10 * self.schw.r_s, np.pi / 2, 0.0]))
        for mu in range(4):
            for nu in range(4):
                if mu != nu:
                    assert abs(g[mu, nu]) < 1e-20

    def test_metric_signature(self):
        """Metric should have signature (-,+,+,+) outside horizon."""
        r = 5.0 * self.schw.r_s
        g = self.schw.metric(np.array([0.0, r, np.pi / 2, 0.0]))
        assert g[0, 0] < 0  # timelike
        assert g[1, 1] > 0  # spacelike
        assert g[2, 2] > 0
        assert g[3, 3] > 0

    def test_effective_potential_diverges_near_origin(self):
        """V_eff should diverge as r -> 0."""
        L = 4.0 * self.schw.r_s * C
        r_small = np.array([self.schw.r_s * 0.1])
        r_large = np.array([self.schw.r_s * 10.0])
        V_small = abs(self.schw.effective_potential(r_small, L)[0])
        V_large = abs(self.schw.effective_potential(r_large, L)[0])
        assert V_small > V_large

    def test_circular_orbit_velocity_real(self):
        """Circular orbit velocity should be real outside ISCO."""
        r = 10.0 * self.schw.r_s
        v = self.schw.circular_orbit_velocity(r)
        assert np.isfinite(v)
        assert v > 0
        assert v < C  # should be subluminal

    def test_orbit_integration_runs(self):
        """Orbit integration should produce arrays of correct length."""
        r0 = 10.0 * self.schw.r_s
        L = 4.0 * self.schw.r_s * C
        result = self.schw.integrate_orbit(
            r0=r0, phi0=0.0, dr_dtau0=0.0, L=L,
            tau_span=(0, 1e3), n_points=100,
        )
        assert "r" in result
        assert "phi" in result
        assert len(result["r"]) == 100


class TestKerrGeodesic:
    """Tests for KerrGeodesic."""

    def setup_method(self):
        self.mass = 10.0 * SOLAR_MASS
        self.kerr = KerrGeodesic(self.mass, spin_parameter=0.9)

    def test_outer_horizon_exists(self):
        """Outer horizon should exist for a < M."""
        r_plus = self.kerr.outer_horizon()
        assert np.isfinite(r_plus)
        assert r_plus > 0

    def test_inner_horizon_smaller(self):
        """Inner horizon should be smaller than outer horizon."""
        r_plus = self.kerr.outer_horizon()
        r_minus = self.kerr.inner_horizon()
        assert r_minus < r_plus

    def test_kerr_reduces_to_schwarzschild(self):
        """For a=0, Kerr outer horizon should equal Schwarzschild radius."""
        kerr_zero = KerrGeodesic(self.mass, spin_parameter=0.0)
        r_plus = kerr_zero.outer_horizon()
        r_s = 2.0 * G * self.mass / C ** 2
        assert r_plus == pytest.approx(r_s / 2.0 + r_s / 2.0, rel=1e-6)  # r_s

    def test_isco_decreases_with_spin(self):
        """Prograde ISCO should decrease with increasing spin."""
        kerr_low = KerrGeodesic(self.mass, spin_parameter=0.1)
        kerr_high = KerrGeodesic(self.mass, spin_parameter=0.9)
        assert kerr_high.isco_radius() < kerr_low.isco_radius()

    def test_metric_has_off_diagonal(self):
        """Kerr metric should have g_{03} != 0 for a != 0."""
        r = 10.0 * self.kerr.r_s
        g = self.kerr.metric(np.array([0.0, r, np.pi / 2, 0.0]))
        assert abs(g[0, 3]) > 0

    def test_orbit_integration_runs(self):
        """Kerr orbit integration should run without error."""
        r0 = 8.0 * self.kerr.r_s
        L = 3.5 * self.kerr.r_s * C
        result = self.kerr.integrate_equatorial_orbit(
            r0=r0, phi0=0.0, dr_dtau0=0.0, E=0.95, L=L,
            tau_span=(0, 1e3), n_points=100,
        )
        assert "r" in result
        assert len(result["r"]) == 100


class TestGeodesicSolver:
    """Tests for the generic GeodesicSolver."""

    def test_flat_space_geodesic_is_straight_line(self):
        """In flat Minkowski space, geodesics should be straight lines."""

        def minkowski_metric(coords):
            g = np.diag([-C ** 2, 1.0, 1.0, 1.0])
            return g

        solver = GeodesicSolver(minkowski_metric)

        x0 = np.array([0.0, 1.0, 0.0, 0.0])
        u0 = np.array([C, 0.1 * C, 0.0, 0.0])  # mostly timelike

        result = solver.integrate(x0, u0, tau_span=(0, 1e-8), n_points=50)

        # In flat space, x1 should be linear in tau
        x1 = result["coords"][:, 1]
        tau = result["tau"]
        # Check linearity: the differences should be roughly constant
        dx = np.diff(x1)
        # nearly constant velocity
        assert np.std(dx) / np.mean(np.abs(dx)) < 0.01
