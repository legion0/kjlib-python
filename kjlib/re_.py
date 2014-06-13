import re

def safe_file_name(file_name):
	return re.sub(r"[^0-9a-zA-Z.]+", "_", file_name)

def find_float(string_value, default=None):
	string_value_clean = re.sub(r"[^0-9\.\+\-]+", "", string_value)
	if string_value_clean == "":
		return default
	return float(string_value_clean)