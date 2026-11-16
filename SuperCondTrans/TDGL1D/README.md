# TDGL1D

> One-dimensional simulation of the order parameter magnitude under a moving vortex-like potential.
>
> Last Updated: 13/11/2026

---

## Model

Solves:

$$
u\,\tau_{\text{GL}}\sqrt{1+\gamma^2 f^2}\,\frac{\partial f}{\partial t} = \xi^2\frac{\partial^2 f}{\partial y^2} + \left[(1-f^2) - V\right]f,
$$

with (in SI units):

| Symbol             | Description                     |
| ------------------:|:------------------------------- |
| $u$                | Relaxation Parameter            |
| $\gamma$           | Inelastic Scattering Parameter  |
| $\tau_{\text{GL}}$ | Ginzburg-Landau Relaxation Time |
| $f(y, t)$          | Order Parameter Magnitude       |
| $\xi$              | Coherence Length                |
| $V(y-vt)$          | Vortex-Like Potential           |
| $v$                | Vortex Velocity                 |

Uses an IMEX finite-difference scheme on a uniform grid with Neumann boundary conditions, capturing the competition between spatial diffusion, Ginzburg-Landau recovery, Kramer-Watts-Tobin (KWT) relaxation, and a prescribed moving vortex core. The model assumes a real order parameter (neglecting phase dynamics, flux quantization, and topological vortex structure), no electromagnetic potentials, a rigid vortex core with prescribed trajectory and no back-reaction or Larkin-Ovchinnikov shrinkage, and no vortex-vortex interactions, pinning, or thermal fluctuations. Valid in the KWT-GL regime near $T_{\text{c}}$.

## Workflow

| Notebook           | Description                                                              |
| ------------------:|:------------------------------------------------------------------------ |
| `Simulation.ipynb` | Run the TDGL1D solver and generate animations from simulation snapshots. |