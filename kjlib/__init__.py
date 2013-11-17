import sys

__version__ = "2.1.0"

def require(required_version):
	current_version = __version__
	require_lib("kjlib", required_version, current_version)

def require_lib(lib_name, required_version, available_version):
	if __compare_versions(required_version, available_version) > 0:
		print >> sys.stderr, "This program requires %s required_version: %s" % (lib_name, required_version)
		exit(-1)

def __compare_versions(ver1, ver2):
	parts1 = [int(x) for x in ver1.split(".")]
	parts2 = [int(x) for x in ver2.split(".")]
	l1 = len(parts1)
	l2 = len(parts2)
	sizeDiff = abs(l1 - l2)
	maxSize = max(l1, l2)
	if l1 < l2:
		parts1.extend([0] * sizeDiff)
	elif l2 < l1:
		parts2.extend([0] * sizeDiff)
	for i in xrange(maxSize):
		if parts1[i] > parts2[i]:
			return 1
		elif parts1[i] < parts2[i]:
			return -1
	return 0
