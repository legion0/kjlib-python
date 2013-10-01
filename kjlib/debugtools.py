from application import LOG_DIR
from datetime import datetime
from glob import glob
import json
import os
import sys
import time

stdall_fpath = os.path.join(LOG_DIR, "stdall")
stdout_fpath = os.path.join(LOG_DIR, "stdout")
stderr_fpath = os.path.join(LOG_DIR, "stderr")

try:
	import jsbeautifier
	jsbeautifierOptions = jsbeautifier.default_options()
	jsbeautifierOptions.indent_with_tabs = True
	jsbeautifierOptions.preserve_newlines = False
	beautifier = jsbeautifier.Beautifier(jsbeautifierOptions)
	pretty_dumper = lambda o: beautifier.beautify(json.dumps(o))
except ImportError:
	pretty_dumper = lambda o: json.dumps(o, indent=4)

def rotate_file(file_path, retain=None):
	if os.path.exists(file_path):
		ctime = datetime.fromtimestamp((os.path.getmtime(file_path)))
		ts = ctime.strftime("%Y%m%d_%H%M%S")
		backup_path = "%s_%s" % (file_path, ts)
		# print fpath, backup_path
		os.rename(file_path, backup_path)
	with open(file_path, "w"):
		pass
	if retain is not None:
		old_files = sorted(glob(file_path + "*"))[1:-30]
		for old_file in old_files:
			os.remove(old_file)

for fpath in (stdout_fpath, stderr_fpath, stdall_fpath):
	rotate_file(fpath, retain=30)

class DebugTools:

	class DEBUG_LEVEL:
		QUIET = 0
		FATAL = 1
		ERROR = 2
		INFO = 3
		VERBOSE = 4
		DEBUG = 5
		DEBUG2 = 6
		DEBUG3 = 7
		STRINGS = {
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
		def get_name(value):
			return DebugTools.DEBUG_LEVEL.STRINGS[value]

		@staticmethod
		def get_value(name):
			value = 3
			for v, n in DebugTools.DEBUG_LEVEL.STRINGS.iteritems():
				if n == name:
					value = v
			return value

	_debug_level = DEBUG_LEVEL.INFO
	_MAX_WIDTH = max([len(x) for x in DEBUG_LEVEL.STRINGS.values()])
	_LOG_TEMPLATE = "%%-%ds | %%s" % _MAX_WIDTH

	@staticmethod
	def set_debug_level(debug_level):
		DebugTools._debug_level = debug_level

	@staticmethod
	def println(message="", debugLevel=DEBUG_LEVEL.INFO):
		if message is None:
			return
		if debugLevel <= DebugTools._debug_level:
			print message
		n = DebugTools.DEBUG_LEVEL.get_name(debugLevel)
		with open(stdout_fpath, "a") as f:
			print >> f, DebugTools._LOG_TEMPLATE % (n, message)
		with open(stdall_fpath, "a") as f:
			print >> f, DebugTools._LOG_TEMPLATE % (n, message)

	@staticmethod
	def printerr(message="", debug_level=DEBUG_LEVEL.ERROR):
		if message is None:
			return
		if debug_level <= DebugTools._debug_level:
			print >> sys.stderr, message
		n = DebugTools.DEBUG_LEVEL.get_name(debug_level)
		with open(stderr_fpath, "a") as f:
			print >> f, DebugTools._LOG_TEMPLATE % (n, message)
		with open(stdall_fpath, "a") as f:
			print >> f, DebugTools._LOG_TEMPLATE % (n, message)

	@staticmethod
	def die(message=None, returncode=-1):
		if returncode != 0:
			DebugTools.printerr(message, DebugTools.DEBUG_LEVEL.FATAL)
		else:
			DebugTools.println(message, DebugTools.DEBUG_LEVEL.INFO)
		exit(returncode)

def dumps(o):
	return pretty_dumper(o)

def dump(o):
	print dumps(o)

def pause(message="Pausing for %r seconds, press Ctrl+C to continue.", seconds=sys.maxint):
	if message is not None:
		DebugTools.println(message)
	try:
		time.sleep(seconds)
	except KeyboardInterrupt:
		pass

def die(message, returncode=-1):
	DebugTools.die(message, returncode)
