import kjlib
from kjlib.debugtools import verify

def main():
	current_version = kjlib.VERSION
	next_verision = inc_version(current_version)
	prev_version = dec_version(current_version)
	
	kjlib.require(current_version)
	kjlib.require(prev_version)
	kjlib.require(prev_version, next_verision)
	kjlib.require(prev_version, current_version)
	kjlib.require(current_version, current_version)
	
	try:
		kjlib.require(next_verision)
	except ImportError:
		pass
	else:
		verify(False, "Next version should be unavailable")

	try:
		kjlib.require(next_verision, next_verision)
	except ImportError:
		pass
	else:
		verify(False, "Next version should be unavailable")

def inc_version(version):
	parts = [int(x) for x in version.split(".")]
	parts[-1] += 1
	version = ".".join([str(x) for x in parts])
	return version

def dec_version(version):
	parts = [int(x) for x in version.split(".")]
	index = len(parts) - 1
	while parts[index] == 0:
		index -= 1
	parts[index] -= 1
	index += 1
	while index < len(parts):
		parts[index] = 9
		index += 1
	version = ".".join([str(x) for x in parts])
	return version

if __name__ == "__main__":
	main()
