#
# you can (but dont have to) put:
# __APP_NAME__
# __VERSION__
# __CONFIG_VERSION__
# __DATA_VERSION__
# __CACHE_VERSION__
# __LOG_VERSION__
# in your main module for the following behaviour:
# for Config and friends: __CONFIG_VERSION__ (and the likes) are the default version
# then fallback to __VERSION__
# For CONFIG_DIR and its friends, path:
# Start from the users home directory, add __APP_NAME__ as directory if it is present else the main modules file name,
# add the versions first 2 parts if present else 0.0

import msgpack
import __main__
import json
import os
import sys
import traceback
import re

if hasattr(__main__, "__APP_NAME__"):
	_app_name = getattr(__main__, "__APP_NAME__")
elif hasattr(__main__, "__file__"):
	_app_name = os.path.splitext(os.path.basename(getattr(__main__, "__file__")))[0]
else: #Using the Python Interpreter
	_app_name = "python_interpreter_session"

if hasattr(__main__, "__VERSION__"):
	_app_major_minor_version = re.sub(r"[^a-z0-9.]+", "_", getattr(__main__, "__VERSION__"), re.IGNORECASE).lower()
	_app_major_minor_version = '.'.join(_app_major_minor_version.split(".")[:2])
else:
	_app_major_minor_version = '0.0'

HOME_DIR = os.getenv('USERPROFILE') or os.path.expanduser("~")  # prefer windows USERPROFILE for windows/cygwin mixes
LOG_DIR = os.path.join(HOME_DIR, ".logs", _app_name)
CACHE_DIR = os.path.join(HOME_DIR, ".cache", _app_name)

CONFIG_DIR = os.path.join(HOME_DIR, ".config", _app_name)
if hasattr(__main__, "__CONFIG_VERSION__"):
	CONFIG_DIR = os.path.join(CONFIG_DIR, getattr(__main__, "__CONFIG_VERSION__"))
else:
	CONFIG_DIR = os.path.join(CONFIG_DIR, _app_major_minor_version)

DATA_DIR = os.path.join(HOME_DIR, ".data", _app_name)
if hasattr(__main__, "__DATA_VERSION__"):
	DATA_DIR = os.path.join(DATA_DIR, getattr(__main__, "__DATA_VERSION__"))
else:
	DATA_DIR = os.path.join(DATA_DIR, _app_major_minor_version)

if hasattr(__main__, "__CACHE_VERSION__"):
	CACHE_DIR = os.path.join(CACHE_DIR, getattr(__main__, "__CACHE_VERSION__"))
else:
	CACHE_DIR = os.path.join(CACHE_DIR, _app_major_minor_version)

if hasattr(__main__, "__LOG_VERSION__"):
	LOG_DIR = os.path.join(LOG_DIR, getattr(__main__, "__LOG_VERSION__"))
else:
	LOG_DIR = os.path.join(LOG_DIR, _app_major_minor_version)

for dir_path in (CONFIG_DIR, DATA_DIR, CACHE_DIR, LOG_DIR):
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)

_NO_ARG = []

class Config(object):

	_ALL_ERRORS = (AttributeError, ValueError, TypeError, IndexError, KeyError)

	def __init__(self, config_name="config"):
		"Raises ValueError if the config cannot be loaded."
		self._gen_path(config_name)
		self._config = {}
		self._load()

	def _gen_path(self, name):
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

	def set(self, key, value=None):
		"""
		Careful: If key is None value is treated as the value for the entire config object.
		Raises KeyError if the key path cannot be reached (for dicts along the path it is created).
		"""
		if key is None:
			self._config = value
			return
		parts = key.split("/")
		last_part = parts[-1]
		parts = parts[:-1]
		pointer = self._config
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
		pass

	def __repr__(self):
		return self._config.__repr__()

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		pass

from debugtools import dumps # recursive dependency, do not move above DIR configs

class JSON_DATA_HANDLER:
	@staticmethod
	def write(o):
		return dumps(o)
	@staticmethod
	def read(s):
		return json.loads(s)
	ext = ".js"


class MSGPACK_DATA_HANDLER:
	write = msgpack.packb
	read = msgpack.unpackb
	ext = ".msgpack"


class Data(object):

	_ALL_ERRORS = (AttributeError, ValueError, TypeError, IndexError, KeyError)

	def __init__(self, data_name="data", data_handler = JSON_DATA_HANDLER):
		self._data_handler = data_handler
		self._gen_path(data_name)
		self._data = {}
		self._load()

	def _gen_path(self, name):
		name = name + self._data_handler.ext
		path = os.path.join(DATA_DIR, name)
		self._path = path

	def _load(self):
		if not os.path.exists(self._path):
			with open(self._path, "wb") as f:
				f.write(self._data_handler.write({}))
		with open(self._path, "rb") as f:
			self._data = self._data_handler.read(f.read())

	def get(self, key=None, default=_NO_ARG):
		"""
		`key` is a forward slash (/) separated path describing the key to get a value for.
		If no `default` is provided the method throws a `KeyError` on bad/missing keys.
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
		Careful: If key is None value is treated as the value for the entire data object.
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
		self.save()

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		if type is None: # there was no exception
			self.save()

	def save(self):
		with open(self._path, "wb") as f:
			f.write(self._data_handler.write(self._data))

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
	print data
	data.set(None, {})
	print data
	data.set("A/B/C", 0)
	data.set("A/B/D", [0])
	print data
	data.set("A/B/D/0", 1)
	print data

	print "#" * 60

	config = Config()
	print config
	print config.get("A/C", None)
	print config.get("A/C")

if __name__ == "__main__":
	test(sys.argv[1:])
