#!/usr/bin/env python2

#import libs
#libs.check()

from kjlib.app_dirs import AppDirs
from kjlib.logger import Logger

_log = Logger.instance()
_app_dirs = AppDirs()

_CACHE_DIR = _app_dirs.cache(storage=AppDirs.MODULE_STORAGE)
_DATA_DIR = _app_dirs.cache(storage=AppDirs.MODULE_STORAGE)
AppDirs.mkdir(_CACHE_DIR)
AppDirs.mkdir(_DATA_DIR)

class SomeClass(object):
	def __init__(self):
		pass

def _tester():
	obj = SomeClass()

if __name__ == "__main__":
	_tester()
