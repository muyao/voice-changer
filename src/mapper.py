import numpy as np

import src.config as conf


def _parse_range(range_str: str) -> tuple[float, float]:
	"""Parses a 'min-max' frequency string into numeric float values"""
	low_str, high_str = range_str.split("-")
	try:
		low, high = float(low_str.strip()), float(high_str.strip())
	except ValueError:
		raise ValueError(f'Invalid format: "{range_str}"')

	if low >= high:
		raise ValueError(
			f'Lower bound must be less than upper bound: "{range_str}"'
		)
	return low, high


def create_mapping() -> list[tuple[slice, slice, float]]:
	parsed_entries = []
	target_ranges = []

	# Parse ranges and validate bandwidth equality
	for out_str, src_spec in conf.VOICE_CHANGER.items():
		in_str, gain = src_spec[0], float(src_spec[1])

		out_min, out_max = _parse_range(out_str)
		in_min, in_max = _parse_range(in_str)

		out_bw = out_max - out_min
		in_bw = in_max - in_min

		# Check bandwidth match
		if not np.isclose(out_bw, in_bw):
			raise ValueError(
				f'Bandwidth mismatch: "{out_str}" ({out_bw} Hz) does not match '
				f'"{in_str}" ({in_bw} Hz)'
			)

		target_ranges.append((out_min, out_max, out_str))
		parsed_entries.append((out_min, out_max, in_min, in_max, gain))

	# Check for output range overlaps
	target_ranges.sort(key=lambda x: x[0])
	for i in range(len(target_ranges) - 1):
		_, curr_max, curr_str = target_ranges[i]
		next_min, _, next_str = target_ranges[i + 1]

		if curr_max > next_min:
			raise ValueError(
				f'Overlapping output ranges: "{curr_str}" and "{next_str}"'
			)

	# Pre-calculate FFT bin indices (Hz to Bin mapping)
	bin_res = conf.SAMPLE_RATE / conf.BLOCK_SIZE
	bin_mappings = []

	for out_min, out_max, in_min, in_max, gain in parsed_entries:
		out_start_bin = int(np.round(out_min / bin_res))
		in_start_bin = int(np.round(in_min / bin_res))
		num_bins = int(np.round((out_max - out_min) / bin_res))

		out_slice = slice(out_start_bin, out_start_bin + num_bins)
		in_slice = slice(in_start_bin, in_start_bin + num_bins)

		bin_mappings.append((out_slice, in_slice, gain))

	return bin_mappings
