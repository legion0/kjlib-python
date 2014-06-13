import sys
from kjlib.version import compare_versions

VERSION = "3.0.0"
LIB_NAME = "kjlib"

def require(minimal_version, maximal_version=VERSION):
	current_version = VERSION
	
	min_ok = compare_versions(current_version, minimal_version) >= 0
	max_ok = compare_versions(maximal_version, current_version) >= 0
	
	if not(min_ok and max_ok):
		raise ImportError("This program requires %r version %r - %r but you have version %r" % (LIB_NAME, minimal_version, maximal_version, VERSION))
