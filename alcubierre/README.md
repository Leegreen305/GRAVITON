# Alcubierre Warp Drive Module

## Reference

Alcubierre, M. (1994). "The warp drive: hyper-fast travel within general relativity." *Classical and Quantum Gravity*, 11(5), L73.

## The Alcubierre Metric

The line element in (3+1) ADM formalism:

```
ds^2 = -c^2 dt^2 + (dx - v_s(t) f(r_s) dt)^2 + dy^2 + dz^2
```

where:
- `v_s(t)` = velocity of the warp bubble center
- `r_s = sqrt((x-x_s)^2 + (y-y_s)^2 + (z-z_s)^2)` = distance from bubble center
- `f(r_s)` = shape function defining bubble wall thickness

## Shape Function

```
f(r_s) = [tanh(sigma*(r_s + R)) - tanh(sigma*(r_s - R))] / [2*tanh(sigma*R)]
```

## Files

| File | Description |
|---|---|
| `metric.py` | Full 4x4 metric tensor, shape function, expansion scalar |
| `energy.py` | Exotic energy density T_00, total energy, Pfenning-Ford bound |
| `bubble.py` | Bubble propagation, tidal forces, causal structure, Hawking radiation |
| `visualizer.py` | 3D Plotly expansion scalar, energy density heatmap, shape function |
