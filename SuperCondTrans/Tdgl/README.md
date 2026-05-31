<h1 align="center">TDGL</h1>

<p align="justify">
Time-Dependent Ginzburg-Landau (TDGL) simulations of thin superconducting films using <a href="https://py-tdgl.readthedocs.io/en/latest/">py-tdgl</a>. Supports static and dynamic vortex regimes with no-pinning, pinning, or antipinning antidot configurations, under uniform, plateau, or stripe-domain magnetic field profiles, with applied transport current or current-voltage sweep mode.
</p>

## Workflow

| Notebook | Description |
|---|---|
| `Setup.ipynb`      | Build the TDGL mesh, compute the epsilon profile (NoPinning, Pinning, Antipinning), and the magnetic field and vector potential profiles (Uniform, Plateau, Domains). |
| `Simulation.ipynb` | Run the TDGL solver (Static, Dynamic, Sweep) and generate animations from simulation snapshots. |
