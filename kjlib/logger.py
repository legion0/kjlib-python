from datetime import datetime
from glob import glob
from json import dumps as json_dumps
import inspect
import os
import sys
import threading
import time

from kjlib.app_dirs import AppDirs
from kjlib.inspect_ import get_calling_module_name

_frame_to_inspect = 3

def _get_caller_info(frame_to_inspect):
	stack = inspect.stack()
	frame = stack[frame_to_inspect]
	frame_info = inspect.getframeinfo(frame[0])
	module = inspect.getmodule(frame[0])
	module_name = get_calling_module_name(module=module)

	caller_info = {
		"module_name"   : module_name,
		"file_path"     : frame_info.filename,
		"line_number"   : frame_info.lineno,
		"function_name" : frame_info.function,
		"line_content"  : frame_info.code_context[0].strip(),
	}
	return caller_info

def _compose_log_msg(msg_text, kwargs, log_level, frame_to_inspect = _frame_to_inspect):

	if "logger_skip_frames" in kwargs:
		frame_to_inspect += kwargs["logger_skip_frames"]
		del kwargs["logger_skip_frames"]
	
	log_obj = _get_caller_info(frame_to_inspect)
	log_obj["time"] = time.time()
	log_obj["level"] = log_level
	log_level_name = Logger.log_level_name(log_level)
	log_obj["level_str"] = log_level_name
	log_obj["msg_text"] = str(msg_text)
	log_obj["pid"] = os.getpid()
	log_obj["tid"] = threading.current_thread().ident
	log_obj["args"] = kwargs
	return log_obj

def _format_log_msg(log_obj):
	return json_dumps(log_obj)

def _format_fatal_msg(log_obj):
	vars_str = " ".join(["%s=%r" % (key, value) for key, value in log_obj["args"].viewitems()])
	if vars_str:
		vars_str = "(%s) " % vars_str
	return "[%s] %s %s<%s:%d>" % (
		log_obj["line_content"],
		log_obj["msg_text"],
		vars_str,
		log_obj["file_path"],
		log_obj["line_number"]
	)

def _format_debug_msg(log_obj):
	vars_str = " ".join(["%s=%r" % (key, value) for key, value in log_obj["args"].viewitems()])
	if vars_str:
		vars_str = "(%s) " % vars_str
	return "%s %s<%s:%s>" % (
		log_obj["msg_text"],
		vars_str,
		log_obj["module_name"],
		log_obj["function_name"]
	)

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

	_LOG_LEVEL_TO_NAME = {
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

	_LOG_LEVEL_NAME_TO_VALUE = {
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

	@staticmethod
	def log_level_choice():
		return Logger._LOG_LEVEL_NAME_TO_VALUE.keys()
	@staticmethod
	def log_level_name_to_value(log_level_name):
		return Logger._LOG_LEVEL_NAME_TO_VALUE[log_level_name]
	@staticmethod
	def log_level_name(log_level):
		return Logger._LOG_LEVEL_TO_NAME[log_level]

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

	def _log_msg(self, log_obj, file_):
		log_msg = _format_log_msg(log_obj)
		print >> file_, log_msg

	def __log(self, log_obj):
		with open(self._log_file_path, "a") as f:
			self._log_msg(log_obj, f)

		log_level = log_obj["level"]
		if log_level <= self.__print_level:

			printed_msg = log_obj["msg_text"]

			if self.__print_level >= self.DEBUG:
				if log_level <= self.FATAL:
					printed_msg = _format_fatal_msg(log_obj)
				else:
					printed_msg = _format_debug_msg(log_obj)

			if printed_msg:
				if log_level <= self.WARN or self.__print_level >= self.DEBUG:
					max_log_level_width = max([len(x) for x in Logger.log_level_choice()])
					level_str = log_obj["level_str"] + (" " * (max_log_level_width - len(log_obj["level_str"])))
					
					printed_msg = "%s: %s" % (level_str, printed_msg)
				if log_level <= self.WARN:
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
