import numpy as np
import scipy.signal as sp

from typing import Any


def create_filter(
	freq_changes: dict, samp_rate: int, numtaps: int = 257
) -> np.ndarray | Any:
	nyquist = 0.5 * samp_rate

	# Filter out frequencies at or above Nyquist
	valid_freqs = sorted([f for f in freq_changes if f < nyquist])

	if not valid_freqs:
		return np.array([1.0])

	gains = [freq_changes[f] for f in valid_freqs]

	# Normalise frequencies relative to Nyquist
	bands = [0.0] + [f / nyquist for f in valid_freqs] + [1.0]

	# Flat extrapolation outside defined boundaries
	desired_gains = [gains[0]] + gains + [gains[-1]]

	# Ensure numtaps is odd for Type-1 linear phase FIR filter
	if numtaps % 2 == 0:
		numtaps += 1

	b = sp.firwin2(numtaps, bands, desired_gains)
	return b
