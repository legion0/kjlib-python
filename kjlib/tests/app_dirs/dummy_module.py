'''
Created on Jun 13, 2014

@author: legion
'''
from kjlib.app_dirs import AppDirs

app_dirs = AppDirs()
print app_dirs.logs()
print app_dirs.logs(storage=AppDirs.MODULE_STORAGE)
print app_dirs.logs(storage=AppDirs.GLOBAL_MODULE_STORAGE)
print app_dirs.logs(location=AppDirs.APP_DIR)
print app_dirs.logs(location=AppDirs.APP_DIR, storage=AppDirs.MODULE_STORAGE)