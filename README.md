# mat423 · Numerical Simulation of Rocket Flight

**Variable mass · Variable thrust · Quadratic aerodynamic drag**
Forward Euler vs 4th-order Runge–Kutta on the coupled ODE system for a
vertically-launched rocket.

Built for *MAT423E: Numerical Solutions of ODEs*. The simulator covers a
realistic vertical-launch model with altitude-dependent gravity, exponential
atmosphere, and proper engine-cutoff handling — including a ground-hold
condition for sub-unity initial thrust-to-weight scenarios.

## Deliverables

| File | Purpose |
|---|---|
| `rocket_simulation.ipynb` | Annotated Jupyter notebook — the main computational submission. |
| `rocket_simulation.py` | Standalone Python script — same physics, runnable from the command line. |
| `rocket_simulator.html` | Interactive in-browser simulator for the live demo. |
| `presentation.pptx` | Peer-presentation deck. |
| `trajectory.png` | Pre-rendered headline figure. |
| `pyproject.toml` | Project metadata and dependency specification. |

## Physics summary

State variables: altitude `y(t)`, velocity `v(t)`. Mass is closed-form in `t`.

```
dy/dt = v
dv/dt = ( T(t) - m(t)·g(y) - ½·ρ(y)·C_d·A·v·|v| ) / m(t)
m(t)  = M₀ − ṁ·t        (until fuel depletion at t = t_burn)
T(t)  = ṁ·vₑ            (until t_burn; then 0)
g(y)  = g₀·(R_E/(R_E + y))²
ρ(y)  = ρ₀·exp(−y/H)
```

The drag term uses `v·|v|` so the force always opposes the velocity, both
ascending and descending. A *ground-hold* condition prevents nonphysical
negative altitude when initial thrust-to-weight is below unity (which is the
case for the assignment's parameters: T/W ≈ 0.92).

## Setup

### With uv (recommended — fastest)

```bash
uv venv
uv pip install -e ".[dev]"
```

### With plain pip

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows:  .venv\Scripts\activate
pip install -e ".[dev]"
```

### Verify the install

```bash
rocket-sim                          # runs the script, prints results, saves trajectory.png
jupyter lab                         # opens the notebook in your browser
```

## Quick start

### Run the script

```bash
python rocket_simulation.py
# or, after `pip install -e .`
rocket-sim
```

Expected output:

```
T/W at t=0 : 0.918
Burn time  : 300.0 s

   Euler  apogee =  1236.72 km at t =  829.0 s   v_at_cutoff =  3986.4 m/s   t_flight = 1200.0 s
     RK4  apogee =  1235.15 km at t =  828.4 s   v_at_cutoff =  3990.6 m/s   t_flight = 1200.0 s

Saved trajectory.png
```

### Open the notebook

```bash
jupyter lab rocket_simulation.ipynb
```

Then run all cells (Kernel → Restart & Run All). The 21 cells walk through the
physics, both solvers, the trajectory plots, the engine-cutoff zoom, and the
log–log convergence study.

### Open the interactive simulator

Just double-click `rocket_simulator.html` — it runs in any modern browser, no
server needed. Chart.js is loaded from the jsDelivr CDN. Try the three preset
buttons (Assignment / Falcon-class / Hobby rocket) and the four chart tabs.

## Suggested 50-minute walk-through

| Time | Section | Reference |
|---|---|---|
| 0–5   | Recap the ODE system; introduce the simulator and T/W feasibility check. | notebook §1 |
| 5–20  | Programming the ODE solver. Walk through Euler then RK4. | notebook §3–5 |
| 20–30 | Run with default parameters; show the trajectory plot. | notebook §6–7 + HTML simulator |
| 30–40 | Engine-cutoff analysis. Show the acceleration discontinuity (≈ 90 m/s²). | notebook §8 |
| 40–50 | Convergence study — slopes 1 and 4 on the log–log plot. Q&A. | notebook §9 + HTML "Convergence" tab |

## Project layout

```
mat423/
├── rocket_simulation.ipynb     ← annotated notebook (main submission)
├── rocket_simulation.py        ← standalone Python module
├── rocket_simulator.html       ← interactive web demo
├── presentation.pptx           ← peer-presentation deck
├── trajectory.png              ← headline figure
├── pyproject.toml              ← dependencies & metadata
├── .python-version             ← pinned interpreter
├── .gitignore
├── LICENSE
└── README.md
```

## Requirements

- Python ≥ 3.10
- A modern web browser (for the HTML simulator)

All Python dependencies are listed in `pyproject.toml`; no hidden requirements.
