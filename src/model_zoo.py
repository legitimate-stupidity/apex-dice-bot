#!/usr/bin/env python3
"""Simple model zoo stub.
Provides a lightweight placeholder for training functions used by HPT.
Real agents would replace these stubs with RL training loops.
"""
import asyncio
import random
from typing import Dict, Any

async def train_random_agent(env, trial) -> float:
    """Simulate a training run by running a sequence of random actions.
    Returns a pseudo-performance metric (float).
    """
    # Run a short simulated episode
    env.reset()
    total = 0.0
    for _ in range(50):
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = await env.step(action)
        total += reward
        if terminated:
            env.reset()
    # Return a random-ish performance metric influenced by total
    return total + random.uniform(-1.0, 1.0)
