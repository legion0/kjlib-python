from datetime import datetime
from glob import glob
from json import dumps as json_dumps
import inspect
import os
import sys
import threading
import time

from kjlib.app_dirs import AppDirs

_frame_to_inspect = 4

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

def _compose_log_msg(msg_text, kwargs, log_level, frame_to_inspect = _frame_to_inspect):
	log_obj = _get_caller_info(frame_to_inspect)
	log_obj["time"] = time.time()
	log_obj["level"] = log_level
	log_level_name = Logger._log_level_name(log_level)
	log_obj["level_str"] = log_level_name
	log_obj["msg_text"] = str(msg_text)
	log_obj["pid"] = os.getpid()
	log_obj["tid"] = threading.current_thread().ident
	log_obj["args"] = kwargs
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

	def f(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.FATAL)
		self.__log(log_obj)
	def e(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.ERROR)
		self.__log(log_obj)
	def w(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.WARN)
		self.__log(log_obj)
	def i(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.INFO)
		self.__log(log_obj)
	def v(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.VERBOSE)
		self.__log(log_obj)
	def d(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.DEBUG)
		self.__log(log_obj)
	def d2(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.DEBUG2)
		self.__log(log_obj)
	def d3(self, msg_text="", **kwargs):
		log_obj = _compose_log_msg(msg_text, kwargs, self.DEBUG3)
		self.__log(log_obj)

	def __print(self, msg, log_level, **kwargs):
		self.__log(msg, log_level)
		if log_level <= self.__print_level:
			print msg

	def _log_msg(self, log_obj, file_):
		log_msg = _format_log_msg(log_obj)
		print >> file_, log_msg

	def __log(self, log_obj):
		with open(self._log_file_path, "a") as f:
			self._log_msg(log_obj, f)

		log_level = log_obj["level"]
		printed_msg = log_obj["msg_text"]
		if log_level <= self.__print_level:
			if log_level <= self.WARN:
				log_level_name = Logger._log_level_name(log_level)
				printed_msg = "%s: %s" % (log_level_name, printed_msg)
				print >> sys.stderr, printed_msg
			else:
				print printed_msg

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
