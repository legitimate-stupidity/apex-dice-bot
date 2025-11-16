#!/usr/bin/env python3
"""Minimal DB manager for strategies used by the server.
This is a lightweight SQLite wrapper to store simple strategy records.
"""
import sqlite3
import os
from typing import Dict, Any, Iterable

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantumleap.db")

def _get_conn():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS strategies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            currency TEXT,
            base_bet_divisor REAL,
            profit_target_percent REAL,
            loss_limit_percent REAL,
            kappa REAL
        )'''
    )
    conn.commit()
    conn.close()

def create_strategy(data: Dict[str, Any]) -> int:
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute(
        'INSERT INTO strategies (name, currency, base_bet_divisor, profit_target_percent, loss_limit_percent, kappa) VALUES (?,?,?,?,?,?)',
        (data.get('name'), data.get('currency'), data.get('base_bet_divisor'), data.get('profit_target_percent'), data.get('loss_limit_percent'), data.get('kappa'))
    )
    conn.commit()
    strategy_id = cur.lastrowid
    conn.close()
    return strategy_id

def get_all_strategies() -> Iterable[Dict[str, Any]]:
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM strategies')
    rows = cur.fetchall()
    conn.close()
    return rows

def get_strategy(strategy_id: int):
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM strategies WHERE id = ?', (strategy_id,))
    row = cur.fetchone()
    conn.close()
    return row
