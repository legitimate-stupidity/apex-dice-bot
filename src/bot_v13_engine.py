#!/usr/bin/env python3
"""Lightweight placeholder for QuantumLeapBot_v13_Engine.
This provides a minimal interface so the server and UI can interact
without the full production bot implementation.
"""
import asyncio
from typing import Dict, Any

class QuantumLeapBot_v13_Engine:
    def __init__(self, strategy_config: Dict[str, Any], emit_callback=None):
        self.strategy_config = strategy_config
        self.emit_callback = emit_callback
        self._running = False
        self._task = None
        self.nonce = 0

    async def _run_loop(self):
        # Simple simulated betting loop that emits logs occasionally
        while self._running:
            await asyncio.sleep(0.5)
            self.nonce += 1
            if self.emit_callback:
                await self.emit_callback({
                    "type": "log",
                    "level": "info",
                    "message": f"[SimBot:{self.strategy_config.get('id')}] tick {self.nonce}"
                })

    def start(self):
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run_loop())

    def stop(self):
        if not self._running:
            return
        self._running = False
        if self._task:
            self._task.cancel()
            self._task = None
