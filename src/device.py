import sounddevice as sd

import src.config as conf


def identify_devices() -> tuple[int, int]:
	mic_id = sd.query_devices(device=conf.MIC_NAME)["index"]
	vrt_id = sd.query_devices(device=conf.VIRTUAL_NAME)["index"]

	return mic_id, vrt_id
