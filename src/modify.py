import numpy as np
from scipy.signal import butter, lfilter

import src.config as conf


def create_filter(cutoff: int, samp_rate: int, order: int = 4) -> tuple:
	nyquist = 0.5 * samp_rate
	cutoff_normal = cutoff / nyquist
	b, a = butter(  # type: ignore
		order,
		cutoff_normal,
		btype="low",
		analog=False,
	)  # type: ignore
	return b, a


b, a = create_filter(conf.CUTOFF_FREQ, conf.SAMPLE_RATE)

zi = np.zeros((max(len(a), len(b)) - 1, 1))


def callback(indat: np.ndarray, outdat: np.ndarray, frames: int, t, st) -> None:
	global zi
	if st:
		print(st)

	# Apply filter to incoming chunk
	filt_dat, zi = lfilter(b, a, indat, axis=0, zi=zi)
	outdat[:] = filt_dat
