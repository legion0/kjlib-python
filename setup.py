#!/usr/bin/env python
'''
Created on Feb 18, 2013

@author: legion
'''
from setuptools import setup
from kjlib import VERSION, LIB_NAME

setup(
	name = LIB_NAME,
    version=VERSION,
	description='Reusable Python Modules',
	packages=[LIB_NAME],
	url=r"https://github.com/legion0/kjlib-python",

	install_requires = [
		'jsbeautifier',
		'msgpack-python',
		'termcolor',
	],

	author='K Jonathan',
	author_email='phenixdoc@gmail.com',

	entry_points = {
        'console_scripts': ['kj_log_reader = kjlib.log_reader:main']
    }
)

