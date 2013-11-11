import msgpack
import __main__
import json
import os
import sys
import traceback
import re

if hasattr(__main__, "__APP_NAME__"):
	_app_name = __main__.__APP_NAME__
else:
	_app_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
if hasattr(__main__, "__VERSION__"):
	_app_major_minor_version = re.sub(r"[^a-z0-9.]+", "_", __main__.__VERSION__, re.IGNORECASE).lower()
	_app_major_minor_version = '.'.join(_app_major_minor_version.split(".")[:2])
else:
	_app_major_minor_version = None

HOME_DIR = os.getenv('USERPROFILE') or os.path.expanduser("~")  # prefer windows USERPROFILE for windows/cygwin mixes
CONFIG_DIR = os.path.join(HOME_DIR, ".config", _app_name)
LOG_DIR = os.path.join(HOME_DIR, ".logs", _app_name)
CACHE_DIR = os.path.join(HOME_DIR, ".cache", _app_name)
DATA_DIR = os.path.join(HOME_DIR, ".data", _app_name)
if _app_major_minor_version is not None:
	LOG_DIR = os.path.join(LOG_DIR, _app_major_minor_version)
	CACHE_DIR = os.path.join(CACHE_DIR, _app_major_minor_version)
	DATA_DIR = os.path.join(DATA_DIR, _app_major_minor_version)
	CONFIG_DIR = os.path.join(CONFIG_DIR, _app_major_minor_version)

for dir_path in (LOG_DIR, CACHE_DIR, DATA_DIR, CONFIG_DIR):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

_NO_ARG = []

class Config(object):

	_ALL_ERRORS = (AttributeError, ValueError, TypeError, IndexError, KeyError)

	def __init__(self, config_name=None):
		"Raises ValueError if the config cannot be loaded."
		self._gen_path(config_name)
		self._config = {}
		self._load()

	def _gen_path(self, name):
		if name is None:
			if hasattr(__main__, "__CONFIG_NAME__"):
				name = getattr(__main__, "__CONFIG_NAME__")
			elif hasattr(__main__, "__APP_NAME__"):
				name = getattr(__main__, "__APP_NAME__")
			else:
				name = os.path.splitext(os.path.basename(traceback.extract_stack(limit=2)[0][0]))[0]
		name = "%s.js" % name
		path = os.path.join(CONFIG_DIR, name)
		self._path = path

	def _load(self):
		"Raises ValueError if the config cannot be loaded."
		if not os.path.exists(self._path):
			with open(self._path, "w") as f:
				f.write("{}")
		try:
			with open(self._path) as f:
				self._config = json.load(f)
		except ValueError as e:
			_raise_value_error(self._path, message=e.message)

	def get(self, key=None, default=_NO_ARG):
		if key is None:
			return self._config
		parts = key.split("/")
		pointer = self._config
		for part in parts:
			try:
				try:
					pointer = pointer[part]
				except TypeError:
					pointer = pointer[int(part)]
			except Config._ALL_ERRORS:
				if default is _NO_ARG:
					_raise_key_error(part, key, message="%s is not a valid key in the path %s." % (part, key))
				else:
					return default
		return pointer

	def __del__(self):
		pass

	def __repr__(self):
		return self._config.__repr__()

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

	def get(self, key=None, default=_NO_ARG):
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
				if default is _NO_ARG:
					_raise_key_error(part, key, message="%s is not a valid key in the path %s." % (part, key))
				else:
					return default
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
			_raise_type_error(value, message="%s is not serializable." % value)
		if key is None:
			self._data = value
			return
		parts = key.split("/")
		last_part = parts[-1]
		parts = parts[:-1]
		pointer = self._data
		for part in parts:
			try:
				pointer = pointer[part]
			except KeyError:
				pointer[part] = {}
				pointer = pointer[part]
			except Data._ALL_ERRORS:
				_raise_key_error(part, key, message="%s is not a valid key in the path %s." % (part, key))
		try:
			try:
				pointer[last_part] = value
			except TypeError:
				last_part = int(last_part)
				pointer[last_part] = value
		except Data._ALL_ERRORS:
			_raise_key_error(last_part, key, message="%s is not a valid key in the path %s." % (last_part, key))

	def __del__(self):
		with open(self._path, "wb") as f:
			f.write(msgpack.packb(self._data))

	def __repr__(self):
		return self._data.__repr__()

def _raise_key_error(*args, **kw_args):
	if "message" in kw_args:
		args = (kw_args["message"],) + args
	error = KeyError(*args)
	for key, value in kw_args.viewitems():
		setattr(error, key, value)
	raise error

def _raise_type_error(*args, **kw_args):
	if "message" in kw_args:
		args = (kw_args["message"],) + args
	error = TypeError(*args)
	for key, value in kw_args.viewitems():
		setattr(error, key, value)
	raise error

def _raise_value_error(*args, **kw_args):
	if "message" in kw_args:
		args = (kw_args["message"],) + args
	error = ValueError(*args)
	for key, value in kw_args.viewitems():
		setattr(error, key, value)
	raise error

def test(args):
	data = Data()
	print repr(data.get())
	data.set("A/B/D/E", "A")
	print repr(data.get())

	print "#" * 60

	config = Config()
	print config.get("A/C")

if __name__ == "__main__":
	test(sys.argv[1:])
