#!/usr/bin/env python3
"""一键启动 DecodeGene 后端 + 前端 (开发模式).

用法::

    python run_dev.py            # 同时启动后端 (uvicorn) 与前端 (vite)
    python run_dev.py --backend-only
    python run_dev.py --frontend-only
"""
from __future__ import annotations

import argparse
import subprocess
import sys
import time
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"


def start_backend() -> subprocess.Popen:
    print("▶ 启动后端 FastAPI (http://localhost:8000/docs) ...")
    return subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--reload",
         "--host", "0.0.0.0", "--port", "8000"],
        cwd=str(BACKEND_DIR),
    )


def start_frontend() -> subprocess.Popen:
    print("▶ 启动前端 Vite (http://localhost:5173) ...")
    npm = "npm.cmd" if sys.platform == "win32" else "npm"
    return subprocess.Popen([npm, "run", "dev"], cwd=str(FRONTEND_DIR))


def main() -> None:
    parser = argparse.ArgumentParser(description="DecodeGene 一键启动")
    parser.add_argument("--backend-only", action="store_true")
    parser.add_argument("--frontend-only", action="store_true")
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()

    procs = []
    try:
        if not args.frontend_only:
            procs.append(start_backend())
        if not args.backend_only:
            procs.append(start_frontend())

        time.sleep(2)
        if not args.no_browser:
            webbrowser.open("http://localhost:5173")

        print("\n✅ DecodeGene 已启动。按 Ctrl+C 停止。\n")
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        print("\n🛑 正在停止…")
    finally:
        for p in procs:
            p.terminate()


if __name__ == "__main__":
    main()
