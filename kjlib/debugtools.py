import json
import os
import sys
import time


__logger = None

def __import_logger():
	global __logger
	if __logger is None:
		from kjlib.logger import Logger
		__logger = Logger.instance()

def die(msg="", exit_code=1):
	__import_logger()
	if exit_code != 0:
		__logger.f(msg)
		os._exit(exit_code)
	else:
		__logger.i(msg)
		exit(exit_code)

def verify(condition, msg, exit_code=1):
	if not condition:
		die(msg, exit_code)

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
		__logger.i(msg)
	try:
		time.sleep(seconds)
	except KeyboardInterrupt:
		pass
