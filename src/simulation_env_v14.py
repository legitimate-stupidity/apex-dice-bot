#!/usr/bin/env python3
"""
v14.0 - Refactored Simulation Environment
Implements the BaseStrategyEnv interface for local simulation.
"""

import secrets
from typing import Dict, Any, Tuple, Optional
import numpy as np

from .interfaces import BaseStrategyEnv

class SimulationEnv(BaseStrategyEnv):
    """
    Simulates the dice game logic locally, implementing
    the standardized v14.0 interface.
    """
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        
        self.profit_target = self.start_balance * config.get("profit_target_percent", 5.0) / 100.0
        self.loss_limit = - (self.start_balance * config.get("loss_limit_percent", 10.0) / 100.0)
        
    def _roll_dice(self) -> int:
        return secrets.randbelow(10000)

    async def _execute_bet(self, action_id: int) -> Tuple[float, bool]:
        """
        Simulates the bet.
        Returns: (normalized_reward, done)
        """
        chance_str, multiplier = self.action_map[action_id]
        chance = float(chance_str)
        amount = self.base_bet * multiplier
        
        if amount > self.balance:
            return 0, True # Terminated due to bankruptcy
            
        roll = self._roll_dice()
        
        # High/Low logic
        payout = (100.0 / chance) * 0.99 # 1% house edge
        is_high = secrets.randbelow(2) == 0
        
        if is_high:
            low_bound = 10000 - int(chance * 100)
            high_bound = 9999
        else:
            low_bound = 0
            high_bound = int(chance * 100) - 1
            
        is_win = (low_bound <= roll <= high_bound)
        
        if is_win:
            profit = (amount * payout) - amount
        else:
            profit = -amount
            
        # De-normalize for state update, then re-normalize for reward
        # This is the "true" profit/loss
        self.session_profit += profit
        self.balance += profit
        
        # Check for termination
        terminated = False
        if self.session_profit >= self.profit_target:
            terminated = True
        if self.session_profit <= self.loss_limit:
            terminated = True
            
        normalized_reward = profit / self.base_bet
        return normalized_reward, terminated

    def reset(self, *, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[np.ndarray, Dict]:
        """Resets the simulation."""
        # Note: We must also reset the internal balance/profit here
        # before calling the parent reset
        self.balance = self.start_balance
        self.session_profit = 0.0
        return super().reset(seed=seed, options=options)
