import sys, os
from pythontools.atrributes import Namespace
from pythontools.collections import OrderedSet


class _ChoicesVerifier(object):
	def __init__(self, arg, choices):
		self.arg = arg
		self.choices = choices
	def __call__(self, value):
		if value not in self.choices:
			raise ValueError("%r is not a valid choice for --%s" % (value, arg.name.lower()))


class Argument(object):
	_FLAG = 0
	_VALUE = 1
	def __init__(self, name, **kwargs):
		"""
		default
#		optional
		verify
		help
		metavar
		choices
		#{METAVAR}
		#{DEFAULT}
		#{HELP}
		"""
#		self.hasDefault = "default" in kwargs
		if "choices" in kwargs and "verify" in kwargs:
			raise ValueError("Only choices or verify can be specified: %s." % name)
		self.optional = "default" in kwargs
		if self.optional:
			self.default = kwargs["default"]
		self.hasDefault = self.optional and self.default is not None
#		if self.hasDefault and "optional" not in kwargs:
#			raise ValueError("Only optional arguments can have a default value: %s." % name)
		self.name = name
		self.choices = kwargs["choices"] if "choices" in kwargs else None
		self.verify = kwargs["verify"] if "verify" in kwargs else _ChoicesVerifier(self, self.choices) if self.choices is not None else None
		if self.hasDefault:
			self.default = kwargs["default"]
#		self.optional = kwargs["optional"] if "optional" in kwargs else None
#		self.optional = self.hasDefault
		self.metavar = kwargs["metavar"] if "metavar" in kwargs else self.name.upper()
		if self.verify is not None:
			self.type = Argument._VALUE
		else:
			self.type = Argument._FLAG
		self.help = kwargs["help"] if "help" in kwargs else self._defaultHelpMsg()
		self.dependencies = set()

	def _defaultHelpMsg(self):
		if self.optional or self.hasDefault:
			msg = []
			if self.optional:
				msg.append("OPTIONAL")
			if self.hasDefault:
				msg.append("DEFAULT: %r" % self.default)
			msg = ", ".join(msg)
			msg += "."
			return msg
		return ""

	def dependsOn(self, other):
		self.dependencies.add(other)

	def __eq__(self, other):
		return self.name == other.name

	def __hash__(self):
		return self.name.__hash__()

	def _consume(self, args):
		_low = self.name.lower()
		_repr = "--%s" % _low
		if _repr in args:
			found = True
			index = args.index(_repr)
			if self.type == Argument._VALUE:
				if len(args) < index + 2:
					die("%s requires a value." % _repr)
				val = args[index + 1]
				del args[index]
				del args[index]
			elif self.type == Argument._FLAG or self.optional:
				val = None
				del args[index]
			else:
				die("DEATH: 0")
		elif self.hasDefault:
			found = True
			val = self.default
		elif self.optional:
			found = False
			val = None
		else:
			raise ArgumentError("%s was not provided and is non-optional." % _repr)
		return found, val, args
	def _verify(self, value):
		if self.verify is None:
			return
		self.verify(value)

class ArgumentError(Exception):
	pass

class ArgumentParser(object):
	def __init__(self, *args, **argss):
		self.args = OrderedSet()
		self.origArgs = OrderedSet()

	def add(self, argument):
		self.args.add(argument)
		self.origArgs.add(argument)
		return argument


	def _consume_args(self, args, namespace):
		for arg in frozenset(self.args):
			try:
				found, val, args = arg._consume(args)
			except ArgumentError as ex:
				self.die(ex)
			if found:
				namespace[arg.name] = val
			else:
				self.args.remove(arg)


	def _verify_args(self, namespace):
		for arg in self.args:
			value = namespace[arg.name] if arg.name in namespace else ""
			if arg.optional and value is None:
				continue
			arg._verify(value)

	def _verify_dependencies(self):
		for arg in self.args:
			arg_repr = "--%s" % arg.name.lower()
			for dep in arg.dependencies:
				dep_repr = "--%s" % dep.name.lower()
				if dep not in self.args:
					self.die("%s requires that you provide %s." % (arg_repr, dep_repr))

	def parse_args(self, args=None, namespace=None):
		if args is None:
			args = sys.argv[1:]
		if "--help" in args:
			self.die(None)
		if namespace is None:
			namespace = Namespace()
		self._consume_args(args, namespace)
		if len(args) > 0:
			self.die("unrecognized argument %r." % args[0])
		self._verify_dependencies()
		self._verify_args(namespace)
#		print repr(namespace)
		return namespace


	def formatHelp(self, arg, width):
		metavarStr = ""
		if arg.type == Argument._VALUE:
			metavarStr = " <%s>" % arg.metavar
		_format = "--%%-%ds%%s" % width
		start = "%s%s" % (arg.name.lower(), metavarStr)
		helpMsg = arg.help
		helpMsg = helpMsg.replace("#{METAVAR}", "%s" % arg.metavar)
		if arg.hasDefault:
			helpMsg = helpMsg.replace("#{DEFAULT}", repr(arg.default))
		helpMsg = helpMsg.replace("#{HELP}", "%s" % arg._defaultHelpMsg())
		return _format % (start, helpMsg)

	def help(self):
		usageMsg = "usage: %s [arguments]\n\n" % os.path.split(sys.argv[0])[1]
		maxWidth = 0
		for arg in self.origArgs:
			metavarLen = len(arg.metavar) if arg.type == Argument._VALUE else 0
			maxWidth = max(len(arg.name) + metavarLen, maxWidth)
		width = maxWidth + 6
		return usageMsg + '\n'.join([self.formatHelp(arg, width) for arg in self.origArgs])

	def die(self, msg, returncode= -1):
		if msg is None:
			print self.help()
			exit(0)
		print >> sys.stderr, msg
		print >> sys.stderr
		print >> sys.stderr, self.help()
		exit(returncode)
#
#parser = ArgumentParser()
#arg1 = Argument("testArg1", optional=True, help="aaa, #{HELP}")
#arg2 = Argument("testArg2", verify=lambda x: True)
#arg2.dependsOn(arg1)
#parser.add(arg1)
#parser.add(arg2)
#options = parser.parse_args(["--testarg2", "X"])
#print repr(options)
