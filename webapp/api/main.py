"""
GRAVITON — FastAPI Backend
Serves physics simulation endpoints for the web dashboard.
"""
from graviton.constants import C, SOLAR_MASS
from geodesic.kerr import KerrGeodesic
from geodesic.schwarzschild import SchwarzschildGeodesic
from zpe.exotic_matter import ExoticMatter
from zpe.quantum_vacuum import QuantumVacuumField
from zpe.casimir import CasimirEffect
from gravitomagnetic.frame_dragging import FrameDragging
from gravitomagnetic.gem_equations import GravitoElectroMagneticField
from alcubierre.bubble import WarpBubble
from alcubierre.energy import ExoticEnergyCalculator
from alcubierre.metric import AlcubierreMetric
import numpy as np
from typing import List, Optional
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
import sys
import os
from pathlib import Path

# Ensure the project root is on the path
PROJECT_ROOT = str(Path(__file__).resolve().parents[2])
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ── Physics module imports ──────────────────────────────────────────

# ── App ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="GRAVITON API",
    description="Exotic Propulsion & Spacetime Engineering Simulator",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ════════════════════════════════════════════════════════════════════
#  REQUEST / RESPONSE MODELS
# ════════════════════════════════════════════════════════════════════

class AlcubierreRequest(BaseModel):
    velocity: float = Field(1.0, description="Warp velocity in multiples of c")
    radius: float = Field(100.0, description="Bubble radius [m]")
    sigma: float = Field(8.0, description="Wall thickness parameter")
    grid_n: int = Field(60, description="Grid resolution per axis")


class AlcubierreResponse(BaseModel):
    expansion_scalar: List[List[float]]
    energy_density: List[List[float]]
    shape_profile_r: List[float]
    shape_profile_f: List[float]
    total_exotic_energy: float
    pfenning_ford_bound: float
    hawking_temperature: float
    is_causally_disconnected: bool
    energy_comparisons: dict
    x_coords: List[float]
    y_coords: List[float]


class GravitomagneticRequest(BaseModel):
    mass: float = Field(5.972e24, description="Central mass [kg]")
    radius: float = Field(6.371e6, description="Orbital radius [m]")
    angular_momentum_z: float = Field(
        7.07e33, description="Angular momentum z-component [kg m^2/s]")


class GravitomagneticResponse(BaseModel):
    Eg_magnitude: float
    Bg_magnitude: float
    lt_precession_rate: float
    time_dilation: float
    Eg_field: List[List[float]]
    Bg_field: List[List[float]]
    x_coords: List[float]
    y_coords: List[float]


class ZPERequest(BaseModel):
    plate_separation: float = Field(1e-7, description="Plate separation [m]")
    cutoff_freq: Optional[float] = Field(
        None, description="ZPE cutoff frequency [rad/s]")
    sweep_points: int = Field(200, description="Number of points for sweep")


class ZPEResponse(BaseModel):
    casimir_force_pa: float
    casimir_energy_density: float
    casimir_total_energy: float
    sweep_d: List[float]
    sweep_force: List[float]
    sweep_energy: List[float]
    zpe_density: float
    cosmological_discrepancy: dict
    qi_bound: float
    lamoreaux: dict
    spectral_omega: List[float]
    spectral_density: List[float]


class GeodesicRequest(BaseModel):
    mass_solar: float = Field(
        10.0, description="Black hole mass in solar masses")
    spin: float = Field(0.0, description="Dimensionless spin parameter [0, 1)")
    r_init_factor: float = Field(
        10.0, description="Initial radius as multiple of r_s")
    phi_init: float = Field(0.0, description="Initial azimuthal angle [rad]")
    n_orbits: int = Field(
        5, description="Number of orbital periods to integrate")


class GeodesicResponse(BaseModel):
    orbit_x: List[float]
    orbit_y: List[float]
    orbit_r: List[float]
    orbit_phi: List[float]
    potential_r: List[float]
    potential_V: List[float]
    isco: float
    schwarzschild_radius: float
    metric_type: str
    outer_horizon: Optional[float] = None
    inner_horizon: Optional[float] = None


# ════════════════════════════════════════════════════════════════════
#  ENDPOINTS
# ════════════════════════════════════════════════════════════════════

@app.post("/api/alcubierre", response_model=AlcubierreResponse)
def compute_alcubierre(req: AlcubierreRequest):
    try:
        metric = AlcubierreMetric(
            bubble_radius=req.radius,
            wall_thickness=req.sigma,
            warp_velocity=req.velocity,
        )
        energy_calc = ExoticEnergyCalculator(
            bubble_radius=req.radius,
            wall_thickness=req.sigma,
            warp_velocity=req.velocity,
        )
        bubble = WarpBubble(
            bubble_radius=req.radius,
            wall_thickness=req.sigma,
            warp_velocity=req.velocity,
        )

        # 2D slice (z=0 plane)
        N = req.grid_n
        extent = 3.0 * req.radius
        lin = np.linspace(-extent, extent, N)
        X, Y = np.meshgrid(lin, lin)
        Z = np.zeros_like(X)

        expansion = metric.compute_expansion_scalar(X, Y, Z)
        energy_dens = energy_calc.compute_energy_density(X, Y, Z)

        # Shape function profile along x-axis
        r_profile = np.linspace(0, 3.0 * req.radius, 200)
        zeros = np.zeros_like(r_profile)
        f_profile = metric.compute_shape_function(r_profile, zeros, zeros)

        total_E = energy_calc.compute_total_exotic_energy(N=40)
        pf_bound = energy_calc.pfenning_ford_bound()
        T_H = bubble.get_hawking_radiation_flux()
        causal = bubble.is_causally_disconnected()
        comparisons = energy_calc.compare_to_known_energies(total_E)

        return AlcubierreResponse(
            expansion_scalar=expansion.tolist(),
            energy_density=energy_dens.tolist(),
            shape_profile_r=r_profile.tolist(),
            shape_profile_f=f_profile.tolist(),
            total_exotic_energy=float(total_E),
            pfenning_ford_bound=float(pf_bound),
            hawking_temperature=float(T_H),
            is_causally_disconnected=bool(causal),
            energy_comparisons=comparisons,
            x_coords=lin.tolist(),
            y_coords=lin.tolist(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/gravitomagnetic", response_model=GravitomagneticResponse)
def compute_gravitomagnetic(req: GravitomagneticRequest):
    try:
        J = (0.0, 0.0, req.angular_momentum_z)
        gem = GravitoElectroMagneticField(mass=req.mass, angular_momentum=J)
        fd = FrameDragging(mass=req.mass, angular_momentum=J)

        # Field on 2D grid in equatorial plane
        N = 40
        extent = 3.0 * req.radius
        lin = np.linspace(-extent, extent, N)
        X, Y = np.meshgrid(lin, lin)
        Z = np.zeros_like(X)

        Ex, Ey, Ez = gem.compute_gravitoelectric(X, Y, Z)
        Bx, By, Bz = gem.compute_gravitomagnetic(X, Y, Z)

        Eg_mag = np.sqrt(Ex**2 + Ey**2 + Ez**2)
        Bg_mag = np.sqrt(Bx**2 + By**2 + Bz**2)

        # Point values at the given radius (on x-axis)
        r = req.radius
        Ex_p, Ey_p, Ez_p = gem.compute_gravitoelectric(
            np.array([r]), np.array([0.0]), np.array([0.0]))
        Eg_point = float(
            np.sqrt(float(Ex_p[0])**2 + float(Ey_p[0])**2 + float(Ez_p[0])**2))

        Bx_p, By_p, Bz_p = gem.compute_gravitomagnetic(
            np.array([r]), np.array([0.0]), np.array([0.0]))
        Bg_point = float(
            np.sqrt(float(Bx_p[0])**2 + float(By_p[0])**2 + float(Bz_p[0])**2))

        Ox, Oy, Oz = fd.compute_precession_rate(
            np.array([r]), np.array([0.0]), np.array([0.0]))
        lt_rate = float(
            np.sqrt(float(Ox[0])**2 + float(Oy[0])**2 + float(Oz[0])**2))

        td = fd.compute_time_dilation(
            np.array([r]), np.array([0.0]), np.array([0.0]))
        td_val = float(td[0])

        return GravitomagneticResponse(
            Eg_magnitude=Eg_point,
            Bg_magnitude=Bg_point,
            lt_precession_rate=lt_rate,
            time_dilation=td_val,
            Eg_field=Eg_mag.tolist(),
            Bg_field=Bg_mag.tolist(),
            x_coords=lin.tolist(),
            y_coords=lin.tolist(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/zpe", response_model=ZPEResponse)
def compute_zpe(req: ZPERequest):
    try:
        casimir = CasimirEffect(plate_area=1.0)
        qvf = QuantumVacuumField(cutoff_frequency=req.cutoff_freq)

        d = req.plate_separation
        fpa = casimir.force_per_area(d)
        u_cas = casimir.energy_density(d)
        E_total = casimir.total_energy(d)

        sweep_d, sweep_f, sweep_u = casimir.sweep_separation(
            d_min=1e-9, d_max=1e-6, N=req.sweep_points)

        zpe_dens = qvf.total_energy_density()
        cosmo = qvf.cosmological_constant_discrepancy()

        tau = 1e-15  # femtosecond sampling
        qi = ExoticMatter.quantum_inequality_bound(tau)

        lamoreaux = CasimirEffect.lamoreaux_1997_comparison()

        # Spectral density plot data
        omega = np.logspace(10, 15, 200)
        spec = qvf.spectral_density(omega)

        return ZPEResponse(
            casimir_force_pa=float(fpa),
            casimir_energy_density=float(u_cas),
            casimir_total_energy=float(E_total),
            sweep_d=sweep_d.tolist(),
            sweep_force=sweep_f.tolist(),
            sweep_energy=sweep_u.tolist(),
            zpe_density=float(zpe_dens),
            cosmological_discrepancy=cosmo,
            qi_bound=float(qi),
            lamoreaux=lamoreaux,
            spectral_omega=omega.tolist(),
            spectral_density=spec.tolist(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/geodesic", response_model=GeodesicResponse)
def compute_geodesic(req: GeodesicRequest):
    try:
        mass = req.mass_solar * SOLAR_MASS

        if req.spin > 0:
            geo = KerrGeodesic(mass=mass, spin_parameter=req.spin)
            metric_type = "Kerr"
            isco = geo.isco_radius()
            r_s = geo.r_s
            r_init = req.r_init_factor * r_s

            # Circular orbit params
            L = np.sqrt(mass * 6.674e-11 * r_init)  # approximate
            E = 1.0

            orbit = geo.integrate_equatorial_orbit(
                r0=r_init, phi0=req.phi_init, dr_dtau0=0.0,
                E=E, L=L,
                tau_span=(0, req.n_orbits * 2 * np.pi * r_init / C),
                n_points=5000,
            )

            # Effective potential
            r_pot = np.linspace(isco * 0.5, r_init * 3, 300)
            V_pot = []
            for rr in r_pot:
                delta = rr**2 - r_s * rr + geo.a**2
                V = -6.674e-11 * mass / rr + L**2 / (2.0 * rr**2)
                V_pot.append(float(V))

            return GeodesicResponse(
                orbit_x=[float(v) for v in orbit["x"]],
                orbit_y=[float(v) for v in orbit["y"]],
                orbit_r=[float(v) for v in orbit["r"]],
                orbit_phi=[float(v) for v in orbit["phi"]],
                potential_r=[float(v) for v in r_pot],
                potential_V=V_pot,
                isco=float(isco),
                schwarzschild_radius=float(r_s),
                metric_type=metric_type,
                outer_horizon=float(geo.outer_horizon()),
                inner_horizon=float(geo.inner_horizon()),
            )
        else:
            geo = SchwarzschildGeodesic(mass=mass)
            metric_type = "Schwarzschild"
            isco = geo.isco_radius()
            r_s = geo.r_s
            r_init = req.r_init_factor * r_s

            # Angular momentum for near-circular orbit
            L = np.sqrt(mass * 6.674e-11 * r_init)

            orbit = geo.integrate_orbit(
                r0=r_init, phi0=req.phi_init, dr_dtau0=0.0,
                L=L,
                tau_span=(0, req.n_orbits * 2 * np.pi * r_init / C),
                n_points=5000,
            )

            # Effective potential curve
            r_pot = np.linspace(isco * 0.5, r_init * 3, 300)
            V_pot = geo.effective_potential(r_pot, L)

            return GeodesicResponse(
                orbit_x=[float(v) for v in orbit["x"]],
                orbit_y=[float(v) for v in orbit["y"]],
                orbit_r=[float(v) for v in orbit["r"]],
                orbit_phi=[float(v) for v in orbit["phi"]],
                potential_r=[float(v) for v in r_pot],
                potential_V=[float(v) for v in V_pot],
                isco=float(isco),
                schwarzschild_radius=float(r_s),
                metric_type=metric_type,
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
def health():
    return {"status": "ok", "modules": ["alcubierre", "gravitomagnetic", "zpe", "geodesic"]}
