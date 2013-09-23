import imp
import sys

def import_non_local(name, custom_name=None):
	custom_name = custom_name or name
	f, pathname, desc = imp.find_module(name, sys.path[1:])
	module = imp.load_module(custom_name, f, pathname, desc)
	f.close()
	return module

class ProgrammingError(object):
	pass
