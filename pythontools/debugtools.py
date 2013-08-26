import sys, os, time
from datetime import datetime
from glob import glob

import __main__
app_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
homedir = os.path.expanduser("~")
logdir = os.path.join(homedir, ".cache", app_name, "logs")
stdall_fpath = os.path.join(logdir, "stdall")
stdout_fpath = os.path.join(logdir, "stdout")
stderr_fpath = os.path.join(logdir, "stderr")

if not os.path.exists(logdir):
	os.makedirs(logdir)
for fpath in (stdout_fpath, stderr_fpath, stdall_fpath):
	if os.path.exists(fpath):
		ctime = datetime.fromtimestamp((os.path.getmtime(fpath)))
		ts = ctime.strftime("%Y%m%d_%H%M%S")
		backup_path = "%s_%s" % (fpath, ts)
		#print fpath, backup_path
		os.rename(fpath, backup_path)
	with open(fpath, "w"):
		pass
	old_files = sorted(glob(fpath + "*"))[1:-30]
	for old_file in old_files:
		os.remove(old_file)

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
			7: 'DEBUG3'


		}

		@staticmethod
		def getName(val):
			return DebugTools.DEBUG_LEVEL.STRINGS[val]
		@staticmethod
		def getValue(val):
			k = 3
			for key, value in DebugTools.DEBUG_LEVEL.STRINGS.iteritems():
				if value == val:
					k = key
			return k

	debugLevel = DEBUG_LEVEL.INFO
	__MAX_WIDTH = max([len(x) for x in DEBUG_LEVEL.STRINGS.values()])
	__LOG_TEMPLATE = "%%-%ds | %%s" % __MAX_WIDTH

	@staticmethod
	def println(arg="", debugLevel=DEBUG_LEVEL.DEBUG):
		if debugLevel <= DebugTools.debugLevel:
			print arg
		n = DebugTools.DEBUG_LEVEL.getName(debugLevel)
		with open(stdout_fpath, "a") as f:
			print >> f, DebugTools.__LOG_TEMPLATE % (n, arg)
		with open(stdall_fpath, "a") as f:
			print >> f, DebugTools.__LOG_TEMPLATE % (n, arg)

	@staticmethod
	def printerr(arg="", debugLevel=DEBUG_LEVEL.ERROR):
		if debugLevel <= DebugTools.debugLevel:
			print >> sys.stderr, arg
		n = DebugTools.DEBUG_LEVEL.getName(debugLevel)
		with open(stderr_fpath, "a") as f:
			print >> f, DebugTools.__LOG_TEMPLATE % (n, arg)
		with open(stdall_fpath, "a") as f:
			print >> f, DebugTools.__LOG_TEMPLATE % (n, arg)

	@staticmethod
	def die(arg="", returncode= -1):
		DebugTools.printerr(arg, DebugTools.DEBUG_LEVEL.FATAL)
		exit(returncode)

	@staticmethod
	def pprint(arg):
		print json.dumps(arg, indent=4)

import json
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
