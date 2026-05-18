#!/usr/bin/env bash
# Bootstrap the git repo and (optionally) push it to GitHub as `mat423`.
# Run from inside the project folder:  bash setup_repo.sh
#
# Prerequisites:
#   git (any recent version)
#   gh  (GitHub CLI)   — optional, only if you want to push automatically
#
set -euo pipefail

# --- 1. Clean up any half-initialized .git from a previous run -------
if [ -d .git ] && [ ! -f .git/HEAD ] || [ -f .git/index.lock ]; then
  echo "Removing incomplete .git/ from a previous run..."
  rm -rf .git
fi

# --- 1b. Remove the legacy notebook filename (replaced by rocket_simulation.ipynb)
if [ -f MAT423E_Module3_Rocket_Simulation.ipynb ]; then
  echo "Removing legacy notebook filename..."
  rm -f MAT423E_Module3_Rocket_Simulation.ipynb
fi

# --- 2. Fresh init ----------------------------------------------------
git init -q -b main
git config user.email "omrselcuk@icloud.com"
git config user.name  "Omer Selcuk"

# --- 3. Initial commit -----------------------------------------------
git add -A
git commit -q -m "Initial commit: Numerical simulation of variable-mass rocket flight

- Python script and Jupyter notebook implementing Forward Euler and RK4
  solvers for the coupled (y, v) ODE system with variable mass, altitude-
  dependent gravity, exponential atmosphere, and quadratic drag.
- Interactive HTML simulator (Chart.js) for live exploration.
- Peer-presentation deck (.pptx).
- Project metadata via pyproject.toml; MIT licensed."

echo
echo "Local repo initialized:"
git log --oneline -1
echo

# --- 4. Push to GitHub as a public repo named `mat423` ---------------
if command -v gh >/dev/null 2>&1; then
  echo "Creating public repo 'mat423' on GitHub and pushing..."
  gh repo create mat423 --public --source . --remote origin --push \
    --description "Numerical simulation of variable-mass rocket flight (Forward Euler vs RK4) for MAT423E."
  echo
  echo "Repo URL:"
  gh repo view --web --no-browser 2>/dev/null || echo "  https://github.com/$(gh api user --jq .login)/mat423"
else
  echo "gh CLI not found. To push manually:"
  echo "  1. Create the repo on github.com/new  →  name: mat423, public, no README."
  echo "  2. Then:"
  echo "       git remote add origin git@github.com:<YOUR_USERNAME>/mat423.git"
  echo "       git push -u origin main"
fi
