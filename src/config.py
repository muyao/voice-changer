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
	if dat["version"] != 2:
		raise ValueError(f"Unsupported version: {dat['version']}")

	MIC_NAME = dat["mic_name"]
	"""Device name of physical microphone"""

	VIRTUAL_NAME = dat["virtual_name"]
	"""Device name of virtual microphone"""

	VOICE_CHANGER: dict = dat["config"]
	"""Amplify specific frequencies"""


# Do not change these
SAMPLE_RATE = 44100
"""Standard audio sample rate"""

BLOCK_SIZE = 2048
"""Buffer size, frames"""

PID_FILE_NAME = "process.pid"
