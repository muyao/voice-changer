import sounddevice as sd


def identify_devices() -> tuple[int, int]:
	mic_id = sd.query_devices(device="MacBook Pro Microphone")["index"]
	bkh_id = sd.query_devices(device="BlackHole 2ch")["index"]

	return mic_id, bkh_id
