'''
Created on Jun 13, 2014

@author: legion
'''

from kjlib import app_dirs

dirs = app_dirs.AppDirs()
print dirs.logs()
# print dirs.logs(storage=app_dirs.MODULE_STORAGE)
# print dirs.logs(storage=app_dirs.GLOBAL_MODULE_STORAGE)
print dirs.logs(location=app_dirs.APP_DIR)
# print dirs.logs(location=app_dirs.APP_DIR, storage=app_dirs.MODULE_STORAGE)

print ""

import dummy_module