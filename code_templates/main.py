#!/usr/bin/env python2

#import libs
#libs.check()
#import kjlib
#kjlib.require("3.0.0")

import argparse
import os
import json

from kjlib.app_dirs import AppDirs
from kjlib.logger import Logger
from kjlib.debugtools import die

_log = Logger.instance()
_app_dirs = AppDirs()

_CONF_DIR = _app_dirs.config()
AppDirs.mkdir(_CONF_DIR)

_CONF_FILE = os.path.join(_CONF_DIR, "config.json")

def parse_args():
	parser = argparse.ArgumentParser(description='Application Description')
	parser.add_argument("-v", "--verbosity", choices=Logger.log_level_choice(), default="INFO")

	args = parser.parse_args()

	_log.set_print_level(Logger.log_level_name_to_value(args.verbosity))

	return args

def main():
	global _config, _datastore

	args = parse_args()

	# validate args
	print args
	exit(0)

	_log.set_print_level(Logger.VERBOSE)
	_config = json.load(open(_CONF_FILE))

if __name__ == "__main__":
	main()
