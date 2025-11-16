QuantumLeap (apex-dice-bot) - Focused Evolution Manifest

Overview
- This workspace contains a simulation and service stack for managing strategy portfolios, running simulated bots, and performing hyperparameter optimization (HPT).
- I unpacked the project manifest from `.buildme` and added minimal supporting modules so the system can run in a demo configuration.

What's new (Enhancements applied)
- Added `src/db_manager.py`: lightweight SQLite-backed store for strategies.
- Added `src/bot_v13_engine.py`: placeholder bot engine to satisfy server imports and provide a simulated bot loop.
- Added `src/model_zoo.py`: simple agent training stub used for experimental HPT integration.
- Added `scripts/focused_evolution_sim.py`: orchestrates the "Focused Evolution" directive by running iterative HPT cycles (doubling trial budgets each cycle). Includes `--fast` demo mode.
- Created `requirements.txt`, `src/*` modules, and `dashboard/index_v18.html` from the project manifest.

Focused Evolution mapping
- Directive: Baseline duration 1 year, 5 iterative doubling cycles -> 32-year equivalent.
- Practical mapping: baseline duration is represented as a baseline HPT trial budget (default 100). Each cycle doubles the trial budget.
- For safety, the simulation script includes a `--fast` mode which scales down trial counts for demonstration runs.

Quick start (demo)

1) Install dependencies (recommended inside your devcontainer):

```bash
pip install -r requirements.txt
```

2) Run the focused evolution demo (fast, completes quickly):

```bash
python scripts/focused_evolution_sim.py --fast
```

3) To run in full rigor (may be long-running; ensure sufficient CPU/time):

```bash
python scripts/focused_evolution_sim.py --cycles 5 --baseline-trials 100
```

Notes & Next steps
- The server expects `DUCKDICE_API_KEY` in the environment; `run_server.py` will exit if it is not set. This is unchanged from the manifest.
- The HPT engine currently uses a dummy training function; replacing `src/model_zoo.py` with real training agents will enable full RL-driven optimization.
- If you want, I can:
  - Replace HPT's dummy training with `model_zoo.train_random_agent` integration.
  - Run a full rigorous Focused Evolution cycle (non-fast) now — confirm if you want me to proceed (it may be CPU- and time-intensive).
