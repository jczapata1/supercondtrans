<h1 align="center">Input</h1>

<p align="justify">
Input files for the TDGL simulations. Contains general parameters (material, external, derived, and solver), the device mesh, magnetic field and vector potential profiles, and transport current settings.
</p>

## Structure

```
input/
├── Input.in                          # General Parameters
├── Device/
│   ├── Device.h5                     # TDGL Mesh
│   └── Device.png                    # Device Geometry Figure
├── Fields/
│   ├── Uniform/
│   │   ├── Input.in                  # Field Parameters
│   │   ├── Magnetic_Field.h5         # Magnetic Field Profile
│   │   ├── Magnetic_Field.png        # Magnetic Field Figure
│   │   ├── Vector_Potential.h5       # Vector Potential Profile
│   │   └── Vector_Potential.png      # Vector Potential Figure
│   ├── Plateau/
│   │   └── ...
│   └── Domains/
│       └── ...
└── Current/
    ├── Static/
    │   └── Input.in                  # Zero Current
    ├── Dynamic/
    │   └── Input.in                  # Fixed Current
    └── Sweep/
        └── Input.in                  # Current Range
```

## Parameters

### General

**Material:**

| Symbol | Description | Unit |
|---|---|---|
| `ξ0` | Coherence Length at T = 0 K | μm |
| `λ0` | Penetration Depth at T = 0 K | μm |
| `u0` | Relaxation Parameter | n.u. |
| `γ` | Inelastic Scattering Parameter | n.u. |
| `σ` | Normal Conductivity | S·m⁻¹ |
| `Lx` | Length | μm |
| `Ly` | Width | μm |
| `Lz` | Thickness | μm |
| `TC` | Critical Temperature | K |

**External:**

| Symbol | Description | Unit |
|---|---|---|
| `T0` | Working Temperature | K |
| `NPP` | Number of Probe Points | n.u. |

**Derived:**

| Symbol | Description | Expression | Unit |
|---|---|---|---|
| `ξ` | Coherence Length | $\xi_0 \left(1 - \left(\frac{T_0}{T_C}\right)^2\right)^{-1/2}$ | μm |
| `λ` | Penetration Depth | $\lambda_0 \left(1 - \left(\frac{T_0}{T_C}\right)^2\right)^{-1/2}$ | μm |
| `κ` | Ginzburg-Landau Parameter | $\lambda / \xi$ | n.u. |
| `Λ` | Pearl Length | $2\lambda^2 / L_z$ | μm |
| `BC2` | Upper Critical Field | $\Phi_0 / 2\pi \xi^2$ | mT |

**Solver:**

| Symbol | Description | Unit |
|---|---|---|
| `solve_time` | Simulation Time | r.u. |
| `save_every` | Save Interval | r.u. |
| `skip_time` | Thermalization Time | r.u. |
| `dt_init` | Initial Time Step | r.u. |
| `dt_max` | Maximum Time Step | r.u. |
| `screening` | Screening | `True`/`False` |
| `gpu` | GPU Acceleration | `True`/`False` |

File: `./Input.in`

### Magnetic Field

| Symbol | Description | Unit |
|---|---|---|
| `B0` | Field Amplitude | mT |
| `k` | Domain Periods | n.u. |
| `Ld` | Domain Half-Width | μm |
| `θ` | Stripe Orientation | rad |
| `φ` | Phase Offset | rad |
| `B_offset` | Field Offset | mT |

File: `./Fields/<profile>/Input.in`

Available profiles: `Uniform`, `Plateau`, and `Domains`.

### Current

| Symbol | Description | Unit |
|---|---|---|
| `Ii` | Initial Transport Current | μA |
| `If` | Final Transport Current | μA |
| `N` | Steps | n.u. |

File: `./Current/<mode>/Input.in`

Available modes: `Static`, `Dynamic`, and `Sweep`.
