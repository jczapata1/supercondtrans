<h1 align="center">TDGL</h1>

<p align="justify">
Time-Dependent Ginzburg-Landau (TDGL) simulations of thin superconducting films using <a href="https://py-tdgl.readthedocs.io/en/latest/">py-TDGL</a>. Solves:
</p>

$$\begin{aligned}
\frac{u}{\sqrt{1+\gamma^2|\psi|^2}}\left(\frac{\partial}{\partial t}+i\mu+\frac{\gamma^2}{2}\frac{\partial |\psi|^2}{\partial t}\right)\psi &= \left[(\epsilon(\mathbf{r})-|\psi|^2)+(\boldsymbol{\nabla}-i\mathbf{A})^2\right]\psi, \\
\mathbf{J}_s &= \mathrm{Im}[\psi^*(\boldsymbol{\nabla}-i\mathbf{A})\psi], \\
\boldsymbol{\nabla}^2\mu &= \boldsymbol{\nabla}\cdot\mathbf{J}_s, \\
\mathbf{J}_n &= -\boldsymbol{\nabla}\mu, \\
\mathbf{J} &= \mathbf{J}_s + \mathbf{J}_n,
\end{aligned}$$

with (in reduced units):

| Symbol                       | Description                    |
|-----------------------------:|:-------------------------------|
| $u$                          | Relaxation Parameter           |
| $\gamma$                     | Inelastic Scattering Parameter |
| $\psi(\mathbf{r}, t)$        | Complex Order Parameter        |
| $\mu(\mathbf{r}, t)$         | Electric Scalar Potential      |
| $\epsilon(\mathbf{r}, t)$    | Local Reduced Temperature      |
| $\mathbf{A}(\mathbf{r}, t)$  | Magnetic Vector Potential      |
| $\mathbf{J}_s(\mathbf{r}, t)$| Supercurrent Density           |
| $\mathbf{J}_n(\mathbf{r}, t)$| Normal Current Density         |
| $\mathbf{J}(\mathbf{r}, t)$  | Total Current Density          |

<p align="justify">
Supports static and dynamic vortex regimes with no-pinning, pinning, or antipinning antidot configurations, under uniform, plateau, or stripe-domain magnetic field profiles, with applied transport current or current-voltage sweep mode.
</p>

## Workflow

| Notebook | Description |
|---|---|
| `Setup.ipynb`      | Build the TDGL mesh, compute the epsilon profile (NoPinning, Pinning, Antipinning), and the magnetic field and vector potential profiles (Uniform, Plateau, Domains). |
| `Simulation.ipynb` | Run the TDGL solver (Static, Dynamic, Sweep) and generate animations from simulation snapshots. |
