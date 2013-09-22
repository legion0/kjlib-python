kjlib-python
============

Reusable python modules and classes

Importing:

```
try:
	import kjlib
	kjlib.require("1.6.0")
	from kjlib.jobcontrol import JobControl
	from kjlib.debugtools import DebugTools, dumps, die
	from kjlib.printers import format_table
	DEBUG_LEVEL = DebugTools.DEBUG_LEVEL
	DebugTools.debugLevel = DEBUG_LEVEL.DEBUG3
except ImportError:
	print >> sys.stderr, "Please install kjlib python library (available at pypi)."
	exit(-1)
```
