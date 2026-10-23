import sounddevice as sd


def identify_devices() -> tuple[int, int]:
	devs = sd.query_devices()
	# None when no id assigned
	mic_id = None
	bkh_id = None

	# Assign IDs
	for idx, dev in enumerate(devs):
		if "BlackHole" in dev["name"]:
			if dev["max_output_channels"] > 0 and bkh_id is None:
				bkh_id = idx
		else:
			# Will not assign id again because mic_id is no longer None
			if dev["max_input_channels"] > 0 and mic_id is None:
				mic_id = idx

	if mic_id is None:
		raise RuntimeError("No compatible input device found")
	if bkh_id is None:
		raise RuntimeError("BlackHole not found")

	# DEBUG
	# TODO

	print(f'Using input device "{devs[mic_id]["name"]}"')
	print(f'Processed output at "{devs[bkh_id]["name"]}"')

	return (mic_id, bkh_id)
