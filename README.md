<h1 align="center">SuperConducting-Transport</h1>

<div align="center">

![Version](https://img.shields.io/badge/Version-1.3.0-brightgreen.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python&logoColor=white)
![Ubuntu](https://img.shields.io/badge/Ubuntu-26.04-E95420.svg?logo=ubuntu&logoColor=white)
</div>

<p align="justify">
This repository contains phenomenological models for transport properties in superconducting systems, including vortex dynamics. The focus is on the temperature and field dependence of transport-related quantities, such as resistance, voltage–current characteristics, critical current behavior, and non-equilibrium effects like the Larkin–Ovchinnikov instability, as well as phase diagrams.
</p>

## Installation

Clone the repository:

```bash
git clone https://github.com/jczapata1/supercondtrans.git
cd supercondtrans
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Version Tracking

* v1.0.0: TDGL Module → Base Code (25/05/2026).
* v1.1.0: TDGL Module → Upgrade + Pinning (05/31/2026).
* v1.2.0: TDGL Module → Normal Current + Supercurrent (06/07/2026).
* v1.3.0: TDGL Module → Plots and Readme Upgrades (06/13/2026).

## Copyright and License

Copyright © 2026 J. C. Zapata. All rights reserved.

This project is licensed under the **MIT License**. See the [LICENSE](./LICENSE) file for details.