#!/usr/bin/env python3
"""Focused Evolution simulation runner.
This script runs iterative HPT cycles, doubling trial budget each cycle.
By default it runs in a fast demo mode to avoid long execution times.

Usage:
  python scripts/focused_evolution_sim.py [--cycles N] [--baseline-trials B] [--fast]

Directive mapping in this workspace:
- Baseline duration: 1 year -> mapped to baseline trial budget (default 100)
- 5 iterative doubling cycles -> doubles 5 times -> 32x (1 -> 32 years)

The script supports `--fast` to run a short demo. Remove `--fast` to execute full rigor (may take long).
"""
import asyncio
import argparse
import time
from src.hpt_engine import HyperparameterEngine
from src.db_manager import initialize_db, get_strategy, create_strategy

async def run_cycle(strategy_cfg, n_trials, emit_log):
    engine = HyperparameterEngine(strategy_cfg, emit_log)
    result = await engine.run_optimization(n_trials=n_trials)
    return result

async def emit_log_print(data):
    # Simple logging callback used by the engine
    if isinstance(data, dict):
        print(f"[LOG] {data.get('level', 'info')}: {data.get('message')}" )
    else:
        print(data)

async def main(args):
    initialize_db()

    # Create or fetch a baseline strategy
    baseline = {
        'name': 'focused_evolution_baseline',
        'currency': 'SIM',
        'base_bet_divisor': 10000.0,
        'profit_target_percent': 5.0,
        'loss_limit_percent': 10.0,
        'kappa': 0.5
    }
    strategy_id = create_strategy(baseline)
    strategy_row = get_strategy(strategy_id)
    strategy_cfg = dict(strategy_row)

    baseline_trials = args.baseline_trials
    cycles = args.cycles

    print(f"Starting Focused Evolution: baseline_trials={baseline_trials}, cycles={cycles}, fast={args.fast}")

    start_time = time.time()
    for c in range(cycles):
        multiplier = 2 ** c
        trials = baseline_trials * multiplier
        if args.fast:
            # Reduce work for demo; scale down by factor
            trials = max(1, int(trials / 16))
        print(f"\nCycle {c+1}/{cycles}: running {trials} trials (multiplier {multiplier})")
        result = await run_cycle(strategy_cfg, n_trials=trials, emit_log=emit_log_print)
        print(f"Cycle {c+1} result: {result}\n")

    elapsed = time.time() - start_time
    print(f"Focused Evolution completed in {elapsed:.2f}s")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cycles', type=int, default=5, help='Number of doubling cycles (default 5)')
    parser.add_argument('--baseline-trials', type=int, default=100, help='Baseline trial budget (default 100)')
    parser.add_argument('--fast', action='store_true', help='Run in fast demo mode (shortened trials)')
    args = parser.parse_args()

    asyncio.run(main(args))
