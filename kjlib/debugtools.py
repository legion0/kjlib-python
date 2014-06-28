import json
import os
import sys
import time


__log = None

def __import_logger():
	global __log
	if __log is None:
		from kjlib.logger import Logger
		__log = Logger.instance()

def die(msg="", exit_code=1, **kwargs):
	__import_logger()
	if not "logger_skip_frames" in kwargs:
		kwargs["logger_skip_frames"] = 1
	if exit_code != 0:
		__log.f(msg, **kwargs)
		os._exit(exit_code)
	else:
		__log.i(msg, **kwargs)
		exit(exit_code)

def verify(condition, msg, exit_code=1, **kwargs):
	kwargs["logger_skip_frames"] = 2
	if not condition:
		die(msg, exit_code, **kwargs)

try:
	import jsbeautifier
	jsbeautifierOptions = jsbeautifier.default_options()
	jsbeautifierOptions.indent_with_tabs = True
	jsbeautifierOptions.preserve_newlines = False
	beautifier = jsbeautifier.Beautifier(jsbeautifierOptions)
	__pretty_dumper = lambda o: beautifier.beautify(json.dumps(o))
except ImportError:
	__pretty_dumper = lambda o: json.dumps(o, indent=4)

def dumps(o):
	return __pretty_dumper(o)

def dump(o):
	print dumps(o)

def pause(msg="Pausing for %r seconds, press Ctrl+C to continue.", seconds=sys.maxint):
	__import_logger()
	if msg is not None:
		__log.i(msg)
	try:
		time.sleep(seconds)
	except KeyboardInterrupt:
		pass
