# Geodesic Motion in Curved Spacetime

## Overview

A geodesic is the path of a freely falling particle through curved spacetime. It is the general relativistic generalisation of a straight line.

## The Geodesic Equation

```
d^2 x^mu / dtau^2 + Gamma^mu_{alpha beta} (dx^alpha/dtau)(dx^beta/dtau) = 0
```

where Gamma^mu_{alpha beta} are the Christoffel symbols computed from the metric.

## References

- Schwarzschild, K. (1916). *Sitzungsber. Preuss. Akad. Wiss. Berlin*, 189.
- Kerr, R.P. (1963). "Gravitational field of a spinning mass as an example of algebraically special metrics." *Phys. Rev. Lett.* 11, 237.
- Boyer, R.H. & Lindquist, R.W. (1967). *J. Math. Phys.* 8, 265.
- Bardeen, J.M., Press, W.H. & Teukolsky, S.A. (1972). *Astrophys. J.* 178, 347.
- Misner, C.W., Thorne, K.S. & Wheeler, J.A. (1973). *Gravitation*. W.H. Freeman.

## Schwarzschild Spacetime

The unique spherically symmetric vacuum solution. Key features:
- Event horizon at r_s = 2GM/c^2
- ISCO at r = 3*r_s (= 6GM/c^2)
- Perihelion precession (confirmed by Mercury's orbit)
- Photon sphere at r = 1.5*r_s

## Kerr Spacetime

The unique axially symmetric vacuum solution for a rotating mass:
- Two horizons: r_+ (outer) and r_- (inner)
- Ergosphere between r_+ and the static limit
- Frame dragging of orbits
- ISCO depends on spin: smaller for prograde orbits

## GRAVITON Implementation

1. Generic geodesic solver using numerical Christoffel symbols
2. Schwarzschild effective potential and equatorial orbit integration
3. Kerr equatorial orbit integration with spin coupling
4. ISCO computation for both metrics
5. Flamm's paraboloid embedding diagram (3D Plotly)
6. Orbital trajectory visualizations
