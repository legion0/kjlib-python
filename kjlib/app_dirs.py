import os

from kjlib.inspect_ import get_calling_module_name


################################################################################

class AppDirs(object):
	APP_DIR = "APP_DIR"
	USER_DIR = "USER_DIR"
	
	APP_STORAGE = "APP_STORAGE"
	MODULE_STORAGE = "MODULE_STORAGE"
	GLOBAL_MODULE_STORAGE = "GLOBAL_MODULE_STORAGE"

	@staticmethod
	def mkdir(path):
		if not os.path.exists(path):
			os.makedirs(path)

	__NO_VALUE = []
	
	def __init__(self, app_name = __NO_VALUE, user_dir = __NO_VALUE, module_name = __NO_VALUE):
		self._app_name = app_name if app_name != AppDirs.__NO_VALUE else AppDirs.__get_app_name()
		self._user_dir = user_dir if user_dir != AppDirs.__NO_VALUE else AppDirs.__get_user_dir()
		self._module_name = module_name if module_name != AppDirs.__NO_VALUE else get_calling_module_name()
		self._app_dir = AppDirs.__get_app_dir()

		self._location_map = {
			AppDirs.APP_DIR: self._app_dir,
			AppDirs.USER_DIR: self._user_dir,
		}

	def logs(self, location = USER_DIR, storage = APP_STORAGE):
		return self.__build_path("logs", location, storage)

	def cache(self, location = USER_DIR, storage = APP_STORAGE):
		return self.__build_path("cache", location, storage)

	def data(self, location = USER_DIR, storage = APP_STORAGE):
		return self.__build_path("data", location, storage)

	def config(self, location = USER_DIR, storage = APP_STORAGE):
		return self.__build_path("config", location, storage)

	def __build_path(self, type_, location, storage):
		location_path = self._location_map[location]
		path = os.path.join(location_path, ".%s" % type_)
		if location != AppDirs.APP_DIR and storage != AppDirs.GLOBAL_MODULE_STORAGE:
			path = os.path.join(path, self._app_name)
		if storage in (AppDirs.MODULE_STORAGE, AppDirs.GLOBAL_MODULE_STORAGE):
			path = os.path.join(path, self._module_name)
		return path

	@staticmethod
	def __get_app_name():
		import __main__
		if hasattr(__main__, "__file__"):
			app_name = os.path.splitext(os.path.basename(__main__.__file__))[0]
		else:
			app_name = "python_interpreter"
		return app_name

	@staticmethod
	def __get_app_dir():
		import __main__
		if hasattr(__main__, "__file__"):
			app_dir = os.path.dirname(__main__.__file__)
		else:
			app_dir = os.getcwd()
		return app_dir

	@staticmethod
	def __get_user_dir():
		return os.getenv('USERPROFILE') or os.path.expanduser("~")
