class Namespace(object):
	def __init__(self, **kwargs):
		for key, val in kwargs:
			setattr(self, key, val)

	def __repr__(self):
		type_name = type(self).__name__
		arg_strings = []
		for name, value in self._get_kwargs():
			if value is None:
				arg_strings.append('%s' % name)
			else:
				arg_strings.append('%s=%r' % (name, value))
		return '%s(%s)' % (type_name, ', '.join(arg_strings))

	def _get_kwargs(self):
		return sorted(self.__dict__.items())

	def __setitem__(self, name, value):
		setattr(self, name, value)

	def __getitem__(self, name):
		return getattr(self, name)

	__hash__ = None

	def __eq__(self, other):
		return vars(self) == vars(other)

	def __ne__(self, other):
		return not (self == other)

	def __contains__(self, key):
		return key in self.__dict__
