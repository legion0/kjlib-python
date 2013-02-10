import sys

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
	
	debugLevel = DEBUG_LEVEL.INFO
	
	@staticmethod
	def println(arg, debugLevel = DEBUG_LEVEL.DEBUG):
		if debugLevel <= DebugTools.debugLevel:
			print arg

	@staticmethod
	def printerr(arg, debugLevel = DEBUG_LEVEL.ERROR):
		if debugLevel <= DebugTools.debugLevel:
			n = DebugTools.DEBUG_LEVEL.getName(debugLevel)
			if n is not None:
				n = n + ": "
			else:
				n = ""
			print >> sys.stderr, n + arg