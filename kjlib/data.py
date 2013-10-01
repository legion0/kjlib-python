from debugtools import DATA_DIR
import __main__
import msgpack
import os
import sys
import traceback

class Data(object):

	_ALL_ERRORS = (AttributeError, ValueError, TypeError, IndexError, KeyError)

	def __init__(self, data_name=None):
		self._gen_path(data_name)
		self._data = {}
		self._load()

	def _gen_path(self, name):
		if name is None:
			if hasattr(__main__, "__DATA_NAME__"):
				name = getattr(__main__, "__DATA_NAME__")
			elif hasattr(__main__, "__APP_NAME__"):
				name = getattr(__main__, "__APP_NAME__")
			else:
				name = os.path.splitext(os.path.basename(traceback.extract_stack(limit=2)[0][0]))[0]
		name = "%s.msgpack" % name
		path = os.path.join(DATA_DIR, name)
		self._path = path

	def _load(self):
		if not os.path.exists(self._path):
			with open(self._path, "wb") as f:
				f.write(msgpack.packb({}))
		with open(self._path, "rb") as f:
			self._data = msgpack.unpackb(f.read())

	def get(self, key=None, default=None):
		"""
		key is a forward slash (/) separated path describing the key to get a value for.
		"""
		if key is None:
			return self._data
		parts = key.split("/")
		pointer = self._data
		for part in parts:
			try:
				try:
					pointer = pointer[part]
				except TypeError:
					part = int(part)
					pointer = pointer[part]
			except Data._ALL_ERRORS:
				return None
		return pointer

	def set(self, key, value=None):
		"""
		If value is None key is treated as value for the entire data object.
		Raises KeyError if the key path cannot be reached (for dicts along the path it is created).
		Raises TypeError if value is not serializable.
		"""
		try:
			msgpack.packb(value)  # raise error is value is not serializable
		except TypeError:
			self._raise_type_error(value, message="%r is not serializable." % value)
		if value is None:
			self._data = key
			return
		parts = key.split("/")
		last_part = parts[-1]
		parts = parts[:-1]
		pointer = self._data
		for part in parts:
			try:
				pointer = pointer[part]
			except KeyError:
				pointer = pointer[part] = {}
			except Data._ALL_ERRORS:
				self._raise_key_error(part, key, message="%r is not a valid key in the path %r." % (part, key))
		try:
			try:
				pointer[last_part] = value
			except TypeError:
				last_part = int(last_part)
				pointer[last_part] = value
		except Data._ALL_ERRORS:
			self._raise_key_error(last_part, key, message="%r is not a valid key in the path %r." % (last_part, key))

	def __del__(self):
		with open(self._path, "wb") as f:
			f.write(msgpack.packb(self._data))

	def _raise_key_error(self, *args, **kw_args):
		if "message" in kw_args:
			args = (kw_args["message"],) + args
		error = KeyError(*args)
		for key, value in kw_args.viewitems():
			setattr(error, key, value)
		raise error

	def _raise_type_error(self, *args, **kw_args):
		if "message" in kw_args:
			args = (kw_args["message"],) + args
		error = TypeError(*args)
		for key, value in kw_args.viewitems():
			setattr(error, key, value)
		raise error

def test(args):
	data = Data()
	print repr(data.get())
	data.set("A/B/D/0", set(["A", "B"]))
	print repr(data.get())

if __name__ == "__main__":
	test(sys.argv[1:])
