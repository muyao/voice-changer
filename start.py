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
	stop_ev = threading.Event()

	def stop_voicechanger(sig, frame) -> None:
		stop_ev.set()

	# Catch stop signals
	signal.signal(signal.SIGINT, stop_voicechanger)
	signal.signal(signal.SIGTERM, stop_voicechanger)
	signal.signal(signal.SIGHUP, signal.SIG_IGN)

	# Where the pid is stored
	PID_FILE_PATH = ROOT_DIR / conf.PID_FILE_NAME

	if PID_FILE_PATH.exists():
		raise FileExistsError(f'"{conf.PID_FILE_NAME}" already exists')

	with open(PID_FILE_PATH, "w") as f:
		f.write(str(os.getpid()))

	mic_id, bkh_id = dev.identify_devices()

	try:
		with sd.Stream(
			device=(mic_id, bkh_id),
			samplerate=conf.SAMPLE_RATE,
			blocksize=conf.BLOCK_SIZE,
			channels=1,
			callback=chg.callback,
		):
			# Wait until stop_voicechanger is called
			stop_ev.wait()

	finally:
		if PID_FILE_PATH.exists():
			os.remove(PID_FILE_PATH)


if __name__ == "__main__":
	main()
