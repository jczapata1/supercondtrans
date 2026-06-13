<h1 align="center">Input</h1>

<p align="justify">
Input files for the TDGL simulations. Contains general parameters (material, external, derived, and solver), the device setup, pinning configurations, magnetic field and vector potential profiles, and transport current settings.
</p>

## Structure

```
input/
├── Input.in                   # General Parameters
├── Default/
│   └── empty
├── Setup/
│   ├── Device.h5              # Device
│   ├── Setup.h5               # Setup
│   ├── Device.png             # Device Figure
│   ├── Epsilon.png            # Epsilon Figure
│   ├── Magnetic_Field.png     # Magnetic Field Figure
│   └── Vector_Potential.png   # Vector Potential Figure
├── Epsilon/
│   ├── Pinning.in             # Pinning Parameters
│   ├── NoPinning.in           # No-Pinning Parameters
│   └── Antipinning.in         # Antipinning Parameters
├── Fields/
│   ├── Uniform.in             # Uniform Parameters
│   ├── Plateau.in             # Plateau Parameters
│   └── Domains.in             # Domains Parameters
└── Current/
    ├── Static.in              # Zero Current
    ├── Dynamic.in             # Fixed Current
    └── Sweep.in               # Current Range
```

## Parameters

### General

**Material:**

| Symbol | Description                    | Type  | Example  | Unit   |
| ------ | ------------------------------ | ----- | -------- | ------ |
| `ξ0`   | Coherence Length at T = 0 K    | float | `0.0054` | μm     |
| `λ0`   | Penetration Depth at T = 0 K   | float | `0.200`  | μm     |
| `u`    | Relaxation Parameter           | float | `5.79`   | n.u.   |
| `γ`    | Inelastic Scattering Parameter | float | `1.0`    | n.u.   |
| `σ`    | Normal Conductivity            | float | `1.0`    | S·μm⁻¹ |
| `Lx`   | Length                         | float | `2.000`  | μm     |
| `Ly`   | Width                          | float | `0.400`  | μm     |
| `Lz`   | Thickness                      | float | `0.010`  | μm     |
| `TC`   | Critical Temperature           | float | `16.81`  | K      |

**External:**

| Symbol     | Description            | Type  | Example                                 | Unit |
| ---------- | ---------------------- | ----- | --------------------------------------- | ---- |
| `T0`       | Working Temperature    | float | `15.80`                                 | K    |
| `NPP`      | Number of Probe Points | int   | `20`                                    | n.u. |
| `disorder` | Pinning Configuration  | str   | `'NoPinning'`/`'Pinning'`/`'Antipinning'` | n.u. |
| `dist`     | Pinning Distribution   | str   | `'Random'`/`'Square'`/`'Hexagonal'`     | n.u. |
| `profile`  | Magnetic Field Profile | str   | `'Uniform'`/`'Plateau'`/`'Domains'`     | n.u. |
| `gauge`    | Vector Potential Gauge | str   | `'Landau-y'`/`'Landau-x'`/`'Rotated'`   | n.u. |

**Derived:**

| Symbol | Description       | Type  | Expression                                                         | Unit |
| ------ | ----------------- | ----- | ------------------------------------------------------------------ | ---- |
| `ξ`    | Coherence Length  | float | $\xi_0 \left[1 - \left(\frac{T_0}{T_C}\right)^2\right]^{-1/2}$     | μm   |
| `λ`    | Penetration Depth | float | $\lambda_0 \left[1 - \left(\frac{T_0}{T_C}\right)^2\right]^{-1/2}$ | μm   |

**Solver:**

| Symbol       | Description         | Type  | Example        | Unit |
| ------------ | ------------------- | ----- | -------------- | ---- |
| `solve_time` | Simulation Time     | int   | `200`          | r.u. |
| `save_every` | Save Interval       | int   | `100`          | r.u. |
| `skip_time`  | Thermalization Time | int   | `200`          | r.u. |
| `dt_init`    | Initial Time Step   | float | `1e-4`         | r.u. |
| `dt_max`     | Maximum Time Step   | float | `1e-1`         | r.u. |
| `screening`  | Screening           | bool  | `True`/`False` | n.u. |
| `gpu`        | GPU Acceleration    | bool  | `True`/`False` | n.u. |

File: `./Input.in`

### Epsilon

| Symbol | Description              | Type  | Example  | Unit |
| ------ | ------------------------ | ----- | -------- | ---- |
| `N`    | Number of Antidots       | int   | `50`     | n.u. |
| `R`    | Antidot Radius           | float | `0.010`  | μm   |
| `σR`   | Antidot Radius Std. Dev. | float | `0.0`    | μm   |
| `ε0`   | Suppression              | float | `-1.0`   | n.u. |
| `σε`   | Suppression Std. Dev.    | float | `0.0`    | n.u. |
| `seed` | Random Seed              | int   | `0`      | n.u. |

File: `./Epsilon/<mode>.in`

Available modes: `Pinning`, `NoPinning`, and `Antipinning`.

### Magnetic Field

| Symbol     | Description        | Type  | Example | Unit |
| ---------- | ------------------ | ----- | ------- | ---- |
| `B0`       | Field Amplitude    | float | `500.0` | mT   |
| `k`        | Domain Periods     | float | `10.0`  | n.u. |
| `Ld`       | Domain Half-Width  | float | `1.0`   | μm   |
| `θ`        | Stripe Orientation | float | `π/2`   | rad  |
| `φ`        | Phase Offset       | float | `0.0`   | rad  |
| `B_offset` | Field Offset       | float | `0.0`   | mT   |

File: `./Fields/<profile>.in`

Available profiles: `Uniform`, `Plateau`, and `Domains`.

### Current

| Symbol | Description               | Type  | Example | Unit |
| ------ | ------------------------- | ----- | ------- | ---- |
| `Ii`   | Initial Transport Current | float | `-10.0` | μA   |
| `If`   | Final Transport Current   | float | `10.0`  | μA   |
| `N`    | Steps                     | int   | `11`    | n.u. |

File: `./Current/<mode>.in`

Available modes: `Static`, `Dynamic`, and `Sweep`.