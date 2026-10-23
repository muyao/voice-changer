import numpy as np
import scipy.signal as sp

import src.config as conf


def create_filter(
	freq_mod: dict, samp_rate: int, numtaps: int = 257
) -> np.ndarray:
	nyquist = 0.5 * samp_rate

	# Filter out frequencies at or above Nyquist
	valid_freqs = sorted([f for f in freq_mod if f < nyquist])

	if not valid_freqs:
		return np.array([1.0])

	gains = [freq_mod[f] for f in valid_freqs]

	# Normalise frequencies relative to Nyquist
	bands = [0.0] + [f / nyquist for f in valid_freqs] + [1.0]

	# Flat extrapolation outside defined boundaries
	desired_gains = [gains[0]] + gains + [gains[-1]]

	# Ensure numtaps is odd for Type-1 linear phase FIR filter
	if numtaps % 2 == 0:
		numtaps += 1

	b = sp.firwin2(numtaps, bands, desired_gains)
	return b  # type: ignore


# Pre-compute filter coefficients
b = create_filter(conf.FREQ_MOD, conf.SAMPLE_RATE)
zi = np.zeros((len(b) - 1, 1))

# Continuous phase accumulator to prevent audio popping
current_phase = 0.0


def callback(indat: np.ndarray, outdat: np.ndarray, frames: int, t, st) -> None:
	global zi, current_phase
	if st:
		print(st)

	# Apply frequency dependent amplification
	filt_dat, zi = sp.lfilter(b, 1.0, indat, axis=0, zi=zi)

	# Apply frequency shift
	shift_hz = getattr(conf, "SHIFT", 0)
	if shift_hz != 0:
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
		outdat[:] = np.real(shifted)  # type: ignore
	else:
		outdat[:] = filt_dat
