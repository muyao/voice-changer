#!/usr/bin/env python3
import os
import signal
import sounddevice as sd
import sys
import threading
from pathlib import Path

# Root dir relative to this file, not working dir
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import src.config as conf
import src.device as dev
import src.changer as chg


def main() -> None:
	stop_event = threading.Event()

	def signal_handler(sig, frame) -> None:
		stop_event.set()

	signal.signal(signal.SIGINT, signal_handler)

	PID_FILE_PATH = ROOT_DIR / conf.PID_FILE_NAME

	with open(PID_FILE_PATH, "w") as f:
		f.write(str(os.getpid()))

	mic_id, bkh_id = dev.identify_devices()

	with sd.Stream(
		device=(mic_id, bkh_id),
		samplerate=conf.SAMPLE_RATE,
		blocksize=conf.BLOCK_SIZE,
		channels=1,
		callback=chg.callback,
	):
		stop_event.wait()


if __name__ == "__main__":
	main()
