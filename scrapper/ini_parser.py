import re

def parse(text):
	parsed_files = {}
	name = ""
	for line in text.splitlines():
		line = re.sub(r"\W*;.*", "", line).strip()
		line = re.sub(r"\W*//.*", "", line).strip()
		if line.lower() in ["", "end"] or line.startswith((";", "/", "#")):
			continue

		if "=" not in line:
			#new object
			try:
				_type, name = line.split()
			except ValueError:
				print(line.split())
				raise

			parsed_files[name] = {"_type": _type}
		else:
			key, value = line.split("=")
			if value.isdigit():
				try:
					value = int(value)
				except ValueError:
					value = float(value)

			parsed_files[name][key.strip()] = value.split(";")[0].strip()

	return parsed_files

def parse_file(filename):
	with open(filename, "r") as f:
		file = f.read()

	return parse(file)
