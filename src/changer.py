import numpy as np
import scipy.signal as sp

import src.config as conf
import src.filter as fil


# Pre-compute filter coefficients
b = fil.create_filter(conf.FREQ_CHANGES, conf.SAMPLE_RATE)
zi = np.zeros((len(b) - 1, 1))

# Continuous phase accumulator to prevent audio popping
current_phase = 0.0


def callback(indat: np.ndarray, outdat: np.ndarray, frames: int, t, st) -> None:
	global zi, current_phase
	if st:
		print(st)

	# Apply frequency dependent amplification
	filt_dat, zi = sp.lfilter(b, 1.0, indat, axis=0, zi=zi)

	# Output if no shift, otherwise apply shift
	shift_hz = conf.SHIFT
	if shift_hz == 0:
		outdat[:] = filt_dat
		return

	# Generate analytic signal with Hilbert Transform
	analytic = sp.hilbert(filt_dat, axis=0)

	# Calculate exact phase increments for this block
	dt = 1.0 / conf.SAMPLE_RATE
	t_samples = np.arange(frames)
	phases = current_phase + 2 * np.pi * shift_hz * dt * t_samples

	# Preserve phase continuity for the next callback block
	current_phase = (phases[-1] + 2 * np.pi * shift_hz * dt) % (2 * np.pi)

	# Rotate phase and extract real component
	shifted = analytic * np.exp(1j * phases[:, None])
	outdat[:] = np.real(shifted)
