# Gravitomagnetic Module

## References

- Mashhoon, B. (2008). "Gravitoelectromagnetism: A Brief Review." arXiv:gr-qc/0311030
- Lense, J. & Thirring, H. (1918). *Phys. Z.* 19, 156.
- Gravity Probe B (2011). *Phys. Rev. Lett.* 106, 221101.

## GEM Field Equations

In the weak-field, slow-motion limit of GR:

```
div E_g  = -4*pi*G*rho
div B_g  = 0
curl E_g = -dB_g/dt
curl B_g = (-4*pi*G/c^2)*J  +  (1/c^2)*dE_g/dt
```

## Gravitomagnetic Lorentz Force

```
F = m (E_g + v x B_g)
```

## Lense-Thirring Precession

```
Omega_LT = (G / c^2 r^3) [3(J . r_hat) r_hat - J]
```

## Files

| File | Description |
|---|---|
| `gem_equations.py` | Gravitoelectric and gravitomagnetic field computation |
| `frame_dragging.py` | Lense-Thirring precession, gyroscope integration, time dilation |
| `force_calculator.py` | Particle trajectory integration in GEM fields |
| `visualizer.py` | Field quiver plots for E_g, B_g, and frame-dragging |
