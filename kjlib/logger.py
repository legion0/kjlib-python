from datetime import datetime
from glob import glob
import os
import sys

import app_dirs


application_dirs = app_dirs.AppDirs()
LOG_DIR = application_dirs.logs()
app_dirs.mkdir(LOG_DIR)

stdall_fpath = os.path.join(LOG_DIR, "stdall")
stdout_fpath = os.path.join(LOG_DIR, "stdout")
stderr_fpath = os.path.join(LOG_DIR, "stderr")

def rotate_file(file_path, retain=None):
	if os.path.exists(file_path):
		ctime = datetime.fromtimestamp((os.path.getmtime(file_path)))
		ts = ctime.strftime("%Y%m%d_%H%M%S")
		backup_path = "%s_%s" % (file_path, ts)
		os.rename(file_path, backup_path)
	with open(file_path, "w"):
		pass
	if retain is not None:
		old_files = sorted(glob(file_path + "*"))[1:-retain]
		for old_file in old_files:
			os.remove(old_file)

for fpath in (stdout_fpath, stderr_fpath, stdall_fpath):
	rotate_file(fpath, retain=30)

class Logger:
	QUIET = 0
	FATAL = 1
	ERROR = 2
	INFO = 3
	VERBOSE = 4
	DEBUG = 5
	DEBUG2 = 6
	DEBUG3 = 7

	_LOG_LEVEL_TO_STRING = {
		0: 'QUIET',
		1: 'FATAL',
		2: 'ERROR',
		3: 'INFO',
		4: 'VERBOSE',
		5: 'DEBUG',
		6: 'DEBUG2',
		7: 'DEBUG3',
	}

	@staticmethod
	def _get_log_level_name(log_level):
		return Logger._LOG_LEVEL_TO_STRING[log_level]
# 
# 	@staticmethod
# 	def get_value(name):
# 		value = 3
# 		for v, n in DebugTools.DEBUG_LEVEL.STRINGS.iteritems():
# 			if n == name:
# 				value = v
# 		return value

	_print_level = INFO
	_MAX_WIDTH = max([len(x) for x in _LOG_LEVEL_TO_STRING.values()])
	_LOG_TEMPLATE = "%%-%ds | %%s" % _MAX_WIDTH

	@staticmethod
	def set_print_level(log_level):
		_print_level = log_level

	@staticmethod
	def f(msg=""):
		Logger._printerr(msg, Logger.FATAL)
	@staticmethod
	def e(msg=""):
		Logger._printerr(msg, Logger.ERROR)
	@staticmethod
	def i(msg=""):
		Logger._println(msg, Logger.INFO)
	@staticmethod
	def v(msg=""):
		Logger._println(msg, Logger.VERBOSE)
	@staticmethod
	def d(msg=""):
		Logger._println(msg, Logger.DEBUG)
	@staticmethod
	def d2(msg=""):
		Logger._println(msg, Logger.DEBUG2)
	@staticmethod
	def d3(msg=""):
		Logger._println(msg, Logger.DEBUG3)

	@staticmethod	
	def _println(msg, log_level):
		Logger._log(msg, log_level)
		if log_level <= Logger._print_level:
			print msg

	@staticmethod	
	def _log(msg, log_level):
		log_level_name = Logger._get_log_level_name(log_level)
		with open(stdout_fpath, "a") as f:
			print >> f, Logger._LOG_TEMPLATE % (log_level_name, msg)
		with open(stdall_fpath, "a") as f:
			print >> f, Logger._LOG_TEMPLATE % (log_level_name, msg)

	@staticmethod
	def _printerr(msg, log_level):
		Logger._log(msg, log_level)
		if log_level <= Logger._print_level:
			print >> sys.stderr, msg
# 
# 	@staticmethod
# 	def die(message=None, returncode=-1):
# 		if returncode != 0:
# 			DebugTools.printerr(message, DebugTools.DEBUG_LEVEL.FATAL)
# 		else:
# 			DebugTools.println(message, DebugTools.DEBUG_LEVEL.INFO)
# 		exit(returncode)
