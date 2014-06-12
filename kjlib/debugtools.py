import json
import sys
import time

from logger import Logger


def die(msg="", exit_code=1):
	if exit_code != 0:
		Logger.f(msg)
	else:
		Logger.i(msg)
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
	pretty_dumper = lambda o: beautifier.beautify(json.dumps(o))
except ImportError:
	pretty_dumper = lambda o: json.dumps(o, indent=4)

def dumps(o):
	return pretty_dumper(o)

def dump(o):
	print dumps(o)

def pause(msg="Pausing for %r seconds, press Ctrl+C to continue.", seconds=sys.maxint):
	if msg is not None:
		Logger.i(msg)
	try:
		time.sleep(seconds)
	except KeyboardInterrupt:
		pass
