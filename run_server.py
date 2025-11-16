#!/usr/bin/env python3
"""
QuantumLeap v18.0 "Chronos" - Main Executable
"""
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

env_file = os.path.join(PROJECT_ROOT, '.env')
if os.path.exists(env_file):
    print("Loading environment from .env file...")
    with open(env_file) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            key, value = line.split('=', 1)
            if value.startswith('"') and value.endswith('"'): value = value[1:-1]
            if value.startswith("'") and value.endswith("'"): value = value[1:-1]
            os.environ[key] = value

if not os.getenv("DUCKDICE_API_KEY"):
    print("Error: DUCKDICE_API_KEY is not set.")
    exit(1)

try:
    # --- This now imports the v18.0 server ---
    from src.server_v18 import run_server
except ImportError as e:
    print("\n---")
    print("Error: Failed to import dependencies.")
    print("Please ensure you have installed all requirements:")
    print("pip install -r requirements.txt")
    print(f"\nDetails: {e}")
    exit(1)

if __name__ == "__main__":
    run_server()
