import dummy_module
from kjlib.app_dirs import AppDirs


app_dirs = AppDirs()
print app_dirs.logs()
# print dirs.logs(storage=app_dirs.MODULE_STORAGE)
# print dirs.logs(storage=app_dirs.GLOBAL_MODULE_STORAGE)
print app_dirs.logs(location=AppDirs.APP_DIR)
# print dirs.logs(location=app_dirs.APP_DIR, storage=app_dirs.MODULE_STORAGE)

print ""

