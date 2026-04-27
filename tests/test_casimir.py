"""
Tests for the Casimir effect and zero-point energy module.
"""

from graviton.constants import HBAR, C
from zpe.exotic_matter import ExoticMatter
from zpe.quantum_vacuum import QuantumVacuumField
from zpe.casimir import CasimirEffect
import pytest
import numpy as np
import sys
import os
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")))


class TestCasimirEffect:
    """Tests for CasimirEffect."""

    def setup_method(self):
        self.casimir = CasimirEffect(plate_area=1.0)

    def test_force_is_attractive(self):
        """Casimir force should be negative (attractive)."""
        fpa = self.casimir.force_per_area(100e-9)
        assert fpa < 0

    def test_force_scales_as_d_minus_4(self):
        """Force should scale as 1/d^4."""
        d1 = 100e-9
        d2 = 200e-9
        f1 = abs(self.casimir.force_per_area(d1))
        f2 = abs(self.casimir.force_per_area(d2))
        ratio = f1 / f2
        expected_ratio = (d2 / d1) ** 4
        assert ratio == pytest.approx(expected_ratio, rel=1e-10)

    def test_energy_density_is_negative(self):
        """Casimir energy density should be negative."""
        u = self.casimir.energy_density(100e-9)
        assert u < 0

    def test_total_energy_is_negative(self):
        """Total Casimir energy should be negative."""
        E = self.casimir.total_energy(100e-9)
        assert E < 0

    def test_sweep_returns_correct_shape(self):
        """Sweep should return arrays of correct length."""
        d, fpa, u = self.casimir.sweep_separation(N=100)
        assert len(d) == 100
        assert len(fpa) == 100
        assert len(u) == 100

    def test_lamoreaux_comparison(self):
        """Lamoreaux comparison should return a dict with expected keys."""
        result = CasimirEffect.lamoreaux_1997_comparison()
        assert "theory_Pa" in result
        assert "experiment_Pa" in result
        assert result["relative_error"] >= 0


class TestQuantumVacuum:
    """Tests for QuantumVacuumField."""

    def setup_method(self):
        # Use a low cutoff for fast tests
        self.vacuum = QuantumVacuumField(cutoff_frequency=1e15)

    def test_spectral_density_positive(self):
        """ZPE spectral density should be positive for positive omega."""
        omega = np.array([1e10, 1e12, 1e14])
        u = self.vacuum.spectral_density(omega)
        assert np.all(u > 0)

    def test_spectral_density_cubic_scaling(self):
        """u(omega) should scale as omega^3."""
        omega1 = 1e12
        omega2 = 2e12
        u1 = self.vacuum.spectral_density(np.array([omega1]))[0]
        u2 = self.vacuum.spectral_density(np.array([omega2]))[0]
        assert u2 / u1 == pytest.approx(8.0, rel=1e-10)

    def test_total_energy_density_positive(self):
        """Total ZPE density should be positive."""
        rho = self.vacuum.total_energy_density()
        assert rho > 0

    def test_analytical_vs_numerical(self):
        """Analytic and numerical integration should agree."""
        rho_analytic = self.vacuum.total_energy_density()
        rho_numerical = self.vacuum.total_energy_density_numerical(N=50000)
        assert rho_numerical == pytest.approx(rho_analytic, rel=0.01)

    def test_cosmological_constant_discrepancy(self):
        """QFT vacuum energy should far exceed the observed cosmological constant."""
        vacuum_full = QuantumVacuumField()  # Planck cutoff
        disc = vacuum_full.cosmological_constant_discrepancy()
        assert disc["ratio"] > 1e50  # should be ~10^120


class TestExoticMatter:
    """Tests for ExoticMatter."""

    def test_quantum_inequality_bound_negative(self):
        """QI bound should be negative."""
        bound = ExoticMatter.quantum_inequality_bound(1e-6)
        assert bound < 0

    def test_qi_bound_scales_as_tau_minus_4(self):
        """QI bound should scale as 1/tau^4."""
        tau1 = 1e-6
        tau2 = 2e-6
        b1 = abs(ExoticMatter.quantum_inequality_bound(tau1))
        b2 = abs(ExoticMatter.quantum_inequality_bound(tau2))
        assert b1 / b2 == pytest.approx((tau2 / tau1) ** 4, rel=1e-10)

    def test_squeezed_vacuum_negative(self):
        """Squeezed vacuum energy density should be negative."""
        rho = ExoticMatter.squeezed_vacuum_energy_density(1.0, 1e15)
        assert rho < 0

    def test_warp_drive_feasibility_returns_dict(self):
        """Feasibility check should return expected keys."""
        result = ExoticMatter.warp_drive_feasibility(-1e40, 100.0)
        assert "required_energy_density_J_m3" in result
        assert "qi_lower_bound_J_m3" in result
        assert "violates_qi" in result
