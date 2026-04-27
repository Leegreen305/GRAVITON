# GRAVITON Physics Reference

## Master Equation Index

This document lists every equation implemented in GRAVITON with its source citation.

---

## 1. Alcubierre Warp Drive

**Source:** Alcubierre, M. (1994). *Class. Quantum Grav.* 11, L73.

### Metric (ADM formalism)
```
ds^2 = -c^2 dt^2 + (dx - v_s f(r_s) dt)^2 + dy^2 + dz^2
```

### Shape function
```
f(r_s) = [tanh(sigma*(r_s + R)) - tanh(sigma*(r_s - R))] / [2*tanh(sigma*R)]
```

### Expansion scalar
```
theta = v_s * (x - x_s) / r_s * df/dr_s
```

### Energy density (from Einstein equations)
```
T_00 = -(c^4 / (32*pi*G)) * v_s^2 * (df/dr)^2 * (y^2+z^2) / r_s^2
```

### Pfenning-Ford energy bound
**Source:** Pfenning & Ford (1997). *Class. Quantum Grav.* 14, 1743.
```
E_min ~ -(c^7 / (G^2 * hbar)) * V_bubble / sigma^2
```

### Hawking-like temperature
**Source:** Hiscock (1997). *Class. Quantum Grav.* 14, L183.
```
T_H = hbar * v_s * sigma / (2*pi*c*k_B)
```

---

## 2. Gravitoelectromagnetism

**Source:** Mashhoon, B. (2008). arXiv:gr-qc/0311030.

### Gravitoelectric field
```
E_g = -GM * r_hat / r^2
```

### Gravitomagnetic field (dipole)
```
B_g = (G / c^2 r^5) [3(J.r)r - r^2 J]
```

### GEM field equations
```
div E_g = -4*pi*G*rho
div B_g = 0
curl E_g = -dB_g/dt
curl B_g = (-4*pi*G/c^2)*J_g + (1/c^2)*dE_g/dt
```

### Lorentz-like force
```
F = m(E_g + v x B_g)
```

### Lense-Thirring precession
**Source:** Lense & Thirring (1918). *Phys. Z.* 19, 156.
```
Omega_LT = (G / c^2 r^3) [3(J.r_hat)r_hat - J]
```

### Gravitomagnetic time dilation
```
dtau/dt = sqrt(1 - 2GM/(rc^2) - (Omega_LT . r)^2/c^2)
```

---

## 3. Zero-Point Energy

### Casimir force
**Source:** Casimir (1948). *Proc. Kon. Ned. Akad. Wetensch.* 51, 793.
```
F/A = -pi^2 * hbar * c / (240 * d^4)
u = -pi^2 * hbar * c / (720 * d^3)
```

### ZPE spectral density
**Source:** Milonni (1994). "The Quantum Vacuum."
```
u(omega) = hbar * omega^3 / (2*pi^2*c^3)
U_total = hbar * omega_max^4 / (8*pi^2*c^3)
```

### Ford-Roman quantum inequality
**Source:** Ford & Roman (1995). *Phys. Rev. D* 51, 4277.
```
<rho> >= -3*hbar / (32*pi^2*tau^4*c)
```

### Squeezed vacuum energy density
**Source:** Wu & Ford (1999). *Phys. Rev. D* 60, 104013.
```
<rho_neg> ~ -(hbar*omega / (4*pi^2*c^3)) * sinh^2(r)
```

---

## 4. Geodesics

### Schwarzschild metric
**Source:** Schwarzschild (1916). *Sitzungsber. Preuss. Akad. Wiss. Berlin*, 189.
```
ds^2 = -(1-r_s/r)c^2 dt^2 + (1-r_s/r)^{-1} dr^2 + r^2 dOmega^2
r_s = 2GM/c^2
r_ISCO = 3*r_s
```

### Effective potential
```
V_eff = -GM/r + L^2/(2r^2) - GML^2/(c^2 r^3)
```

### Kerr metric
**Source:** Kerr (1963). *Phys. Rev. Lett.* 11, 237.
```
Sigma = r^2 + a^2 cos^2(theta)
Delta = r^2 - r_s*r + a^2
```

### Geodesic equation
**Source:** Misner, Thorne & Wheeler (1973). *Gravitation*.
```
d^2 x^mu / dtau^2 + Gamma^mu_{alpha beta} (dx^alpha/dtau)(dx^beta/dtau) = 0
```
