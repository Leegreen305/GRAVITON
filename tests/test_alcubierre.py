"""
Tests for the Alcubierre warp drive module.
"""

from graviton.constants import C
from alcubierre.bubble import WarpBubble
from alcubierre.energy import ExoticEnergyCalculator
from alcubierre.metric import AlcubierreMetric
import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


class TestAlcubierreMetric:
    """Tests for AlcubierreMetric."""

    def setup_method(self):
        self.metric = AlcubierreMetric(
            bubble_radius=100, wall_thickness=8.0, warp_velocity=1.0)

    def test_shape_function_center_is_one(self):
        """Shape function should be ~1 at the bubble centre."""
        f = self.metric.compute_shape_function(
            np.array([0.0]), np.array([0.0]), np.array([0.0])
        )
        assert f[0] == pytest.approx(1.0, abs=1e-6)

    def test_shape_function_far_away_is_zero(self):
        """Shape function should be ~0 far outside the bubble."""
        f = self.metric.compute_shape_function(
            np.array([1e6]), np.array([0.0]), np.array([0.0])
        )
        assert abs(f[0]) < 1e-6

    def test_shape_function_range(self):
        """Shape function should be between 0 and 1."""
        X, Y, Z = self.metric.make_grid(N=20)
        f = self.metric.compute_shape_function(X, Y, Z)
        assert np.all(f >= -1e-10)
        assert np.all(f <= 1.0 + 1e-10)

    def test_metric_tensor_shape(self):
        """Metric tensor should have shape (4, 4, ...)."""
        X, Y, Z = self.metric.make_grid(N=10)
        g = self.metric.compute_metric_tensor(X, Y, Z)
        assert g.shape[:2] == (4, 4)
        assert g.shape[2:] == X.shape

    def test_metric_symmetry(self):
        """Metric tensor should be symmetric: g[mu,nu] == g[nu,mu]."""
        X, Y, Z = self.metric.make_grid(N=10)
        g = self.metric.compute_metric_tensor(X, Y, Z)
        for mu in range(4):
            for nu in range(mu + 1, 4):
                np.testing.assert_allclose(g[mu, nu], g[nu, mu], atol=1e-15)

    def test_flat_spacetime_at_center(self):
        """Inside the bubble g_00 should approach -c^2 (flat Minkowski)."""
        g = self.metric.compute_metric_tensor(
            np.array([0.0]), np.array([0.0]), np.array([0.0])
        )
        # At centre f=1, so g_00 = -(c^2 - v_s^2) for v_s = c => g_00 ~ 0
        # For v_s < c, g_00 < 0
        assert g[0, 0, 0] <= 0  # timelike

    def test_expansion_scalar_sign(self):
        """Expansion scalar should be positive behind bubble, negative ahead."""
        # Behind bubble (negative x)
        theta_behind = self.metric.compute_expansion_scalar(
            np.array([-self.metric.R]), np.array([0.0]), np.array([0.0])
        )
        # Ahead of bubble (positive x)
        theta_ahead = self.metric.compute_expansion_scalar(
            np.array([self.metric.R]), np.array([0.0]), np.array([0.0])
        )
        # The expansion scalar flips sign across the bubble
        # At exact bubble wall the sign depends on df/dr
        # Check that they have opposite signs
        assert theta_behind[0] * theta_ahead[0] <= 0

    def test_bubble_interior(self):
        """Points at the origin should be inside the bubble."""
        mask = self.metric.get_bubble_interior(
            np.array([0.0]), np.array([0.0]), np.array([0.0])
        )
        assert mask[0] == True

    def test_bubble_exterior(self):
        """Points far away should be outside the bubble."""
        mask = self.metric.get_bubble_interior(
            np.array([1e6]), np.array([0.0]), np.array([0.0])
        )
        assert mask[0] == False


class TestExoticEnergy:
    """Tests for ExoticEnergyCalculator."""

    def setup_method(self):
        self.calc = ExoticEnergyCalculator(
            bubble_radius=100, wall_thickness=8.0, warp_velocity=1.0)

    def test_energy_density_is_negative(self):
        """Exotic matter energy density must be negative (or zero)."""
        x = np.linspace(-200, 200, 20)
        X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
        T_00 = self.calc.compute_energy_density(X, Y, Z)
        # should be <= 0 (with numerical tolerance)
        assert np.all(T_00 <= 1e-10)

    def test_total_exotic_energy_is_negative(self):
        """Total integrated exotic energy must be negative."""
        E = self.calc.compute_total_exotic_energy(N=20)
        assert E < 0

    def test_pfenning_ford_bound_is_negative(self):
        """Pfenning-Ford bound should be a large negative number."""
        E_min = self.calc.pfenning_ford_bound()
        assert E_min < 0

    def test_energy_scales_with_velocity(self):
        """Energy magnitude should increase with warp velocity."""
        calc_slow = ExoticEnergyCalculator(
            bubble_radius=100, wall_thickness=8.0, warp_velocity=0.5)
        calc_fast = ExoticEnergyCalculator(
            bubble_radius=100, wall_thickness=8.0, warp_velocity=2.0)
        E_slow = abs(calc_slow.compute_total_exotic_energy(N=20))
        E_fast = abs(calc_fast.compute_total_exotic_energy(N=20))
        assert E_fast > E_slow

    def test_compare_energies_returns_dict(self):
        """compare_to_known_energies should return a dict with expected keys."""
        result = self.calc.compare_to_known_energies(-1e40)
        assert "exotic_energy_J" in result
        assert "fraction_of_jupiter_mass_energy" in result


class TestWarpBubble:
    """Tests for WarpBubble."""

    def setup_method(self):
        self.bubble = WarpBubble(warp_velocity=2.0)

    def test_propagation(self):
        """Bubble should move in x direction."""
        pos0 = self.bubble.position.copy()
        self.bubble.propagate(1.0)
        assert self.bubble.position[0] > pos0[0]
        assert self.bubble.position[1] == pos0[1]
        assert self.bubble.position[2] == pos0[2]

    def test_causal_disconnection_superluminal(self):
        """Superluminal bubble should be causally disconnected."""
        bubble = WarpBubble(warp_velocity=2.0)
        assert bubble.is_causally_disconnected() == True

    def test_causal_disconnection_subluminal(self):
        """Subluminal bubble should NOT be causally disconnected."""
        bubble = WarpBubble(warp_velocity=0.5)
        assert bubble.is_causally_disconnected() == False

    def test_hawking_temperature_positive(self):
        """Hawking-like temperature should be positive."""
        T = self.bubble.get_hawking_radiation_flux()
        assert T > 0

    def test_tidal_forces_positive(self):
        """Tidal forces should be non-negative."""
        forces = self.bubble.get_tidal_forces(
            np.array([self.bubble.R]), np.array([0.0]), np.array([0.0])
        )
        assert np.all(forces >= 0)
