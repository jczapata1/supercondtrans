<h1 align="center">TDGL</h1>

<p align="justify">
Time-Dependent Ginzburg-Landau (TDGL) simulations of thin superconducting films using <a href="https://py-tdgl.readthedocs.io/en/latest/">py-TDGL</a>. Solves:
</p>

$$\begin{aligned}
\frac{u}{\sqrt{1+\gamma^2|\psi|^2}}\left(\frac{\partial}{\partial t}+i\mu+\frac{\gamma^2}{2}\frac{\partial |\psi|^2}{\partial t}\right)\psi &= \left[(\epsilon(\vec{r})-|\psi|^2)+(\vec{\nabla}-i\vec{A})^2\right]\psi, \\
\vec{J}_s &= \mathrm{Im}[\psi^*(\vec{\nabla}-i\vec{A})\psi], \\
\vec{\nabla}^2\mu &= \vec{\nabla}\cdot\vec{J}_s, \\
\vec{J}_n &= -\vec{\nabla}\mu, \\
\vec{J} &= \vec{J}_s + \vec{J}_n,
\end{aligned}$$

with (in reduced units):

| Symbol                  | Description                    |
|------------------------:|:-------------------------------|
| $u$                     | Relaxation Parameter           |
| $\gamma$                | Inelastic Scattering Parameter |
| $\psi(\vec{r}, t)$      | Complex Order Parameter        |
| $\mu(\vec{r}, t)$       | Electric Scalar Potential      |
| $\epsilon(\vec{r})$     | Local Reduced Temperature      |
| $\vec{A}(\vec{r})$      | Magnetic Vector Potential      |
| $\vec{J}_s(\vec{r}, t)$ | Supercurrent Density           |
| $\vec{J}_n(\vec{r}, t)$ | Normal Current Density         |
| $\vec{J}(\vec{r}, t)$   | Total Current Density          |

<p align="justify">
Supports static and dynamic vortex regimes with no-pinning, pinning, or antipinning antidot configurations, under uniform, plateau, or stripe-domain magnetic field profiles, with applied transport current or current-voltage sweep mode.
</p>

## Workflow

| Notebook | Description |
|---|---|
| `Setup.ipynb`      | Build the TDGL mesh, compute the epsilon profile (NoPinning, Pinning, Antipinning), and the magnetic field and vector potential profiles (Uniform, Plateau, Domains). |
| `Simulation.ipynb` | Run the TDGL solver (Static, Dynamic, Sweep) and generate animations from simulation snapshots. |
