from datetime import datetime
from glob import glob
import os
import sys

from kjlib.app_dirs import AppDirs

class Logger(object):
	QUIET   = 0
	FATAL   = 1
	ERROR   = 2
	WARN    = 3
	INFO    = 4
	VERBOSE = 5
	DEBUG   = 6
	DEBUG2  = 7
	DEBUG3  = 8

	__LOG_LEVEL_TO_STRING = {
		0: 'QUIET'  ,
		1: 'FATAL'  ,
		2: 'ERROR'  ,
		3: 'WARN'   ,
		4: 'INFO'   ,
		5: 'VERBOSE',
		6: 'DEBUG'  ,
		7: 'DEBUG2' ,
		8: 'DEBUG3' ,
	}

	__MAX_WIDTH = max([len(x) for x in __LOG_LEVEL_TO_STRING.values()])
	__LOG_TEMPLATE = "%%-%ds | %%s" % __MAX_WIDTH

	@staticmethod
	def __get_log_level_name(log_level):
		return Logger.__LOG_LEVEL_TO_STRING[log_level]
# 
	__instance = None
	@staticmethod
	def instance(*args, **kwargs):
		if Logger.__instance is None:
			Logger.__instance = Logger(*args, **kwargs)
		return Logger.__instance

	def __init__(self, log_dir=None, retain=30, print_level=INFO):
# 		from kjlib.app_dirs import AppDirs
		self.__app_dirs = AppDirs()

		self.__log_dir = log_dir

		if self.__log_dir is None:
			self.__LOG_DIR = self.__app_dirs.logs()
		AppDirs.mkdir(self.__LOG_DIR)

		self.__retain = retain
	
		self.__stdall_file_path = os.path.join(self.__LOG_DIR, "stdall")
		self.__stdout_file_path = os.path.join(self.__LOG_DIR, "stdout")
		self.__stderr_file_path = os.path.join(self.__LOG_DIR, "stderr")

		for file_path in (self.__stdout_file_path, self.__stderr_file_path, self.__stdall_file_path):
			self.__rotate_file(file_path)

		self.__print_level = print_level

	def set_print_level(self, log_level):
		self.__print_level = log_level

	def f(self, msg=""):
		self.__printerr(msg, self.FATAL)
	def e(self, msg=""):
		self.__printerr(msg, self.ERROR)
	def w(self, msg=""):
		self.__printerr(msg, self.WARN)
	def i(self, msg=""):
		self.__println(msg, self.INFO)
	def v(self, msg=""):
		self.__println(msg, self.VERBOSE)
	def d(self, msg=""):
		self.__println(msg, self.DEBUG)
	def d2(self, msg=""):
		self.__println(msg, self.DEBUG2)
	def d3(self, msg=""):
		self.__println(msg, self.DEBUG3)

	def __println(self, msg, log_level):
		self.__log(msg, log_level)
		if log_level <= self.__print_level:
			print msg

	def __log(self, msg, log_level):
		log_level_name = Logger.__get_log_level_name(log_level)
		with open(self.__stdout_file_path, "a") as f:
			print >> f, Logger.__LOG_TEMPLATE % (log_level_name, msg)
		with open(self.__stdall_file_path, "a") as f:
			print >> f, Logger.__LOG_TEMPLATE % (log_level_name, msg)

	def __printerr(self, msg, log_level):
		self.__log(msg, log_level)
		if log_level <= self.__print_level:
			print >> sys.stderr, msg

	def __rotate_file(self, file_path):
		if os.path.exists(file_path):
			ctime = datetime.fromtimestamp((os.path.getmtime(file_path)))
			ts = ctime.strftime("%Y%m%d_%H%M%S")
			backup_path = "%s_%s" % (file_path, ts)
			os.rename(file_path, backup_path)
		with open(file_path, "w"):
			pass
		if self.__retain is not None:
			old_files = sorted(glob(file_path + "*"))[1:-self.__retain]
			for old_file in old_files:
				os.remove(old_file)
