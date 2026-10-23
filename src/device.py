import sounddevice as sd

import src.config as conf


def identify_devices() -> tuple[int, int]:
	mic_id = sd.query_devices(device=conf.MIC_NAME)["index"]
	bkh_id = sd.query_devices(device=conf.BLACKHOLE_NAME)["index"]

	return mic_id, bkh_id
