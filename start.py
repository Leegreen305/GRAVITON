"""
Launch both the FastAPI backend and Next.js frontend for GRAVITON.
Usage: python start.py
"""
import subprocess
import sys
import os
import time
import signal

ROOT = os.path.dirname(os.path.abspath(__file__))
API_DIR = ROOT
FRONTEND_DIR = os.path.join(ROOT, "webapp", "frontend")


def main():
    print("\n  GRAVITON — Enterprise Dashboard")
    print("  ================================\n")

    # Start FastAPI
    print("  [1/2] Starting FastAPI backend on http://localhost:8001 ...")
    api_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "webapp.api.main:app",
         "--host", "0.0.0.0", "--port", "8001", "--reload"],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    time.sleep(2)

    # Start Next.js
    print("  [2/2] Starting Next.js frontend on http://localhost:3000 ...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        shell=True,
    )

    print("\n  ✓ Dashboard ready at: http://localhost:3000")
    print("  ✓ API docs at:        http://localhost:8001/docs")
    print("\n  Press Ctrl+C to stop both servers.\n")

    def shutdown(sig, frame):
        print("\n  Shutting down...")
        api_proc.terminate()
        frontend_proc.terminate()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
