import sounddevice as sd

import src.helper as h


def identify_devices() -> tuple[int, int]:
	devs = sd.query_devices()

	# Print IDs
	print("Available Devices:")
	for idx, dev in enumerate(devs):
		print(f"{idx}: {dev['name']}")

	print()

	# User input
	mic_id = h.safe_input_int("Select Physical Microphone: ", range(len(devs)))
	bkh_id = h.safe_input_int("Select BlackHole Device: ", range(len(devs)))

	return mic_id, bkh_id
