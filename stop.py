#!/usr/bin/env python3
import os
import signal
import sys
from pathlib import Path

# Root dir relative to this file, not working dir
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import src.config as conf


def main() -> None:
	PID_FILE_PATH = ROOT_DIR / conf.PID_FILE_NAME

	if not PID_FILE_PATH.exists():
		raise FileNotFoundError(
			f'File "{conf.PID_FILE_NAME}" not found. Was it removed?'
		)

	with open(PID_FILE_PATH, "r") as f:
		pid = int(f.read().strip())

	try:
		os.kill(pid, signal.SIGTERM)
	except ProcessLookupError:
		raise ProcessLookupError("No such process. Was it already stopped?")


if __name__ == "__main__":
	main()
