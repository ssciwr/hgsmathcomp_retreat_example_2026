# AGENTS.md

## Purpose
This package implements a simple python CLI tool to solve and visualize the Lotka Volterra equations.
```math
\frac{dx}{dt} &= \alpha x - \beta xy \\
\frac{dy}{dt} &= \delta xy - \gamma y \\
& \alpha, \beta, \gamma, \delta \in \mathbb{R}_{+} \\
& x, y \in \mathbb{R}_{+}
```

It can be called via command line with
```bash
python3 ./src/hgscomp/lotka.py --alpha value --beta value --gamma value --delta value --x0 value --y0 value
```
from a virtual environment that has the package installed.

## Setup

- Requires Python 3.10+.
- Install with `pip install -e '.[tests]'`.
- Run tests with `pytest`.

## Tests
The project has both unit tests in test_lotka.py and behavior tests via pytest-bdd in test_solve_lotka.py

## Content

- Library code: `src/hgscomp/`
- Tests and BDD features: `tests/`

## Instructions

- Keep changes focused.
- Do not modify tests unless explicitly requested.
- Use numpy style docstrings
- The project uses the test-driven- and behavior-driven-development paradigms. Adhere to those unless instructed otherwise.
