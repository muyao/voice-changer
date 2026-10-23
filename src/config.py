import json
import sys
from pathlib import Path

# Read from custom path if given
if len(sys.argv) == 1:
	CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"
elif len(sys.argv) == 2:
	CONFIG_PATH = Path(sys.argv[1]).resolve()
	if not CONFIG_PATH.exists():
		raise FileNotFoundError(f"Config file not found: {sys.argv[1]}")
else:
	raise ValueError("Usage: ./start.py [config_path]")

# Reading from config.json
with open(CONFIG_PATH, "r") as f:
	dat = json.load(f)
	if dat["version"] != 1:
		raise ValueError(f"Unsupported version: {dat['version']}")

	SHIFT = dat["shift"]
	"""Shift audio right by SHIFT hz. Happens after amplification"""

	freqch_raw: dict = dat["freq_changes"]
	FREQ_CHANGES = {int(k): v for k, v in freqch_raw.items()}
	"""Amplify specific frequencies"""

	MIC_NAME = dat["mic_name"]
	"""Device name of physical microphone"""

	BLACKHOLE_NAME = dat["blackhole_name"]
	"""Device name of BlackHole"""

# Do not change these
SAMPLE_RATE = 44100
"""Standard audio sample rate"""

BLOCK_SIZE = 1024
"""Buffer size, frames"""

PID_FILE_NAME = "stream.pid"
