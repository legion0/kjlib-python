import sys, os
from atrributes import Namespace
from mycollections import OrderedSet
from meta import ProgrammingError


class _ChoicesVerifier(object):
	def __init__(self, arg, choices):
		self.arg = arg
		self.choices = choices
	def __call__(self, value):
		if value not in self.choices:
			raise ValueError("%r is not a valid choice for --%s" % (value, self.arg.name.lower()))

def _null_verify(_):
	return True
def _flag_verify(value):
	if value not in [True, False]:
		raise ProgrammingError()
	return True

class Argument(object):
	_FLAG = 0
	_CHOICE = 1
	_VALUE = 2

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
		#{CHOICES}
		"""
		self.name = name
		self.metavar = kwargs["metavar"] if "metavar" in kwargs else self.name.upper()
		if "verify" not in kwargs and "default" not in kwargs and "choices" not in kwargs:
			self.type = Argument._FLAG
			self.optional = True
			self.default = False
			self.verify = _flag_verify
		elif "choices" in kwargs:
			self.type = Argument._CHOICE
			self.choices = kwargs["choices"]
			self.optional = "default" in kwargs
			if self.optional:
				self.default = kwargs["default"]
				if self.default not in self.choices:
					raise ValueError("%r is not in %r." % (self.default, self.choices))
			self.verify = _ChoicesVerifier(self, self.choices)
		else:
			self.type = Argument._VALUE
			self.optional = "default" in kwargs
			if self.optional:
				self.default = kwargs["default"]
			self.verify = kwargs["verify"]
			if self.verify is None:
				self.verify = _null_verify
		self.hasPost = "post" in kwargs
		if self.hasPost:
			self.post = kwargs["post"]
		self.help = kwargs["help"] if "help" in kwargs else self._defaultHelpMsg()
		self.dependencies = set()

	def _defaultHelpMsg(self):
		msg = []
		if self.type == Argument._CHOICE:
			msg.append("CHOICES: {%s}" % ', '.join(self.choices))
		if self.optional:
			msg.append("DEFAULT: %r" % self.default)
		if len(msg) > 0:
			msg = ", ".join(msg)
			msg += "."
		else:
			msg = ""
		return msg

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
			index = args.index(_repr)
			if self.type == Argument._VALUE:
				if len(args) < index + 2:
					raise ArgumentError("%s requires a value." % _repr)
				val = args[index + 1]
				del args[index]
				del args[index]
			elif self.type == Argument._FLAG or self.optional:
				val = True
				del args[index]
			else:
				raise ProgrammingError()
		elif self.optional:
			val = self.default
		elif self.optional:
			val = False
		else:
			raise ArgumentError("%s was not provided and is non-optional." % _repr)
		return val, args
	def _verify(self, value):
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
		for arg in tuple(self.args):
			try:
				val, args = arg._consume(args)
			except ArgumentError as ex:
				self.die(ex)
			namespace[arg.name] = val

	def _verify_args(self, namespace):
		for arg in self.args:
			value = namespace[arg.name] if arg.name in namespace else ""
			if arg.optional and value is None:
				continue
			try:
				arg._verify(value)
			except TypeError as ex:
				self.die(ex)
			except ValueError as ex:
				self.die(ex)

	def _post_args(self, namespace):
		for arg in self.args:
			if arg.hasPost:
				arg.post(arg.name, namespace[arg.name], namespace)

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
# 		print repr(namespace)
		self._post_args(namespace)
		return namespace


	def formatHelp(self, arg, width):
		metavarStr = ""
		if arg.type == Argument._VALUE:
			metavarStr = " <%s>" % arg.metavar
		_format = "--%%-%ds%%s" % width
		start = "%s%s" % (arg.name.lower(), metavarStr)
		helpMsg = arg.help
		helpMsg = helpMsg.replace("#{METAVAR}", "%s" % arg.metavar)
		if arg.optional:
			helpMsg = helpMsg.replace("#{DEFAULT}", repr(arg.default))
		helpMsg = helpMsg.replace("#{HELP}", arg._defaultHelpMsg())
		if arg.type == Argument._CHOICE:
			helpMsg = helpMsg.replace("#{CHOICES}", ', '.join(arg.choices))
		return _format % (start, helpMsg)

	def help(self):
		usageMsg = "usage: %s [arguments]\n\n" % os.path.split(sys.argv[0])[1]
		maxWidth = 0
		nonOptional = []
		optional = []
		for arg in self.origArgs:
			if not arg.optional:
				nonOptional.append(arg)
			else:
				optional.append(arg)
			metavarLen = len(arg.metavar) if arg.type == Argument._VALUE else 0
			maxWidth = max(len(arg.name) + metavarLen, maxWidth)
		width = maxWidth + 6
		return usageMsg + '\n'.join([self.formatHelp(arg, width) for arg in nonOptional + optional])

	def die(self, msg, returncode= -1):
		if msg is None:
			print self.help()
			exit(0)
		print >> sys.stderr, msg
		print >> sys.stderr
		print >> sys.stderr, self.help()
		exit(returncode)

def invert_flag(newName):
	return lambda argName, value, namespace: setattr(namespace, newName, not value) or delattr(namespace, argName.lower())

parser = ArgumentParser()

arg_excelFile = parser.add(Argument(
	"excelFile",
	verify=None,
	help="excel file to parse."
))
arg_simulation = parser.add(Argument(
	"write",
	post=invert_flag("simulation"),
	help="write protections to output directory (otherwise simulation is run).",
))
arg_assurent = parser.add(Argument(
	"assurent",
	help="use the assurent converter (otherwise a template xml is used).",
))
arg_verbosity = parser.add(Argument(
	"verbosity",
	choices=("A", "B", "C"),
	default="A",
	help="#{HELP}",
))

options = parser.parse_args(["--excelfile", "X", "--write"])
# options = parser.parse_args(["--excelfile", "X"])
print repr(options)

print >> sys.stderr, parser.help()
