#!/usr/bin/env python3
"""
v14.0 "Janus" - Environment Interfaces
Defines the abstract base class for all environments (live,
simulation, or other games). Based on Gymnasium (OpenAI Gym).
"""
import gymnasium as gym
from gymnasium import spaces
import numpy as np
from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, Optional

# The state is defined by 7 features (from v9.0)
# [profit_norm, win_rate, loss_streak, balance_norm,
#  pub_win_rate, pub_vol, jackpot_norm]
STATE_SIZE = 7

# The action space is discrete (5 predefined actions)
ACTION_SPACE_SIZE = 5

class BaseStrategyEnv(gym.Env, ABC):
    """
    Abstract Base Class for all strategy environments.
    """
    metadata = {'render_modes': ['human']}
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        
        self.config = config
        self.start_balance = config.get("start_balance", 1.0)
        self.balance = self.start_balance
        self.session_profit = 0.0
        self.total_bets = 0
        self.wins = 0
        self.loss_streak = 0
        
        # Define action and observation space
        self.action_space = spaces.Discrete(ACTION_SPACE_SIZE)
        self.observation_space = spaces.Box(
            low=-1.0, high=2.0, shape=(STATE_SIZE,), dtype=np.float32
        )
        
        # Configurable parameters
        self.base_bet = self.start_balance / config.get("base_bet_divisor", 10000.0)
        self.action_map = {
            0: ("49.5", 1.0),
            1: ("33.0", 1.5),
            2: ("75.0", 0.75),
            3: ("49.5", 2.0),
            4: ("25.0", 3.0),
        }

    @abstractmethod
    async def _execute_bet(self, action_id: int) -> Tuple[float, bool]:
        """
        Executes the bet in the child environment (live or sim).
        Returns: (reward, done)
        """
        pass

    def _get_state(self) -> np.ndarray:
        """Calculates the current state vector."""
        profit_norm = max(-1.0, min(1.0, self.session_profit / self.start_balance))
        win_rate_norm = (self.wins / self.total_bets) if self.total_bets > 0 else 0.5
        loss_streak_norm = min(self.loss_streak, 20) / 20.0
        balance_norm = max(0.0, min(2.0, self.balance / self.start_balance))
        
        # Simulated public stats (for now)
        pub_win_rate_norm = 0.5
        pub_vol_norm = 0.5
        jackpot_norm = 0.5

        return np.array([
            profit_norm, win_rate_norm, loss_streak_norm, balance_norm,
            pub_win_rate_norm, pub_vol_norm, jackpot_norm
        ], dtype=np.float32)

    async def step(self, action: int) -> Tuple[np.ndarray, float, bool, bool, Dict]:
        """Run one timestep of the environment's dynamics."""
        if action not in self.action_map:
            raise ValueError("Invalid action")
            
        reward, terminated = await self._execute_bet(action)
        
        self.session_profit += (reward * self.base_bet) # De-normalize reward
        self.balance += (reward * self.base_bet)
        self.total_bets += 1
        
        if reward > 0:
            self.wins += 1
            self.loss_streak = 0
        else:
            self.loss_streak += 1
            
        truncated = False # No early truncation
        obs = self._get_state()
        info = {"balance": self.balance, "session_profit": self.session_profit}
        
        return obs, reward, terminated, truncated, info

    def reset(self, *, seed: Optional[int] = None, options: Optional[Dict] = None) -> Tuple[np.ndarray, Dict]:
        """Resets the environment to an initial state."""
        super().reset(seed=seed)
        
        self.balance = self.start_balance
        self.session_profit = 0.0
        self.total_bets = 0
        self.wins = 0
        self.loss_streak = 0
        
        obs = self._get_state()
        info = {"balance": self.balance, "session_profit": self.session_profit}
        return obs, info

    def render(self):
        """Renders the environment (console)."""
        print(f"Bets: {self.total_bets}, Balance: {self.balance:.8f}, P/L: {self.session_profit:.8f}")
