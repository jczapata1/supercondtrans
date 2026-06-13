<h1 align="center">Input</h1>

<p align="justify">
Input file for the TDGL1D simulations. Contains material, external, derived, vortex, and solver parameters.
</p>

## Structure

```
input/
└── Input.in   # Parameters
```

## Parameters

### General

**Material:**

| Symbol | Description                    | Type  | Example  | Unit |
| ------ | ------------------------------ | ----- | -------- | ---- |
| `ξ0`   | Coherence Length at T = 0 K    | float | `5.4e-9` | m    |
| `u`    | Relaxation Parameter           | float | `5.79`   | n.u. |
| `γ`    | Inelastic Scattering Parameter | float | `0.001`  | n.u. |
| `Ly`   | Width                          | float | `5.0e-6` | m    |
| `Ny`   | Number of Grid Points          | int   | `1000`   | n.u. |
| `TC`   | Critical Temperature           | float | `16.81`  | K    |

**External:**

| Symbol | Description           | Type  | Example | Unit |
| ------ | --------------------- | ----- | ------- | ---- |
| `T0`   | Working Temperature   | float | `15.80` | K    |

**Derived:**

| Symbol | Description                         | Type  | Expression                                                     | Unit |
| ------ | ----------------------------------- | ----- | -------------------------------------------------------------- | ---- |
| `ξ`    | Coherence Length                    | float | $\xi_0 \left[1 - \left(\frac{T_0}{T_C}\right)^2\right]^{-1/2}$ | m    |
| `τGL`  | Ginzburg-Landau Characteristic Time | float | $\dfrac{\pi\hbar}{8\,k_B\left(T_C - T_0\right)}$               | s    |

**Vortex:**

| Symbol | Description        | Type  | Example              | Unit |
| ------ | ------------------ | ----- | -------------------- | ---- |
| `V0`   | Vortex Amplitude   | float | `15.0`               | n.u. |
| `v`    | Velocity           | float | `0.5 * ξ/τGL`        | m/s  |
| `mode` | Mode               | str   | `'Single'`/`'Train'` | n.u. |
| `Nv`   | Number of Vortices | int   | `20`                 | n.u. |
| `a`    | Vortex Spacing     | float | `Ly/5`               | m    |

**Solver:**

| Symbol       | Description   | Type  | Example          | Unit |
| ------------ | ------------- | ----- | ---------------- | ---- |
| `dt`         | Time Step     | float | `0.1 * τGL`      | s    |
| `Nt`         | Time Steps    | int   | `int(Ly/(v·dt))` | n.u. |
| `save_every` | Save Interval | int   | `200`            | n.u. |

File: `./Input.in`