import os
import inspect

APP_DIR = 0
USER_DIR = 1

APP_STORAGE = 0
MODULE_STORAGE = 1
GLOBAL_MODULE_STORAGE = 2

################################################################################

_NO_VALUE = []

def _get_app_name():
	try:
		import __main__
		return os.path.splitext(os.path.basename(__main__.__file__))[0];
	except ImportError:
		return "python_interpreter"

def _get_app_dir():
	try:
		import __main__
		return os.path.dirname(__main__.__file__);
	except ImportError:
		return os.getcwd()

def _get_user_dir():
	return os.getenv('USERPROFILE') or os.path.expanduser("~")

def _get_calling_module_name():
	stack = inspect.stack()
	frame = stack[2]
	module = inspect.getmodule(frame[0])
	module_name = module.__name__
	return module_name

################################################################################

def mkdir(path):
	if not os.path.exists(path):
		os.makedirs(path)

class AppDirs:
	def __init__(self, app_name = _NO_VALUE, user_dir = _NO_VALUE, module_name = _NO_VALUE):
		self._app_name = app_name if app_name != _NO_VALUE else _get_app_name()
		self._user_dir = user_dir if user_dir != _NO_VALUE else _get_user_dir()
		self._module_name = module_name if module_name != _NO_VALUE else _get_calling_module_name()
		self._app_dir = _get_app_dir()

		self._location_map = {
			APP_DIR: self._app_dir,
			USER_DIR: self._user_dir,
		}

	def logs(self, location = USER_DIR, storage = APP_STORAGE):
		return self._build_path("logs", location, storage)

	def cache(self, location = USER_DIR, storage = APP_STORAGE):
		return self._build_path("cache", location, storage)

	def data(self, location = USER_DIR, storage = APP_STORAGE):
		return self._build_path("data", location, storage)

	def _build_path(self, type_, location, storage):
		location_path = self._location_map[location]
		path = os.path.join(location_path, ".%s" % type_)
		if location != APP_DIR and storage != GLOBAL_MODULE_STORAGE:
			path = os.path.join(path, self._app_name)
		if storage in (MODULE_STORAGE, GLOBAL_MODULE_STORAGE):
			path = os.path.join(path, self._module_name)
		return path

################################################################################

def tester():
	app_dirs = AppDirs()
	print app_dirs.logs()
	print app_dirs.logs(storage=MODULE_STORAGE)
	print app_dirs.logs(storage=GLOBAL_MODULE_STORAGE)
	print app_dirs.logs(location=APP_DIR)
	print app_dirs.logs(location=APP_DIR, storage=MODULE_STORAGE)

if __name__ == "__main__":
	tester()
