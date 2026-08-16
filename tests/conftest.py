"""Pytest fixtures: ensure project paths are importable."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
PIPELINE = ROOT / "pipeline"

for path in (str(ROOT), str(BACKEND), str(PIPELINE)):
    if path not in sys.path:
        sys.path.insert(0, path)
