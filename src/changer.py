import numpy as np

import src.config as conf
import src.mapper as mapr


# Pre-compute mapping
BIN_MAPPINGS = mapr.create_mapping()

# OLA State Setup
WINDOW_SIZE = conf.BLOCK_SIZE
HOP_SIZE = WINDOW_SIZE // 2  # 50% Overlap

# Periodic Hanning window ensures constant overlap-add sum is 1.0
WINDOW = 0.5 * (1 - np.cos(2 * np.pi * np.arange(WINDOW_SIZE) / WINDOW_SIZE))

IN_BUFFER = np.zeros(WINDOW_SIZE, dtype=np.float32)
OUT_BUFFER = np.zeros(WINDOW_SIZE * 2, dtype=np.float32)


def _process_hop(in_hop: np.ndarray) -> np.ndarray:
	"""Processes a single hop of audio using windowed FFT and Overlap-Add"""
	# Slide input buffer and append incoming hop
	IN_BUFFER[:HOP_SIZE] = IN_BUFFER[HOP_SIZE:]
	IN_BUFFER[HOP_SIZE:] = in_hop

	# Apply window to taper block edges to zero
	windowed_in = IN_BUFFER * WINDOW

	# Compute real FFT
	in_fft = np.fft.rfft(windowed_in)

	# Initialise zeroed spectrum
	out_fft = np.zeros_like(in_fft)

	# Map frequencies with gain scaling
	for out_slice, in_slice, gain in BIN_MAPPINGS:
		length = min(len(in_fft[in_slice]), len(out_fft[out_slice]))
		out_fft[out_slice.start : out_slice.start + length] = (
			in_fft[in_slice.start : in_slice.start + length] * gain
		)

	# Inverse FFT back to time domain
	out_signal = np.fft.irfft(out_fft, n=WINDOW_SIZE)

	# Overlap-Add into output buffer
	OUT_BUFFER[:WINDOW_SIZE] += out_signal

	# Extract completed audio hop
	out_hop = OUT_BUFFER[:HOP_SIZE].copy()

	# Shift output buffer left by HOP_SIZE and zero out the tail
	OUT_BUFFER[:-HOP_SIZE] = OUT_BUFFER[HOP_SIZE:]
	OUT_BUFFER[-HOP_SIZE:] = 0.0

	return out_hop


def callback(
	indata: np.ndarray, outdata: np.ndarray, frames: int, time, status
) -> None:
	if status:
		print(f"SoundDevice status warning: {status}", flush=True)

	in_signal = indata[:, 0]
	out_signal = np.zeros(frames, dtype=np.float32)

	# Process input in hop sized sub-blocks
	for i in range(0, frames, HOP_SIZE):
		chunk_in = in_signal[i : i + HOP_SIZE]
		if len(chunk_in) == HOP_SIZE:
			out_signal[i : i + HOP_SIZE] = _process_hop(chunk_in)
		else:
			padded_in = np.zeros(HOP_SIZE, dtype=np.float32)
			padded_in[: len(chunk_in)] = chunk_in
			out_hop = _process_hop(padded_in)
			out_signal[i : i + len(chunk_in)] = out_hop[: len(chunk_in)]

	outdata[:, 0] = out_signal
