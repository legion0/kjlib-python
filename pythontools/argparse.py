import sys
from pythontools.atrributes import Namespace

class Argument(object):
	FLAG = 0
	VALUE = 1
	def __init__(self, name, **kwargs):
		"""
		default
		optional
		verify
		help
		"""
		self.hasDefault = "default" in kwargs
		if self.hasDefault and "optional" not in kwargs:
			raise ValueError("Only optional arguments can have a default value: %s." % name)
		self.name = name
		self.verify = kwargs["verify"] if "verify" in kwargs else None
		if self.hasDefault:
			self.default = kwargs["default"]
		self.optional = kwargs["optional"] if "optional" in kwargs else None
		self.help = kwargs["help"] if "help" in kwargs else "DEF_ARG_MSG"
		if self.verify is not None:
			self.type = Argument.VALUE
		else:
			self.type = Argument.FLAG
		self.dependencies = set()

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
			if self.type == Argument.VALUE:
				if len(args) < index + 2:
					die("%s requires a value." % _repr)
				val = args[index + 1]
				del args[index]
				del args[index]
			elif self.type == Argument.FLAG or self.optional:
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
			die("%s was not provided and is non-optional." % _repr)
		return found, val, args
	def _verify(self, value):
		if self.verify is None:
			return
		self.verify(value)

class ArgumentError(Exception):
	pass

class ArgumentParser(object):
	def __init__(self, *args, **argss):
		self.args = set()
		self.origArgs = set()

	def add(self, argument):
		self.args.add(argument)
		self.origArgs.add(argument)


	def _consume_args(self, args, namespace):
		for arg in frozenset(self.args):
			found, val, args = arg._consume(args)
			if found:
				namespace[arg.name] = val
			else:
				self.args.remove(arg)


	def _verify_args(self, namespace):
		for arg in self.args:
			value = namespace[arg.name] if arg.name in namespace else None
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
		if namespace is None:
			namespace = Namespace()
		self._consume_args(args, namespace)
		if len(args) > 0:
			die("unrecognized argument %r." % args[0])
		self._verify_dependencies()
		self._verify_args(namespace)
		return namespace


	def formatHelp(self, arg, width):
		format = "--%%-%ds%%s" % width
		helpMsg = arg.help
		return format % (arg.name, helpMsg)


	def help(self):
		maxWidth = 0
		for arg in self.origArgs:
			maxWidth = max(len(arg.name), maxWidth)
		width = maxWidth + 3
		return '\n'.join([self.formatHelp(arg, width) for arg in self.origArgs])

	def die(self, msg, returncode= -1):
		print >> sys.stderr, msg
		print >> sys.stderr, self.help()
		exit(returncode)

parser = ArgumentParser()
arg1 = Argument("testArg1", optional=True, help="testArg1 is the 1st arg")
arg2 = Argument("testArg2", verify=lambda x: True)
arg2.dependsOn(arg1)
parser.add(arg1)
parser.add(arg2)
options = parser.parse_args(["--testarg2", "X"])
print repr(options)
