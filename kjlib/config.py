from debugtools import CONFIG_DIR
import __main__
import json
import os
import sys
import traceback

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
			self._raise_value_error(self._path, message=e.message)

	def get(self, key=None, default=None):
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
				return None
		return pointer

	def __del__(self):
		pass

	def _raise_value_error(self, *args, **kw_args):
		if "message" in kw_args:
			args = (kw_args["message"],) + args
		error = ValueError(*args)
		for key, value in kw_args.viewitems():
			setattr(error, key, value)
		raise error

def test(args):
	config = Config()
	print config.get("A/C")

if __name__ == "__main__":
	test(sys.argv[1:])
