#!/usr/bin/env python3
import sounddevice as sd
import sys
from pathlib import Path

# Root dir relative to this file, not working dir
ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

import src.config as conf
import src.device as dev
import src.modify as mod


def main() -> None:

	mic_id, bkh_id = dev.identify_devices()

	try:
		with sd.Stream(
			device=(mic_id, bkh_id),
			samplerate=conf.SAMPLE_RATE,
			blocksize=conf.BLOCK_SIZE,
			channels=1,
			callback=mod.callback,
		):
			while True:
				sd.sleep(1000)

	except KeyboardInterrupt:
		return


if __name__ == "__main__":
	main()
