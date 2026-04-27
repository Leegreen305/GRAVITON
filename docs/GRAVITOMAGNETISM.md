# Gravitoelectromagnetism (GEM)

## Overview

Gravitoelectromagnetism is a formal analogy between the linearised Einstein field equations and Maxwell's equations of electromagnetism. In the weak-field, slow-motion limit of General Relativity, gravity produces two types of fields:

1. **Gravitoelectric field** E_g -- analogous to the electric field (Newtonian gravity)
2. **Gravitomagnetic field** B_g -- analogous to the magnetic field (caused by mass currents / angular momentum)

## References

- Mashhoon, B. (2008). "Gravitoelectromagnetism: A Brief Review." arXiv:gr-qc/0311030
- Lense, J. & Thirring, H. (1918). *Phys. Z.* 19, 156.
- Gravity Probe B (2011). *Phys. Rev. Lett.* 106, 221101.
- Ciufolini, I. & Pavlis, E.C. (2004). *Nature* 431, 958.

## The Lense-Thirring Effect

A rotating mass drags the local inertial frames around it. This was predicted by Lense and Thirring in 1918 and confirmed experimentally by:

- **Gravity Probe B** (2011): Measured frame-dragging precession of gyroscopes in Earth orbit at ~37 milliarcseconds/year, matching GR predictions to ~19%.
- **LAGEOS satellites** (Ciufolini & Pavlis, 2004): Confirmed Lense-Thirring precession of satellite orbits to ~10%.

## GRAVITON Implementation

The gravitomagnetic module computes:
1. Gravitoelectric field from Newtonian potential
2. Gravitomagnetic dipole field from angular momentum
3. Lense-Thirring precession rate at any point
4. Gyroscope spin evolution via ODE integration
5. Gravitomagnetic time dilation
6. Particle trajectories in combined GEM fields
