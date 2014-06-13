from datetime import datetime
from glob import glob
import inspect
from json import dumps as json_dumps
import os
import sys

from kjlib.app_dirs import AppDirs
import time

_frame_to_inspect = 5

def _get_caller_info(frame_to_inspect):
	stack = inspect.stack()
	frame = stack[frame_to_inspect]
	frame_info = inspect.getframeinfo(frame[0])
	module = inspect.getmodule(frame[0])
	caller_info = {
		"module_name": module.__name__,
		"file_path": frame[1],
		"line_number": frame[2],
		"function_name": frame_info.function
	}
	return caller_info

def _compose_log_msg(msg_text, log_level, frame_to_inspect = _frame_to_inspect):
	log_obj = _get_caller_info(frame_to_inspect)
	log_obj["time"] = time.time()
	log_obj["level"] = log_level
	log_level_name = Logger._log_level_name(log_level)
	log_obj["level_str"] = log_level_name
	log_obj["msg_text"] = str(msg_text)
	return log_obj

def _format_log_msg(log_obj):
	return json_dumps(log_obj)


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

	_LOG_LEVEL_TO_STRING = {
		QUIET   : 'QUIET'  ,
		FATAL   : 'FATAL'  ,
		ERROR   : 'ERROR'  ,
		WARN    : 'WARN'   ,
		INFO    : 'INFO'   ,
		VERBOSE : 'VERBOSE',
		DEBUG   : 'DEBUG'  ,
		DEBUG2  : 'DEBUG2' ,
		DEBUG3  : 'DEBUG3' ,
	}

	_LOG_LEVEL_STRING_TO_VALUE = {
		'QUIET'  : QUIET  ,
		'FATAL'  : FATAL  ,
		'ERROR'  : ERROR  ,
		'WARN'   : WARN   ,
		'INFO'   : INFO   ,
		'VERBOSE': VERBOSE,
		'DEBUG'  : DEBUG  ,
		'DEBUG2' : DEBUG2 ,
		'DEBUG3' : DEBUG3 ,
	}

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
	
		self._log_file_path = os.path.join(self.__LOG_DIR, "log")
		self.__rotate_file(self._log_file_path)

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

	def _log_msg(self, log_obj, file_):
		log_msg = _format_log_msg(log_obj)
		print >> file_, log_msg

	def __log(self, msg_text, log_level):
		log_obj = _compose_log_msg(msg_text, log_level, )
		
		log_msg = _format_log_msg(log_obj)

		with open(self._log_file_path, "a") as f:
			print >> f, log_msg

	def __printerr(self, msg, log_level):
		self.__log(msg, log_level)
		if log_level <= self.__print_level:
			log_level_name = Logger._log_level_name(log_level)
			print >> sys.stderr, "%s: %s" % (log_level_name, msg)

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

	@staticmethod
	def _log_level_name(log_level):
		return Logger._LOG_LEVEL_TO_STRING[log_level]
