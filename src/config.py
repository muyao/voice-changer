SHIFT = 0
"""Shift audio right by SHIFT hz. Happens after amplification"""

FREQ_MOD = {
	10: 10.0,
	400: 10.0,
	401: 1.0,
}
"""Amplify specific frequencies"""

# Do not change below this line

SAMPLE_RATE = 44100
"""Standard audio sample rate"""

BLOCK_SIZE = 1024
"""Buffer size, frames"""
