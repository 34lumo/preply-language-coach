import sys
import os

# Add project root to path so _api.py and other modules are importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app  # noqa: F401 — Vercel uses this ASGI app
