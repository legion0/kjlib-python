#!/usr/bin/env python2

import libs
libs.check()
import kjlib
kjlib.require("3.0.0")

import argparse
import json
import os

from kjlib.app_dirs import AppDirs
from kjlib.logger import Logger
from kjlib.debugtools import die

_log = Logger.instance()
_app_dirs = AppDirs()

_CONF_DIR = _app_dirs.config()
AppDirs.mkdir(_CONF_DIR)

_CONF_FILE = os.path.join(_CONF_DIR, "config.json")
_DEFAULT_CONFIG = {}

def parse_args():
	parser = argparse.ArgumentParser(description='Application Description')
	parser.add_argument("-v", "--verbosity", choices=Logger.log_level_choice(), default="INFO")

	args = parser.parse_args()

	_log.set_print_level(Logger.log_level_name_to_value(args.verbosity))

	return args

def _load_config():
	config = {}
	if not os.path.exists(_CONF_FILE):
		config = _DEFAULT_CONFIG
		with open(_CONF_FILE, "w") as f:
			f.write(json.dumps(config, indent=4))
	else:
		with open(_CONF_FILE) as f:
			config = json.load(open(_CONF_FILE))
	return config

def main():
	args = parse_args()

	# validate args
	print args
	exit(0)

	_config = json.load(open(_CONF_FILE))

if __name__ == "__main__":
	main()
