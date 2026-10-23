def safe_input_int(msg: str, allowed_range: range) -> int:
	while True:
		input_str = input(msg)

		try:
			output = int(input_str)
		except ValueError:
			# If user input is not int, ask again
			continue

		# If user input is not in range, ask again
		if output not in allowed_range:
			continue

		break

	return output